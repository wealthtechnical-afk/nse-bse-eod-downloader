"""
wt_india_eod – free helper for the data folder of the free WealthTechnical NSE/BSE EOD Downloader.

The Downloader (https://www.wealthtechnical.com/eod-downloader/) keeps NSE and BSE end-of-day
data on YOUR PC and exports it for MetaStock, AmiBroker, NinjaTrader 8, CSV and more.
This module reads those local files so you can build scanners, dashboards, research and
your own tools in Python, Excel or AI tools.

    import wt_india_eod as wti
    kit    = wti.Kit()                                   # finds the Downloader's data folder
    nifty  = kit.watchlist("NIFTY50")                    # ['ADANIENT', 'ADANIPORTS', ...]
    prices = kit.stocks(nifty)                           # split/bonus-adjusted daily bars
    index  = kit.index("NIFTY50")                        # index history
    b      = wti.breadth(prices)                         # advances/declines, % above 200-DMA, 52-week highs/lows
    rot    = kit.sector_rotation()                       # sector table from the NSE sector watchlists

Command line:
    python wt_india_eod.py info
    python wt_india_eod.py breadth  --list NIFTY500
    python wt_india_eod.py sectors
    python wt_india_eod.py export   --list NIFTY50 nifty50.csv         (.parquet, or .db for SQLite)
    python wt_india_eod.py export   --list NIFTY50 --format mt5 C:/mt5 (nt8, amibroker, metastock-csv, mt5, csv-per-symbol, wealthtool)

For education and analysis only – not investment advice. MIT licence (see LICENSE).
This kit does not download, contain or redistribute any market data: it only reads files
that the Downloader has already saved on your own computer, for your personal use.
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path
from typing import Iterable

import pandas as pd

__version__ = "1.1.1"

EXCHANGES = ("NSE", "BSE")
COLS = ["date", "open", "high", "low", "close", "volume"]


# ----------------------------------------------------------------------------- locating
def find_data_dir() -> Path:
    """The Downloader's data folder: from its settings file (%APPDATA%\\NSE_EOD_Tool\\settings.json),
    else Documents\\NSE_EOD. Raises FileNotFoundError if neither exists."""
    cands = []
    appdata = os.environ.get("APPDATA")
    if appdata:
        s = Path(appdata) / "NSE_EOD_Tool" / "settings.json"
        if s.exists():
            try:
                d = json.loads(s.read_text(encoding="utf-8")).get("data_dir")
                if d:
                    cands.append(Path(d))
            except (OSError, ValueError):
                pass
    cands.append(Path.home() / "Documents" / "NSE_EOD")
    for c in cands:
        if (c / "exports").is_dir():
            return c
    raise FileNotFoundError("Downloader data folder not found – pass it explicitly: Kit(r'D:\\path\\to\\data')")


def _ci(parent: Path, name: str) -> Path:
    """Case-insensitive child lookup (e.g. 'Watchlists' vs 'watchlists')."""
    p = parent / name
    if p.exists():
        return p
    if parent.is_dir():
        for c in parent.iterdir():
            if c.name.lower() == name.lower():
                return c
    return p


def read_csv_bars(path: str | os.PathLike, symbol: str | None = None) -> pd.DataFrame:
    """Read one exported CSV (Date,Open,High,Low,Close,Volume)."""
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df.insert(0, "symbol", symbol or Path(path).stem)
    return df[["symbol"] + COLS]


# ----------------------------------------------------------------------------- the kit
class Kit:
    """Reads one Downloader data folder. exchange='NSE' or 'BSE'."""

    def __init__(self, data_dir: str | os.PathLike | None = None, exchange: str = "NSE"):
        self.root = Path(data_dir) if data_dir else find_data_dir()
        self.exchange = exchange.upper()
        if self.exchange not in EXCHANGES:
            raise ValueError("exchange must be NSE or BSE")
        self.exports = _ci(self.root / "exports", self.exchange)
        if not self.exports.is_dir():
            raise FileNotFoundError(f"{self.exports} not found – is {self.exchange} ticked in the Downloader?")
        # read the CSV export if present, otherwise the WealthTechnical Data Tool ("WealthTool") export
        csv_dir = self._dir("Stocks", "CSV")
        self.source = "CSV" if csv_dir.is_dir() and any(csv_dir.glob("*.csv")) else \
            ("WealthTool" if self._dir("Stocks", "WealthTool").is_dir() else "CSV")
        self.ext = ".csv" if self.source == "CSV" else ".txt"

    def _read(self, path: Path, symbol: str | None = None) -> pd.DataFrame:
        if self.source == "CSV":
            return read_csv_bars(path, symbol)
        df = read_wealthtool(path)
        if symbol:
            df["symbol"] = symbol
        return df

    # folders
    def _dir(self, kind: str, fmt: str) -> Path:
        return _ci(_ci(self.exports, kind), fmt)

    @property
    def review_dir(self) -> Path:
        r = self.root / "review"
        return r if self.exchange == "NSE" else _ci(r, "BSE")

    # lists
    def symbols(self) -> list[str]:
        """All stock symbols in the CSV export."""
        return sorted(p.stem for p in self._dir("Stocks", self.source).glob("*" + self.ext))

    def watchlists(self) -> list[str]:
        d = self._dir("Watchlists", "Lists")
        return sorted(p.stem for p in d.glob("*.txt")) if d.is_dir() else []

    def watchlist(self, name: str) -> list[str]:
        p = self._dir("Watchlists", "Lists") / f"{name}.txt"
        if not p.exists():
            raise KeyError(f"watchlist {name!r} not found. Available: {', '.join(self.watchlists()[:30])}")
        return [s.strip() for s in p.read_text(encoding="utf-8-sig").splitlines() if s.strip()]

    def indices(self) -> pd.DataFrame:
        """Index name -> symbol table (index_symbols.csv)."""
        return pd.read_csv(_ci(self.exports, "Indices") / "index_symbols.csv")

    def last_date(self) -> pd.Timestamp | None:
        """Latest date in the exported files (reads only the last line of the index files,
        falling back to stock files)."""
        files = sorted(self._dir("Indices", self.source).glob("*" + self.ext)) or \
            sorted(self._dir("Stocks", self.source).glob("*" + self.ext))[:300]
        best = None
        for f in files:
            try:
                with open(f, "rb") as fh:
                    fh.seek(0, 2); fh.seek(max(0, fh.tell() - 200))
                    last = fh.read().decode("utf-8", "ignore").strip().splitlines()[-1].split(",")
                    raw = last[0] if self.source == "CSV" else last[1]
                    d = pd.to_datetime(raw, format="%Y%m%d" if raw.isdigit() else None, errors="coerce")
                if pd.notna(d) and (best is None or d > best):
                    best = d
            except (OSError, IndexError):
                continue
        return best

    # prices
    def stock(self, symbol: str) -> pd.DataFrame:
        return self._read(self._dir("Stocks", self.source) / f"{symbol}{self.ext}", symbol)

    def stocks(self, symbols: Iterable[str] | str | None = None, start: str | None = None,
               missing: str = "warn") -> pd.DataFrame:
        """Long DataFrame of adjusted daily bars. symbols: list, a watchlist name, or None for all."""
        if isinstance(symbols, str):
            symbols = self.watchlist(symbols)
        symbols = list(symbols) if symbols is not None else self.symbols()
        frames, miss = [], []
        d = self._dir("Stocks", self.source)
        for s in symbols:
            p = d / f"{s}{self.ext}"
            if not p.exists():
                miss.append(s)
                continue
            df = self._read(p, s)
            if start:
                df = df[df["date"] >= pd.Timestamp(start)]
            frames.append(df)
        if miss and missing == "warn":
            print(f"{len(miss)} symbol(s) not found: {', '.join(miss[:10])}{' …' if len(miss) > 10 else ''}", file=sys.stderr)
        if not frames:
            return pd.DataFrame(columns=["symbol"] + COLS)
        return pd.concat(frames, ignore_index=True)

    def index(self, symbol: str) -> pd.DataFrame:
        """Index history by symbol (e.g. NIFTY50, NIFTYBANK, INDIAVIX). Also accepts the index name."""
        d = self._dir("Indices", self.source)
        p = d / f"{symbol}{self.ext}"
        if not p.exists():
            t = self.indices()
            hit = t[t["index"].str.upper() == symbol.upper()]
            if hit.empty:
                raise KeyError(f"index {symbol!r} not found")
            p = d / f"{hit['symbol'].iloc[0]}{self.ext}"
        return self._read(p, p.stem)

    # review files written by the Downloader
    def review(self, name: str) -> pd.DataFrame:
        """Load a review file: quality_report, unexplained_price_jumps, auto_corporate_actions,
        corporate_actions_to_review, cross_check_nse_bse (NSE folder only)."""
        p = self.review_dir / f"{name}.csv"
        if not p.exists():
            raise FileNotFoundError(p)
        return pd.read_csv(p)

    def sector_rotation(self, lists: Iterable[str] | None = None, start: str | None = None) -> pd.DataFrame:
        """Sector table from watchlists (default: the NSE sector lists that exist)."""
        if lists is None:
            lists = [w for w in self.watchlists() if w in SECTOR_LISTS or w.startswith("DEMO_")]
        groups = {w: self.watchlist(w) for w in lists}
        allsyms = sorted({s for v in groups.values() for s in v})
        close = to_wide(self.stocks(allsyms, start=start, missing="ignore"), "close")
        if start is None:
            close = close.iloc[-400:]          # enough for 1-year returns and the 200-day average
        return sector_table(close, groups)

    # read-only access to the Downloader's database (advanced)
    def db(self) -> sqlite3.Connection:
        """Read-only connection to nse_eod.sqlite / bse_eod.sqlite. The layout is internal to the
        Downloader and may change between versions; the exported files are the stable interface."""
        name = "nse_eod.sqlite" if self.exchange == "NSE" else "bse_eod.sqlite"
        p = self.root / name
        return sqlite3.connect(f"file:{p.as_posix()}?mode=ro", uri=True)

    def corporate_actions(self) -> pd.DataFrame:
        """Splits/bonuses the Downloader applied (symbol, ex_date, kind, factor, subject)."""
        with self.db() as con:
            df = pd.read_sql("select symbol, ex_date, kind, factor, subject from corp_actions", con)
        df["ex_date"] = pd.to_datetime(df["ex_date"].astype(str), format="%Y%m%d", errors="coerce")
        return df

    def raw(self, symbol: str, series: str = "EQ") -> pd.DataFrame:
        """Unadjusted bars straight from the database (as the exchange published them)."""
        with self.db() as con:
            df = pd.read_sql("select date, open, high, low, close, volume from bars where symbol=? and series=? order by date",
                             con, params=(symbol, series))
        df["date"] = pd.to_datetime(df["date"].astype(str), format="%Y%m%d")
        df.insert(0, "symbol", symbol)
        return df

    def adjusted_from_raw(self, symbol: str, series: str = "EQ") -> pd.DataFrame:
        """Rebuild split/bonus-adjusted bars from the raw database prices and the corporate-actions
        table (prices before each ex-date x factor, volume / factor) – the same 'Option A' rule the
        Downloader uses for its exports. Handy to check an adjustment or to adjust raw data yourself."""
        df = self.raw(symbol, series)
        ca = self.corporate_actions()
        for _, r in ca[ca["symbol"] == symbol].iterrows():
            m = df["date"] < r["ex_date"]
            df.loc[m, ["open", "high", "low", "close"]] *= r["factor"]
            df.loc[m, "volume"] = (df.loc[m, "volume"] / r["factor"]).round()
        return df


SECTOR_LISTS = {"NIFTYAUTO", "NIFTYBANK", "NIFTYCONSDUR", "NIFTYENERGY", "NIFTYFINSERV", "NIFTYFMCG",
                "NIFTYHEALTHCARE", "NIFTYIT", "NIFTYMEDIA", "NIFTYMETAL", "NIFTYOILGAS", "NIFTYPHARMA",
                "NIFTYPSUBANK", "NIFTYPVTBANK", "NIFTYREALTY"}


# ----------------------------------------------------------------------------- analytics
def to_wide(df: pd.DataFrame, field: str = "close") -> pd.DataFrame:
    d = df.dropna(subset=["date"]).drop_duplicates(["symbol", "date"], keep="last")
    return d.pivot(index="date", columns="symbol", values=field).sort_index()


def breadth(df: pd.DataFrame, min_history: int = 200) -> pd.DataFrame:
    """Daily market breadth for a set of stocks (long DataFrame from Kit.stocks()).

    Columns: advances, declines, unchanged, ad_line (cumulative advances - declines),
    pct_above_50dma, pct_above_200dma, new_52w_highs, new_52w_lows, stocks (counted that day).
    A stock counts for a moving average only once it has enough history."""
    close, high, low = (to_wide(df, f) for f in ("close", "high", "low"))
    chg = close.diff()
    traded = close.notna() & close.shift().notna()
    out = pd.DataFrame(index=close.index)
    out["advances"] = ((chg > 0) & traded).sum(axis=1)
    out["declines"] = ((chg < 0) & traded).sum(axis=1)
    out["unchanged"] = ((chg == 0) & traded).sum(axis=1)
    out["ad_line"] = (out["advances"] - out["declines"]).cumsum()
    for n in (50, 200):
        ma = close.rolling(n, min_periods=n).mean()
        valid = ma.notna() & close.notna()
        cnt = valid.sum(axis=1).astype(float)
        out[f"pct_above_{n}dma"] = (((close > ma) & valid).sum(axis=1) / cnt.where(cnt > 0)) * 100
    hi = high.rolling(252, min_periods=min_history).max().shift()
    lo = low.rolling(252, min_periods=min_history).min().shift()
    out["new_52w_highs"] = (high > hi).sum(axis=1)
    out["new_52w_lows"] = (low < lo).sum(axis=1)
    out["stocks"] = close.notna().sum(axis=1)
    return out


def returns_table(close: pd.DataFrame, periods: dict | None = None) -> pd.DataFrame:
    """% change over 1 week, 1/3/6 months and 1 year (trading days) for each column."""
    periods = periods or {"1w": 5, "1m": 21, "3m": 63, "6m": 126, "1y": 252}
    last = close.ffill().iloc[-1]
    return pd.DataFrame({k: (last / close.ffill().iloc[-n - 1] - 1) * 100 for k, n in periods.items()
                         if len(close) > n}).round(2)


def sector_table(close: pd.DataFrame, groups: dict[str, list[str]]) -> pd.DataFrame:
    """Median % returns per group plus % of the group's stocks above their 200-day average."""
    rt = returns_table(close)
    ma200 = close.rolling(200, min_periods=200).mean().iloc[-1]
    above = (close.ffill().iloc[-1] > ma200) & ma200.notna()
    rows = {}
    for g, syms in groups.items():
        s = [x for x in syms if x in close.columns]
        if not s:
            continue
        r = rt.loc[s].median()
        r["pct_above_200dma"] = round(above[s].sum() / max(ma200[s].notna().sum(), 1) * 100, 1)
        r["stocks"] = len(s)
        rows[g] = r
    out = pd.DataFrame(rows).T
    out["stocks"] = out["stocks"].astype(int)
    return out.sort_values(list(rt.columns)[min(2, len(rt.columns) - 1)], ascending=False)


def relative_strength(close: pd.Series, benchmark: pd.Series, window: int = 63) -> pd.Series:
    """Ratio of a stock or sector to a benchmark, rebased to 100, plus its change over `window` days."""
    a = pd.concat([close, benchmark], axis=1, join="inner").dropna()
    rs = a.iloc[:, 0] / a.iloc[:, 1]
    return (rs / rs.iloc[0] * 100).rename("rs")


def check_quality(df: pd.DataFrame, max_gap_days: int = 10, jump_pct: float = 40.0) -> pd.DataFrame:
    """Same checks as the global toolkit: duplicates, high<low, out-of-range, non-positive prices,
    gaps (calendar days) and big one-day moves."""
    issues = []
    for sym, g in df.dropna(subset=["date"]).sort_values("date").groupby("symbol"):
        for d in g.loc[g["date"].duplicated(), "date"]:
            issues.append((sym, d, "duplicate date", ""))
        v = g.dropna(subset=["open", "high", "low", "close"])
        for _, r in v[v["high"] < v["low"]].iterrows():
            issues.append((sym, r["date"], "high < low", f"{r['high']} < {r['low']}"))
        for _, r in v[(v[["open", "high", "low", "close"]] <= 0).any(axis=1)].iterrows():
            issues.append((sym, r["date"], "non-positive price", ""))
        u = v.drop_duplicates("date")
        gap = u["date"].diff().dt.days
        for i in u.index[gap > max_gap_days]:
            issues.append((sym, u.at[i, "date"], "gap", f"{int(gap[i])} days"))
        ch = u["close"].pct_change() * 100
        for i in u.index[ch.abs() > jump_pct]:
            issues.append((sym, u.at[i, "date"], "big move", f"{ch[i]:+.1f}%"))
    return pd.DataFrame(issues, columns=["symbol", "date", "issue", "detail"])


# ----------------------------------------------------------------------------- writers
def export(df: pd.DataFrame, path: str | os.PathLike) -> Path:
    """Save a long DataFrame to .csv or .parquet (parquet needs pyarrow)."""
    path = Path(path)
    if path.suffix.lower() == ".parquet":
        df.to_parquet(path, index=False)
    else:
        df.to_csv(path, index=False, date_format="%Y-%m-%d")
    return path


def _n(x) -> str:
    return f"{x:.4f}"


def write_nt8(df: pd.DataFrame, folder: str | os.PathLike) -> list[Path]:
    """NinjaTrader 8 end-of-day files: SYMBOL.Last.txt, yyyyMMdd;open;high;low;close;volume."""
    folder = Path(folder); folder.mkdir(parents=True, exist_ok=True); out = []
    for s, g in df.dropna(subset=["date"]).sort_values("date").groupby("symbol"):
        p = folder / f"{s}.Last.txt"
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            for r in g.itertuples(index=False):
                f.write(f"{r.date:%Y%m%d};{_n(r.open)};{_n(r.high)};{_n(r.low)};{_n(r.close)};{int(r.volume or 0)}\n")
        out.append(p)
    return out


def write_amibroker(df: pd.DataFrame, folder: str | os.PathLike) -> list[Path]:
    """AmiBroker ASCII import files: SYMBOL.txt with Ticker,Date(yyyymmdd),Open,High,Low,Close,Volume."""
    folder = Path(folder); folder.mkdir(parents=True, exist_ok=True); out = []
    for s, g in df.dropna(subset=["date"]).sort_values("date").groupby("symbol"):
        p = folder / f"{s}.txt"
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write("Ticker,Date,Open,High,Low,Close,Volume\n")
            for r in g.itertuples(index=False):
                f.write(f"{s},{r.date:%Y%m%d},{_n(r.open)},{_n(r.high)},{_n(r.low)},{_n(r.close)},{int(r.volume or 0)}\n")
        out.append(p)
    return out


def write_metastock_csv(df: pd.DataFrame, folder: str | os.PathLike) -> list[Path]:
    """MetaStock 'ASCII' CSV (<TICKER>,<PER>,<DTYYYYMMDD>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>) – import
    with MetaStock's downloader. One file per symbol."""
    folder = Path(folder); folder.mkdir(parents=True, exist_ok=True); out = []
    for s, g in df.dropna(subset=["date"]).sort_values("date").groupby("symbol"):
        p = folder / f"{s}.csv"
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write("<TICKER>,<PER>,<DTYYYYMMDD>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>\n")
            for r in g.itertuples(index=False):
                f.write(f"{s},D,{r.date:%Y%m%d},{_n(r.open)},{_n(r.high)},{_n(r.low)},{_n(r.close)},{int(r.volume or 0)}\n")
        out.append(p)
    return out


def write_mt5(df: pd.DataFrame, folder: str | os.PathLike) -> list[Path]:
    """MetaTrader 5 bar files for custom symbols (Symbols → Bars → Import Bars): tab-separated
    <DATE> <TIME> <OPEN> <HIGH> <LOW> <CLOSE> <TICKVOL> <VOL> <SPREAD>, dates as yyyy.MM.dd."""
    folder = Path(folder); folder.mkdir(parents=True, exist_ok=True); out = []
    for s, g in df.dropna(subset=["date"]).sort_values("date").groupby("symbol"):
        p = folder / f"{s}.csv"
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write("<DATE>\t<TIME>\t<OPEN>\t<HIGH>\t<LOW>\t<CLOSE>\t<TICKVOL>\t<VOL>\t<SPREAD>\n")
            for r in g.itertuples(index=False):
                v = int(r.volume or 0)
                f.write(f"{r.date:%Y.%m.%d}\t00:00:00\t{_n(r.open)}\t{_n(r.high)}\t{_n(r.low)}\t{_n(r.close)}\t{v}\t{v}\t0\n")
        out.append(p)
    return out


def write_csv_per_symbol(df: pd.DataFrame, folder: str | os.PathLike) -> list[Path]:
    """Plain CSV per symbol (Date,Open,High,Low,Close,Volume) for backtesting tools and charting apps."""
    folder = Path(folder); folder.mkdir(parents=True, exist_ok=True); out = []
    for s, g in df.dropna(subset=["date"]).sort_values("date").groupby("symbol"):
        p = folder / f"{s}.csv"
        g[["date", "open", "high", "low", "close", "volume"]].rename(columns=str.capitalize).to_csv(
            p, index=False, date_format="%Y-%m-%d", float_format="%.4f")
        out.append(p)
    return out


def to_sqlite(df: pd.DataFrame, path: str | os.PathLike, table: str = "bars") -> Path:
    """Save to a SQLite database file (indexed on symbol+date) for SQL queries and reporting tools.
    Replaces the table if it exists."""
    path = Path(path)
    d = df.dropna(subset=["date"]).copy()
    d["date"] = d["date"].dt.strftime("%Y-%m-%d")
    with sqlite3.connect(path) as con:
        d[["symbol"] + COLS].to_sql(table, con, if_exists="replace", index=False)
        con.execute(f"CREATE INDEX IF NOT EXISTS idx_{table}_symbol_date ON {table}(symbol, date)")
    return path


# ----------------------------------------------------------------------------- WealthTechnical Data Tool format
WEALTHTOOL_COLUMNS = ["Ticker", "Date", "Open", "High", "Low", "Close", "Volume"]


def write_wealthtool(df: pd.DataFrame, folder: str | os.PathLike, delimiter: str = ",",
                     date_format: str = "%Y%m%d", header: bool = True,
                     columns: list | None = None, extension: str = ".txt") -> list[Path]:
    """WealthTechnical Data Tool files – the same layout as the Downloader's "WealthTool" export:
    SYMBOL.txt with Ticker,Date(yyyymmdd),Open,High,Low,Close,Volume (prices to 4 decimals).
    delimiter, date_format, header, columns and extension follow the Downloader's WealthTool settings."""
    cols = columns or WEALTHTOOL_COLUMNS
    folder = Path(folder); folder.mkdir(parents=True, exist_ok=True); out = []
    for sym, g in df.dropna(subset=["date"]).sort_values("date").groupby("symbol"):
        p = folder / f"{sym}{extension}"
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            if header:
                f.write(delimiter.join(cols) + "\n")
            for r in g.itertuples(index=False):
                vals = {"Ticker": str(sym), "Date": r.date.strftime(date_format), "Open": f"{r.open:.4f}",
                        "High": f"{r.high:.4f}", "Low": f"{r.low:.4f}", "Close": f"{r.close:.4f}",
                        "Volume": str(0 if pd.isna(r.volume) else int(r.volume))}
                f.write(delimiter.join(vals[c] for c in cols if c in vals) + "\n")
        out.append(p)
    return out


def read_wealthtool(path: str | os.PathLike, delimiter: str = ",", date_format: str = "%Y%m%d") -> pd.DataFrame:
    """Read one WealthTechnical Data Tool file (with a header line, as the Downloader writes by default)."""
    d = pd.read_csv(path, sep=delimiter, dtype={"Date": str})
    d.columns = [c.strip().lower() for c in d.columns]
    d["date"] = pd.to_datetime(d["date"].astype(str).str.strip(), format=date_format, errors="coerce")
    sym = d.pop("ticker") if "ticker" in d.columns else Path(path).stem
    d.insert(0, "symbol", sym if isinstance(sym, str) else sym.astype(str))
    for c in ["open", "high", "low", "close", "volume"]:
        if c not in d.columns:
            d[c] = pd.NA
        d[c] = pd.to_numeric(d[c], errors="coerce")
    return d[["symbol", "date", "open", "high", "low", "close", "volume"]]


WRITERS = {"nt8": write_nt8, "amibroker": write_amibroker, "metastock-csv": write_metastock_csv,
           "mt5": write_mt5, "csv-per-symbol": write_csv_per_symbol, "wealthtool": write_wealthtool}


# ----------------------------------------------------------------------------- command line
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="wt_india_eod", description="Work with the NSE/BSE EOD Downloader's local data.")
    ap.add_argument("--data", help="Downloader data folder (default: found automatically)")
    ap.add_argument("--exchange", default="NSE", choices=EXCHANGES)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("info", help="folders, symbol count, watchlists, latest date")
    b = sub.add_parser("breadth", help="market breadth for a watchlist"); b.add_argument("--list", default="NIFTY500"); b.add_argument("--days", type=int, default=10)
    sub.add_parser("sectors", help="sector rotation table (NSE sector watchlists)")
    e = sub.add_parser("export", help="export a watchlist (or all) to .csv/.parquet or a platform folder")
    e.add_argument("--list"); e.add_argument("--start")
    e.add_argument("--format", default="file", choices=["file"] + sorted(WRITERS),
                   help="file = one .csv/.parquet/.db (SQLite) file; otherwise one file per symbol in the output folder")
    e.add_argument("output")
    a = ap.parse_args(argv)
    kit = Kit(a.data, a.exchange)
    pd.set_option("display.width", 200); pd.set_option("display.max_columns", 20)
    if a.cmd == "info":
        syms = kit.symbols(); wl = kit.watchlists()
        last = kit.last_date()
        print(f"data folder : {kit.root}\nexchange    : {kit.exchange}\nstocks      : {len(syms)}\nwatchlists  : {len(wl)} – {', '.join(wl[:12])}{' …' if len(wl) > 12 else ''}\nlast date   : {last:%Y-%m-%d}" if last is not None else "no stock files")
    elif a.cmd == "breadth":
        print(breadth(kit.stocks(a.list)).tail(a.days).round(1))
    elif a.cmd == "sectors":
        print(kit.sector_rotation())
    elif a.cmd == "export":
        df = kit.stocks(a.list, start=a.start) if a.list else kit.stocks(start=a.start)
        if a.format == "file":
            if str(a.output).lower().endswith((".db", ".sqlite")):
                print("saved", to_sqlite(df, a.output))
            else:
                print("saved", export(df, a.output))
        else:
            print(f"wrote {len(WRITERS[a.format](df, a.output))} files to {a.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

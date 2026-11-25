"""Creates MADE-UP sample data (NOT real market data, fictional symbols) laid out like the
NSE/BSE EOD Downloader's data folder, so every example runs without the Downloader.
Run:  python make_sample_data.py"""
import numpy as np, pandas as pd
from pathlib import Path
root = Path(__file__).parent / "NSE_EOD"
ex = root / "exports" / "NSE"
for d in ["Stocks/CSV", "Indices/CSV", "Watchlists/Lists"]:
    (ex / d).mkdir(parents=True, exist_ok=True)
(root / "review").mkdir(parents=True, exist_ok=True)
dates = pd.bdate_range("2023-01-02", "2025-06-30")
rng = np.random.default_rng(7)
sectors = {"DEMO_BANK": 0.0002, "DEMO_IT": 0.0007, "DEMO_PHARMA": 0.0005, "DEMO_AUTO": -0.0001}
members, closes = {}, []
for sec, drift in sectors.items():
    base = sec.split("_")[1]
    syms = [f"{base}{c}DEMO" for c in "ABCDEFGHIJ"]
    members[sec] = syms
    mkt = rng.normal(0, 0.008, len(dates))
    for s in syms:
        p0 = float(rng.uniform(80, 3000))
        r = drift + mkt + rng.normal(0, 0.015, len(dates))
        c = p0 * np.exp(np.cumsum(r)); o = np.r_[p0, c[:-1]] * (1 + rng.normal(0, 0.004, len(dates)))
        h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.006, len(dates))))
        l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.006, len(dates))))
        v = rng.lognormal(13, 0.6, len(dates)).astype(int)
        pd.DataFrame({"Date": dates.strftime("%Y-%m-%d"), "Open": o.round(4), "High": h.round(4), "Low": l.round(4),
                      "Close": c.round(4), "Volume": v}).to_csv(ex / "Stocks/CSV" / f"{s}.csv", index=False, float_format="%.4f")
        closes.append(c / c[0])
idx = 10000 * np.mean(closes, axis=0)
pd.DataFrame({"Date": dates.strftime("%Y-%m-%d"), "Open": idx.round(2), "High": (idx * 1.004).round(2), "Low": (idx * 0.996).round(2),
              "Close": idx.round(2), "Volume": 0}).to_csv(ex / "Indices/CSV/DEMO40.csv", index=False, float_format="%.4f")
pd.DataFrame({"index": ["DEMO 40"], "symbol": ["DEMO40"]}).to_csv(ex / "Indices/index_symbols.csv", index=False)
allm = sorted(s for v in members.values() for s in v)
(ex / "Watchlists/Lists/DEMO40.txt").write_text("\n".join(allm) + "\n")
for sec, syms in members.items():
    (ex / "Watchlists/Lists" / f"{sec}.txt").write_text("\n".join(syms) + "\n")
pd.DataFrame(columns=["symbol", "date", "issue", "detail"]).to_csv(root / "review/quality_report.csv", index=False)
pd.DataFrame(columns=["symbol", "date"]).to_csv(root / "review/unexplained_price_jumps.csv", index=False)
print("made-up sample data written to", root)

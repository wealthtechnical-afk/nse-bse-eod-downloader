"""Export a watchlist for other tools: one CSV, Parquet, SQLite, and one file per symbol for
NinjaTrader 8, AmiBroker, MetaStock ASCII, MetaTrader 5 and plain CSV."""
from pathlib import Path
from _path import wti, DATA, UNIVERSE

kit = wti.Kit(DATA)
df = kit.stocks(UNIVERSE, start="2024-01-01")
out = Path("output"); out.mkdir(exist_ok=True)
print("saved", wti.export(df, out / f"{UNIVERSE}.csv"))
try:
    print("saved", wti.export(df, out / f"{UNIVERSE}.parquet"))
except ImportError:
    print("(pip install pyarrow for Parquet)")
print(len(wti.write_nt8(df, out / "NinjaTrader8")), "NinjaTrader 8 files")
print(len(wti.write_amibroker(df, out / "AmiBroker")), "AmiBroker files")
print(len(wti.write_metastock_csv(df, out / "MetaStockASCII")), "MetaStock ASCII files")
print(len(wti.write_mt5(df, out / "MetaTrader5")), "MetaTrader 5 files")
print(len(wti.write_csv_per_symbol(df, out / "CSV_per_symbol")), "plain CSV files (backtesting tools)")
print("saved", wti.to_sqlite(df, out / f"{UNIVERSE}.db"), "(SQLite)")

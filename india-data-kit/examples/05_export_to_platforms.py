"""Export a watchlist for other tools: one CSV, Parquet, NinjaTrader 8, AmiBroker and MetaStock ASCII."""
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

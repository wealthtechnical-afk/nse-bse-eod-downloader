"""What is in the Downloader's data folder: stocks, watchlists, an index, one stock."""
from _path import wti, DATA, INDEX, UNIVERSE
import pandas as pd
pd.set_option("display.width", 160)

kit = wti.Kit(DATA)
print("data folder:", kit.root)
print("stocks:", len(kit.symbols()), "| watchlists:", ", ".join(kit.watchlists()))
members = kit.watchlist(UNIVERSE)
print(f"{UNIVERSE}: {len(members)} members, first five {members[:5]}")
print(f"\n{INDEX} – last 5 days\n", kit.index(INDEX).tail().to_string(index=False))
one = kit.stock(members[0])
print(f"\n{members[0]}: {len(one)} bars from {one.date.min():%Y-%m-%d} to {one.date.max():%Y-%m-%d}")

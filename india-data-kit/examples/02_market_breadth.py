"""Market breadth: advances/declines, A/D line, % above 50/200-day averages, new 52-week highs/lows.
Saves breadth.csv and (with matplotlib) breadth.png."""
from _path import wti, DATA, UNIVERSE, INDEX
import pandas as pd
pd.set_option("display.width", 160); pd.set_option("display.max_columns", 12)

kit = wti.Kit(DATA)
b = wti.breadth(kit.stocks(UNIVERSE))
print(b.tail(10).round(1))
b.to_csv("breadth.csv")
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    idx = kit.index(INDEX).set_index("date")["close"].reindex(b.index)
    fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    idx.plot(ax=ax[0], title=f"{INDEX}"); b["pct_above_200dma"].plot(ax=ax[1], title="% of stocks above 200-day average")
    (b["new_52w_highs"] - b["new_52w_lows"]).plot(ax=ax[2], title="new 52-week highs minus lows")
    fig.tight_layout(); fig.savefig("breadth.png", dpi=110); print("saved breadth.csv and breadth.png")
except ImportError:
    print("saved breadth.csv (pip install matplotlib for the chart)")

"""A simple end-of-day scanner over a watchlist:
close above the 200-day average, within 5 % of its 52-week high, volume at least 1.5x its 20-day average.
For education and analysis only – not investment advice or a recommendation."""
from _path import wti, DATA, UNIVERSE
import pandas as pd
pd.set_option("display.width", 160)

kit = wti.Kit(DATA)
df = kit.stocks(UNIVERSE)
c, h, v = (wti.to_wide(df, f) for f in ("close", "high", "volume"))
last = c.ffill().iloc[-1]
t = pd.DataFrame({
    "close": last,
    "pct_vs_200dma": (last / c.rolling(200).mean().iloc[-1] - 1) * 100,
    "pct_below_52w_high": (1 - last / h.rolling(252, min_periods=200).max().iloc[-1]) * 100,
    "vol_vs_20d": v.iloc[-1] / v.rolling(20).mean().iloc[-1],
}).round(2)
hits = t[(t.pct_vs_200dma > 0) & (t.pct_below_52w_high <= 5) & (t.vol_vs_20d >= 1.5)]
print(f"{len(hits)} of {len(t)} stocks pass on {c.index[-1]:%Y-%m-%d}")
print(hits.sort_values("pct_below_52w_high") if len(hits) else t.sort_values("pct_below_52w_high").head(10))

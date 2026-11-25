"""Which sectors are leading? Median returns of each sector's stocks over 1w/1m/3m/6m/1y and the
share of stocks above their 200-day average. Uses the NSE sector watchlists from the Downloader."""
from _path import wti, DATA
import pandas as pd
pd.set_option("display.width", 160)

kit = wti.Kit(DATA)
print(kit.sector_rotation().round(1))

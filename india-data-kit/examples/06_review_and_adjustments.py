"""The Downloader's own checks and corporate actions (needs your real Downloader data: run with 'auto').
- quality notes, unexplained price jumps, NSE vs BSE cross-check (same ISIN, closes >2 % apart)
- the splits/bonuses it applied, and rebuilding adjusted prices from raw prices for one stock"""
import sys
from _path import wti, DATA, USING_SAMPLE
import pandas as pd
pd.set_option("display.width", 160)

if USING_SAMPLE:
    sys.exit("Run with your Downloader data:  python 06_review_and_adjustments.py auto")
kit = wti.Kit(DATA)
for name in ("quality_report", "unexplained_price_jumps", "cross_check_nse_bse", "corporate_actions_to_review"):
    try:
        r = kit.review(name); print(f"\n{name}: {len(r)} rows"); print(r.tail(5).to_string(index=False))
    except FileNotFoundError:
        print(f"\n{name}: not found")
ca = kit.corporate_actions().sort_values("ex_date")
print("\nlatest splits/bonuses applied:\n", ca.tail(8).to_string(index=False))
# pick the latest split/bonus that the exported files already include
exported_to = kit.index("NIFTY50")["date"].max()
sym = ca[ca["ex_date"] <= exported_to]["symbol"].iloc[-1]
newer = ca[ca["ex_date"] > exported_to]
if len(newer):
    print(f"\n{len(newer)} split(s)/bonus(es) are newer than your exported files ({exported_to:%Y-%m-%d}) – run the Downloader's export to include them.")
a, e = kit.adjusted_from_raw(sym), kit.stock(sym)
m = a.merge(e, on="date", suffixes=("_raw_adj", "_export"))
print(f"\n{sym}: rebuilt from raw vs exported – max close difference {((m.close_raw_adj / m.close_export - 1).abs().max() * 100):.4f} %")

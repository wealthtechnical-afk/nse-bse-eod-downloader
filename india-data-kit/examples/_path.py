# Lets the examples import wt_india_eod from ../python without installing anything.
# Usage:  python 01_quick_look.py            -> made-up sample data
#         python 01_quick_look.py auto       -> your Downloader data folder (found automatically)
#         python 01_quick_look.py "E:\Data"  -> a specific Downloader data folder
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
import wt_india_eod as wti  # noqa: E402

SAMPLE = ROOT / "sample_data" / "NSE_EOD"
arg = sys.argv[1] if len(sys.argv) > 1 else None
DATA = None if arg == "auto" else (arg or SAMPLE)
USING_SAMPLE = DATA == SAMPLE
UNIVERSE = "DEMO40" if USING_SAMPLE else "NIFTY500"
INDEX = "DEMO40" if USING_SAMPLE else "NIFTY50"

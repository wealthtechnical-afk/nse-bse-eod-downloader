"""Run your own scripts automatically after the Downloader's evening update.

How it works: it looks at the last date in the index file (NIFTY50 by default). If that date is newer than
the one it saw last time, it runs every *.py file in the folder given (in name order) and remembers the date.

Schedule it with Windows Task Scheduler a little after the Downloader's daily update (default 19:30 IST),
e.g. daily at 19:50:
    python run_after_update.py  "C:\\my_scans"            (Downloader data found automatically)
    python run_after_update.py  "C:\\my_scans"  "E:\\Data" (explicit data folder)
"""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))
import wt_india_eod as wti

scripts = (Path(sys.argv[1]) if len(sys.argv) > 1 else Path("my_scans")).resolve()
data = sys.argv[2] if len(sys.argv) > 2 else None
kit = wti.Kit(data)
last = kit.last_date()
state = scripts / ".last_run.json"
seen = json.loads(state.read_text())["date"] if state.exists() else None
if seen == f"{last:%Y-%m-%d}":
    print(f"No new data since {seen} – nothing to do."); sys.exit(0)
print(f"New data up to {last:%Y-%m-%d} – running scripts in {scripts}")
for s in sorted(scripts.glob("*.py")):
    print("  ->", s.name); subprocess.run([sys.executable, str(s)], cwd=scripts, check=False)
state.write_text(json.dumps({"date": f"{last:%Y-%m-%d}"}))

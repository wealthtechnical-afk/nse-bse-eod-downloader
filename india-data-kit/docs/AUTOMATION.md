# Run your scripts after every evening update

The Downloader updates on weekdays in the evening (19:30 IST by default). `examples/run_after_update.py` runs every `*.py` in a folder of yours **once per new trading day**.

1. Put your scripts (scanner, breadth report, export…) in a folder, e.g. `C:\my_scans`.
2. Windows Task Scheduler → *Create Basic Task* → Daily, 19:50 → *Start a program*
   - Program: `python` (or the full path to python.exe)
   - Arguments: `"C:\path\to\india-data-kit\examples\run_after_update.py" "C:\my_scans"`
3. That's it. If the data has not changed (holiday, PC was off), nothing runs; the next day it catches up.

Tip: write results to Excel/CSV, a dashboard, or send them to yourself – keep everything on your own PC.

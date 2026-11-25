# Using the data in Excel

**Quickest:** export one combined file and open it in Excel:
```
python python/wt_india_eod.py export --list NIFTY50 --start 2024-01-01 nifty50.csv
```
Then Insert → PivotTable, or Insert → Chart.

**Without Python:** the Downloader's `exports\NSE\Stocks\CSV` files open directly in Excel (Date, Open, High, Low, Close, Volume). For many symbols use Data → Get Data → From File → **From Folder** → that CSV folder → *Combine & Transform*; the `Source.Name` column is the symbol (remove `.csv`).

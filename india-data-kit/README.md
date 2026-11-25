# India Data Kit – build on free NSE & BSE end-of-day data (Python · Excel · AI)

Free, open-source (MIT) kit for the data folder of the free **[WealthTechnical NSE/BSE EOD Downloader](https://www.wealthtechnical.com/eod-downloader/)**. The Downloader keeps split- and bonus-adjusted NSE and BSE data on your PC; this kit lets you **build on it** – scanners, market breadth, sector rotation, research, dashboards, exports to any platform.

[⬇ Get the Downloader (free)](https://www.wealthtechnical.com/eod-downloader/) · [हिंदी में पढ़ें](README_HI.md) · [Data folder layout](docs/DATA_FOLDER.md)

> The Downloader is free to use but its source code is not published. This folder is the open kit around its output. The kit reads files on **your** PC only – it contains and shares no market data.

## What you get

| | |
|---|---|
| **One-line loading** | NSE or BSE stocks, ~100 NSE indices (NIFTY50, NIFTYBANK, INDIAVIX…) and every watchlist (Nifty 50/100/200/500, Midcap, Smallcap, sector lists) straight into pandas |
| **Market breadth** | advances/declines, A/D line, % above 50- and 200-day averages, new 52-week highs/lows – for any watchlist |
| **Sector rotation** | median 1w/1m/3m/6m/1y returns and % above 200-DMA for each NSE sector list |
| **Scanner example** | above 200-DMA, near 52-week high, volume surge – edit the rules |
| **Exports** | one CSV/Parquet file, or folders for **AmiBroker**, **NinjaTrader 8** and **MetaStock ASCII** |
| **The Downloader's own checks** | quality notes, unexplained jumps, NSE-vs-BSE cross-check by ISIN, corporate actions applied |
| **Raw + adjusted** | read raw exchange prices (read-only) and rebuild the split/bonus adjustment yourself – matches the Downloader's exports |
| **Automation** | run your scripts after every evening update ([guide](docs/AUTOMATION.md)) |
| **Made-up sample data** | 40 fictional stocks in the Downloader's exact layout – everything runs before you install anything |

## Quick start

```bash
pip install pandas matplotlib            # pyarrow optional (Parquet)
cd india-data-kit/examples
python 01_quick_look.py                  # made-up sample data
python 02_market_breadth.py auto         # your Downloader data (found automatically)
python 03_sector_rotation.py auto
python 04_scanner.py auto
python 05_export_to_platforms.py auto
python 06_review_and_adjustments.py auto
```

Command line (from `india-data-kit`):

```bash
python python/wt_india_eod.py info
python python/wt_india_eod.py breadth --list NIFTY500
python python/wt_india_eod.py sectors
python python/wt_india_eod.py export --list NIFTY50 --format amibroker  C:\AB_import
python python/wt_india_eod.py --exchange BSE info
```

In Python:

```python
import sys; sys.path.insert(0, "python")
import wt_india_eod as wti

kit    = wti.Kit()                         # or wti.Kit(r"E:\my data folder", exchange="BSE")
prices = kit.stocks("NIFTY50")             # watchlist name or list of symbols
nifty  = kit.index("NIFTY50")
b      = wti.breadth(kit.stocks("NIFTY500"))
kit.sector_rotation()
```

Guides: [data folder](docs/DATA_FOLDER.md) · [automation](docs/AUTOMATION.md) · [Excel](docs/EXCEL.md) · [AI tools](docs/AI_TOOLS.md)

Working with MetaStock-format data from other markets? See the [global developer toolkit](https://github.com/wealthtechnical-afk/metastock-to-ninjatrader8-converter/tree/main/developer-toolkit).

---

## ⚠ Important
**This free kit is for education and analysis only** – not investment advice or a recommendation to buy or sell any security. WealthTechnical LLP is not a SEBI-registered investment adviser or research analyst. It contains and shares no market data: it only reads files the Downloader saved on your own PC for your personal use. WealthTechnical LLP is not affiliated with NSE or BSE. Trading futures & options, crypto and other speculative instruments involves a high risk of loss and suits only those who understand and can bear that risk. See [DISCLAIMER.md](DISCLAIMER.md) and the [full disclaimer](https://www.wealthtechnical.com/disclaimer.html).

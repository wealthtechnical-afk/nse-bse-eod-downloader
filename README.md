# WealthTechnical EOD Downloader – free NSE & BSE end-of-day data

**▶ [Get NinjaTrader 8 FREE](https://ninjatraderdomesticvendor.sjv.io/wealthtechnical)** – chart this data free in NinjaTrader 8.

Free Windows program that downloads **NSE and BSE end-of-day (EOD) stock and index data** straight from the exchanges to your PC, adjusts it for **splits, bonuses and symbol changes**, and writes it for **MetaStock, NinjaTrader 8, AmiBroker and CSV** (Excel, Python, AI tools).

**[⬇ Download the latest version (Windows)](https://www.wealthtechnical.com/eod-downloader/)** · [User guide](https://www.wealthtechnical.com/eod-downloader/) · [Releases](../../releases)

🎬 Videos: [English](https://www.youtube.com/watch?v=I0L1LM-toe8) · [हिंदी](https://www.youtube.com/watch?v=TkCG8Jj9fpc) · [How to download NinjaTrader 8](https://www.youtube.com/watch?v=mFkVCLbghkY)

## Features
- NSE and BSE stocks and indices – full history and daily updates
- Split, bonus and symbol-change adjustment
- Output formats: NinjaTrader 8 ASCII, MetaStock, AmiBroker, WealthTechnical Data Tool, CSV
- Automatic update every weekday evening (19:30 IST)
- Health status – checks your files against the exchanges
- Special sessions (e.g. Diwali Muhurat trading) detected automatically
- Digitally signed installer by WealthTechnical LLP; data and settings kept on upgrade

## Install in 3 steps
1. Download and run the installer.
2. Choose a data folder and tick your charting programs.
3. Click **Download / Update now**. After that it updates by itself on weekdays.

## Chart the data free in NinjaTrader 8
1. [Download NinjaTrader 8 free](https://ninjatraderdomesticvendor.sjv.io/wealthtechnical) ([video guide](https://www.youtube.com/watch?v=mFkVCLbghkY)).
2. Tick **NinjaTrader 8** in the downloader – it writes NT8 ASCII files.
3. In NT8: Tools → Import → Historical Data. Already have MetaStock data? Use our free [MetaStock → NT8 Converter](https://github.com/wealthtechnical-afk/metastock-to-ninjatrader8-converter).

## For developers – free India Data Kit (open source, MIT)

Build on the data this program saves on your PC. The free **[india-data-kit](india-data-kit/)** ([हिंदी](india-data-kit/README_HI.md)) gives you:

**Install:** `pip install wt-india-eod` ([PyPI](https://pypi.org/project/wt-india-eod/))

- **One-line loading** of NSE/BSE stocks, ~100 NSE indices and every watchlist (Nifty 50/100/200/500, Midcap, Smallcap, sectors) into pandas
- **Market breadth** – advances/declines, % above 50/200-day averages, new 52-week highs/lows
- **Sector rotation** table, a **scanner** example, and exports for **AmiBroker, NinjaTrader 8, MetaStock ASCII**, CSV and Parquet
- The program's own **quality and NSE-vs-BSE checks**, raw + split/bonus-adjusted prices, and a runner that starts your scripts after every evening update
- **Made-up sample data** so everything runs before you install anything

```bash
cd india-data-kit/examples
python 02_market_breadth.py auto      # 'auto' finds this program's data folder
python 03_sector_rotation.py auto
```

The kit contains and shares no market data – it only reads files on your own PC. Working with MetaStock-format data from other markets? See the [global developer toolkit](https://github.com/wealthtechnical-afk/metastock-to-ninjatrader8-converter/tree/main/developer-toolkit).

## Requirements
Windows 10 or 11 (64-bit) · internet connection

## Important
**This free tool is for education and analysis only.** Data comes directly from the NSE and BSE websites to your own computer, for your personal use. WealthTechnical LLP does not host or sell market data, and is not an investment adviser or research analyst – nothing here is investment advice. Investments in the securities market are subject to market risks. Trading futures & options, crypto and other speculative instruments involves a high risk of loss and suits only those who understand and can bear that risk. By installing you agree to the [Terms of Use](https://www.wealthtechnical.com/eod-downloader/terms.txt) and [Disclaimer](https://www.wealthtechnical.com/disclaimer.html).

MetaStock®, NinjaTrader® and AmiBroker are trademarks of their respective owners. WealthTechnical LLP is an Ecosystem Vendor of NinjaTrader Group LLC. The NinjaTrader link on this page is our referral link.

This repository hosts release notes, documentation and the open India Data Kit; the program itself is closed-source freeware.

---
**Keywords:** NSE data download, BSE data, EOD data India, bhavcopy, MetaStock data India, AmiBroker data, NinjaTrader 8 NSE data, Nifty, Sensex, CSV stock data

© WealthTechnical LLP · [wealthtechnical.com](https://www.wealthtechnical.com)

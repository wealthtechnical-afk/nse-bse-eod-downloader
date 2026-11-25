# The Downloader's data folder

The free WealthTechnical NSE/BSE EOD Downloader saves everything on your own PC. Default location `Documents\NSE_EOD`; you can change it in the program (the kit reads the choice from `%APPDATA%\NSE_EOD_Tool\settings.json`).

```
<data folder>\
├─ exports\
│  ├─ NSE\
│  │  ├─ Stocks\     CSV | AmiBroker | MetaStock | NinjaTrader8 | WealthTool
│  │  ├─ Indices\    same formats + index_symbols.csv  (index name -> symbol, e.g. NIFTY 50 -> NIFTY50)
│  │  └─ Watchlists\ Lists\NIFTY50.txt … (one symbol per line) | MetaStock | NinjaTrader8
│  └─ BSE\           same layout (BSE watchlists folder may be named "watchlists")
├─ review\           quality_report.csv, unexplained_price_jumps.csv, cross_check_nse_bse.csv,
│                    auto_corporate_actions.csv, corporate_actions_to_review.csv  (review\BSE\ for BSE)
├─ nse_eod.sqlite    raw NSE prices + corporate actions (the Downloader's own database)
└─ bse_eod.sqlite    raw BSE prices + corporate actions
```

## Formats the kit reads

| What | File | Columns |
|---|---|---|
| Stock prices (adjusted for splits & bonuses) | `exports\NSE\Stocks\CSV\SYMBOL.csv` | `Date,Open,High,Low,Close,Volume` (Date = yyyy-mm-dd) |
| Index prices | `exports\NSE\Indices\CSV\SYMBOL.csv` | same |
| Watchlists | `exports\NSE\Watchlists\Lists\NAME.txt` | one symbol per line |
| Index names | `exports\NSE\Indices\index_symbols.csv` | `index,symbol` |

**Adjustment rule (“Option A”):** splits and bonuses only. Prices before the ex-date are multiplied by the factor and volume divided by it; dividends are not adjusted. `Kit.adjusted_from_raw()` rebuilds this from the raw database so you can check it.

## The databases (advanced)
`Kit.raw()`, `Kit.corporate_actions()` and `Kit.db()` open the SQLite files **read-only**. Their layout is internal to the Downloader and may change between versions – for anything long-lived, use the exported files, which are the stable interface. Close the Downloader before heavy database queries.

## Your data, your PC
The kit never downloads, uploads or shares data. It only reads files the Downloader saved on your computer for your personal use. The Downloader fetches publicly available end-of-day files from NSE and BSE; WealthTechnical LLP does not supply or redistribute market data and is not affiliated with NSE or BSE.

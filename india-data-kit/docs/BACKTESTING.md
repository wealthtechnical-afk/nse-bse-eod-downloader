# Using the data in Python backtesting tools

The kits give you clean daily bars as a pandas DataFrame (`symbol, date, open, high, low, close, volume`), so most Python backtesting tools can use them directly. Two common routes:

## 1. Plain CSV per symbol (works with almost every tool)
```
python python/wt_india_eod.py export --list NIFTY50 --format csv-per-symbol C:/bt_data
```
Each file has `Date,Open,High,Low,Close,Volume` – the layout most backtesters, charting apps and spreadsheets read.

## 2. Straight from pandas – example with backtrader
```python
import backtrader as bt

one = df[df["symbol"] == "RELIANCE"].set_index("date")[["open", "high", "low", "close", "volume"]]

class SmaCross(bt.Strategy):
    def __init__(self):
        self.cross = bt.ind.CrossOver(bt.ind.SMA(period=50), bt.ind.SMA(period=200))
    def next(self):
        if not self.position and self.cross > 0:
            self.buy()
        elif self.position and self.cross < 0:
            self.close()

cerebro = bt.Cerebro()
cerebro.adddata(bt.feeds.PandasData(dataname=one))
cerebro.addstrategy(SmaCross)
cerebro.run()
print("final value:", round(cerebro.broker.getvalue(), 2))
```
`pip install backtrader` first. Other tools (vectorbt, zipline-style bundles, your own code) take the same DataFrame or the per-symbol CSVs.

## Before you trust a backtest
* Run the quality check first – duplicates, impossible bars, gaps and unadjusted splits distort results.
* Past or hypothetical results do not guarantee future results.

For education and analysis only – not investment advice.

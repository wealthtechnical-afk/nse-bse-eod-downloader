# Using the data with AI tools

1. Export what you need: `python python/wt_india_eod.py export --list NIFTY50 --start 2024-01-01 nifty50.csv`
2. Upload the CSV to your AI assistant and describe it: *"Columns: symbol, date, open, high, low, close, volume. Daily NSE data adjusted for splits and bonuses."*
3. Ask, for example:
   * "Which stocks are within 5 % of their 52-week high and above the 200-day average?"
   * "Rank the stocks by 3-month return and show the top 10 in a table."
   * "Plot the close and 50/200-day averages for one symbol."
   * "Write pandas code that does this so I can rerun it every day."

⚠ AI answers can be wrong – ask for the working and check it against the data. For education and analysis only – not investment advice.

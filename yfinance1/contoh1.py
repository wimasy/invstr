import yfinance as yf

bbca=yf.Ticker('BBCA.JK')

# data info emiten
bbca.info

# data history maksimum
bbca.history(period="MAX")

# data history range
bbca.history(start="2022-01-01",end="2022-02-02")

# opsi yang tersedia untuk history 
# period : 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
# interval : 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

# data history beberapa stock
data = yf.download("BBNI.JK BBCA.JK", start="2022-01-01", end="2022-04-30")
print(data)

# data dividends, splits
bbca.actions

# data dividend
bbca.dividends

# data stock split
bbca.splits

# data finansial
bbca.financials
bbca.quarterly_financials

# data neraca
bbca.balance_sheet
bbca.quarterly_balance_sheet

# data cashflow
bbca.cashflow
bbca.quarterly_cashflow

# data revenue earnings
bbca.earnings
bbca.quarterly_earnings

# data pemegang saham
bbca.major_holders

import yfinance as yf
import mplfinance as mp

data = yf.download("BBCA",start="2021-08-01", end="2021-09-1")
mp.plot(data)

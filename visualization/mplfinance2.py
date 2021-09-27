import yfinance as yf
import mplfinance as mp

data = yf.download("BBCA.JK",start="2020-08-01", end="2021-09-1")

mp.plot(data,type='candle',mav=(5,10,20),volume=True)

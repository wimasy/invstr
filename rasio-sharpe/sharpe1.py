import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

ticker = "TINS.JK"
start = "2025-04-01"
end = "2026-04-09"
risk_free_rate = 0.06
trading_days = 252

df = yf.download(ticker, start=start, end=end)
dv = df[["Volume"]]
if isinstance(df.columns, pd.MultiIndex):
    df.columns = [col[0] for col in df.columns]
df = df[["Close"]].rename(columns={"Close": "Price"})

df["Return"] = df["Price"].pct_change()


# Strategi 1: Buy & Hold
df["BH"] = df["Return"]

# Strategi 2: MA 20/50 Crossover
df["MA20"] = df["Price"].rolling(20).mean()
df["MA50"] = df["Price"].rolling(50).mean()
df["Signal_MA"] = (df["MA20"] > df["MA50"]).astype(int)
df["MA_Strategy"] = df["Signal_MA"].shift(1) * df["Return"]

# Strategi 3 : 20 Day Breakout
df["High20"] = df["Price"].rolling(20).max()
df["Signal_BO"] = (df["Price"] > df["High20"].shift(1)).astype(int)
df["BO_Strategy"] = df["Signal_BO"].shift(1) * df["Return"]

# Strategi 4 : RSI Mean Reversion
delta = df["Price"].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()
rs = avg_gain / avg_loss
df["RSI"] = 100 - (100 / (1 + rs))

df["Signal_RSI"] = 0
df.loc[df["RSI"] < 30, "Signal_RSI"] = 1
df.loc[df["RSI"] > 50, "Signal_RSI"] = 0
df["RSI_Strategy"] = df["Signal_RSI"].shift(1) * df["Return"]

# Strategi 5 : Volatility Filtered Trend
df["Vol20"] = dv["Volume"].rolling(20).std()
vol_threshold = df["Vol20"].median()

df["Signal_VolTrend"] = (
    (df["MA20"] > df["MA50"]) &
    (df["Vol20"] < vol_threshold)
).astype(int)

df["VolTrend_Strategy"] = df["Signal_VolTrend"].shift(1) * df["Return"]

# Fungsi Metrik
def sharpe_ratio(returns, rf=0.0):
    returns = returns.dropna()
    excess = returns - rf / trading_days
    return np.sqrt(trading_days) * excess.mean() / excess.std()

def total_return(returns):
    return (1 + returns.dropna()).prod() - 1

def cagr(returns):
    returns = returns.dropna()
    equity = (1 + returns).cumprod()
    years = len(returns) / trading_days
    return equity.iloc[-1] ** (1 / years) - 1

def win_rate(returns):
    returns = returns.dropna()
    traded = returns != 0
    wins = returns[traded] > 0
    return wins.sum() / traded.sum()

def max_drawdown(returns):
    returns = returns.dropna()
    equity = (1 + returns).cumprod()
    running_max = equity.cummax()
    drawdown = equity / running_max - 1
    return drawdown.min()

results = pd.DataFrame({
    "Total Return (%)": {
        "Buy & Hold": total_return(df["BH"]) * 100,
        "MA Crossover": total_return(df["MA_Strategy"]) * 100,
        "Breakout": total_return(df["BO_Strategy"]) * 100,
        "RSI Mean Reversion": total_return(df["RSI_Strategy"]) * 100,
        "Vol Filtered Trend": total_return(df["VolTrend_Strategy"]) * 100,
    },
    "CAGR (%)": {
        "Buy & Hold": cagr(df["BH"]) * 100,
        "MA Crossover": cagr(df["MA_Strategy"]) * 100,
        "Breakout": cagr(df["BO_Strategy"]) * 100,
        "RSI Mean Reversion": cagr(df["RSI_Strategy"]) * 100,
        "Vol Filtered Trend": cagr(df["VolTrend_Strategy"]) * 100,
    },
    "Sharpe": {
        "Buy & Hold": sharpe_ratio(df["BH"], risk_free_rate),
        "MA Crossover": sharpe_ratio(df["MA_Strategy"], risk_free_rate),
        "Breakout": sharpe_ratio(df["BO_Strategy"], risk_free_rate),
        "RSI Mean Reversion": sharpe_ratio(df["RSI_Strategy"], risk_free_rate),
        "Vol Filtered Trend": sharpe_ratio(df["VolTrend_Strategy"], risk_free_rate),
    },
    "Win Rate (%)": {
        "Buy & Hold": win_rate(df["BH"]) * 100,
        "MA Crossover": win_rate(df["MA_Strategy"]) * 100,
        "Breakout": win_rate(df["BO_Strategy"]) * 100,
        "RSI Mean Reversion": win_rate(df["RSI_Strategy"]) * 100,
        "Vol Filtered Trend": win_rate(df["VolTrend_Strategy"]) * 100,
    },
    "Max Drawdown (%)": {
        "Buy & Hold": max_drawdown(df["BH"]) * 100,
        "MA Crossover": max_drawdown(df["MA_Strategy"]) * 100,
        "Breakout": max_drawdown(df["BO_Strategy"]) * 100,
        "RSI Mean Reversion": max_drawdown(df["RSI_Strategy"]) * 100,
        "Vol Filtered Trend": max_drawdown(df["VolTrend_Strategy"]) * 100,
    }
})

print("\nHasil Strategi:")
print(results.round(2).sort_values("Sharpe", ascending=False))

equity = (1 + df[
    ["BH", "MA_Strategy", "BO_Strategy", "RSI_Strategy", "VolTrend_Strategy"]
].fillna(0)).cumprod()

equity.columns = [
    "Buy & Hold",
    "MA Crossover",
    "Breakout",
    "RSI Mean Reversion",
    "Vol Filtered Trend"
]

plt.figure(figsize=(11, 6))
equity.plot()
plt.title(f"Perbandingan Strategi – {ticker}")
plt.xlabel("Tanggal")
plt.ylabel("Ekuitas")
plt.grid(True)
plt.show()

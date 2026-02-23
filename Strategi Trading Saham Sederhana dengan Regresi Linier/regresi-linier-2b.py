import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Download
ticker = "BMRI.JK"
data = yf.download(ticker, start="2023-01-01", end="2026-01-01")

close_price_data = data[['Close']]

# Return harian
data['Return'] = data['Close'].pct_change()
data.dropna(inplace=True)

# Return(n-1)
data['Return(n-1)'] = data['Return'].shift(1)
data.dropna(inplace=True)

X = data[['Return(n-1)']]
y = data['Return']

model = LinearRegression()
model.fit(X, y)

print("Slope (A):", model.coef_[0])
print("Intercept (B):", model.intercept_)

data['Predicted'] = model.predict(X)

plt.figure(figsize=(10,6))
plt.scatter(data['Return(n-1)'], data['Return'], alpha=0.4, label='Return Aktual')
plt.plot(data['Return(n-1)'], data['Predicted'], color='red', linewidth=2, label='Garis Regresi')
plt.title('Linear Regression: Prediksi Return')
plt.xlabel('Return(n-1)')
plt.ylabel('Return')
plt.legend()
plt.show()

#Backtest

split = data.index.searchsorted('2025-01-01')
train = data.iloc[:split].copy()
test = data.iloc[split:].copy()

X_train = train[['Return(n-1)']]
y_train = train['Return']

model = LinearRegression()
model.fit(X_train, y_train)

X_test = test[['Return(n-1)']]
test['Predicted'] = model.predict(X_test)

test['Signal'] = np.where(test['Predicted'] > 0, 1, -1)

test['AdjSignal'] = 0
position = 0

#Sell hanya terjadi setelah Buy
for i, row in test.iterrows():
    
    current_signal_value = row['Signal'].item()

    if current_signal_value == 1 and position == 0:
        test.loc[i, 'AdjSignal'] = 1
        position = 1
    elif current_signal_value == -1 and position == 1:
        test.loc[i, 'AdjSignal'] = -1
        position = 0
    else:
        test.loc[i, 'AdjSignal'] = 0

test['Signal'] = test['AdjSignal']

#Return
test['Strategy'] = test['Signal'].shift(1) * test['Return']
test['Kumulatif Strategi'] = (1 + test['Strategy']).cumprod()
test['Kumulatif Market'] = (1 + test['Return']).cumprod()

strategy_return = test['Strategy'].mean()
strategy_vol = test['Strategy'].std()
market_return = test['Return'].mean()
sharpe = strategy_return / strategy_vol

print("Sharpe Ratio:", sharpe)
print("Return Kumulatif Strategi:", test['Kumulatif Strategi'].iloc[-1])
print("Return Kumulatif Market:", test['Kumulatif Market'].iloc[-1])

plt.figure(figsize=(10,6))
test['Kumulatif Strategi'].plot(label='Strategi')
test['Kumulatif Market'].plot(label='Market', color='gray', linestyle='--')
plt.title('Strategi Linear Regression vs Market (Periode Test)')
plt.legend()
plt.xlabel('Tanggal')
plt.ylabel('Return Kumulatif')
plt.show()

## BUY SELL
plt.figure(figsize=(14, 7))
plt.plot(test['Close'], label='Close', color='blue', alpha=0.7)

buy_signals_adjusted = test[test['Signal'] == 1]
sell_signals_adjusted = test[test['Signal'] == -1]

plt.plot(buy_signals_adjusted.index, buy_signals_adjusted['Close'], '^', markersize=10, color='green', label='Buy')
plt.plot(sell_signals_adjusted.index, sell_signals_adjusted['Close'], 'v', markersize=10, color='red', label='Sell')

plt.title('Close & Signal Buy/Sell')
plt.xlabel('Tanggal')
plt.ylabel('Close')
plt.legend()
plt.grid(True)
plt.show()

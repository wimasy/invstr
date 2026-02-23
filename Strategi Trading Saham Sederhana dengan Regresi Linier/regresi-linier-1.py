import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Download stock data
ticker = "BMRI.JK"
data = yf.download(ticker, start="2023-01-01", end="2026-01-01")

close_price_data = data[['Close']]

# Return
data['Return'] = data['Close'].pct_change()
data.dropna(inplace=True)

# Use Return(n-1) Return to predict next-day Return
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
plt.title(f'Regresi Linier: Prediksi Return ({ticker})')
plt.xlabel('Return (n-1)')
plt.ylabel('Return')
plt.legend()
plt.show()

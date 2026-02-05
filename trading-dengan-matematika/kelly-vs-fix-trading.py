import numpy as np
import matplotlib.pyplot as plt

# Parameter
n_trades = 20
initial_capital = 10000
win_prob = 0.55
win_return = 0.10
loss_return = -0.05

# Kelly fraction
b = abs(win_return / loss_return)
kelly_fraction = (win_prob * (b + 1) - 1) / b
#print(f"Optimal Kelly fraction: {kelly_fraction*100:.2f}%")

# Modal awal
capital_fixed = [initial_capital]
capital_kelly = [initial_capital]

# Simulasi
for _ in range(n_trades):
    # Hasil : win or lose, secara random
    is_win = np.random.rand() < win_prob

    # Trader 1 fixed 10% risk
    risk_fixed = 0.10
    change_fixed = win_return if is_win else loss_return
    capital_fixed.append(capital_fixed[-1] * (1 + risk_fixed * (change_fixed / abs(loss_return))))

    # Trader 2 Kelly-based risk
    risk_kelly = kelly_fraction
    capital_kelly.append(capital_kelly[-1] * (1 + risk_kelly * (change_fixed / abs(loss_return))))

# Plot
plt.figure(figsize=(10,6))
plt.plot(capital_fixed, label="Fixed 10% Risk Trader")
plt.plot(capital_kelly, label="Kelly Criterion Trader")
plt.title("Kelly Criterion vs Fixed-Risk Trading")
plt.xlabel("Jumlah trading")
plt.ylabel("Kapital")
plt.legend()
plt.grid(True)
plt.show()

# Print final results
fixed_return = (capital_fixed[-1] / initial_capital - 1) * 100
kelly_return = (capital_kelly[-1] / initial_capital - 1) * 100
print(f"Fixed Risk Trader Final: {capital_fixed[-1]:,.2f} | Return: {fixed_return:.2f}%")
print(f"Kelly Trader Final:     {capital_kelly[-1]:,.2f} | Return: {kelly_return:.2f}%")

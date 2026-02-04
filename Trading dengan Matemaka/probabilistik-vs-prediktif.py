import numpy as np
import matplotlib.pyplot as plt

# Parameter
n_trades = 10
initial_capital = 100000

# Probabilistic trader setup
win_prob = 0.55
win_return = 0.10
loss_return = -0.05

# Predictive trader setup
# Rasio kalah menang 50:50
pred_win_prob = 0.50
pred_win_return = 0.12
pred_loss_return = -0.12

## EV
ev_prob = (win_prob * win_return) + ((1 - win_prob) * loss_return)
ev_pred = (pred_win_prob * pred_win_return) + ((1 - pred_win_prob) * pred_loss_return)

# Portofolio awal
prob_capital = [initial_capital]
pred_capital = [initial_capital]
pred2_capital = [initial_capital]

position_size = 1.0

# Simulasi
for _ in range(n_trades):
    # Probabilistic trader — resiko tetap
    r_prob = np.random.choice([win_return, loss_return], p=[win_prob, 1 - win_prob])
    prob_capital.append(prob_capital[-1] * (1 + r_prob))

    # Predictive trader — menebak, hasil bervariasi
    r_pred = np.random.choice([pred_win_return, pred_loss_return], p=[pred_win_prob, 1 - pred_win_prob])
    pred_capital.append(pred_capital[-1] * (1 + r_pred))

    # Emosional overconfiden: menambah resiko setelah menang, dan mengurangi setelah kalah.
    r_pred_2 = np.random.choice([pred_win_return, pred_loss_return], p=[pred_win_prob, 1 - pred_win_prob])
    pred2_capital.append(pred2_capital[-1] * (1 + r_pred * position_size))
    # tambah 30% jika menang, kurangi 70% setelah kalah
    position_size = 1.3 if r_pred > 0 else 0.7


# Plot
plt.figure(figsize=(10,6))
plt.plot(prob_capital, label="Trader Probabilistik (55% win rate, steady risk)")
plt.plot(pred_capital, label="Trader Prediktif (50% win rate, inconsistent risk)", alpha=0.8)
plt.plot(pred2_capital, label="Trader Prediktif (50% win rate, emotional risk, overconfidence)", alpha=0.8)
plt.title("Trader Probabilistik vs Prediktif")
plt.xlabel("Jumlah Trade")
plt.ylabel("Kapital")
plt.legend()
plt.grid(True)
plt.show()

# summary stats
prob_return = (prob_capital[-1] / initial_capital - 1) * 100
pred_return = (pred_capital[-1] / initial_capital - 1) * 100
pred2_return = (pred2_capital[-1] / initial_capital - 1) * 100

print(f"Trader Probabilistik Final: {prob_capital[-1]:,.2f}  | Total Return: {prob_return:.2f}%")
print(f"Trader Prediktif Final:    {pred_capital[-1]:,.2f}  | Total Return: {pred_return:.2f}%")
print(f"Trader Prediktif (Over) Final:    {pred2_capital[-1]:,.2f}  | Total Return: {pred2_return:.2f}%")
print("-" * 5)
print("Expected Value per Trade:")
print(f"Trader Probabilistik EV = {ev_prob*100:.2f}% per trade")
print(f"Trader Prediktif EV = {ev_pred*100:.2f}% per trade")
print("-" * 50)

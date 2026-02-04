import pandas as pd
import numpy as np

# === Strategy parameters ===
# Format: (win_rate, gain %, loss %)
strategies = [
    (0.45, 1.5, 1),
    (0.60, 20, 15),
    (0.7, 10, 2),
    (0.6, 10, 3),
    (0.4, 20, 5),
    (0.739,12.21, 5),
    (0.3,10,1),
    (0.4,5,3)
]

Z = 1.96          # 95% confidence level
E = 0.05          # margin of error (5%)
modal = 100000000  # modal awal

rows = []

for win_rate, gain, loss in strategies:
    loss_rate = 1 - win_rate  

    gain_r = gain / 100
    loss_r = loss / 100

    # Proporsi jumlah sampel
    n_trading = (Z**2 * win_rate * (1 - win_rate)) / (E**2)
    n_trading = round(n_trading)

    # Expected Value
    ev = (win_rate * gain) - (loss_rate * loss)

    # Skip losing - jika ev < 0 tidak perlu dihitung, karena pasti rugi
    if ev <= 0:
        rows.append({
            "Win rate": win_rate,
            "Loss rate": loss_rate,
            "Gain %": gain,
            "Loss %": loss,
            "EV %": ev,
            "N Trading (95%)": "-",
            "Kelly %": "-",
            "Modal": modal,
            "Modal Kelly": "-",
            "10% Modal": "-",
            "25% Modal": "-",
            "50% Modal": "-",
            "ROR Kelly": "-",
            "ROR 10%": "-",
            "ROR 25%": "-",
            "ROR 50%": "-",
        })
        continue  # stop

    # Kelly fraction
    kelly_fraction = (win_rate * (gain_r / loss_r) - loss_rate) / (gain_r / loss_r)
   
    # Position sizing
    modal_kelly = modal * kelly_fraction
    modal_10 = modal * 0.10
    modal_25 = modal * 0.25
    modal_50 = modal * 0.50

    # Risk of Ruin
    def ror(cap, bet):
        if bet <= 0:
            return 1
        val = ((1-win_rate)/win_rate) * (1/(gain / loss))
        return val ** (cap / bet)

    ror_kelly = ror(modal, modal_kelly)
    ror_10 = ror(modal, modal_10)
    ror_25 = ror(modal, modal_25)
    ror_50 = ror(modal, modal_50)
    rows.append({
        "Win rate": win_rate,
        "Loss rate": loss_rate,
        "Gain %": gain,
        "Loss %": loss,
        "EV %": ev,
        "N Trade": n_trading,
        "Kelly %": kelly_fraction,
        "Modal": f"{modal:,}",
        "Modal Kelly": f"{modal_kelly:,.0f}%",
        "ROR Kelly": f"{ror_kelly:.2f}%",
        "Modal 10%": f"{modal_10:,.0f}%",
        "ROR 10%": f"{ror_10:.2f}%",
        "Modal 25%": f"{modal_25:,.0f}%",
        "ROR 25%": f"{ror_25:.2f}%",
        "Modal 50%": f"{modal_50:,.0f}%",        
        "ROR 50%": f"{ror_50:.2f}%"
    })

df = pd.DataFrame(rows)
pd.set_option('display.width', 1000)
#pd.options.display.float_format = '{:,.2f}'.format
print(df)

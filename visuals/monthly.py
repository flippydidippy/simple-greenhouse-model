import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_monthly_means(simulated_data):
    """Plots monthly mean greenhouse temperature, external temperature, and dni."""

    simulated_data["month"] = simulated_data["time"].dt.strftime('%b')  # 'Jan', 'Feb', ...
    simulated_data["month_num"] = simulated_data["time"].dt.month  # 1, 2, 3, ...
    monthly_means = simulated_data.groupby("month_num").mean(numeric_only=True)

    # colors
    num_months = len(monthly_means)
    colors = plt.cm.viridis(np.linspace(0, 1, num_months)) 

    fig, ax1 = plt.subplots(figsize=(12, 6))
    for i, (month_num, row) in enumerate(monthly_means.iterrows()):
        month_label = simulated_data.loc[simulated_data["month_num"] == month_num, "month"].iloc[0]
        
        ax1.scatter(month_label, row["greenhouse_temperature"], color=colors[i], label=f"{month_label} - Greenhouse Temp", marker="o", s=100)
        ax1.scatter(month_label, row["temperature"], color=colors[i], label=f"{month_label} - External Temp", marker="s", s=100)

    ax1.set_xlabel("Month")
    ax1.set_ylabel("Temperature (°C)")
    ax1.set_title("Monthly Mean Temperatures and dni")
    
    # dni
    ax2 = ax1.twinx()
    for i, (month_num, row) in enumerate(monthly_means.iterrows()):
        month_label = simulated_data.loc[simulated_data["month_num"] == month_num, "month"].iloc[0]
        ax2.scatter(month_label, row["dni"], color=colors[i], label=f"{month_label} - dni", marker="^", s=100, edgecolors="black")

    ax2.set_ylabel("dni (W/m²)")

    # combine
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2, loc="upper left", fontsize=10)

    plt.grid()
    plt.show()


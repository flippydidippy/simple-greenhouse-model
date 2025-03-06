import matplotlib.pyplot as plt
import pandas as pd

def plot_monthly_hourly_means(simulated_data, month=None):
    """
    Plots hourly mean GH temperature, external temperature, and solar for a selected month.
    
    Args:
        simulated_data (pd.DataFrame): The simulation output data.
        selected_month (str, optional): The month to display (e.g., "Jan", "Feb"). If None, default to first available month.
    """

    simulated_data["month"] = simulated_data["time"].dt.strftime('%b')
    simulated_data["hour"] = simulated_data["time"].dt.hour
    if month is None:
        month = simulated_data["month"].unique()[0]
    month_data = simulated_data[simulated_data["month"] == month]
    if month_data.empty:
        print(f"No data found for month '{month}'. Please check the dataset.")
        return
    hourly_means = month_data.groupby("hour").mean(numeric_only=True)

    _, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(hourly_means.index, hourly_means["GH_T_air"], label="GH Temp", color="blue", linestyle="-", marker="o")
    ax1.plot(hourly_means.index, hourly_means["temperature"], label="External Temp", color="red", linestyle="dashed", marker="s")

    ax1.set_xlabel("Hour of the Day")
    ax1.set_ylabel("Temperature (°C)")
    ax1.set_title(f"Hourly Mean Temperatures and solar for {month}")
    ax1.set_xticks(range(0, 24, 1))  # Ensure x-axis has all hours (0-23)
    ax1.legend(loc="upper left")

    ax2 = ax1.twinx()
    ax2.plot(hourly_means.index, hourly_means["solar"], label="solar", color="orange", linestyle="dotted", marker="^")
    ax2.set_ylabel("solar (W/m²)")
    ax2.legend(loc="upper right")

    plt.grid()
    plt.show()

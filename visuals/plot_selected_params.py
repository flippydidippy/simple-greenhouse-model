import pandas as pd
import matplotlib.pyplot as plt

def plot_parameters(df, parameters, date):
    df["time"] = pd.to_datetime(df["time"])
    daily_data = df[df["time"].dt.date == pd.to_datetime(date).date()]
    plt.figure(figsize=(12, 6))

    for param in parameters:
        if param in daily_data.columns:
            plt.plot(daily_data["time"], daily_data[param], marker='o', markersize=3, linewidth=1, label=param)
        else:
            print(f"Warning: Parameter '{param}' not found in the DataFrame.")

    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(f"Selected Parameters for {date}")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)

    plt.show()
    plt.close('all')

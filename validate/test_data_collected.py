import pandas as pd
import matplotlib.pyplot as plt
import os

hourly_file_path = "data/validate_data/suticollo 2025-02-11 to 2025-02-19.csv"
df_hourly = pd.read_csv(hourly_file_path, parse_dates=["datetime"])
df_hourly = df_hourly.rename(columns={"datetime": "Date", "temp": "online data"})
df_hourly["online data"] = (df_hourly["online data"] - 32) * 5.0 / 9.0


data_path = "data/validate_data/"
csv_files = {
    "Sensor 4": os.path.join(data_path, "1.csv"),
    "Sensor 2": os.path.join(data_path, "2.csv"),
    "Sensor 3": os.path.join(data_path, "3.csv"),
    "Sensor 1": os.path.join(data_path, "4.csv"),
}

sensor_names = {
    "Sensor 4": "top_temp",
    "Sensor 2": "croplvl_temp",
    "Sensor 3": "air_temp",
    "Sensor 1": "outside_temp",
}

data_frames = {}
for sensor, file in csv_files.items():
    df = pd.read_csv(file, delimiter=";", parse_dates=["Date"], dayfirst=True)
    df = df.rename(columns={df.columns[2]: sensor})
    data_frames[sensor] = df[["Date", sensor]]

# merging all
merged_df = data_frames["Sensor 4"]
for sensor in ["Sensor 2", "Sensor 3", "Sensor 1"]:
    merged_df = merged_df.merge(data_frames[sensor], on="Date", how="outer")

merged_df = merged_df.sort_values(by="Date")
merged_df["DateOnly"] = merged_df["Date"].dt.date
last_day = merged_df["DateOnly"].max()
merged_df = merged_df[merged_df["DateOnly"] < last_day]
unique_days = merged_df["DateOnly"].unique()



for day in unique_days:
    daily_data = merged_df[merged_df["DateOnly"] == day]
    hourly_data = df_hourly[df_hourly["Date"].dt.date == day]
    
    plt.figure(figsize=(12, 6))
    
    for sensor in ["Sensor 1", "Sensor 2", "Sensor 3", "Sensor 4"]:
        plt.plot(daily_data["Date"], daily_data[sensor], marker='o', markersize=1, linewidth=0.5, label=sensor_names[sensor])
    
    # plot online data to fill
    plt.plot(hourly_data["Date"], hourly_data["online data"], linestyle="--", linewidth=1, color="red", label="online data")
    
    plt.xlabel("Time")
    plt.ylabel("Temperature")
    plt.title(f"Temperature Readings for {day}")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    
    plt.show()

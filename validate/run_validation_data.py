import pandas as pd
import os
from simulation.run import run_simulation  # Import your simulation function
from analysis.RMSE import calculate_rmse  # Import your RMSE function
from data.read_nrel import compile_nrel_data

def validate_simulation(data_path, params_dict=None):

    csv_files = {
        "Sensor 1": os.path.join(data_path, "1.csv"),  # Top Temp
        "Sensor 2": os.path.join(data_path, "2.csv"),  # Crop Level Temp
        "Sensor 3": os.path.join(data_path, "3.csv"),  # Air Temp
        "Sensor 4": os.path.join(data_path, "4.csv"),  # Outside Temp
    }

    sensor_names = {
        "Sensor 1": "top_temp",
        "Sensor 2": "croplvl_temp",
        "Sensor 3": "air_temp",
        "Sensor 4": "outside_temp",
    }

    # aggrigate to hourly
    data_frames = []
    for sensor, file in csv_files.items():
        df = pd.read_csv(file, delimiter=";", parse_dates=["Date"], dayfirst=True)
        df = df.rename(columns={df.columns[2]: sensor_names[sensor]})  # rename
        df = df.set_index("Date").resample("h").mean().reset_index()  # hourly (through averaging)
        data_frames.append(df[["Date", sensor_names[sensor]]])

    # merge sensor data
    merged_df = data_frames[0]
    for df in data_frames[1:]:
        merged_df = merged_df.merge(df, on="Date", how="outer")

    merged_df = merged_df.sort_values(by="Date")
    merged_df = merged_df.rename(columns={"Date": "time"})  #align columns

    #loud hourly
    hourly_file_path = os.path.join(data_path, "suticollo 2025-02-11 to 2025-02-19.csv")
    df_hourly = pd.read_csv(hourly_file_path, parse_dates=["datetime"])

    solar_angle_data_path = os.path.join(data_path, "solar_angle.csv")
    solar_angle_data = compile_nrel_data(solar_angle_data_path)


    df_hourly = df_hourly.rename(columns={"datetime": "time", "humidity": "humidity", "solarradiation": "solar"}) # keep relevant only in our data

    merged_df["time"] = pd.to_datetime(merged_df["time"]) # ensure timestamps are good
    df_hourly["time"] = pd.to_datetime(df_hourly["time"])
    solar_angle_data["time"] = pd.to_datetime(solar_angle_data["time"])

    merged_df = pd.merge_asof(merged_df, solar_angle_data[["time", "solar_angle"]], on="time", direction="nearest")
    merged_df = pd.merge_asof(merged_df, df_hourly[["time", "humidity", "solar"]], on="time", direction="nearest")

    # filling in the values missing
    #merged_df["humidity"].fillna(constant_humidity, inplace=True)
    #merged_df["solar"].fillna(constant_solar, inplace=True)
    merged_df["temperature"] = merged_df["outside_temp"]
    merged_df["pressure"] = 721

    T_air_init = merged_df["air_temp"].dropna().iloc[0]  
    T_top_init = merged_df["top_temp"].dropna().iloc[0]  
    RH_init = merged_df["humidity"].dropna().iloc[0]  

    simulated_data, cycles, crop_mass = run_simulation(merged_df, T_air_init, T_top_init, RH_init, "Lettuce", 3600, "suticollo_opt1.json", params_dict) # run sim
    #simulated_data.to_csv("data/raqaypampa/simulated_greenhouse_suticollo_2025.csv", index=False)


    # compute difference
    simulated_data["difference"] = simulated_data["air_temp"] - simulated_data["GH_T_air"]

    # compute rmse
    rmse_value = calculate_rmse(simulated_data["air_temp"], simulated_data["GH_T_air"])
    simulated_data["RMSE"] = rmse_value

    return simulated_data

import pandas as pd

def load_csv_profile():
    pass


def save_csv():
    pass


def compile_nrel_data(file_path):
    weather_data = pd.read_csv(file_path, skiprows=2)

    # Rename columns for clarity's sake.
    weather_data = weather_data.rename(columns={
        "Year": "year",
        "Month": "month",
        "Day": "day",
        "Hour": "hour",
        "Temperature": "temperature",
        "Relative Humidity": "humidity",
        "Pressure": "pressure",
        "DNI": "solar",
        "Solar Zenith Angle": "solar_angle"
    })


    weather_data["time"] = pd.to_datetime(weather_data[["year", "month", "day", "hour"]]) # single data format
    weather_data = weather_data[["time", "year", "month", "day", "hour", "temperature", "humidity", "solar", "pressure", "solar_angle"]] # relevant info
    weather_data[["temperature", "humidity", "solar", "solar_angle"]] = weather_data[["temperature", "humidity", "solar", "solar_angle"]].astype(float) # to float

    #weather_data["pressure"] *= 100 # hPa to Pa

    return weather_data
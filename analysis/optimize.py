import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution
from simulation.run import run_simulation 
from greenhouse_setups.params import update_params
from data.read_nrel import compile_nrel_data


PLANT_TEMPERATURE_RANGES = {
    "Wheat": {"day_min": 15, "day_max": 25, "night_min": 10, "night_max": 15},
    "Potato": {"day_min": 18, "day_max": 22, "night_min": 10, "night_max": 15},
    "Tomato": {"day_min": 21, "day_max": 27, "night_min": 16, "night_max": 18},
    "Cassava": {"day_min": 25, "day_max": 29, "night_min": 18, "night_max": 22},
    "Carrot": {"day_min": 16, "day_max": 24, "night_min": 10, "night_max": 15},
    "Greenbean": {"day_min": 18, "day_max": 24, "night_min": 15, "night_max": 18},
    "Maize": {"day_min": 24, "day_max": 30, "night_min": 18, "night_max": 22},
    "Lettuce": {"day_min": 15, "day_max": 20, "night_min": 10, "night_max": 15},
    "Chard": {"day_min": 16, "day_max": 24, "night_min": 10, "night_max": 15},
    "Parsley": {"day_min": 16, "day_max": 24, "night_min": 10, "night_max": 15},
    "Barley": {"day_min": 15, "day_max": 25, "night_min": 10, "night_max": 15},
    "Beans": {"day_min": 18, "day_max": 24, "night_min": 15, "night_max": 18},
    "Peas": {"day_min": 16, "day_max": 24, "night_min": 10, "night_max": 15},
    "Squash": {"day_min": 24, "day_max": 30, "night_min": 18, "night_max": 22},
    "Quinoa": {"day_min": 15, "day_max": 25, "night_min": 10, "night_max": 15}
}



def simulate_greenhouse_raqaypampa(year, crop, profile, params=None):
    file_path = f"data/raqaypampa/{year}.csv"
    weather_data = compile_nrel_data(file_path)
    
    # init
    T_init = weather_data["temperature"].iloc[0]
    RH_init = weather_data["humidity"].iloc[0]  # Initial humidity

    simulated_data, cycles, crop_mass = run_simulation(weather_data, T_init, T_init, RH_init, crop, 3600, profile, params)
    
    return simulated_data, cycles, crop_mass


def optimize_greenhouse_design(year, crop, optimizing_strategy):
    """
    Optimizes greenhouse parameters to maintain ideal temperature ranges for plant growth.

    Args:
        year (int): The year of weather data to use.
        crop (str): The type of plant being grown (default: tomato).

    Returns:
        dict: Optimized greenhouse parameters.
    """
    #target_temps = PLANT_TEMPERATURE_RANGES.get(crop)

    param_bounds = {
        "nr_water_bottles": (0, 50),
        "bottles_percent_open": (0,1),
        #"wall_conductivity": (0.8, 0.9),
        "wall_thickness": (0.10, 0.5),  # Wall thickness in meters
        "gh_length": (3, 10),
        "gh_width": (3, 10),  # Greenhouse area in m²
        "gh_height": (1.5, 5),  # Greenhouse area in m²
        "gh_roof_height": (0,0.5)
    }

    bounds = [param_bounds[key] for key in param_bounds.keys()]

    def objective_function1(param_values):
        """
        Objective function for optimization: Minimize temperature deviation from ideal range.
        """
        # Map parameter values
        param_keys = list(param_bounds.keys())
        param_dict = {param_keys[i]: param_values[i] for i in range(len(param_keys))}

        simulated_data, _ = simulate_greenhouse_raqaypampa(year, crop, "raqay_default.json", param_dict)
        T_greenhouse = simulated_data["GH_T_air"]

        day_mask = (simulated_data["time"].dt.hour >= 6) & (simulated_data["time"].dt.hour < 18)
        night_mask = ~day_mask


        rmse_day = np.sqrt(np.mean(np.maximum(0, T_greenhouse[day_mask] - target_temps["day_max"])**2 + np.maximum(0, target_temps["day_min"] - T_greenhouse[day_mask])**2))

        rmse_night = np.sqrt(np.mean(np.maximum(0, T_greenhouse[night_mask] - target_temps["night_max"])**2 + np.maximum(0, target_temps["night_min"] - T_greenhouse[night_mask])**2))

        total_rmse = rmse_day + rmse_night

        print(f"Trying Parameters: {param_dict}, RMSE: {total_rmse:.4f}")

        return total_rmse

    def objective_function2(param_values):
        """
        Objective function: maximize the amount of cycles.
        """
        # Map parameter values
        param_keys = list(param_bounds.keys())
        param_dict = {param_keys[i]: param_values[i] for i in range(len(param_keys))}

        simulated_data, cycles, crop_mass = simulate_greenhouse_raqaypampa(year, crop, "raqay_default.json", param_dict)
        print(f"Trying Parameters: {param_dict}, CYCLES: {cycles:.4f}, CROP MASS {crop_mass:.4f}")

        return -cycles

    def objective_function3(param_values):
        """
        Objective function: maximize the amount of cycles.
        """
        # Map parameter values
        param_keys = list(param_bounds.keys())
        param_dict = {param_keys[i]: param_values[i] for i in range(len(param_keys))}

        simulated_data, cycles, crop_mass = simulate_greenhouse_raqaypampa(year, crop, "raqay_default.json", param_dict)
        print(f"Trying Parameters: {param_dict}, CYCLES: {cycles:.4f}, CROP MASS {crop_mass:.4f}")

        return -crop_mass

    if optimizing_strategy == "cycle":
        result = differential_evolution(objective_function2, bounds, strategy="best1bin", popsize=15, tol=0.1)

    elif optimizing_strategy == "crop_mass":
        result = differential_evolution(objective_function3, bounds, strategy="best1bin", popsize=15, tol=0.1)
    else:
        result = differential_evolution(objective_function1, bounds, strategy="best1bin", popsize=15, tol=0.1)



    result = differential_evolution(objective_function2, bounds, strategy="best1bin", popsize=15, tol=0.5)
    optimal_params = {list(param_bounds.keys())[i]: result.x[i] for i in range(len(result.x))}

    print("\noptimal Greenhouse params:")
    print(optimal_params)
    update_params(optimal_params)

    return optimal_params

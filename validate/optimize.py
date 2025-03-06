import numpy as np
import pandas as pd
from scipy.optimize import minimize
from validate.run_validation_data import validate_simulation  # Your validation function
from greenhouse_setups.params import update_all_params, roof_solar_absorp_coef, wall_solar_absorp_coef  # Import parameter update function
from analysis.RMSE import calculate_rmse  # Import RMSE function
from scipy.optimize import differential_evolution
from visuals.plot_selected_params import plot_parameters
from analysis.RMSE import rmse_for_validation


def optimize_params():

    global param_bounds

    # Define parameter bounds for optimization (lower bound, upper bound)
    param_bounds = {
        #"h_conv": (20, 25),  # Convective heat transfer coefficient
        "wall_solar_absorp_coef": (0, 100),  # Solar radiation absorption fraction
        "roof_solar_absorp_coef": (0, 1000),  # Solar radiation absorption fraction
        "vent_rate": (0, 100),  # Air exchange rate
        "top_vent_rate": (0, 100),
        #"thermal_mass": (0, 10000),
        #"thermal_mass_top": (0, 10000)
        #"plant_transpiration_rate": (0.0001, 0.1),  # Transpiration effect on humidity
        #"soil_depth": (0.001, 5),  # Soil depth range (m)
        #"soil_conduct": (0.1, 5),  # Soil thermal conductivity (W/mK)
    }
    #init_guess = [20, 73, 5, 3]
    bounds = [param_bounds[key] for key in param_bounds.keys()]


    # run opt
    result = differential_evolution(objective_function, bounds, strategy="best1bin", popsize=15, tol=0.1)

    # params extract
    optimal_params = {list(param_bounds.keys())[i]: result.x[i] for i in range(len(result.x))}

    print("\nOptimal Parameters Found:")
    print(optimal_params)

    recorded_data_path = "data/validate_data/"
    validated_results = validate_simulation(recorded_data_path)

    return optimal_params, validated_results

def objective_function(param_values):
    """
    Objective function for optimization, runs the simulation with given parameters and returns the RMSE.
    
    Parameters:
        param_values (list): List of parameter values in the order of param_keys.
    
    Returns:
        float: RMSE value (error between simulation and recorded data).
    """

    
    param_keys = list(param_bounds.keys()) # mapping to values
    param_dict = {param_keys[i]: param_values[i] for i in range(len(param_keys))}


    recorded_data_path = "data/validate_data/"  
    validated_results = validate_simulation(recorded_data_path, param_dict) # run
    rmse = rmse_for_validation(validated_results)

    print(f"Trying Parameters: {param_dict}, RMSE: {rmse:.4f}")

    # date = "2025-02-12"
    # if rmse < 10:
    #     plot_parameters(validated_results, ["GH_T_air", "GH_T_top", "GH_T_ground", "GH_T_wall_ext", "GH_T_wall_int", "air_temp", "outside_temp", "top_temp"], date)

    return rmse  # We want to minimize this value



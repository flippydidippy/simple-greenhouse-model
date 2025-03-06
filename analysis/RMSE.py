import numpy as np

def calculate_rmse(actual, predicted):
    """Computes the Root Mean Square Error (RMSE) for the actualy and perdicted values.

    Parameters:
        actual (array): The observed/measured values.
        predicted (array): The predicted values.

    Returns:
        float: The RMSE value.
    """
    
    if actual.shape != predicted.shape:
        raise ValueError("Input arrays must have the same shape.")

    return np.sqrt(np.mean((np.array(actual) - np.array(predicted))**2))

def rmse_for_validation(data):
    rmse = calculate_rmse(data["air_temp"], data["GH_T_air"])
    rmse2 = calculate_rmse(data["top_temp"], data["GH_T_top"])

    return rmse+rmse2
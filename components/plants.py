import numpy as np

def humidity_effect(humidity, plant_count, transpiration_rate):
    """Increase in humidity due to plant transpiration.

    Args:
        humidity (float): humidity (RH)
        plant_count (float): number of plants (approx.)
        transpiration_rate (float): transpiration rate coef. ex. kg/time unit plant

    Returns:
        float: _description_
    """
    return transpiration_rate * plant_count * humidity

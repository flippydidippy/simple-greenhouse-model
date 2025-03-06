import numpy as np

def solar_rad_calc(solar_radiation, solar_absorption, area):
    """Heat gain from solar radiation

    Args:
        solar_radiation (float): radiation from the sun
        solar_absorption (float): absorption coef. from the sun
        area (float): area affected (heated)

    Returns:
        float: heat transfer per unit time.
    """
    return solar_absorption * solar_radiation * area 

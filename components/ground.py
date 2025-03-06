import numpy as np
from greenhouse_setups.params import soil_conduct 

def ground_heat_storage(T_deep, T_air, floor_area, soil_depth):
    """Heat storage and conduction through the ground w/ Fourier's Law.

    Args:
        T_deep (float): temp. of floor
        T_air (float): temp. of air (interior)
        floor_area (float): area of floor where conduction happens.
        soil_depth (float): depth of soil.

    Returns:
        float: heat transfered per time unit
    """

    return soil_conduct * floor_area * (T_air - T_deep) / soil_depth

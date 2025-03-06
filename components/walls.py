import numpy as np

def conduction_calc(T_inside, T_outside, conductivity, thickness, area):
    """Heat conduction through greenhouse [walls] using Fourier’s Law.

    Args:
        T_inside (float): temp. on interior
        T_outside (float): temp. on outside
        conductivity (float): wall conductivity on wall affected
        thickness (float): wall thickness on wall affected
        area (float): wall area on wall affected

    Returns:
        float: heat transfer on
    """

    return (conductivity * area * (T_inside - T_outside)) / thickness


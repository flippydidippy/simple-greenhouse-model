import numpy as np
from components.const import SIGMA, C_TO_K

def radiation_loss_calc(T_inside, T_outside, wall_emissivity, wall_area):
    """_summary_

    Args:
        T_inside (float): temperature inside (°C)
        T_outside (float): temperature outside (°C)
        wall_emissivity (float): the emissivity of wall affected. 
        wall_area (float): the wall area affected 

    Returns:
        float: heat loss
    """

    T_inside_K = T_inside + C_TO_K
    T_outside_K = T_outside + C_TO_K

    loss = wall_emissivity * SIGMA * wall_area * (T_inside_K**4 - T_outside_K**4) # stefan-boltz

    #print(f"T_inside: {T_inside_K} K, T_outside: {T_outside_K} K")
    #print(f"Radiation loss: {loss:.2f} W")

    return loss
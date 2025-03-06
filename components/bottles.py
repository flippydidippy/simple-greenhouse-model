import numpy as np
from components.moisture import cp_water_calc
from components.const import CP_WATER
from components.radiation import radiation_loss_calc
from components.walls import conduction_calc

def bottle_heat_exchange(T_top, T_bottle, bottle_mass, bottle_area, h_bottle, dt):
    """
    Computes conductive, convective, and radiative heat exchange between air and hanging water bottles.

    Args:
        T_air (float): Greenhouse air temperature (°C).
        T_bottle (float): Temperature of water inside bottles (°C).
        bottle_mass (float): Total mass of water bottles (kg).
        bottle_area (float): Total surface area of bottles (m²).
        h_bottle (float): Convective heat transfer coefficient (W/m²K).

    Returns:
        tuple: (Total heat exchanged (W), New bottle temperature (°C)).
    """

    EMISSITIVITY = 1
    K_BOTTLE = 1
    THICKNESS = 0.001

    # Convert temperatures to Kelvin for radiation calculations
    if bottle_mass > 0 and bottle_area > 0:
        Q_convection = h_bottle * bottle_area * (T_top - T_bottle)
        Q_radiation = radiation_loss_calc(T_bottle, T_top, EMISSITIVITY, bottle_area)
        Q_conduction = conduction_calc(T_top, T_bottle, K_BOTTLE, THICKNESS, bottle_area)
        #print(Q_radiation, Q_convection, Q_conduction)

        Q_total = Q_convection + Q_conduction - Q_radiation  

        # Compute new bottle temperature
        M_bottle = bottle_mass * CP_WATER  # Effective thermal mass
        T_bottle_new = T_bottle + (Q_total / M_bottle)

        return Q_total, T_bottle_new
    else:
        return 0, T_bottle
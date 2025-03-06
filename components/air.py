import numpy as np
from components.const import C_TO_K, SVP_WATER, R_AIR, R_WATER
from components.moisture import P_sat_calc

def convection(T_air, T_ext, h_conv, exchange_area):
    """Convective heat exchange between indoor air and external air.

    Args:
        T_air (float): Temperature of interior
        T_ext (float): Temperature of exterior
        h_conv (float): heat transfer coef.
        exchange_area (float): Area of where the heat transfer takes place.

    Returns:
        float: heat transfered per time unit
    """
    return h_conv * exchange_area * (T_air - T_ext) 

def ventilation_loss(T_air, T_ext, cp_air, rho_air, ventilation_rate, volume):
    """Heat loss due to ventilation exchange (accounting for air mass flow).

    Args:
        T_air (float): Temp. of interior
        T_ext (float): Temp. of exterior
        rho_air (float): dens. of air
        ventilation_rate (float): Ventilation rate coef.
        volume (float): exchanged heat volume

    Returns:
        float: Heat transfered per time unit
    """
    return rho_air * volume * ventilation_rate * cp_air * (T_air - T_ext) 

import numpy as np

def rho_air_calc(P, T_air, RH):
    """
    Computes air density using Engineering Toolbox saturation pressure formula.

    Args:
        T_air (float): Air temperature in Celsius (°C).
        RH (float): Relative humidity in % (0-100).
        P (float): Total air pressure in Pascals (Pa) [Default: 101325 Pa (sea level)].

    Returns:
        float: Humid air density (kg/m³).
    """
    # Constants
    T_K = T_air + C_TO_K  # Convert temperature to Kelvin

    # Saturation vapor pressure from Engineering Toolbox formula (Pa)
    P_sat = P_sat_calc(T_air)*1000

    # Actual vapor pressure
    P_vapor = (RH / 100) * P_sat
    P_dry = P*1000 - P_vapor  # Partial pressure of dry air

    # Compute humid air density
    rho_humid = (P_dry / (R_AIR * T_K)) + (P_vapor / (R_WATER * T_K))
    
    return rho_humid



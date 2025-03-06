import numpy as np
from components.const import C_TO_K, PA_SEA_LVL, AIR_DEN, WP_RATIO, SVP_WATER

def compute_humidity_change(T_air, RH_air, T_ext, RH_ext, ventilation_rate, transpiration_rate, debug):
    """Calculates new relative humidity inside the greenhouse.

    Args:
        T_air (float): Temperature of interior (air)
        RH_air (float): Relative humidity in the interior air
        T_ext (float): Temperature of the exterior
        RH_ext (float): Relative humidity in the exterior air
        ventilation_rate (float): ventilation rate coef.
        transpiration_rate (float): transpiration rate coef.
    """
    H_air = absolute_humidity(T_air, RH_air)
    H_ext = absolute_humidity(T_ext, RH_ext)

    humidity_change_ventilation = ventilation_rate * (H_ext - H_air) # ventilation
    humidity_change_transpiration = transpiration_rate / AIR_DEN # transpiration 

    new_H = H_air + humidity_change_ventilation + humidity_change_transpiration

    #print(H_air, humidity_change_ventilation, humidity_change_transpiration)
    # if debug < 100:
    #     print(RH_air, H_air, RH_ext, H_ext, humidity_change_ventilation, humidity_change_transpiration)
    #     print("change:", new_H - H_air)
    
    return relative_humidity_from_absolute(T_air, new_H)

def absolute_humidity(T, RH):
        """Converts relative humidity % to absolute humidity in kg/m3.

        Args:
            T (float): temperature
            RH (float): relative humidity

        Returns:
            float: absolute humidty in kg/m3
        """
        svp = P_sat_calc(T)  # svp eq., Tetens eq.
        avp = RH / 100 * svp # actual vapor pressure
        return max(0, WP_RATIO * avp / (PA_SEA_LVL - avp))  # kg/m3


def P_sat_calc(T):
    """
    Computes saturation vapor pressure (P_sat) in kPa based on air temperature (T in °C).
    
    Parameters:
    T (float): Temperature in degrees Celsius (°C).
    
    Returns:
    float: Saturation vapor pressure (kPa).
    """
    return SVP_WATER * np.exp((17.27 * T) / (T + 237.3))

def relative_humidity_from_absolute(T, H):
    """Converts absolute humidity (kg/m3) back to relative humidity (%).

    Args:
        T (float): Temperature in Celsius
        H (float): Absolute humidity in kg/m3

    Returns:
        float: Relative humidity / RH %
    """
    svp = SVP_WATER * np.exp((17.27 * T) / (T + 237.3))  # saturation vapor pressure (Pa)
    avp = (H * PA_SEA_LVL) / (WP_RATIO + H)  # Compute actual vapor pressure
    RH = (avp / svp) * 100  # Convert to relative humidity
    return np.clip(RH, 0, 100)  # Ensure RH is between 0-100%

def cp_water_calc(T_water):
    """
    Computes the specific heat capacity of water as a function of temperature.

    Args:
        T_water (float): Temperature of water (°C).

    Returns:
        float: Specific heat capacity (J/kgK).
    """
    return 4181.3 - 3.2 * T_water + 0.0024 * T_water**2

def moisture_balance(M_v, V_air, R, T, M_transp, M_cond, M_vent):
    return (M_transp - M_cond - M_vent) * (R * T) / (M_v * V_air)

def condensation(xi, U, P_air, P_sat):
    return xi * U * (P_air - P_sat)

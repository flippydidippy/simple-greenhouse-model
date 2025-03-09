import numpy as np
from components.const import C_TO_K, PA_SEA_LVL, AIR_DEN, WP_RATIO, SVP_WATER

def compute_humidity_change(T_air, RH_air, T_ext, RH_ext, ventilation_rate, transpiration_rate, T_soil, radiation, evap_coef, T_wall, cond_coef, cond_area, T_bottle, bottle_area, debug=False):
    """
    Computes the change in relative humidity in the greenhouse.

    Args:
        T_air (float): Interior air temperature (°C)
        RH_air (float): Interior relative humidity (%)
        T_ext (float): Exterior temperature (°C)
        RH_ext (float): Exterior relative humidity (%)
        ventilation_rate (float): Ventilation coefficient
        transpiration_rate (float): Plant transpiration coefficient
        T_soil (float): Soil temperature (°C)
        radiation (float): Incoming solar radiation (W/m²)
        evap_coef (float): Soil evaporation coefficient
        T_wall (float): Greenhouse wall temperature (°C)
        cond_coef (float): Condensation coefficient (kg/m²·s·Pa)
        cond_area (float): Available condensation area (m²)
        debug (bool): Print debug information if True

    Returns:
        float: Updated relative humidity inside the greenhouse (%)
    """

    # Compute absolute humidity inside and outside
    H_air = absolute_humidity(T_air, RH_air)
    H_ext = absolute_humidity(T_ext, RH_ext)

    humidity_change_ventilation = ventilation_rate * (H_ext - H_air)
    humidity_change_transpiration = transpiration_rate * AIR_DEN
    humidity_change_evaporation = compute_evap_soil(T_soil, RH_air, radiation, evap_coef)
    humidity_change_condensation = compute_condensation(T_air, RH_air, T_wall, cond_coef, cond_area)
    humidity_change_bottle_evap = compute_open_bottle_evap(T_bottle, RH_air, bottle_area, evap_coef)

    # New absolute humidity
    new_H = (
        H_air
        + humidity_change_ventilation
        + humidity_change_transpiration
        + humidity_change_evaporation
        + humidity_change_bottle_evap
        - humidity_change_condensation
    )

    if debug:
        print(f"H_air: {H_air:.5f}, H_ext: {H_ext:.5f}")
        print(f"Ventilation Effect: {humidity_change_ventilation:.5f}")
        print(f"Transpiration Effect: {humidity_change_transpiration:.5f}")
        print(f"Soil Evaporation Effect: {humidity_change_evaporation:.5f}")
        print(f"Condensation Loss: {humidity_change_condensation:.5f}")
        print(f"New Absolute Humidity: {new_H:.5f}")

    #print(H_air, humidity_change_ventilation, humidity_change_transpiration)
    # if debug < 100:
    #     print(RH_air, H_air, RH_ext, H_ext, humidity_change_ventilation, humidity_change_transpiration)
    #     print("change:", new_H - H_air)

    # Convert absolute humidity back to relative humidity
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

def compute_evap_soil(T_soil, RH_air, radiation, evap_coef):
    """
    Computes water vapor added from soil evaporation.
    
    Args:
        T_soil (float): Soil surface temperature (°C)
        RH_air (float): Relative humidity of the air (%)
        radiation (float): Solar radiation at soil level (W/m²)
        evap_coef (float): Empirical evaporation coefficient
    
    Returns:
        float: Moisture contribution from soil evaporation (kg/m³)
    """
    e_s = P_sat_calc(T_soil)  # Saturation vapor pressure (kPa)
    e_air = e_s * (RH_air / 100)  # Air vapor pressure (kPa)
    
    evaporation_rate = evap_coef * radiation * (e_s - e_air) / PA_SEA_LVL / 1000 # Evaporation (kg/s·m²)
    
    return evaporation_rate  # kg/m³

def compute_open_bottle_evap(T_bottle, RH_air, area, evap_coef):
    """
    Computes water vapor added from soil evaporation.
    
    Args:
        T_soil (float): Soil surface temperature (°C)
        RH_air (float): Relative humidity of the air (%)
        area (float): area exposed
        evap_coef (float): Empirical evaporation coefficient
    
    Returns:
        float: Moisture contribution from soil evaporation (kg/m³)
    """
    e_s = P_sat_calc(T_bottle)  # Saturation vapor pressure (kPa)
    e_air = e_s * (RH_air / 100)  # Air vapor pressure (kPa)
    
    evaporation_rate = evap_coef * area * (e_s - e_air) / PA_SEA_LVL / 1000 # Evaporation (kg/s·m²)
    
    return evaporation_rate  # kg/m³

def compute_condensation(T_air, RH_air, T_wall, cond_coef, cond_area):
    """
    Computes moisture lost via condensation.

    Args:
        T_air (float): Interior air temperature (°C)
        RH_air (float): Relative humidity (%)
        T_wall (float): Greenhouse wall temperature (°C)
        cond_coef (float): Condensation coefficient (kg/m²·s·Pa)
        cond_area (float): Surface area available for condensation (m²)

    Returns:
        float: Moisture removed from air via condensation (kg/m³)
    """
    e_s_wall = P_sat_calc(T_wall)  # Saturation vapor pressure at wall (kPa)
    e_air = P_sat_calc(T_air) * (RH_air / 100)  # Actual vapor pressure (kPa)

    if e_air > e_s_wall:  # Condensation occurs if the air is oversaturated
        condensation_rate = cond_coef * cond_area * (e_air - e_s_wall)  # kg/s
        return condensation_rate  # Moisture removed in kg/m³

    return 0  # No condensation


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

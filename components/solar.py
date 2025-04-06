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

def solar_position(day_of_year, hour, latitude):
    """
    Calculate solar zenith and azimuth angles.
    """
    decl = 23.44 * np.sin(np.radians(360 / 365 * (day_of_year - 81)))  # Solar declination
    hour_angle = 15 * (hour - 12)  # Degrees

    latitude_rad = np.radians(latitude)
    decl_rad = np.radians(decl)
    hour_angle_rad = np.radians(hour_angle)

    cos_zenith = np.sin(latitude_rad) * np.sin(decl_rad) + np.cos(latitude_rad) * np.cos(decl_rad) * np.cos(hour_angle_rad)
    zenith = np.degrees(np.arccos(np.clip(cos_zenith, -1, 1)))

    return zenith

def projected_irradiance(GHI, zenith_deg, tilt_deg):
    """
    Project global horizontal irradiance (GHI) onto a tilted surface.
    Assumes azimuth alignment.
    """
    zenith_rad = np.radians(zenith_deg)
    tilt_rad = np.radians(tilt_deg)

    # Angle of incidence approximation (for vertical wall facing equator)
    cos_theta = np.cos(zenith_rad - tilt_rad)
    cos_theta = np.clip(cos_theta, 0, 1)

    return GHI * cos_theta

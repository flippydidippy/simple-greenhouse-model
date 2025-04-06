import pandas as pd
import numpy as np

from simulation.update import update_cycle
from greenhouse_setups.read_profiles import load_params
from greenhouse_setups.params import update_all_params
from components.crop_model import compute_crop_growth
from crops.retrieve_dict import get_crop_dict
from components.const import RHO_AIR

def run_simulation(weather_data, T_air_init, T_top_init, RH_init, crop, dt, profile=None, params_dict=None):
    """Runs the full-year greenhouse simulation with minute-level updates and humidity considerations."""
    if profile: load_params(profile)
    if params_dict: update_all_params(params_dict)

    T_air = T_air_init
    T_wall_ext = T_air_init
    T_wall_int = T_air_init
    T_top = T_top_init
    T_bottle = T_air_init + 5
    T_ground = T_air_init
    RH_air = RH_init
    GH_T_air = []
    GH_T_top = []
    GH_T_bottle = []
    GH_T_ground = []
    GH_T_wall_int = []
    GH_T_wall_ext = []
    GH_humidities = []
    crop_masses = []
    old_rho_air = RHO_AIR
    old_rho_air_top = RHO_AIR

    #T_base, T_opt, RUE, ideal_RH, RH_sensitivity, GDD_maturity, CO2_rsponse = get_crop_dict(crop)
    T_sum, HI, I50A, I50B, T_base, T_opt, RUE, I50maxH, I50maxW, T_heat, T_extreme, SCO2, S_water = get_crop_dict(crop)
    TT = 0
    crop_mass = 0
    radiation_MJ_24h = 0
    cycles = 0
    is_unstable = False
    total_crop_mass = 0

    for i in range(len(weather_data)): # run the simualtion for the whole data set
        T_ext = weather_data.loc[i, "temperature"]
        RH_outside = weather_data.loc[i, "humidity"]
        pressure = weather_data.loc[i, "pressure"]
        solar = weather_data.loc[i, "solar"]
        solar_angle = weather_data.loc[i, "solar_angle"]
        time = weather_data.loc[i, "time"]
        hour = pd.to_datetime(time).hour
        date = pd.to_datetime(time)

        radiation_MJ_24h += solar*0.0036


        if hour == 0 and i>0:
            last_day_rel_idx = max(0, i-24)
            T_air_24 = GH_T_air[last_day_rel_idx:i]
            
            # crops
            T_max, T_min, T_mean = max(T_air_24), min(T_air_24), np.mean(T_air_24)
            crop_mass, TT = compute_crop_growth(crop_mass, TT, radiation_MJ_24h, T_mean, T_base, T_opt, T_max, T_heat, T_extreme, I50A, RUE, 400, SCO2)
            if TT >= T_sum:
                #print("MATURED", crop_mass)
                total_crop_mass += crop_mass
                TT, crop_mass = 0, 0.01
                cycles += 1
            
            #print(T_mean)

            #reset after
            radiation_MJ_24h = 0

        # Call the updated temperature model
        T_air, T_top, T_wall_ext, T_wall_int, T_ground, T_bottle, RH_air, old_rho_air, old_rho_air_top, is_unstable, variables = update_cycle(
            T_ext, T_top, T_air,  # temp
            T_ground, T_wall_ext, T_wall_int, T_bottle,  # temp
            solar, solar_angle,  # solar
            RH_air, RH_outside,  # humidity
            pressure,

            400, 3,
            old_rho_air, old_rho_air_top,
            
            dt, date, is_unstable, i, # Ventilation & Humidity
        )

        # if i < 10:
        #     print(T_air,T_top, T_bottle)

        if i < 1:
            greenhouse_data = {key: [] for key in variables.keys()}

        # Append the current values to their respective lists
        for key, value in variables.items():
            greenhouse_data[key].append(value)

        if is_unstable:
            cycles = 0
            total_crop_mass = 0
            return None, cycles, total_crop_mass

        GH_T_air.append(T_air)
        GH_T_bottle.append(T_bottle)
        GH_T_ground.append(T_ground)
        GH_T_wall_ext.append(T_wall_ext)
        GH_T_wall_int.append(T_wall_int)
        GH_T_top.append(T_top)
        GH_humidities.append(RH_air)
        crop_masses.append(crop_mass)

    weather_data["GH_T_air"] = GH_T_air
    weather_data["GH_T_top"] = GH_T_top
    weather_data["GH_T_bottle"] = GH_T_bottle
    weather_data["GH_T_ground"] = GH_T_ground
    weather_data["GH_T_wall_ext"] = GH_T_wall_ext
    weather_data["GH_T_wall_int"] = GH_T_wall_int
    weather_data["GH_humidity"] = GH_humidities
    weather_data["crop_mass"] = crop_masses

    for key, value_list in greenhouse_data.items():
        weather_data[key] = value_list

    cycles += TT/T_sum
    total_crop_mass += crop_mass

    

    return weather_data, cycles, total_crop_mass

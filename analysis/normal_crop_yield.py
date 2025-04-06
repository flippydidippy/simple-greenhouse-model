import pandas as pd
import numpy as np

from simulation.update import update_cycle
from greenhouse_setups.read_profiles import load_params
from greenhouse_setups.params import update_all_params
from components.crop_model import compute_crop_growth
from crops.retrieve_dict import get_crop_dict
from components.const import RHO_AIR
from data.read_nrel import compile_nrel_data, compile_multiple_nrel_data

def normal_crop_yield(file_path, crop):
    
    if isinstance(file_path, list):
        weather_data = compile_multiple_nrel_data(file_path)
    else:
        weather_data = compile_nrel_data(file_path)
    
    #T_base, T_opt, RUE, ideal_RH, RH_sensitivity, GDD_maturity, CO2_rsponse = get_crop_dict(crop)
    T_sum, HI, I50A, I50B, T_base, T_opt, RUE, I50maxH, I50maxW, T_heat, T_extreme, SCO2, S_water = get_crop_dict(crop)

    temps = []
    cycles = 0
    radiation_MJ_24h = 0
    crop_mass = 0
    TT = 0
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
            T_air_24 = temps[last_day_rel_idx:i]
            
            # crops
            T_max, T_min, T_mean = max(T_air_24), min(T_air_24), np.mean(T_air_24)
            crop_mass, TT = compute_crop_growth(crop_mass, TT, radiation_MJ_24h, T_mean, T_base, T_opt, T_max, T_heat, T_extreme, I50A, RUE, 400, SCO2)
            if TT >= T_sum:
                #print("MATURED", crop_mass)

                total_crop_mass += crop_mass
                TT, crop_mass = 0, 0 
                cycles += 1
                #print("MATURED")
            
            #print(T_mean)

            #reset after
            radiation_MJ_24h = 0

        temps.append(T_ext)

    cycles += TT/T_sum
    total_crop_mass += crop_mass

    return cycles, total_crop_mass

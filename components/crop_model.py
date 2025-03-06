import numpy as np

def compute_crop_growth(biomass, old_TT, radiation, T_air, T_base, T_opt, T_max, T_heat_stress, T_extreme, I_50a, RUE, CO2_conc, S_CO2):
    """FROM SIMPLE CROP MODEL

    Args:
        biomass (_type_): _description_
        radiation (_type_): _description_
        T_air (_type_): _description_
        T_base (_type_): _description_
        T_opt (_type_): _description_
        T_max (_type_): _description_
        T_heat_stress (_type_): _description_
        T_extreme (_type_): _description_
        I_50a (_type_): _description_
        RUE (_type_): _description_
        CO2_conc (_type_): _description_
        S_CO2 (_type_): _description_

    Returns:
        _type_: _description_
    """

    new_TT = delta_tt(T_air, T_base)
    acc_TT = old_TT + new_TT
    new_biomass = biomass_rate(radiation, new_TT, T_air, T_base, T_opt, T_max, T_heat_stress, T_extreme, I_50a, RUE, CO2_conc, S_CO2) + biomass
    return new_biomass,  acc_TT

def biomass_rate(radiation, TT, T_air, T_base, T_opt, T_max, T_heat_stress, T_extreme, I_50a, RUE, CO2_conc, S_CO2):
    #assume water is fine
    return radiation * f_solar(TT, 0.95, I_50a) * RUE * f_co2(CO2_conc, S_CO2) * f_temp(T_air, T_base, T_opt) * min(f_heat(T_max, T_heat_stress, T_extreme), 1)

# def biomass_cumulative(biomass_cum, biomass_rate):
#     return biomass_cum + biomass_rate

# def yield_calculation(biomass_cum_maturity, hi):
#     return biomass_cum_maturity * hi

def delta_tt(t, t_base):
    return max(t - t_base, 0)

# solar func
def f_solar(I, f_solar_max, I_50a, tt_sum=0, tt_50b=0, growth_period=True):
    if growth_period:
        return f_solar_max / (1 + np.exp(-0.01 * (I - I_50a)))
    # else:
    #     return f_solar_max / (1 + np.exp(0.01 * (tt - (tt_sum - tt_50b))))

def f_temp(t, t_base, t_opt):
    if t < t_base:
        return 0
    elif t_base <= t < t_opt:
        return (t - t_base) / (t_opt - t_base)
    else:
        return 1

def f_heat(t_max, t_heat, t_extreme):
    if t_max <= t_heat:
        return 1
    elif t_heat < t_max <= t_extreme:
        return 1 - ((t_max - t_heat) / (t_extreme - t_heat))
    else:
        return 0

def f_co2(co2, s_co2):
    if 350 <= co2 < 700:
        return 1 + s_co2 * (co2 - 350)
    else:
        return 1 + s_co2 * 350

# def i50b_next(i50b_current, i_max_heat, f_heat):
#     return i50b_current + i_max_heat * (1 - f_heat)

# def arid_index(et0, paw):
#     return 1 - min(et0, 0.096 * paw) / et0

# def f_water(s_water, arid):
#     return 1 - s_water * arid

# def f_solar_water(f_water):
#     if f_water < 0.1:
#         return 0.9 + f_water
#     else:
#         return 1

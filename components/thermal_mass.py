from components.moisture import P_sat_calc


def thermal_mass_calc(rho_air, cp_air, cp_water, 
                 volume_air, wall_area, wall_thickness, wall_density, wall_cp,
                 floor_area, floor_depth, floor_density, floor_cp, 
                 water_mass, RH, T_air, P_atm):
    """Computes total thermal mass of a greenhouse"""
    M_air = volume_air * rho_air * cp_air # air

    #thermal mass through RH
    P_atm = P_atm
    P_sat = P_sat_calc(T_air)/100
    M_water_vapor = max((RH / 100) * (0.622 * (P_sat / (P_atm - P_sat))) * M_air/6, 0)
    M_RH = M_water_vapor * cp_water  # Water vapor thermal mass contribution

    M_walls = wall_area * wall_thickness * wall_density * wall_cp #walls thermal mass
    M_floor = floor_area * floor_depth * floor_density * floor_cp #floor thermal mass
    M_water = water_mass * cp_water # water thermal mass

    #print(M_RH, M_water, M_water, M_floor, M_air)
    
    # print(M_air, M_walls, M_floor, M_water)
    # 
    return M_air + M_walls + M_floor + M_water + M_RH
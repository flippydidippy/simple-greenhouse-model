import numpy as np
from components.air import convection, ventilation_loss, rho_air_calc
from components.walls import conduction_calc
from components.ground import ground_heat_storage
from components.solar import solar_rad_calc
from components.radiation import radiation_loss_calc
from components.moisture import compute_humidity_change, absolute_humidity, condensation, cp_water_calc
from components.latent import latent_calc
from components.const import RHO_AIR, CP_AIR, CP_WATER
from components.plants import humidity_effect
from components.hydroponic import hydroponic_pipe_cooling
from components.thermal_mass import thermal_mass_calc
from components.bottles import bottle_heat_exchange
from components.solar import solar_position, projected_irradiance

def update_cycle(T_ext, T_top, T_air, 
                    T_ground, T_wall_ext, T_wall_int, T_bottle, 
                    solar, solar_angle, 
                    RH_air, RH_ext, 
                    pressure,
                    CO2_conc, crop_mass,
                    old_rho_air, old_rho_air_top,
                
                    dt, date, is_unstable, debug=0):


    from greenhouse_setups.params import h_conv, vent_rate, \
                                  plant_transpiration_rate, volume, roof_area, top_vent_rate, \
                                  wall_cp, wall_rho, wall_conductivity, wall_thickness, wall_emissivity, wall_solar_absorp_coef, \
                                  roof_conductivity, roof_thickness, roof_emissivity, roof_solar_absorp_coef, roof_rho, roof_cp, \
                                  wall_area, roof_area, ground_area, roof_area, roof_volume, \
                                  soil_depth, soil_density, soil_cp, \
                                  nr_water_bottles, bottles_percent_open


    MAX_T_FLUC = 50
    MAX_RHO_AIR_FLUC = 0.8
    PRESET_WATER_BOTTLE_SIZE = 3 # liters//mass
    PRESET_WATER_BOTTLE_AREA = 0.15 # square meters
    # EXTRA_FACTOR_BOTTLE = 100
    # nr_water_bottles *= EXTRA_FACTOR_BOTTLE

    tot_water_mass = PRESET_WATER_BOTTLE_SIZE*nr_water_bottles
    tot_bottle_area = PRESET_WATER_BOTTLE_AREA*nr_water_bottles

    H_absolute = absolute_humidity(T_air, RH_air)
    cp_air = np.clip(CP_AIR + (H_absolute * 1860), CP_AIR*0.8, CP_AIR*1.2)
    cp_water = np.clip(cp_water_calc(T_bottle), CP_WATER*0.95, CP_WATER*1.05)
    rho_air = np.clip(rho_air_calc(pressure, T_air, RH_air),  RHO_AIR*0.2, RHO_AIR*1.8)

    rho_air_top = np.clip(rho_air_calc(pressure, T_top, RH_air), RHO_AIR*0.2, RHO_AIR*1.8)

    # if abs(rho_air - old_rho_air) > MAX_RHO_AIR_FLUC:
    #     rho_air = abs(rho_air - old_rho_air)/2

    # if abs(rho_air_top - old_rho_air_top) > MAX_RHO_AIR_FLUC:
    #     rho_air_top = abs(rho_air_top - old_rho_air_top)/2

    thermal_mass_soil = thermal_mass_calc(0, 0, 0, 0, 0, 0, 0, 0, ground_area, soil_depth, soil_density, soil_cp, 0, 0, 0, 0)
    thermal_mass_mid = thermal_mass_calc(rho_air, cp_air, cp_water, volume, wall_area, wall_thickness, wall_rho, wall_cp, 0, 0, 0, 0, tot_water_mass, RH_air, T_air, pressure)
    thermal_mass_wall = thermal_mass_calc(0, 0, 0, 0, wall_area, wall_thickness, wall_rho, wall_cp, 0, 0, 0, 0, 0, 0, 0, 0)
    thermal_mass_top = thermal_mass_calc(rho_air_top, cp_air, cp_water, volume, wall_area, wall_thickness, wall_rho, wall_cp, 0,  0, 0, 0, tot_water_mass, RH_air, T_top, pressure)





    Q_bottle, T_bottle_new = bottle_heat_exchange(T_top, T_bottle, tot_water_mass, tot_bottle_area, bottles_percent_open, 15, dt)

    # ### Solar
    # latitude = 52.0  # Adjust to your location
    # day_of_year = date.timetuple().tm_yday
    # hour = date.hour + date.minute / 60

    # zenith = solar_position(day_of_year, hour, latitude)

    # # Assume wall tilt = 90°, roof tilt = 30°
    # irr_wall = projected_irradiance(solar, zenith, 90)
    # irr_roof = projected_irradiance(solar, zenith, 30)

    # Q_wall_solar = irr_wall * wall_solar_absorp_coef * wall_area
    # Q_top_solar = irr_roof * roof_solar_absorp_coef * roof_area


    #### WALLS
    # External heat transfer (outside wall surface)
    Q_wall_solar = max(solar_rad_calc(solar*(1000000/dt), wall_solar_absorp_coef, wall_area),0) #* np.sin(np.radians(solar_angle))  # Solar absorption
    Q_wall_rad_ext = radiation_loss_calc(T_wall_ext, T_ext, wall_emissivity, wall_area)  # Radiation loss to sky
    Q_wall_ext_conv = convection(T_wall_ext, T_ext, wall_conductivity, wall_area)  # Convection with external air
    Q_wall_ext_cond = conduction_calc(T_wall_ext, T_wall_int, wall_conductivity, wall_thickness, wall_area)  # Conduction from exterior to interior

    # Internal heat transfer (between interior wall surface and greenhouse air)
    Q_wall_int_conv = convection(T_wall_int, T_air, wall_conductivity, wall_area)  # Convection with interior air
    Q_wall_int_cond = conduction_calc(T_wall_int, T_air, wall_conductivity, wall_thickness, wall_area)  # Conduction from interior surface to air


    if wall_thickness < 0.005:
        Q_net_ext = Q_wall_solar + Q_wall_ext_conv - Q_wall_rad_ext - Q_wall_int_conv - Q_wall_int_cond
        Q_net_int = Q_net_ext
        T_wall_ext_new = T_wall_ext + (Q_net_ext) / thermal_mass_wall
        T_wall_int_new = T_wall_ext_new
    
    else:
        # Net heat flux for external and internal wall surfaces
        Q_net_ext = Q_wall_solar + Q_wall_ext_conv - (Q_wall_rad_ext + Q_wall_ext_cond)
        Q_net_int = Q_wall_ext_cond - (Q_wall_int_conv + Q_wall_int_cond)

        # Update temperatures using wall thermal mass
        T_wall_ext_new = T_wall_ext + (Q_net_ext * dt) / thermal_mass_wall
        T_wall_int_new = T_wall_int + (Q_net_int * dt) / thermal_mass_wall

    

    #### TOP TEMP. BODY
    Q_top_solar = max(solar_rad_calc(solar*(1000000/dt), roof_solar_absorp_coef, roof_area) * np.cos(np.radians(solar_angle)), 0)  # Fixed projection
    Q_top_cond = conduction_calc(T_top, T_ext, roof_conductivity, roof_thickness, roof_area)  # Roof conduction
    Q_top_conv = convection(T_top, T_ext, roof_conductivity, roof_area)  # Roof convection with outside air
    Q_top_rad = radiation_loss_calc(T_top, T_ext, roof_emissivity, roof_area)  # Radiation loss to sky
    Q_top_vent = ventilation_loss(T_top, T_ext, cp_air, rho_air_top, top_vent_rate*(1000000/dt), roof_volume)

    Q_roof_int_conv = convection(T_top, T_air, roof_conductivity, roof_area)  # Internal convection
    Q_roof_int_rad = radiation_loss_calc(T_top, T_air, roof_emissivity, roof_area)  # Internal radiation

    #### GROUND HEAT STORAGE (MULTILAYER CONDUCTION)
    Q_ground_cond = conduction_calc(T_ground, T_air, soil_cp, soil_depth, ground_area)
    Q_ground_air_conv = convection(T_air, T_ground, 1, ground_area)

    Q_ground_net = Q_ground_air_conv - Q_ground_cond
    T_ground_new = T_ground + (dt * Q_ground_net) / (RHO_AIR * CP_AIR * thermal_mass_soil)
    Q_ground = ground_heat_storage(T_ground, T_ext, ground_area, soil_depth)


    #### MAIN TEMP. BODY
    Q_air_cond = conduction_calc(T_air, T_ext, wall_conductivity, wall_thickness, wall_area)
    Q_air_conv = convection(T_air, T_ext, wall_conductivity, wall_area)
    Q_air_rad = radiation_loss_calc(T_air, T_ext, wall_emissivity, wall_area)
    Q_air_vent = ventilation_loss(T_air, T_ext, cp_air, rho_air, vent_rate*(1000000/dt), volume)

    # Internal exchange with walls and roof
    Q_air_internal = convection(T_air, T_top, h_conv, roof_area + wall_area)
    Q_wall_air_conv = convection(T_wall_int, T_air, wall_conductivity, wall_area)
    Q_wall_air_rad = radiation_loss_calc(T_wall_int, T_air, wall_emissivity, wall_area)

    



    #### CROPS
    OPEN_BOTTLE_EXPOSED_RATIO = 0.0001
    RH_air_new = np.clip(compute_humidity_change(T_air, RH_air, T_ext, RH_ext, vent_rate*dt, plant_transpiration_rate, T_ground, solar, 0.2, T_wall_int, 0.01, wall_area+roof_area, T_bottle, tot_bottle_area*bottles_percent_open*OPEN_BOTTLE_EXPOSED_RATIO), 0.5, 100)
    Q_latent = latent_calc(plant_transpiration_rate, RH_air, T_air)
    #cond = condensation(0.5, 0.1, 2000, 1700)

    # top and main
    Q_top_net = Q_top_solar - (Q_top_cond + Q_top_conv + Q_top_rad + Q_top_vent + Q_roof_int_conv + Q_roof_int_rad) + Q_bottle
    T_top_new = T_top + np.clip(dt * Q_top_net / (thermal_mass_top), -MAX_T_FLUC, MAX_T_FLUC)

    Q_air_net = Q_top_solar/4 + Q_air_internal + Q_wall_int_conv + Q_wall_int_cond - (Q_air_cond + Q_air_conv + Q_air_rad + Q_air_vent + Q_ground + Q_latent) + Q_bottle/4
    T_air_new = T_air + np.clip(dt * Q_air_net / (thermal_mass_mid), -MAX_T_FLUC, MAX_T_FLUC)

    if (abs(T_top-T_top_new) == MAX_T_FLUC or abs(T_air-T_air_new) == MAX_T_FLUC) and not is_unstable:
        # is_unstable = True
        # print(f"{date}: UNSTABLE SOLUTION")
        pass



    # if hour % 24 < 6 or hour % 24 > 19:
    #     Q_pipe = hydroponic_pipe_cooling(T_air, 14, 30, 30, 20, 0.01)
    # else:
    #     Q_pipe = 0

    if debug < 100:
        #print(nr_water_bottles, Q_bottle, T_bottle_new) 
        #print(thermal_mass_mid, thermal_mass_top, cp_water, rho_air, rho_air_top)


        # print(T_ext, T_top, T_air, 
        #             T_ground, T_wall_ext, T_wall_int, T_bottle, 
        #             solar, solar_angle, 
        #             RH_air, RH_ext, 
        #             pressure,
        #             CO2_conc, crop_mass,
                
        #             dt, hour)
        #print(f"Q_wall_solar: {Q_wall_solar:.2f}, Q_wall_ext_conv: {Q_wall_ext_conv:.2f}, Q_wall_rad_ext: {Q_wall_rad_ext:.2f}, "
    #   f"Q_wall_int_cond: {Q_wall_int_cond:.2f}, Q_wall_int_conv: {Q_wall_int_conv:.2f}, Q_net_ext: {Q_net_ext:.2f}, "
    #   f"Q_net_int: {Q_net_int:.2f}, T_wall_ext_new: {T_wall_ext_new:.2f}, T_wall_int_new: {T_wall_int_new:.2f}, "
    #   f"Q_top_solar: {Q_top_solar:.2f}, Q_top_cond: {Q_top_cond:.2f}, Q_top_conv: {Q_top_conv:.2f}, "
    #   f"Q_top_rad: {Q_top_rad:.2f},  Q_top_vent: {Q_top_vent:.2f}, Q_top_net: {Q_top_net:.2f}, Q_air_cond: {Q_air_cond:.2f}, "
    #   f"Q_air_conv: {Q_air_conv:.2f}, Q_air_rad: {Q_air_rad:.2f}, Q_air_vent: {Q_air_vent:.2f}")

        # print(h_conv, vent_rate, \
        #                           thermal_mass, plant_transpiration_rate, volume, roof_area, top_vent_rate, \
        #                           wall_cp, wall_rho, wall_conductivity, wall_thickness, wall_emissivity, wall_solar_absorp_coef, \
        #                           roof_conductivity, roof_thickness, roof_emissivity, roof_solar_absorp_coef, \
        #                           wall_area, roof_area, ground_area, \
        #                           soil_depth, soil_density, soil_cp, \
        #                           water_bottle_mass)
        # print(Q_wall_solar, Q_wall_ext_conv, Q_wall_rad, Q_wall_cond)
        # print(T_air_new, T_top_new, T_wall_ext_new, T_wall_int_new)
        #print(thermal_mass_mid)
        #print(Q_solar_top, Q_cond_top, Q_rad_top, Q_vent_top, Q_internal)
        #print(RH_air_new)
        #print(solar_gain, conduction_loss, radiation_loss_val, convection_loss, ventilation, latent_heat_loss, floor_loss)
        pass

    variables = {
        #"thermal_mass_mid": thermal_mass_mid,
        #"thermal_mass_top": thermal_mass_top,
        #"thermal_mass_wall": thermal_mass_wall,
        #"T_bottle_new": T_bottle_new,
        "T_ext": T_ext,
        "Q_wall_solar": Q_wall_solar,
        "Q_wall_ext_conv": Q_wall_ext_conv,
        "Q_wall_rad_ext": Q_wall_rad_ext,
        "Q_wall_ext_cond": Q_wall_ext_cond,
        "Q_wall_int_conv": Q_wall_int_conv,
        "Q_net_ext": Q_net_ext,
        "Q_net_int": Q_net_int,
        "T_wall_ext_new": T_wall_ext_new,
        "T_wall_int_new": T_wall_int_new,
        "Q_top_solar": Q_top_solar,
        "Q_top_cond": Q_top_cond,
        "Q_top_conv": Q_top_conv,
        "Q_top_rad": Q_top_rad,
        "Q_top_vent": Q_top_vent,
        "Q_roof_int_conv": Q_roof_int_conv,
        "Q_roof_int_rad": Q_roof_int_rad,
        "roof_rho": roof_rho,
        "roof_cp": roof_cp,
        #"Q_ground_cond": Q_ground_cond,
        #"Q_ground_air_conv": Q_ground_air_conv,
        #"Q_ground_net": Q_ground_net,
        #"T_ground_new": T_ground_new,
        "Q_air_cond": Q_air_cond,
        "Q_air_conv": Q_air_conv,
        "Q_air_rad": Q_air_rad,
        "Q_air_vent": Q_air_vent,
        "Q_air_internal": Q_air_internal,
        "Q_wall_air_conv": Q_wall_air_conv,
        "Q_wall_air_rad": Q_wall_air_rad,
        "crop_mass": crop_mass,
        "RH_air_new": RH_air_new,
        "Q_top_net": Q_top_net,
        "T_top_new": T_top_new,
        "Q_air_net": Q_air_net,
        "T_air_new": T_air_new,
        "thermal_mass_top": thermal_mass_top
    }



    return T_air_new, T_top_new, T_wall_ext_new, T_wall_int_new, T_ground_new, T_bottle_new, RH_air_new, old_rho_air, old_rho_air_top, is_unstable, variables


    # H_absolute = absolute_humidity(T_air, RH_air)
    # cp_humid = CP_AIR + (1860 * H_absolute)

    # solar_gain = np.clip(solar_heat_gain(solar, solar_absorp, roof_area), 0, max_heat_flux)

    # conduction_loss = np.clip(heat_conduction(T_air, T_ext, wall_conductivity, wall_thickness, wall_area), -max_heat_flux, max_heat_flux)
    # radiation_loss_val = np.clip(radiation_loss(T_air, T_ext, wall_emissivity, wall_area), -max_heat_flux, max_heat_flux)
    # convection_loss = np.clip(air_heat_transfer(T_air, T_ext, h_conv, wall_area + roof_area), -max_heat_flux, max_heat_flux)
    # ventilation = np.clip(ventilation_loss(T_air, T_ext, cp_humid, vent_rate, volume), -max_heat_flux, max_heat_flux)

    # latent_heat_loss = np.clip(compute_latent_heat_loss(plant_transpiration_rate), -max_heat_flux, max_heat_flux)
    # RH_air_new = compute_humidity_change(T_air, RH_air, T_ext, RH_ext, vent_rate, plant_transpiration_rate, debug)

    # floor_loss = np.clip(ground_heat_storage(T_floor, T_ext, floor_area, soil_depth), -max_heat_flux, max_heat_flux)
    # Q_net = solar_gain - (conduction_loss + radiation_loss_val + convection_loss + ventilation + latent_heat_loss + floor_loss)
    # T_new = T_air + np.clip(Q_net / (RHO_AIR * CP_AIR * thermal_mass), -max_temp_flux, max_temp_flux)
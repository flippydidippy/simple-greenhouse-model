import json
import numpy as np

def calc_dimensions(l, w, h, roof_h):
    global wall_area, roof_area, roof_volume, ground_area, volume

    wall_area = (h*l + h*w) * 2
    ground_area = l * w
    volume = l*w*gh_height
    if roof_h:
        roof_area = arch_greenhouse_area(roof_h, gh_length, gh_width)
        roof_volume = arch_greenhouse_volume(roof_h, gh_length, gh_length)
        #print(roof_area, roof_volume, wall_area, volume)
    else:
        roof_area = l * w
        roof_volume = volume/10

def arch_greenhouse_volume(height, length, width):
    span = min(length, width)
    extrusion_length = max(length, width) 

    R = (span ** 2) / (8 * height) + (height / 2)

    theta = 2 * np.asin(span / (2 * R))
    segment_area = 0.5 * R**2 * (theta - np.sin(theta))

    volume = segment_area * extrusion_length
    return volume

def arch_greenhouse_area(height, length, width):
    span = min(length, width)
    extrusion_length = max(length, width) # longer side

    R = (span ** 2) / (8 * height) + (height / 2)
    theta = 2 * np.asin(span / (2 * R))

    roof_area = theta * R * extrusion_length # arch

    segment_area = 0.5 * R**2 * (theta - np.sin(theta)) # sidewall of roof
    sidewall_area = 2 * segment_area

    total_area = roof_area + sidewall_area

    return total_area

def update_defaults(new_params):
    global gh_length, gh_height, gh_width, roof_area, gh_roof_height

    gh_length = new_params.get("gh_length", gh_length)
    gh_width = new_params.get("gh_width", gh_width)
    gh_height = new_params.get("gh_height", gh_height)
    gh_roof_height = new_params.get("gh_roof_height", gh_roof_height)

    calc_dimensions(gh_length, gh_width, gh_height, gh_roof_height)

def update_params(new_params):
    global h_conv, vent_rate, top_vent_rate, plant_transpiration_rate, soil_depth, soil_conduct, thermal_mass, thermal_mass_top, soil_density, soil_cp, nr_water_bottles, bottles_percent_open

    h_conv = new_params.get("h_conv", h_conv)
    vent_rate = new_params.get("vent_rate", vent_rate)
    top_vent_rate = new_params.get("top_vent_rate", top_vent_rate)
    plant_transpiration_rate = new_params.get("plant_transpiration_rate", plant_transpiration_rate)

    nr_water_bottles = new_params.get("nr_water_bottles", nr_water_bottles)
    bottles_percent_open = new_params.get("bottles_percent_open", bottles_percent_open)
    thermal_mass = new_params.get("thermal_mass", thermal_mass)
    thermal_mass_top = new_params.get("thermal_mass_top", thermal_mass_top)

    soil_depth = new_params.get("soil_depth", soil_depth)
    soil_conduct = new_params.get("soil_conduct", soil_conduct)
    soil_cp = new_params.get("soil_cp", soil_cp)
    soil_density = new_params.get("soil_density", soil_density)

def update_walls(new_params):
    global wall_solar_absorp_coef, R_wall, wall_conductivity, wall_thickness, wall_emissivity, wall_cp, wall_rho

    wall_solar_absorp_coef = new_params.get("wall_solar_absorp_coef", wall_solar_absorp_coef)
    wall_conductivity = new_params.get("wall_conductivity", wall_conductivity)
    wall_thickness = new_params.get("wall_thickness", wall_thickness)
    wall_emissivity = new_params.get("wall_emissivity", wall_emissivity)
    wall_cp = new_params.get("wall_cp", wall_cp)
    wall_rho = new_params.get("wall_rho", wall_rho)

    R_wall = wall_thickness/wall_conductivity

def update_roof(new_params):
    global roof_solar_absorp_coef, R_roof, roof_conductivity, roof_thickness, roof_emissivity, roof_cp, roof_rho

    roof_solar_absorp_coef = new_params.get("roof_solar_absorp_coef", roof_solar_absorp_coef)
    roof_conductivity = new_params.get("roof_conductivity", roof_conductivity)
    roof_thickness = new_params.get("roof_thickness", roof_thickness)
    roof_emissivity = new_params.get("roof_emissivity", roof_emissivity)
    roof_cp = new_params.get("roof_cp", roof_cp)
    roof_rho = new_params.get("roof_rho", roof_rho)

    R_roof = roof_thickness/roof_conductivity

def update_all_params(params):
    update_walls(params)
    update_roof(params)
    update_defaults(params)
    update_params(params)

### GREENHOUSE DEFAULT PARAMS
gh_length = 0
gh_width = 0
gh_height = 0
gh_roof_height = 0


wall_area, roof_area, ground_area, volume, roof_volume = 0, 0, 0, 0, 0 # dimensions

h_conv = 0 #W/m2*K (Convective heat transfer coefficient)
vent_rate = 0 # Air exchange rate (higher = more cooling)
top_vent_rate = 0 # Top air exchange rate (higher = more cooling)
plant_transpiration_rate = 0  # Effect of plants on humidity


nr_water_bottles = 0
bottles_percent_open = 0
thermal_mass = 0  # Represents greenhouse's ability to store heat
thermal_mass_top = 0  # Represents greenhouse's ability to store heat


soil_depth = 0
soil_conduct = 0 # soil thermal conductivity
soil_cp = 0
soil_density = 0

wall_solar_absorp_coef = 0 # Fraction of solar radiation absorbed of the wall
wall_conductivity = 0
wall_thickness = 0
wall_emissivity = 0
wall_cp = 0
wall_rho = 0
R_wall = 1

roof_solar_absorp_coef = 0
roof_conductivity = 0
roof_thickness = 0
roof_emissivity = 0
roof_cp = 0
roof_rho = 0
R_roof = 1

default_params_path = "greenhouse_setups/suticollo_opt1.json"
with open(default_params_path, "r") as file:
    params_dict = json.load(file)
    update_all_params(params_dict)
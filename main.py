import pandas as pd
from simulation.run import run_simulation
from visuals.plot_temp import plot_temperature
from visuals.monthly import plot_monthly_means
from visuals.plot_monthly_means import plot_monthly_hourly_means
from validate.run_validation_data import validate_simulation
from visuals.plot_selected_params import plot_parameters
from gui.visualize_greenhouse import run_visualizer
from validate.optimize import optimize_params
from greenhouse_setups.params import update_all_params
from analysis.optimize import simulate_greenhouse_raqaypampa, optimize_greenhouse_design
from data.read_nrel import compile_nrel_data
from gui.interface_wip import *
from analysis.RMSE import rmse_for_validation
from analysis.normal_crop_yield import normal_crop_yield


# file_path = "data/suticollo/2023.csv" # load in data
# weather_data = compile_nrel_data(file_path)
# T_init = weather_data["temperature"][0] #init temp
# RH_init = weather_data["humidity"][0] #init temp
# simulated_data, _, _ = run_simulation(weather_data, T_init, T_init, RH_init, "Lettuce", 3600, "raqay_default.json") # full year simulation



# selected_day = "2023-01-01" # select specific day
# single_day = simulated_data[simulated_data["time"].dt.strftime('%Y-%m-%d') == selected_day]

# plot_temperature(single_day, selected_day)
# plot_monthly_hourly_means(simulated_data, "Feb")
# run_viewer(simulated_data)


# app = QApplication(sys.argv)
# main_window = MainWindow()
# main_window.show()
# sys.exit(app.exec())


# # for date in ["2025-02-11", "2025-02-12", "2025-02-13","2025-02-14", "2025-02-15", "2025-02-16", "2025-02-17", "2025-02-18", "2025-02-19"]:
# #    plot_parameters(data, ["GH_T_air", "GH_T_top", "GH_T_ground", "GH_T_wall_ext", "GH_T_wall_int", "air_temp", "outside_temp", "top_temp"], date)
# # plot_parameters(data, ["humidity", "GH_humidity"], "2025-02-15")


opt_params, data = optimize_params()
data = validate_simulation("data/validate_data/")

print(rmse_for_validation(data))

for date in ["2025-02-11", "2025-02-12", "2025-02-13","2025-02-14", "2025-02-15", "2025-02-16", "2025-02-17", "2025-02-18", "2025-02-19"]:
   plot_parameters(data, ["GH_T_air", "GH_T_top", "GH_T_ground", "GH_T_wall_ext", "GH_T_wall_int", "air_temp", "outside_temp", "top_temp"], date)
   daily_data = data[data["time"].dt.date == pd.to_datetime(date).date()]
   print(rmse_for_validation(daily_data))


plot_parameters(data, ["humidity", "GH_humidity"], "2025-02-12")


param_file = "greenhouse_setups/suticollo_opt1.json"
run_visualizer(param_file, data)


#simulate suticollo house in raqaypampa
# simulated_data, _ = simulate_greenhouse_raqaypampa(2023, "Lettuce", "raqay_default.json")

# simulated_data.to_csv("data/raqaypampa/simulated_greenhouse_2023.csv", index=False)
# print(simulated_data.head())

# selected_day = "2023-05-16"
# single_day = simulated_data[simulated_data["time"].dt.strftime('%Y-%m-%d') == selected_day]
# plot_temperature(single_day, selected_day)
# plot_monthly_hourly_means(simulated_data, "Jan")

# param_file = "greenhouse_setups/suticollo_opt1.json"
# run_visualizer(param_file, simulated_data)

# crop = "Lettuce"
# crop_yield, total_crop = normal_crop_yield("data/raqaypampa/2023.csv", crop)
# print(crop_yield, total_crop)

# b_param = optimize_greenhouse_design("2023", crop, "cycle")
# _, cycles, crop_yield = simulate_greenhouse_raqaypampa("2023", crop, None, b_param)
# print(b_param)


save_values = {}
years = [2023,2022,2021,2020,2019]

for optimizing in ["cycle", "crop_mass"]:
   save_values[optimizing] = {}
   for crop in ["Lettuce", "Tomato", "Potato", "Maize", "Cassava", "Carrot", "Greenbean", "Chard", "Parsley", "Wheat", "Barley", "Beans", "Peas", "Squash", "Quinoa"]:
      save_values[optimizing][crop] = {}

      normal_cycles, total_crop_normal = normal_crop_yield([f"data/raqaypampa/{year}.csv" for year in years], crop)
      print(normal_cycles, total_crop_normal)
      b_param = optimize_greenhouse_design(years, crop, optimizing)
      _, cycles, crop_yield = simulate_greenhouse_raqaypampa(years, crop, None, b_param)

      save_values[optimizing][crop]["normal_cycles"] = normal_cycles
      save_values[optimizing][crop]["total_crop_normal"] = total_crop_normal
      save_values[optimizing][crop]["cycles"] = cycles
      save_values[optimizing][crop]["crop_yield"] = crop_yield
      save_values[optimizing][crop]["b_param"] = b_param

      print(save_values)
      with open('opt_tis11_2023_2019.json', 'w') as f:
         json.dump(save_values, f, indent=4)

print(save_values)

# for crop in ["Lettuce", "Tomato", "Potato", "Maize", "Cassava", "Carrot", "Greenbean", "Chard", "Parsley", "Wheat", "Barley", "Beans", "Peas", "Squash", "Quinoa"]:
#    normal_cycles, total_crop_normal = normal_crop_yield("data/raqaypampa/2023.csv", crop)
#    print(normal_cycles, total_crop_normal)




# with open("opt.json", "r") as file:
#     data = json.load(file)

# # Select crop
# selected_crop = "Maize" 
# profile = "raqay_default2.json"

# # Extract b_param
# b_param = next((category[selected_crop]["b_param"] for category in data.values() if selected_crop in category), None)
# simulated_data, cycles, crop_yield = simulate_greenhouse_raqaypampa("2023", selected_crop, profile, b_param)

# print(crop_yield, cycles)
# normal_cycles, total_crop_normal = normal_crop_yield("data/raqaypampa/2023.csv", selected_crop)
# print(normal_cycles, total_crop_normal)

# selected_day = "2023-05-16"
# single_day = simulated_data[simulated_data["time"].dt.strftime('%Y-%m-%d') == selected_day]
# plot_temperature(single_day, selected_day)
# plot_monthly_hourly_means(simulated_data, "Jun")


# Tomato:
# 1.2002532679738562 21.201642101202715
# Trying Parameters: {'nr_water_bottles': np.float64(5.93013335930079), 'bottles_percent_open': np.float64(0.8213871390344029), 'wall_conductivity': np.float64(0.9), 'wall_thickness': np.float64(0.15), 'gh_length': np.float64(7.552509650583443), 'gh_width': np.float64(3.6517424754578647), 'gh_height': np.float64(1.50000001)}, CYCLES: 2.0000, CROP MASS 203.8133

# Lettuce:
# 3.2776875 420.7564518765578
#Trying Parameters: {'nr_water_bottles': np.float64(24.19723978120133), 'bottles_percent_open': np.float64(0.1266852498001711), 'wall_conductivity': np.float64(0.9), 'wall_thickness': np.float64(0.19867650402684234), 'gh_length': np.float64(9.658709311488328), 'gh_width': np.float64(8.267565895753739), 'gh_height': np.float64(1.50000001)}, CYCLES: 8.4225, CROP MASS 381.8326

# Potato: 

#{'thermal_mass': np.float64(2000.0), 'wall_conductivity': np.float64(0.8360625156908734), 'wall_thickness': np.float64(0.28552570106486724), 'greenhouse_size': np.float64(36.496849758675054), 'ventilation_rate': np.float64(0.32914956859105704)}

# for Maize: {'nr_water_bottles': np.float64(25.228450766965278), 'wall_conductivity': np.float64(0.8546427287976959), 'wall_thickness': np.float64(0.3087412382283724), 'gh_length': np.float64(28.83701710201484), 'gh_width': np.float64(3.1540194604367713), 'gh_height': np.float64(2.5802024289983967)}

# Maize: {'nr_water_bottles': np.float64(20.017608932289964), 'wall_conductivity': np.float64(0.8590652776157565), 'wall_thickness': np.float64(0.3316541389993037), 'gh_length': np.float64(3.6315276677608743), 'gh_width': np.float64(44.116133793749334), 'gh_height': np.float64(1.5083533057771197)}

# Lettuce: 'nr_water_bottles': np.float64(16.18669695884607), 'wall_conductivity': np.float64(0.8157412907508119), 'wall_thickness': np.float64(0.42570877008569186), 'gh_length': np.float64(31.62150948273126), 'gh_width': np.float64(47.569532614048036), 'gh_height': np.float64(1.54466617709275)}

# Parsley: {'nr_water_bottles': np.float64(11.993136738203457), 'wall_conductivity': np.float64(0.8736755539906707), 'wall_thickness': np.float64(0.3053573602665481), 'gh_length': np.float64(6.473871867437861), 'gh_width': np.float64(6.055872949474129), 'gh_height': np.float64(2.8589017880465133)}

#{'wall_solar_absorp_coef': np.float64(34.97706649197201), 'roof_solar_absorp_coef': np.float64(21.827419710562054), 'vent_rate': np.float64(4.217714937637555), 'top_vent_rate': np.float64(9.056099433570402)}

# Potato: normally 1.53, 2.7815 {'nr_water_bottles': np.float64(36.46809311609771), 'wall_conductivity': np.float64(0.9), 'wall_thickness': np.float64(0.15), 'gh_length': np.float64(7.260290637995842), 'gh_width': np.float64(8.173521912644855), 'gh_height': np.float64(1.5)}
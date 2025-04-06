import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Load the JSON file
def load_data(filepath):
    with open(filepath, "r") as file:
        return json.load(file)

def plot_crop_yield(data1, data2, config_path):
    with open(config_path, "r") as file:
        config = json.load(file)

    crops = list(data1["crop_mass"].keys())
    HI_values = {crop: config.get(crop, {}).get("HI", 1) for crop in crops}

    normal_yield_1 = [(data1["crop_mass"][crop]["total_crop_normal"] * HI_values[crop]) for crop in crops]
    optimized_yield_1 = [(data1["crop_mass"][crop]["crop_yield"] * HI_values[crop]) for crop in crops]

    normal_yield_2 = [(data2["crop_mass"][crop]["total_crop_normal"] * HI_values[crop]) for crop in crops]
    optimized_yield_2 = [(data2["crop_mass"][crop]["crop_yield"] * HI_values[crop]) for crop in crops]

    x = np.arange(len(crops))

    plt.figure(figsize=(12, 6))
    plt.bar(x - 0.3, normal_yield_1, width=0.15, label="Normal Yield (File 1)")
    plt.bar(x - 0.15, optimized_yield_1, width=0.15, label="Optimized Yield (File 1)")
    plt.bar(x + 0.0, normal_yield_2, width=0.15, label="Normal Yield (File 2)")
    plt.bar(x + 0.15, optimized_yield_2, width=0.15, label="Optimized Yield (File 2)")

    plt.xticks(x, crops, rotation=45, ha="right")
    plt.ylabel("Crop Yield (t ha⁻¹ per year)")
    plt.title("Crop Yield Comparison (File 1 vs File 2)")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_growth_cycles(data1, data2):
    crops = list(data1["crop_mass"].keys())

    normal1 = [data1["cycle"][crop]["normal_cycles"] for crop in crops]
    opt1 = [data1["cycle"][crop]["cycles"] for crop in crops]

    normal2 = [data2["cycle"][crop]["normal_cycles"] for crop in crops]
    opt2 = [data2["cycle"][crop]["cycles"] for crop in crops]

    x = np.arange(len(crops))
    
    plt.figure(figsize=(12, 6))
    plt.bar(x - 0.3, normal1, width=0.15, label="Normal (File 1)")
    plt.bar(x - 0.15, opt1, width=0.15, label="Optimized (File 1)")
    plt.bar(x + 0.0, normal2, width=0.15, label="Normal (File 2)")
    plt.bar(x + 0.15, opt2, width=0.15, label="Optimized (File 2)")

    plt.xticks(x, crops, rotation=45, ha="right")
    plt.ylabel("Growth Cycles per Year")
    plt.title("Growth Cycle Comparison (File 1 vs File 2)")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_greenhouse_sizes(data1, data2):
    crops = list(data1["cycle"].keys())

    params = ["gh_width", "gh_length", "gh_height", "gh_roof_height", 
              "nr_water_bottles", "bottles_percent_open", "wall_thickness"]

    for param_x, param_y in [("gh_width", "gh_length"), ("gh_height", "gh_roof_height"), 
                             ("nr_water_bottles", "bottles_percent_open")]:
        x1 = [data1["cycle"][crop]["b_param"][param_x] for crop in crops]
        y1 = [data1["cycle"][crop]["b_param"][param_y] for crop in crops]

        x2 = [data2["cycle"][crop]["b_param"][param_x] for crop in crops]
        y2 = [data2["cycle"][crop]["b_param"][param_y] for crop in crops]

        plt.figure(figsize=(8, 6))
        for i, crop in enumerate(crops):
            plt.plot([x1[i], x2[i]], [y1[i], y2[i]], color='black', linestyle='--', alpha=0.5)
            plt.scatter(x1[i], y1[i], color='blue', label='File 1' if i == 0 else "", edgecolors='black')
            plt.scatter(x2[i], y2[i], color='red', label='File 2' if i == 0 else "", edgecolors='black')
            plt.text(x2[i], y2[i], crop, fontsize=8, ha="center")

        plt.xlabel(param_x.replace("_", " ").title())
        plt.ylabel(param_y.replace("_", " ").title())
        plt.title(f"{param_x.replace('_',' ').title()} vs {param_y.replace('_',' ').title()}")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # Wall thickness plot
    wall1 = [data1["cycle"][crop]["b_param"]["wall_thickness"] for crop in crops]
    wall2 = [data2["cycle"][crop]["b_param"]["wall_thickness"] for crop in crops]

    plt.figure(figsize=(8, 6))
    for i, crop in enumerate(crops):
        plt.plot([wall1[i], wall2[i]], [i, i], color="black", linestyle='--', alpha=0.5)
        plt.scatter(wall1[i], i, color="blue", edgecolors="black")
        plt.scatter(wall2[i], i, color="red", edgecolors="black")
        plt.text(wall2[i] + 0.01, i, crop, fontsize=8)

    plt.yticks(range(len(crops)), crops)
    plt.xlabel("Wall Thickness (m)")
    plt.title("Wall Thickness Comparison")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_comprehensive_greenhouse_comparison(data1, data2):
    crops = list(data1["cycle"].keys())

    df1 = pd.DataFrame({
        "Crop": crops,
        "Width": [data1["cycle"][crop]["b_param"]["gh_width"] for crop in crops],
        "Length": [data1["cycle"][crop]["b_param"]["gh_length"] for crop in crops],
        "Height": [data1["cycle"][crop]["b_param"]["gh_height"] for crop in crops],
        "Roof Height": [data1["cycle"][crop]["b_param"]["gh_roof_height"] for crop in crops],
        "Water Bottles": [data1["cycle"][crop]["b_param"]["nr_water_bottles"] for crop in crops],
        "Bottles Open %": [data1["cycle"][crop]["b_param"]["bottles_percent_open"] for crop in crops],
        "Wall Thickness": [data1["cycle"][crop]["b_param"]["wall_thickness"] for crop in crops]
    })

    df2 = df1.copy()
    for param in df1.columns[1:]:
        df2[param] = [data2["cycle"][crop]["b_param"][param.lower().replace(" ", "_")] for crop in crops]
    
    df1["Source"] = "File 1"
    df2["Source"] = "File 2"

    df = pd.concat([df1, df2])

    df_normalized = df.copy()
    for col in df.columns[1:-1]:
        min_val = df[col].min()
        max_val = df[col].max()
        df_normalized[col] = (df[col] - min_val) / (max_val - min_val)

    plt.figure(figsize=(12, 6))
    for crop in crops:
        sns.lineplot(data=df_normalized[df_normalized["Crop"] == crop].set_index("Crop").drop(columns=["Source"]).T,
                     label=crop)

    plt.xticks(rotation=20, ha="right")
    plt.ylabel("Normalized Scale (0-1)")
    plt.title("Comprehensive Greenhouse Parameter Comparison")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    filepath1 = "opt_tis11_2022_2018.json"
    filepath2 = "opt_tis11_2023_2019.json"
    config_path = "crops/crop_data.json"

    data1 = load_data(filepath1)
    data2 = load_data(filepath2)

    plot_crop_yield(data1, data2, config_path)
    plot_growth_cycles(data1, data2)
    plot_greenhouse_sizes(data1, data2)
    plot_comprehensive_greenhouse_comparison(data1, data2)

if __name__ == "__main__":
    main()

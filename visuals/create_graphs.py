import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Load the JSON file
def load_data(filepath):
    """Load the crop growth data from a JSON file."""
    with open(filepath, "r") as file:
        data = json.load(file)
    return data


import numpy as np
import matplotlib.pyplot as plt
import json

def plot_crop_yield(data, config_path):
    """
    Plot the difference in accumulated crop mass when optimizing for crop_mass, 
    adjusted by the Harvest Index (HI) and converted to t ha⁻¹.
    
    Args:
        data (dict): Dictionary containing crop mass data.
        config_path (str): Path to the JSON configuration file with crop-specific HI values.
    """
    
    # Load configuration parameters (includes HI values)
    crops = list(data["crop_mass"].keys())


    normal_cycles = [data["cycle"][crop]["normal_cycles"] for crop in crops]
    optimized_cycles = [data["cycle"][crop]["cycles"] for crop in crops]
    relation = [optimized_cycles[i]/normal_cycles[i] for i in range(len(optimized_cycles))]


    with open(config_path, "r") as file:
        config = json.load(file)

    crops = list(data["crop_mass"].keys())
    
    # Extract HI values from the configuration
    HI_values = {crop: config[crop]["HI"] for crop in crops if crop in config}

    # Calculate final crop yield using HI values and converting to t ha⁻¹
    normal_yield = [
        (data["crop_mass"][crop]["total_crop_normal"] * HI_values.get(crop, 1)) 
        for crop in crops
    ]
    optimized_yield = [
        (data["crop_mass"][crop]["crop_yield"] * HI_values.get(crop, 1)) 
        for i, crop in enumerate(crops)
    ]

    x = np.arange(len(crops))
    
    plt.figure(figsize=(12, 6))
    plt.bar(x - 0.2, normal_yield, width=0.4, label="Normal Crop Yield", alpha=0.7)
    plt.bar(x + 0.2, optimized_yield, width=0.4, label="Optimized Crop Yield", alpha=0.7)

    plt.xticks(x, crops, rotation=45, ha="right")
    plt.ylabel("Crop Yield (t ha⁻¹ per year)")
    plt.title("Optimized vs. Normal Crop Yield")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_growth_cycles(data):
    """Plot the number of cycles per year when optimizing for cycles."""
    crops = list(data["crop_mass"].keys())

    normal_cycles = [data["cycle"][crop]["normal_cycles"] for crop in crops]
    optimized_cycles = [data["cycle"][crop]["cycles"] for crop in crops]
    print(np.array(optimized_cycles)/np.array(normal_cycles))

    x = np.arange(len(crops))
    
    plt.figure(figsize=(12, 6))
    plt.bar(x - 0.2, normal_cycles, width=0.4, label="Normal Cycles", alpha=0.7)
    plt.bar(x + 0.2, optimized_cycles, width=0.4, label="Optimized Cycles", alpha=0.7)

    plt.xticks(x, crops, rotation=45, ha="right")
    plt.ylabel("Growth Cycles per Year")
    plt.title("Optimized vs. Normal Growth Cycles")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_greenhouse_sizes(data):
    """Create scatter plots for greenhouse parameters across different crops with text offsets."""
    crops = list(data["crop_mass"].keys())

    # Extracting greenhouse parameters
    gh_width = [data["cycle"][crop]["b_param"]["gh_width"] for crop in crops]
    gh_length = [data["cycle"][crop]["b_param"]["gh_length"] for crop in crops]
    gh_height = [data["cycle"][crop]["b_param"]["gh_height"] for crop in crops]
    gh_roof_height = [data["cycle"][crop]["b_param"]["gh_roof_height"] for crop in crops]
    nr_water_bottles = [data["cycle"][crop]["b_param"]["nr_water_bottles"] for crop in crops]
    bottles_percent_open = [data["cycle"][crop]["b_param"]["bottles_percent_open"] for crop in crops]
    wall_thickness = [data["cycle"][crop]["b_param"]["wall_thickness"] for crop in crops]

    import numpy as np
    import matplotlib.pyplot as plt

    def plot_scatter(x, y, xlabel, ylabel, title, crop_labels, crops_to_offset, offset_y, crop_colors):
        """Helper function for scatter plots with color-coded crops and bold text labels."""
        plt.figure(figsize=(8, 6))

        # Plot each crop with its unique color
        for i, crop in enumerate(crop_labels):
            plt.scatter(x[i], y[i], color=crop_colors[crop], label=crop if i == 0 else "", alpha=0.7, edgecolors="black")

        # Apply text labels with offset to avoid overlap
        n = 0
        for i, crop in enumerate(crop_labels):
            y_offset = (-1)**n * offset_y * n if crop in crops_to_offset else 0  # Offset for selected crops
            n += 1 if crop in crops_to_offset else 0
            plt.text(x[i], y[i] + y_offset, crop, fontsize=8, fontweight="bold", ha="center")

        plt.xlabel(xlabel, fontsize=10)
        plt.ylabel(ylabel, fontsize=10)
        plt.title(title, fontsize=12, fontweight="bold")
        plt.grid(True)
        plt.show()

    # Define unique colors for each crop
    crops = list(data["cycle"].keys())
    colors = plt.cm.get_cmap("tab10", len(crops))  # Get a colormap with 10 distinct colors
    crop_colors = {crop: colors(i) for i, crop in enumerate(crops)}  # Assign colors to crops

    # Extracting greenhouse parameters
    gh_width = [data["cycle"][crop]["b_param"]["gh_width"] for crop in crops]
    gh_length = [data["cycle"][crop]["b_param"]["gh_length"] for crop in crops]
    gh_height = [data["cycle"][crop]["b_param"]["gh_height"] for crop in crops]
    gh_roof_height = [data["cycle"][crop]["b_param"]["gh_roof_height"] for crop in crops]
    nr_water_bottles = [data["cycle"][crop]["b_param"]["nr_water_bottles"] for crop in crops]
    bottles_percent_open = [data["cycle"][crop]["b_param"]["bottles_percent_open"] for crop in crops]
    wall_thickness = [data["cycle"][crop]["b_param"]["wall_thickness"] for crop in crops]

    # Scatter plot for greenhouse width vs. length
    plot_scatter(gh_width, gh_length, 
                "Greenhouse Width (m)", "Greenhouse Length (m)", 
                "Greenhouse Width vs. Length", crops, [], offset_y=0.1, crop_colors=crop_colors)

    # Scatter plot for greenhouse height vs. roof height
    plot_scatter(gh_height, gh_roof_height, 
                "Greenhouse Height (m)", "Greenhouse Roof Height (m)", 
                "Greenhouse Height vs. Roof Height", crops, 
                [], offset_y=0.01, crop_colors=crop_colors)

    # Scatter plot for number of water bottles vs. percent open
    plot_scatter(nr_water_bottles, bottles_percent_open, 
                "Number of Water Bottles", "Percent of Bottles Open", 
                "Water Bottles vs. Percentage Open", crops, [], offset_y=0.05, crop_colors=crop_colors)

    # Scatter plot for wall thickness per crop (y-axis categorical)
    plt.figure(figsize=(8, 6))
    for i, crop in enumerate(crops):
        plt.scatter(wall_thickness[i], i, color=crop_colors[crop], alpha=0.7, edgecolors="black")
        plt.text(wall_thickness[i] + 0.01, i, crop, fontsize=8, fontweight="bold", ha="center")

    plt.xlabel("Wall Thickness (m)", fontsize=10)
    plt.yticks(range(len(crops)), crops, fontsize=8, fontweight="bold")
    plt.title("Wall Thickness per Crop", fontsize=12, fontweight="bold")
    plt.grid(True)
    plt.show()



def plot_comprehensive_greenhouse_comparison(data):
    """Create a parallel coordinates plot for all greenhouse parameters."""
    crops = list(data["cycle"].keys())

    # Creating a DataFrame
    df = pd.DataFrame({
        "Crop": crops,
        "Width": [data["cycle"][crop]["b_param"]["gh_width"] for crop in crops],
        "Length": [data["cycle"][crop]["b_param"]["gh_length"] for crop in crops],
        "Height": [data["cycle"][crop]["b_param"]["gh_height"] for crop in crops],
        "Roof Height": [data["cycle"][crop]["b_param"]["gh_roof_height"] for crop in crops],
        "Water Bottles": [data["cycle"][crop]["b_param"]["nr_water_bottles"] for crop in crops],
        "Bottles Open %": [data["cycle"][crop]["b_param"]["bottles_percent_open"] for crop in crops],
        "Wall Thickness": [data["cycle"][crop]["b_param"]["wall_thickness"] for crop in crops]
    })

    df_normalized = (df.iloc[:, 1:] - df.iloc[:, 1:].min()) / (df.iloc[:, 1:].max() - df.iloc[:, 1:].min())
    df_normalized["Crop"] = df["Crop"]

    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    sns.lineplot(data=df_normalized.set_index("Crop").T, dashes=False, palette="tab10", alpha=0.8)
    plt.xticks(rotation=20, ha="right")
    plt.ylabel("Normalized Scale (0-1)")
    plt.title("Comprehensive Greenhouse Parameter Comparison Across Crops")
    plt.legend(labels=crops, bbox_to_anchor=(0.95, 1), loc='upper left')
    plt.show()


# Main function to run all visualizations
def main():
    filepath = "opt_tis11_2022_2018.json"  # Update this with the actual path to your JSON file
    data = load_data(filepath)
    
    plot_crop_yield(data, "crops/crop_data.json")
    plot_growth_cycles(data)
    plot_greenhouse_sizes(data)
    plot_comprehensive_greenhouse_comparison(data)


# Run the script
if __name__ == "__main__":
    main()

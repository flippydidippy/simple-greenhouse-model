import matplotlib.pyplot as plt
import numpy as np

def plot_temperature(single_day, selected_day):
    """Plots GH temperature, external temperature, and solar for a specific day."""

    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Temp plot (Primary plot)
    ax1.set_xlabel("Hour")
    ax1.set_ylabel("Temperature (°C)")
    ax1.plot(single_day["hour"], single_day["GH_T_air"], label="GH Temperature", color="blue")
    ax1.plot(single_day["hour"], single_day["GH_T_top"], label="GH Top", color="green", linestyle="dashed")
    ax1.plot(single_day["hour"], single_day["temperature"], label="External Temperature", color="red", linestyle="dashed")
    ax1.tick_params(axis='y')
    ax1.legend(loc="upper left")

    # solar plot (Secondary plot)
    ax2 = ax1.twinx()
    ax2.set_ylabel("solar (W/m²)")
    ax2.plot(single_day["hour"], single_day["solar"], label="solar", color="orange", linestyle="dotted")
    ax2.tick_params(axis='y')

    # Humidity GH plot
    #ax3 = ax1.twinx()
    #ax3.set_ylabel("RH (%)")
    #ax3.plot(single_day["hour"], single_day["GH_humidity"], label="GH Humidity", color="gray")
    #ax3.plot(single_day["hour"], single_day["humidity"], label="External Humidity", color="gray", linestyle="dashed")
    #ax3.tick_params(axis='y')   

    # Titles & Legend
    fig.suptitle(f"Hourly Temperature and solar on {selected_day}")
    fig.tight_layout()
    fig.legend(loc="upper right")

    # Grid & Show Plot
    plt.grid()
    plt.show()

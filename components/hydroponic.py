def hydroponic_pipe_cooling(T_air, T_water, A_pipe, h_pipe, k_pipe, d_pipe):
    """Computes heat transfer between greenhouse air and hydroponic water pipes.

    Args:
        T_air (float): Greenhouse air temperature 
        T_water (float): Hydroponic circulating water temperature (assumed constant ~16°C)
        A_pipe (float): tot surface area of water pipes (m2)
        h_pipe (float): Convective heat transfer coefficient of pipes (W/m2K)
        k_pipe (float): Thermal conductivity of pipe material (W/mK)
        d_pipe (float): pipe wall thickness (m)

    Returns:
        float: Heat removed from greenhouse air by hydroponic system (W)
    """

    #! Note: not used; rather an attempt in the validation process.
    # Convective cooling from air to pipes
    Q_conv_pipe = h_pipe * A_pipe * (T_air - T_water)
    
    # Conductive cooling through pipe walls (optional, for thick pipes)
    Q_cond_pipe = (k_pipe * A_pipe * (T_air - T_water)) / d_pipe if d_pipe > 0 else 0
    
    return Q_conv_pipe + Q_cond_pipe  # Total cooling effect

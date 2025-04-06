from components.const import LV

def latent_calc(transpiration_potential_kg_per_s, RH, temperature=20):
    """
    Calculate latent heat loss from evaporation/transpiration adjusted by RH.

    Args:
        transpiration_potential_kg_per_s (float): Max possible transpiration or evaporation rate (kg/s) at RH=0.
        RH (float): Relative humidity as a fraction (0 to 1).
        temperature (float): Temperature in °C for Lv adjustment.

    Returns:
        float: Latent heat loss in watts (J/s).
    """

    Lv = LV - 2370 * temperature  # Latent heat of vaporization (J/kg)
    effective_transpiration = transpiration_potential_kg_per_s * (1 - RH)  # Mass loss reduced by RH
    Q_latent = effective_transpiration * Lv

    return Q_latent


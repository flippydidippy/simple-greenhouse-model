from components.const import LV

def latent_calc(transpiration_rate):
    """Calculates heat loss due to plant transpiration (latent heat).

    Args:
        transpiration_rate (float): transpiration rate coef.

    Returns:
        float: heat transfered per unit time
    """
    return transpiration_rate * LV

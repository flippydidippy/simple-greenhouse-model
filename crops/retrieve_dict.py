import json

def read_json(json_file):
    with open(json_file, "r") as file:
        return json.load(file)

def get_crop_dict(selected_crop: str):
    # crop_models = read_json("crops/crop_data.json")
    # crop_data = crop_models[selected_crop]

    # T_base = crop_data.get("T_base")
    # T_opt = crop_data.get("T_opt")
    # RUE = crop_data.get("RUE")
    # ideal_RH = crop_data.get("ideal_RH")
    # RH_sensitivity = crop_data.get("RH_sensitivity")
    # GDD_maturity = crop_data.get("GDD_maturity")
    # CO2_rsponse = crop_data.get("CO2_response")

    #return T_base, T_opt, RUE, ideal_RH, RH_sensitivity, GDD_maturity, CO2_rsponse¨

    crop_models = read_json("crops/simple_crop_data.json")
    crop_data = crop_models[selected_crop]

    T_sum = crop_data.get("Tsum")
    HI = crop_data.get("HI")
    I50A = crop_data.get("I50A")
    I50B = crop_data.get("I50B")
    T_base = crop_data.get("Tbase")
    T_opt = crop_data.get("Tbase")
    RUE = crop_data.get("RUE")
    I50maxH = crop_data.get("I50maxH")
    I50maxW = crop_data.get("I50maxW")
    T_heat = crop_data.get("Tmax")
    T_extreme = crop_data.get("Text")
    SCO2 = crop_data.get("SCO2")
    S_water = crop_data.get("Swater")

    return T_sum, HI, I50A, I50B, T_base, T_opt, RUE, I50maxH, I50maxW, T_heat, T_extreme, SCO2, S_water
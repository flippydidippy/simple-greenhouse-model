import json
from greenhouse_setups.params import update_all_params

def load_params(data_path):
    file_path = "greenhouse_setups/" + data_path
    with open(file_path, "r") as file:
        params_dict = json.load(file)
        update_all_params(params_dict)

def save_params(file_path, params):
    with open(file_path, "w") as file:
        json.dump(params, file, indent=4)
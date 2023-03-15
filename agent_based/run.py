from agent_based.models.base_model import ModelV1
from utils.process import process_ure_rse_source, load_config, load_clean_res_data
import datetime

if __name__ == "__main__":
    config_file = "./config/config.yml"
    config = load_config(config_file)

    try:
        wind_sources, pv_sources, res = load_clean_res_data(config)

    except FileNotFoundError:
        process_ure_rse_source(config)
        wind_sources, pv_sources, res = load_clean_res_data(config)

    model = ModelV1(wind_sources, pv_sources, time_list=[0, 1, 2])

    for i in range(2):
        model.step()

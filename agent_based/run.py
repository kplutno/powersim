from agent_based.models.base_model import ModelV1
from utils.process import process_ure_rse_source, load_config, load_clean_res_data
from utils.topo_data_process import process_topo


if __name__ == "__main__":
    config_file = "./config/config.yml"
    config = load_config(config_file)

    # Data processing before 
    if config.process.process_ure_rse_source:
        process_ure_rse_source(config)

    if config.process.process_topo:
        process_topo(config)
    
    
    model = ModelV1(wind_sources, pv_sources, time_list=[0, 1, 2])

    for i in range(2):
        model.step()

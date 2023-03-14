from agent_based.models.base_model import ModelV1
from utils.process import process_ure_rse_source, load_config

if __name__ == "__main__":
    config_file = "./config/config.yml"
    config = load_config(config_file)

    rse, wind_sources, pv_sources = process_ure_rse_source(config)

    model = ModelV1(wind_sources, pv_sources, dt=config.computations.dt)

    for i in range(10):
        model.step()

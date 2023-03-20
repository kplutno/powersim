from agent_based.models.base_model import ModelV1
from utils.process import process_ure_rse_source, load_config, load_clean_res_data
from utils.topo_data_process import process_topo
import pandas as pd
import logging
import datetime
from pytz import timezone

def main():
    config_file = "./config/config.yml"
    config = load_config(config_file)

    logger = logging.getLogger(__name__)
    logger.info("Data processing")
    # Data processing before
    if config.process.process_ure_rse_source:
        process_ure_rse_source(config)

    if config.process.process_topo:
        process_topo(config)

    logger.info("Loading data.")
    wind_df, pv_df, res_df = load_clean_res_data(config)

    wind_df = wind_df.iloc[0:3]
    pv_df = pv_df.iloc[0:3]
    
    logger.info("Creating model.")
    
    default_timezone = timezone(config.time.timezone)
    
    starttime = datetime.datetime(2022, 1, 12, 0, 0,  tzinfo=default_timezone)
    deltatime = datetime.timedelta(hours=1)
    
    model = ModelV1(wind_df, pv_df, starttime=starttime, deltatime=deltatime)

    for i in range(24):
        model.step()


if __name__ == "__main__":
    main()

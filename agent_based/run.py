from agent_based.models.base_model import ModelV1
from utils.process import process_ure_rse_source, load_config, load_clean_res_data
from utils.topo_data_process import process_topo
import logging
import datetime
from pytz import timezone
import time


def main():
    config_path = "./config/*.yml"
    config = load_config(config_path)

    logger = logging.getLogger(__name__)
    logger.info("Data processing")
    # Data processing before
    if config.process.process_ure_rse_source:
        process_ure_rse_source(config)

    if config.process.process_topo:
        process_topo(config)

    logger.info("Loading data.")
    wind_df, pv_df, res_df = load_clean_res_data(config)

    wind_df = wind_df.iloc[0:500]
    pv_df = pv_df.iloc[0:500]

    logger.info("Creating model.")

    default_timezone = timezone(config.time.timezone)

    starttime = datetime.datetime(2022, 1, 12, 12, 0, tzinfo=default_timezone)
    deltatime = datetime.timedelta(minutes=15)

    model = ModelV1(wind_df, pv_df, config, starttime=starttime, deltatime=deltatime)

    logger.info(f"Running code with scheduler: {config.computations.scheduler}")
    sttime = time.time()
    for i in range(4):
        model.step()
    long = time.time() - sttime

    print(f"Scheduler: {config.computations.scheduler} took: {long} seconds.")

    agent_power = model.datacollector.get_agent_vars_dataframe()

    print(agent_power)


if __name__ == "__main__":
    main()

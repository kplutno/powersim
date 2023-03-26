from agent_based.models.base_model import ModelV1
from utils.process import process_ure_rse_source, load_config, load_clean_res_data
from utils.process_ready_res_sources import add_ure_res_grid_coordinates
from utils.topo_data_process import process_topo
import logging
from datetime import datetime, timedelta
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

    if config.process.process_add_row_col:
        add_ure_res_grid_coordinates(config)

    if config.process.process_topo:
        process_topo(config)

    logger.info("Loading data.")
    wind_df, pv_df, res_df = load_clean_res_data(config)

    wind_df = wind_df.iloc[0:300]
    pv_df = pv_df.iloc[0:300]

    logger.info("Creating model.")

    default_timezone = timezone(config.time.timezone)

    start_time = datetime.strptime(config.time.start_time, config.time.format)
    end_time = datetime.strptime(config.time.end_time, config.time.format)
    deltatime = timedelta(**config.time.time_delta)
    steps = int((end_time - start_time) / deltatime)

    model = ModelV1(wind_df, pv_df, config, starttime=start_time, deltatime=deltatime)

    logger.info(f"Running code with scheduler: {config.computations.scheduler}")

    sttime = time.time()
    for i in range(steps):
        model.step()
    long = time.time() - sttime

    logger.info(f"Scheduler: {config.computations.scheduler} took: {long} seconds.")

    logger.info("End of the calculations.")


if __name__ == "__main__":
    main()

import mesa
import datetime
from agent_based.agents.pv_farm import PVInstallation
from agent_based.agents.wind_farm import WindInstallation
from agent_based.utils.meteo import fetch_meteo_um_data, load_db_store
import pandas as pd
import logging
from agent_based.schedulers.concurent_scheduler import SimpleMPScheduler
import sys
import os
from dotenv import load_dotenv
import datetime

load_dotenv()


class ModelV1(mesa.Model):
    def __init__(
        self,
        wind: pd.DataFrame,
        pv: pd.DataFrame,
        config: dict,
        starttime: datetime = None,
        deltatime: datetime.timedelta = None,
        time_list: list = None,
    ):
        # Init
        super().__init__(self)
        self.logger = logging.getLogger(__name__)
        
        # Config setup
        self.config = config
        self.logger.debug(f"Config size: {sys.getsizeof(config)}")
        
        self.meteo_token = os.environ["METEO_API_KEY"]
        
        # Checking what forecasts are saved
        self.meteo_db = load_db_store(self.config)
        
        # Provide list of times or starttime and delta
        if starttime is not None:
            self.dt = deltatime
            self.time = starttime
        else:
            self.time_list = time_list
            self.starttime = time_list[0]
            self.dt = time_list[1] - time_list[0]
            self.time = self.starttime

        # Choose the scheduler
        schedulers = {
            "random_sequential": mesa.time.RandomActivation,
            "parallel": SimpleMPScheduler,
        }

        self.schedule = schedulers[config.computations.scheduler](self)

        # Logging the dataframes shapes
        self.logger.info(f"Wind sources dataframe shape: {wind.shape}")
        self.logger.info(f"PV sources shape: {pv.shape}")

        for index, wind_turbine in wind.iterrows():
            self.schedule.add(
                WindInstallation(
                    self.next_id(),
                    self,
                    wind_turbine["woje"],
                    wind_turbine["powiat"],
                    wind_turbine["moc"],
                    wind_turbine["lat"],
                    wind_turbine["lon"],
                    wind_turbine["P5"],
                    wind_turbine["p5"]
                )
            )

        for index, pv_elem in pv.iterrows():
            self.schedule.add(
                PVInstallation(
                    self.next_id(),
                    self,
                    pv_elem["woje"],
                    pv_elem["powiat"],
                    pv_elem["moc"],
                    pv_elem["lat"],
                    pv_elem["lon"],
                    pv_elem["P5"],
                    pv_elem["p5"]
                )
            )

        self.datacollector = mesa.DataCollector(
            model_reporters={"time": "time"}, agent_reporters={"Power": "power"}
        )

    def step(self):
        self.logger.info(f"Starting computations for time {self.time}")
        self.datacollector.collect(self)
        self.schedule.step()
        self.time += self.dt

    def get_weather(self, time: datetime, coordinates: dict):
        time_string = time.strftime(self.config.meteo.save_time_format)
        
        store_name = self.config.meteo.db.um.store_template.format(
            date=time_string,
            coordinates_P5=coordinates["P5"],
            coordinates_p5=coordinates["p5"]
        )
        
        if store_name in self.meteo_db:
            # self.logger.debug(f"Loading weather data from store.")
            path = self.config.meteo.db.um.path
            path = os.path.join(path, store_name) + self.config.meteo.db.um.store_file_extension
            weather_df = pd.read_parquet(path)
            return weather_df
        
        weather_df = fetch_meteo_um_data(self.config, time, self.meteo_token, coordinates)
        
        # Update list
        self.meteo_db = load_db_store(self.config)
        
        return weather_df

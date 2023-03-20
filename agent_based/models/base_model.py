import mesa
import datetime
from agent_based.agents.pv_farm import PVInstallation
from agent_based.agents.wind_farm import WindInstallation
import pandas as pd
import logging
from agent_based.schedulers.concurent_scheduler import SimpleMPScheduler


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
        self.config = config

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
                )
            )

        self.datacollector = mesa.DataCollector(
            model_reporters={"time": "time"}, agent_reporters={"Power": "power"}
        )

    def step(self, number_of_steps):
        self.logger.info(f"Starting computations for time {self.time}")
        self.datacollector.collect(self)
        self.schedule.step()

    def steps(self, number_of_steps):
        self.logger.info(f"Starting computations for time n steps: {number_of_steps}")
        self.schedule.step(number_of_steps)

    def get_weather_pv(self, latitude: float, longitude: float):
        model = "um"
        grid = "P5"
        coordinates = "4,5"
        fields = ["01215_0000000", "01216_0000000", "01235_0000000"]
        date = self.time

        for field in fields:
            url = f"https://api.meteo.pl/api/v1/model/{model}/grid/{grid}/coordinates/{coordinates}/field/{field}/level/_/date/{date}/forecast/"

        weather = dict()

        index = pd.DatetimeIndex(
            [
                self.time,
            ]
        )

        weather["pressure"] = 1000.0
        weather["temp_air"] = 20.0
        weather["dni"] = 800
        weather["ghi"] = 600
        weather["dhi"] = 1000
        weather["wind_speed"] = 5

        return pd.DataFrame(data=weather, index=index)

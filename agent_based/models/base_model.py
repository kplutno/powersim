import mesa
import datetime
from agent_based.agents.pv_farm import PVInstallation
from agent_based.agents.wind_farm import WindInstallation
import pandas as pd
import logging


class ModelV1(mesa.Model):
    def __init__(
        self,
        wind: pd.DataFrame,
        pv: pd.DataFrame,
        starttime: datetime = None,
        deltatime: datetime.timedelta = None,
        time_list: list = None,
    ):
        # Init
        super().__init__(self)
        self.logger = logging.getLogger(__name__)

        # Provide list of times or starttime and delta
        if starttime is not None:
            self.starttime = starttime
            self.dt = deltatime
            self.time = starttime
        else:
            self.time_list = time_list
            self.starttime = time_list[0]
            self.dt = time_list[1] - time_list[0]
            self.time = self.starttime

        # Choose the scheduler
        self.scheduler = mesa.time.RandomActivation(self)

        # Logging the dataframes shapes
        self.logger.info(f"Wind sources dataframe shape: {wind.shape}")
        self.logger.info(f"PV sources shape: {pv.shape}")

        for index, wind_turbine in wind.iterrows():
            self.scheduler.add(
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
            self.scheduler.add(
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

    def step(self):
        self.logger.info(f"Starting computations for time: {self.time}")
        self.time += self.dt

        self.scheduler.step()

import mesa
import datetime
from agent_based.agents.pv_farm import PVInstallation
from agent_based.agents.wind_farm import WindInstallation
import pandas as pd


class ModelV1(mesa.Model):
    def __init__(
        self,
        wind: pd.DataFrame,
        pv: pd.DataFrame,
        starttime: datetime = None,
        deltatime: datetime.timedelta = None,
        time_list: list = None
    ):
        super().__init__(self)
        
        # Provide list of times or starttime and delta
        if starttime is not None:
            self.starttime = starttime
            self.dt = deltatime
            self.time = starttime
        else:
            self.time_list = iter(time_list)
            self.time = next(self.time_list)
        
        self.scheduler = mesa.time.RandomActivation(self)

        for index, wind_turbine in wind.iterrows():
            self.scheduler.add(
                WindInstallation(
                    self.next_id(),
                    self,
                    wind_turbine["woje"],
                    wind_turbine["powiat"],
                    wind_turbine["moc"],
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
                )
            )

    def step(self):
        # Timestep
        if self.starttime is None:
            self.time = next(self.time_list)
        else:
            self.starttime += self.dt
        
        self.scheduler.step()

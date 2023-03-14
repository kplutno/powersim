import mesa
import datetime
from agent_based.agents.pv_farm import PVAgent
import pandas as pd

class ModelV1(mesa.Model):
    def __init__(self, wind: pd.DataFrame, pv: pd.DataFrame, start_time: datetime, dt: datetime.timedelta):
        super().__init__(self)
        self.dt = dt
        self.time = start_time
        self.scheduler = mesa.time.RandomActivation(self)
        wind_array = wind.to_dict(orient="list")

    def step(self):
        """Advance the model by one step."""
        self.time += self.dt
        self.scheduler.step()

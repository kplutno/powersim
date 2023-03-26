import mesa
import pandas as pd
import logging
import os


class BaseAgent(mesa.Agent):
    def __init__(
        self,
        unique_id: int,
        model: mesa.Model,
        voivodeship: str,
        powiat: str,
        power: float,
        latitude: float,
        longitude: float,
        P5: str,
        p5: str,
        altitude: float = 0.0,
        timezone: str = "Europe/Warsaw",
    ):
        super().__init__(unique_id, model)
        self.logger = logging.getLogger(__name__)

        self.voivodeship = voivodeship
        self.powiat = powiat

        # Power in Watts (Watt-Peaks)
        self.max_power = power * 1e6
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.altitude = float(altitude)
        self.timezone = timezone
        self.coordinates = {"P5": P5, "p5": p5}

        self.power = None

    def save_power(self):
        df = pd.DataFrame()

        df["power"] = self.power
        df["max_power"] = self.max_power
        df["unique_id"] = self.unique_id
        df["lon"] = self.longitude
        df["lat"] = self.latitude
        df["P5"] = self.coordinates["P5"]
        df["p5"] = self.coordinates["p5"]
        df["type"] = self.__class__.__name__

        filename = self.model.config.data.output.name_template.format(
            date=self.model.time.strftime(self.model.config.meteo.api.time_format),
            unique_id=self.unique_id,
        )

        output_path = self.model.config.data.output.path
        output_format = self.model.config.data.output.format

        full_path = os.path.join(output_path, filename) + output_format

        df.to_parquet(full_path)

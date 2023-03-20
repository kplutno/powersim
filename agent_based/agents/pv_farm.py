import mesa
import logging


class PVInstallation(mesa.Agent):
    def __init__(
        self,
        unique_id: int,
        model: mesa.Model,
        voivodeship: str,
        powiat: str,
        power: float,
        latitude: float,
        longitude: float,
    ):
        super().__init__(unique_id, model)
        self.logger = logging.getLogger(__name__)
        
        self.voivodeship = voivodeship
        self.powiat = powiat
        self.power = power
        self.latitude = latitude
        self.longitude = longitude

    def step(self):
        self.logger.debug(f"Calculations for PVInstallation id: {self.unique_id}")
        

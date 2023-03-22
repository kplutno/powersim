import mesa


class WindInstallation(mesa.Agent):
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
        p5: str
    ):
        super().__init__(unique_id, model)
        self.voivodeship = voivodeship
        self.powiat = powiat
        self.power = power
        self.latitude = latitude
        self.longitude = longitude
        self.coordinates = {
            "P5" : P5,
            "p5" : p5
        }

    def step(self):
        self.power += self.power

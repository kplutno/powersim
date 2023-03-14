import mesa

class PVInstallation(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.Model, voivodeship: str, powiat: str, power: float):
        super().__init__(unique_id, model)
        self.voivodeship = voivodeship
        self.powiat = powiat
        self.power = power
        
    def step(self):
        pass

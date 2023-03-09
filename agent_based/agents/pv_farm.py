import mesa

class PVAgent(mesa.Agent):

    def __init__(self, unique_id: int, model: mesa.Model):
        super().__init__(unique_id, model)
        
        
    def step(self):
        print(f"Producing PV energy. ID: {self.unique_id}")
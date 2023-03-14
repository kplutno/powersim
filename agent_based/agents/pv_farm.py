import mesa
import multiprocessing as mp
import numpy as np

class PVAgent(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.Model):
        super().__init__(unique_id, model)
        self.test = 0
        
    def step(self):
        self.test += 1
        randomarray = np.random.rand(2048)
        ffttransform = np.fft.fft(randomarray)
        return self

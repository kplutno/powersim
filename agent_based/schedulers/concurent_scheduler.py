import mesa
from multiprocessing import Manager, Pool, cpu_count, Barrier

class SimpleMPScheduler(mesa.time.BaseScheduler):
    def __init__(self, model: mesa.Model) -> None:
        super().__init__(model)

    def step(self) -> None:
        with Manager() as manager:
            keys = self._agents.keys()
            with Pool(processes=cpu_count()) as pool:
                newStep = pool.map(self.execute, self._agents.keys())
        
        self._agents = {id: agent for id, agent in zip(keys, newStep)}
        self.steps += 1
        self.time += self.model.dt

    def execute(self, id):
        return self._agents[id].step()
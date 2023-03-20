import mesa
from multiprocessing import Manager, Pool, cpu_count
from joblib import Parallel, delayed


class SimpleMPScheduler(mesa.time.BaseScheduler):
    def __init__(self, model: mesa.Model) -> None:
        super().__init__(model)

    def step(self, number_of_steps) -> None:
        ids = self._agents.keys()
        with Parallel(
            n_jobs=self.model.config.computations.number_of_processes,
            prefer=self.model.config.computations.backend,
            max_nbytes=1e6
        ) as parallel:
            for i in range(number_of_steps):
                results = parallel(delayed(execute)(agent) for agent in self._agents.values())
                self._agents = {id : agent for id, agent in zip(ids, results) }
                self.steps += 1
                
                # Incrementing model's time
                self.model.time += self.model.dt
                
                # Collecting model
                self.model.datacollector.collect(self.model)


def execute(agent):
    agent.step()
    return agent

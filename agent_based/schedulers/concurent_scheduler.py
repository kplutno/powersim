import mesa
from multiprocessing import Manager, Pool, cpu_count
from joblib import Parallel, delayed


class SimpleMPScheduler(mesa.time.BaseScheduler):
    def __init__(self, model: mesa.Model) -> None:
        super().__init__(model)

    def step(self, number_of_steps) -> None:
        ids = self._agents.keys()
        Parallel(
            n_jobs=self.model.config.computations.number_of_processes,
            prefer=self.model.config.computations.backend,
            max_nbytes=1e6,
        )(delayed(execute)(agent) for agent in self._agents.values())

        self._agents = {id: agent for id, agent in zip(ids, results)}
        self.steps += 1


def execute(agent):
    agent.step()
    return agent

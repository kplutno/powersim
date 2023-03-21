import mesa
from multiprocessing import Manager, Pool, cpu_count
from joblib import Parallel, delayed


class SimpleMPScheduler(mesa.time.BaseScheduler):
    def __init__(self, model: mesa.Model) -> None:
        super().__init__(model)

    def step(self) -> None:
        ids = self._agents.keys()
        results = Parallel(
            n_jobs=self.model.config.computations.number_of_processes,
            prefer=self.model.config.computations.backend,
            max_nbytes=1e6,
        )(delayed(execute)(agent) for agent in self.agent_buffer(shuffled=True))

        self._agents = {agent.unique_id: agent for agent in results}
        self.steps += 1


def execute(agent):
    agent.step()
    return agent

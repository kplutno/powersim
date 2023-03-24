import mesa
from multiprocessing import Manager, Pool, cpu_count
from joblib import Parallel, delayed


class SimpleMPScheduler(mesa.time.BaseScheduler):
    def __init__(self, model: mesa.Model) -> None:
        super().__init__(model)

    def step(self) -> None:
        number_of_tasks = self.get_agent_count()
        batch_size = int(number_of_tasks // self.model.config.computations.number_of_processes) + 1
        results = Parallel(
            n_jobs=self.model.config.computations.number_of_processes,
            prefer=self.model.config.computations.prefer,
            pre_dispatch=self.model.config.computations.pre_dispatch,
            batch_size=batch_size,
            verbose=self.model.config.computations.verbose
        )(delayed(execute)(agent) for agent in self.agent_buffer(shuffled=True))

        self._agents = {agent.unique_id: agent for agent in results}
        self.steps += 1


def execute(agent):
    agent.step()
    return agent

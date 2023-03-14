import mesa
from agent_based.schedulers.concurent_scheduler import SimpleMPScheduler
from agent_based.agents.pv_farm import PVAgent


class Model(mesa.Model):
    def __init__(self, number_of_agents: int, dt: float):
        super().__init__(self)
        self.dt = dt
        self.time = 0
        self.scheduler = SimpleMPScheduler(self)
        for i in range(number_of_agents):
            self.scheduler.add(PVAgent(self.next_id(), self))

    def step(self):
        """Advance the model by one step."""
        self.time += self.dt
        self.scheduler.step()

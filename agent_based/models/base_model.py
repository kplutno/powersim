import mesa
from agent_based.schedulers.concurent_scheduler import SimpleConcurentScheduler
from agent_based.agents.pv_farm import PVAgent

class Model(mesa.Model):

    def __init__(self, number_of_agents: int):
        super().__init__(self)
        self.__id_gen = 0
        self.scheduler = SimpleConcurentScheduler(self)
        for i in range(number_of_agents):
            self.scheduler.add(PVAgent(self.next_id(), self))

    def step(self):
        """Advance the model by one step."""
        self.scheduler.step()

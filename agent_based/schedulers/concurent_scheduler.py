import mesa

class SimpleConcurentScheduler(mesa.time.BaseScheduler):
    def step(self) -> None:
        for agent in self.agent_buffer(shuffled=True):
            agent.step()
        self.steps += 1
        self.time += 1

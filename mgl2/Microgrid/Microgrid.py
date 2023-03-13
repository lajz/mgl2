from abc import ABC, abstractmethod

class Microgrid(ABC):
    def __init__(self, prosumers, state):
        self.prosumers = prosumers
        self.state = state

    @abstractmethod
    def update_state(self, action, descriptor):
        pass

    @abstractmethod
    def simulate(self, action, descriptor):
        pass

    def step(self, action, descriptor):
        self.update_state(action, descriptor)
        state, energy_reward = self.simulate(action, descriptor)
        return state, energy_reward

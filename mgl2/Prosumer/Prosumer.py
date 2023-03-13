from abc import ABC, abstractmethod

class Prosumer(ABC):
    def __init__(self, id, state):
        self.id = id
        # Dictionary containing relevant attributes
        self.state = state

    @abstractmethod
    def step(self, action, descriptor):
        pass

    @abstractmethod
    def reset(self):
        pass

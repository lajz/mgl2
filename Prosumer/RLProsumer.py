from Prosumer import Prosumer, ProsumerState, ProsumerDayMetrics
import numpy as np

TARGET_ACTION = np.array([4, 5, 3, 9, 9, 1, 2], dtype=np.float64) / 10

class RLProsumerState(ProsumerState):
    energy_demand: np.ndarray

    def update(self, action: np.ndarray):
        self.energy_demand += action


class RLProsumerMetrics(ProsumerDayMetrics):
    reward: float = 0.0

    def update(self, **kwargs):
        super().update(**kwargs)
        self.reward = -np.sum(np.abs(self.total_demand - TARGET_ACTION))


class RLProsumer(Prosumer):

    def __init__(self, state: RLProsumerState, demand: np.ndarray) -> None:
        super().__init__(state)
        self.metrics = RLProsumerMetrics()
        self.demand = demand

    def simulate(self, action: np.ndarray):
        self.state.update(action)
        self.metrics.update(step_demand=self.state.energy_demand)
        print({'demand': self.state.energy_demand, 'reward': self.metrics.reward})

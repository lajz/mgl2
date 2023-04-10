from Prosumer import Prosumer, ProsumerState, ProsumerDayMetrics
import numpy as np

TARGET_ACTION = np.array([4, 5, 3, 9, 9, 1, 2], dtype=np.float64) / 10

class RLProsumerState(ProsumerState):
    energy_demand: np.ndarray

    def update(self, action: np.ndarray):
        self.energy_demand += action


class RLProsumerMetrics(ProsumerDayMetrics):
    reward: float = 0.0
    energy_price: np.ndarray

    def update(self, **kwargs):
        super().update(**kwargs)
        self.reward = -np.sum((self.total_demand - TARGET_ACTION) * self.energy_price)


class RLProsumer(Prosumer):

    def __init__(self, state: RLProsumerState, demand: np.ndarray, energy_price: np.ndarray) -> None:
        super().__init__(state)
        self.metrics = RLProsumerMetrics(energy_price=energy_price)
        self.demand = demand
        self.energy_price = energy_price

    def simulate(self, action: np.ndarray):
        self.state.update(action)
        self.metrics.update(step_demand=self.state.energy_demand, energy_price=self.energy_price)  # Pass the energy price to the metrics update
        print({'demand': self.state.energy_demand, 'reward': self.metrics.reward})

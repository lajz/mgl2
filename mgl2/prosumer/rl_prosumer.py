from mgl2.prosumer.prosumer import Prosumer, ProsumerState, ProsumerDayMetrics
from mgl2.utils.constants import DAY_LENGTH
import numpy as np

TARGET_ACTION = np.array([4, 5, 3, 9, 9, 1, 2], dtype=np.float64)

class RLProsumerState(ProsumerState):
    energy_demand: np.ndarray = np.zeros(DAY_LENGTH)

    def update_props(self, action: np.ndarray):
        self.energy_demand = action


class RLProsumerMetrics(ProsumerDayMetrics):
    reward: float = 0.0

    def update(self, **kwargs):
        super().update(**kwargs)
        self.reward = -np.sum(np.abs(self.step_demand - TARGET_ACTION))


class RLProsumer(Prosumer):

    def __init__(self, state: RLProsumerState,) -> None:
        super().__init__(state)
        self.metrics = RLProsumerMetrics()

    @classmethod
    def default(cls) -> "RLProsumer":
        return cls(RLProsumerState())

    def simulate(self):
        self.metrics.update(step_demand=self.state.energy_demand)
        # print({'demand': self.state.energy_demand, 'reward': self.metrics.reward})

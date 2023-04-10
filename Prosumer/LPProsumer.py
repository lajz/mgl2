import numpy as np
from Prosumer import Prosumer, ProsumerState, ProsumerDayMetrics
from scipy.optimize import linprog

class LPProsumerState(ProsumerState):
    energy_demand: np.ndarray

class LPProsumerMetrics(ProsumerDayMetrics):
    cost: float = 0.0
    energy_price: np.ndarray

    def update(self, **kwargs):
        super().update(**kwargs)
        self.cost = np.sum(self.total_demand * self.energy_price)

class LPProsumer(Prosumer):

    def __init__(self, state: LPProsumerState, demand: np.ndarray, energy_price: np.ndarray) -> None:
        super().__init__(state)
        self.metrics = LPProsumerMetrics(energy_price=energy_price)
        self.demand = demand
        self.energy_price = energy_price

    def simulate(self):
        # Objective function: minimize cost
        c = self.energy_price

        A_eq = np.eye(len(self.energy_price))
        b_eq = self.demand

        # TODO: add bounds
        bounds = [(0, None) for _ in range(len(self.energy_price))]

        result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

        # Update the state and metrics
        self.state.energy_demand = result.x
        self.metrics.update(step_demand=self.state.energy_demand, energy_price=self.energy_price)

        print({'demand': self.state.energy_demand, 'cost': self.metrics.cost})


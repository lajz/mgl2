from mgl2.prosumer.rl_prosumer import RLProsumer, RLProsumerState, RLProsumerMetrics
from mgl2.utils.battery import Battery
import numpy as np

class VehicleState(RLProsumerState):
    battery: Battery = Battery()

    def update_props(self, action: np.ndarray):
        self.energy_demand = self.battery.step(action)

class Vehicle(RLProsumer):
    def __init__(self, state: VehicleState) -> None:
        super().__init__(state)
        self.metrics = RLProsumerMetrics()

    @classmethod
    def default(cls) -> "Vehicle":
        return cls(VehicleState())

    def simulate(self):
        self.metrics.update(step_demand=self.state.energy_demand)

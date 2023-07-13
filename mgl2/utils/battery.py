from pydantic import BaseModel
from mgl2.utils.constants import DAY_LENGTH

import numpy as np

class BatteryState(BaseModel):
    charge_level: float = 0.0
    charge_capacity: float = 100.0

    class Config:
        arbitrary_types_allowed = True

# class Battery:
#     def __init__(self, state: BatteryState):
#         self.state = state
#
#     def charge(self, amount):
#         self.state.charge_level = min(self.state.charge_level + amount, self.state.charge_capacity)
#
#     def discharge(self, amount):
#         discharge_amount = min(self.state.charge_level, amount)
#         self.state.charge_level -= discharge_amount
#         return discharge_amount
#
#     def get_charge_level(self):
#         return self.state.charge_level
class Battery:

    def __init__(self, capacity=100.0):
        self.capacity = capacity
        self.current_charge = np.zeros(DAY_LENGTH)

    def step(self, action):
        potential_charge = self.current_charge + action
        
        # cannot charge beyond the battery's capacity
        self.current_charge = np.clip(potential_charge, 0, self.capacity)
        return self.current_charge

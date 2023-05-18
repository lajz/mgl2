from abc import ABC, abstractmethod
from pydantic import BaseModel
import numpy as np
from mgl2.utils.constants import DAY_LENGTH

class ProsumerState(BaseModel):

    def update_props(action):
        pass
    
    def update(self, action, **kwargs):
        self.update_props(action)

    class Config:
        arbitrary_types_allowed = True

class ProsumerMetrics(BaseModel):
    def update():
        pass

    class Config:
        arbitrary_types_allowed = True

class Prosumer(ABC):

    def __init__(self, state : ProsumerState):
        self.state : ProsumerState = state
        self.metrics = ProsumerMetrics()

    def update_state(self, action, **kwargs):
        self.state.update(action, **kwargs)

    @abstractmethod
    def simulate(self):
        pass


###
### Constant Prosumer Example
###

class ProsumerDayMetrics(ProsumerMetrics):

    step_demand: np.ndarray = np.zeros(DAY_LENGTH)
    total_demand: np.ndarray = np.zeros(DAY_LENGTH)

    def update(self, step_demand: np.ndarray, **kwargs):
        self.step_demand = step_demand
        self.total_demand += step_demand

class ConstantProsumer(Prosumer):

    def __init__(self, state : ProsumerState, demand: np.ndarray):
        self.state : ProsumerState = state
        self.metrics = ProsumerDayMetrics()
        self.demand = demand

    def simulate(self):
        ProsumerDayMetrics.update(self.demand)





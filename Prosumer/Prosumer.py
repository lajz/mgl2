from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
import numpy as np
DAY_LENGTH = 7

class ProsumerState(BaseModel):

    def update(action):
        pass

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

    def update_state(self, action):
        self.state.update(action)

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





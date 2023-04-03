from abc import ABC, abstractmethod
from mgl2.prosumer.prosumer import Prosumer, ProsumerDayMetrics
import numpy as np

from pydantic import BaseModel

from mgl2.utils.constants import DAY_LENGTH


class MicrogridState(BaseModel):
    
    def update(action):
        pass
    
class MicrogridMetrics(BaseModel):

    def update(prosumer_metrics):
            pass

class Microgrid(ABC):
    
    def __init__(self, state : MicrogridState):
        self.state : MicrogridState = state
        self.metrics = MicrogridMetrics()

    @abstractmethod
    def update_state(self, action):
        pass

    @abstractmethod
    def simulate(self):
        pass
    
###
### Building Microgrid
###

class MicrogridDayMetrics(BaseModel):

    step_demand : np.ndarray
    total_demand : np.ndarray = np.zeros(DAY_LENGTH)
    
    def update(self, prosumer_day_metrics_list : list[ProsumerDayMetrics]):
        self.step_demand = np.zeros(DAY_LENGTH)
        for prosumer_day_metrics in prosumer_day_metrics_list:
            self.step_demand+=prosumer_day_metrics.step_demand
        self.total_demand+=self.step_demand

class BuildingMicrogrid(Microgrid):
    '''
    Microgrid with prosumers that are only part of this micogrid
    '''
    def __init__(self, state : MicrogridState, prosumers : list[Prosumer]):
        self.state : MicrogridState = state
        self.metrics = MicrogridMetrics()
        self.prosumers = prosumers

    @abstractmethod
    def update_state(self, action):
        self.state.update(action)
        for prosumer in self.prosumers:
            prosumer.update_state(action)

    @abstractmethod
    def simulate(self):
        prosumer_day_metrics_list : list[ProsumerDayMetrics] = []
        for prosumer in self.prosumers:
            prosumer.simulate()
            prosumer_day_metrics_list.append(prosumer.metrics)
        self.metrics.update(prosumer_day_metrics_list)
        

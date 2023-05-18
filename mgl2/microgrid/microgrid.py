from abc import ABC, abstractmethod
from mgl2.prosumer.prosumer import Prosumer, ProsumerDayMetrics
import numpy as np

from pydantic import BaseModel

from mgl2.utils.constants import DAY_LENGTH


class MicrogridState(BaseModel):
    
    prosumers : list[Prosumer]
    
    def update_props(self, action):
        pass
    
    def update(self, action: dict, **kwargs):
        for prosumer in self.prosumers:
            prosumer.update_state(action, **kwargs)
        self.update_props(action)
    
    class Config:
        arbitrary_types_allowed = True
    
class MicrogridMetrics(BaseModel):

    def update(self, prosumer_metrics):
        pass
        
    class Config:
        arbitrary_types_allowed = True

class Microgrid(ABC):
    
    def __init__(self, state : MicrogridState):
        self.state : MicrogridState = state
        self.metrics = MicrogridMetrics()

    def update_state(self, action, **kwargs):
        self.state.update(action, **kwargs)

    @abstractmethod
    def simulate(self):
        pass
    
    
###
### Building Microgrid
###

class MicrogridDayMetrics(MicrogridMetrics):

    step_demand : np.ndarray = np.zeros(DAY_LENGTH)
    total_demand : np.ndarray = np.zeros(DAY_LENGTH)
    reward : float = 0.0
    
    def update(self, prosumer_day_metrics_list : list[ProsumerDayMetrics]):
        self.step_demand = np.zeros(DAY_LENGTH)
        self.reward = 0.0
        for prosumer_day_metrics in prosumer_day_metrics_list:
            self.step_demand+=prosumer_day_metrics.step_demand
            self.reward+=prosumer_day_metrics.reward
        self.total_demand+=self.step_demand

class BuildingMicrogrid(Microgrid):
    '''
    Microgrid with prosumers that are only part of this micogrid
    '''

    def __init__(self, state : MicrogridState):
        self.state : MicrogridState = state
        self.metrics = MicrogridDayMetrics()
        
    @classmethod
    def default(cls, prosumer_list : list[Prosumer]) -> "BuildingMicrogrid":
        return cls(MicrogridState(prosumers=prosumer_list))
    
    def simulate(self):
        prosumer_day_metrics_list : list[ProsumerDayMetrics] = []
        for prosumer in self.state.prosumers:
            prosumer.simulate()
            prosumer_day_metrics_list.append(prosumer.metrics)
        self.metrics.update(prosumer_day_metrics_list)
        

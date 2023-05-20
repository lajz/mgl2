from abc import ABC, abstractmethod
from mgl2.prosumer.prosumer import Prosumer
from mgl2.microgrid.microgrid import Microgrid, MicrogridMetrics

from pydantic import BaseModel

class EnvironmentState(BaseModel):
    
    def update_props(self, action):
        pass
    
    def update(self, action, **kwargs):
        self.update_props(action)
        
    class Config:
        arbitrary_types_allowed = True
        
class SingleMicrogridEState(EnvironmentState):

    microgrid : Microgrid = []
    
    def update(self, action : dict):
        self.microgrid.update_state(action)
            
            
class MultiMicrogridEState(EnvironmentState):

    microgrids : list[Microgrid] = []
    
    def update(self, action : dict, **kwargs):
        for microgrid in self.microgrids:
            microgrid.update_state(action,  **kwargs)
        self.update_props(action)
        
    
class EnvironmentMetrics(BaseModel):
    
    def update(self, microgrid_metrics):
        pass

class Environment(ABC):
    
    def __init__(self, state : EnvironmentState, **kwargs):
        self.state : EnvironmentState = state
        self.metrics = EnvironmentMetrics()
    
    def update_state(self, action, **kwargs):
        self.state.update(action, **kwargs)
    
    @abstractmethod
    def simulate(self) -> EnvironmentMetrics:
        pass
    
    def step(self, action) -> EnvironmentMetrics:
        self.update_state(action)
        self.simulate()
        return self.metrics
    
class SingleMicrogridE(Environment):
    
    def __init__(self, state : SingleMicrogridEState, **kwargs):
        self.state : SingleMicrogridEState = state
        self.metrics = EnvironmentMetrics()
    
    @classmethod
    def default(cls, microgrid : Microgrid) -> "SingleMicrogridE":
        return cls(SingleMicrogridEState(microgrid=microgrid))
    
    def simulate(self) -> EnvironmentMetrics:
        self.state.microgrid.simulate()
    


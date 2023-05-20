from abc import ABC, abstractmethod
from mgl2.prosumer.prosumer import Prosumer
from mgl2.microgrid.microgrid import Microgrid, MicrogridMetrics

from pydantic import BaseModel


'''
STATES
'''
class EnvironmentState(BaseModel):
    
    '''
    Base Environment state all other environment states should inheiret from this class.
    
    The environment state holds all state information for an environment, such as any microgrids or prosumers.
    '''

    def update_props(self, action):
        '''
        Update properties of environment based on ACTION
        
        If any classes inheiret from Enviuronment state they should probably implement this function. 
        '''
        pass
    
    def update_sub_states(self, action, **kwargs):
        '''
        Update state of sub objects such as microgrids, passing ACTION and KWARGS. 
        Must ensure that each microgrid and prosumer only has update state called once per step.
        '''
        pass
    
    def update(self, action, **kwargs):
        '''
        Update state based on ACTION.
        May also pass in KWARGS as supplemental information.
        '''
        self.update_sub_states(action, **kwargs)
        self.update_props(action)
        
    class Config:
        '''Config class for pydantic.'''
        arbitrary_types_allowed = True
        
class SingleMicrogridEState(EnvironmentState):
    '''
    Environement state for environement with a single microgrid.
    '''
    microgrid : Microgrid = []
    
    def update_sub_states(self, action : dict, **kwargs):
        self.microgrid.update_state(action, kwargs)
            
            
class MultiMicrogridEState(EnvironmentState):
    '''
    Environement state for environement with multiple microgrids.
    '''
    microgrids : list[Microgrid] = []
    
    def update_sub_states(self, action : dict, **kwargs):
        for microgrid in self.microgrids:
            microgrid.update_state(action,  **kwargs)        

'''
Metrics
'''
class EnvironmentMetrics(BaseModel):
    '''
    Environement Metrics object to hold results from a step such as reward and demand.
    '''
    
    def update(self, **kwargs):
        '''Update metrics based on KWARGS.'''
        pass
    

class SingleMicrogridEMetrics(EnvironmentMetrics):
    '''
    Environement metrics object to hold results for a single microgrid.
    '''
    
    microgrid_metrics : MicrogridMetrics
    
    def update(self, **kwargs):
        assert "microgrid_metrics" in kwargs
        
        self.microgrid_metrics = kwargs["microgrid_metrics"]
        
'''
ENVIRONMENTS
'''
class Environment(ABC):
    '''
    Environment abstraction may hold multiple microgrids and prosumers.
    Responsible for updating and simulating contained microgrids and prosumers based on action.
    '''
    def __init__(self, state : EnvironmentState, **kwargs):
        '''Initialize environment'''
        self.state : EnvironmentState = state
        self.metrics = EnvironmentMetrics()
    
    def update_state(self, action, **kwargs):
        '''Helper function for updating environment state'''
        self.state.update(action, **kwargs)
    
    @abstractmethod
    def simulate(self) -> EnvironmentMetrics:
        '''Simulate a single time step of environment'''
        pass
    
    def step(self, action) -> EnvironmentMetrics:
        '''Update the state and then simulate a single time step of environment'''
        self.update_state(action)
        self.simulate()
        return self.metrics
    
class SingleMicrogridE(Environment):
    
    def __init__(self, state : SingleMicrogridEState, **kwargs):
        self.state : SingleMicrogridEState = state
        self.metrics = SingleMicrogridEMetrics()
    
    @classmethod
    def default(cls, microgrid : Microgrid) -> "SingleMicrogridE":
        '''Create default version of environment'''
        return cls(SingleMicrogridEState(microgrid=microgrid))
    
    def simulate(self) -> SingleMicrogridEMetrics:
        self.state.microgrid.simulate()
    


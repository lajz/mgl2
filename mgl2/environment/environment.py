from abc import ABC, abstractmethod
from mgl2.prosumer.prosumer import Prosumer
from mgl2.microgrid.microgrid import Microgrid, MicrogridMetrics

from pydantic import BaseModel


class EnvironmentState(BaseModel):

    def update(self, action):
        pass
    
class EnvironmentMetrics(BaseModel):
    microgrid_metrics : MicrogridMetrics = MicrogridMetrics()
    
    def update(self, microgrid_metrics):
        self.microgrid_metrics = microgrid_metrics

class Environment(ABC):
    
    def __init__(self, state : EnvironmentState, **kwargs):
        self.state : EnvironmentState = state
        self.metrics = EnvironmentMetrics()

    @abstractmethod
    def update_state(self, action):
        pass
    
    @abstractmethod
    def simulate(self) -> EnvironmentMetrics:
        pass

    def step(self, action) -> EnvironmentMetrics:
        self.update_state(action)
        self.simulate()
        return self.metrics

###
### Single Microgrid Environment
###

# TODO: metrics

class SingleMircogridE(Environment):
    '''
    Single Microgrid Environment
    
    An environment containing a single microgrid
    '''

    def __init__(self, state : EnvironmentState, microgrid : Microgrid):
        super().__init__(state)
        self.microgrid = microgrid

    def update_state(self, action):
        self.state.update(action)
        self.microgrid.update_state(action)

    def simulate(self) ->  EnvironmentMetrics:
        self.microgrid.simulate()
        self.metrics.update(self.microgrid.metrics)
        return self.metrics
        

###
### Many Microgrid Environment
###

# TODO: metrics

class ManyMircogridE(Environment):
    '''
    Many Microgrid Environment
    
    An environment containing many microgrids that do not share prosumers.
    '''

    def __init__(self, state : EnvironmentState, microgrids : list[Microgrid]):
        super().__init__(state)
        self.microgrids = microgrids

    def update_state(self, action):
        self.state.update(action)
        for microgrid in self.microgrids:
            microgrid.update_state(action)

    def simulate(self):
        microgrid_metrics_list: list[MicrogridMetrics] = []
        for microgrid in self.microgrids:
            microgrid_metrics = microgrid.simulate()
            microgrid_metrics_list.append(microgrid_metrics)
        self.metrics.update(microgrid_metrics_list)


class ManyMircogridSharedProsumerE(Environment):
    '''
    Many Microgrid Environment with shared prosumers
    
    An environment containing many microgrids that do not share prosumers.
    '''

    def __init__(self, state : EnvironmentState, microgrids : list[Microgrid], prosumers : list[Prosumer]):
        super().__init__(state)
        self.microgrids = microgrids
        self.prosumers = prosumers

    def update_state(self, action):
        self.state.update(action)
        for microgrid in self.microgrids:
            microgrid.update_state(action)
        for prosumer in self.prosumers:
            prosumer.update_state(action)

    def simulate(self):
        microgrid_metrics_list: list[MicrogridMetrics] = []
        for prosumer in self.prosumers:
            prosumer.simulate()
        for microgrid in self.microgrids:
            microgrid.simulate()
            microgrid_metrics_list.append(microgrid.metrics)
        self.metrics.update(microgrid_metrics_list)

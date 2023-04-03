from mgl2.Prosumer.Prosumer import RLProsumer, RLProsumerState
import numpy as np

#### TESTY ####
initial_energy_demand = np.array([10, 12, 8, 11, 9, 14, 13], dtype=np.float64)

rl_prosumer_state = RLProsumerState(energy_demand=initial_energy_demand)
demand_array = np.array([10, 11, 9, 12, 10, 13, 12], dtype=np.float64)

rl_prosumer = RLProsumer(state=rl_prosumer_state, demand=demand_array)
action_array = np.array([-1, 2, -2, 1, 0, -1, 1],  dtype=np.float64)
simulation_result = rl_prosumer.simulate(action=action_array)

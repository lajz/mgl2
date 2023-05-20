from mgl2.prosumer.lp_prosumer import LPProsumer, LPProsumerState
import numpy as np

# Create an energy demand array
initial_energy_demand = np.array([10, 12, 8, 11, 9, 14, 13], dtype=np.float64)

# Create a demand array
demand_array = np.array([10, 11, 9, 12, 10, 13, 12], dtype=np.float64)
 
# Create an energy price array
energy_price_array = np.array([0.15, 0.14, 0.16, 0.15, 0.17, 0.15, 0.14], dtype=np.float64)
 
def test_LPProsumer():
	
	# Instantiate an LPProsumerState object
	lp_prosumer_state = LPProsumerState(energy_demand=initial_energy_demand)

	# Instantiate an LPProsumer object
	lp_prosumer = LPProsumer(state=lp_prosumer_state, demand=demand_array, energy_price=energy_price_array)

	# Optimize the energy cost
	optimization_result = lp_prosumer.simulate()

	# Print the result of the optimization
	print(optimization_result)

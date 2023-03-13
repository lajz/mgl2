"""Main module."""


"""
action -> numpy vector + action descriptor
hour 0 to 23 buy prices (mg buys from grid)
hour 0 to 23 sale prices (mg sells to prosumer)

step(action, action_descriptor)
- descriptor can specify how env should interpret the action vector
    - (entry start, entry end, buy-prices, (prosumer, microgrid, environment) -> which states are affected by this part of the action)

- update state
- simulate
    - on state dictionary general {demand, storage, prices}
    - propagates simulate to prosumer


state dictionary for microgrid and prosumer
- within microgrid class




simulate (Microgrid, Prosumer)
- takes state at time t and runs for one time step





"""

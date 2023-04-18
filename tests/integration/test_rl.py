import gymnasium as gym
import ray
import numpy as np
from ray.rllib.algorithms import ppo

import sys
sys.path.append('./')

from mgl2.environment.environment import SingleMircogridE, EnvironmentState
from mgl2.microgrid.microgrid import BuildingMicrogrid, MicrogridState
from mgl2.prosumer.RLProsumer import RLProsumer, RLProsumerState
from mgl2.utils.constants import DAY_LENGTH

class MyEnv(gym.Env): # gym.wrapper
    def __init__(self, env_config):
        prosumer_list = [RLProsumer(RLProsumerState()), RLProsumer(RLProsumerState())]
        building_microgrid = BuildingMicrogrid(MicrogridState(), prosumer_list)
        self.environment = SingleMircogridE(EnvironmentState(), building_microgrid)
        
        self.action_space = gym.spaces.Box(low=0.0, high=10.0, shape=(DAY_LENGTH,), dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=-20.0, high=20.0, shape=(DAY_LENGTH,), dtype=np.float32)
    
    def reset(self):
        return np.zeros(DAY_LENGTH)
    
    def step(self, action):
        metrics = self.environment.step(action)
        obs = metrics.microgrid_metrics.step_demand
        return obs,  metrics.microgrid_metrics.reward, True, {}
        # return <obs>, <reward: float>, <done: bool>, <info: dict>

ray.init()
algo = ppo.PPO(env=MyEnv, config={
    "env_config": {},  # config to pass to env class
})

step = 0
while True:
    
    result = algo.train()
    print(step, result['episode_reward_max'], result['episode_reward_mean'])
        
    if result['episode_reward_mean'] > -1:
        break
    
    step+=1

print(f"{step} steps required to train.")
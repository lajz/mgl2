import gymnasium as gym
import ray
import numpy as np
from ray.rllib.algorithms import ppo

import sys
sys.path.append('./')

from mgl2.environment.environment import SingleMicrogridE, SingleMicrogridEState
from mgl2.microgrid.microgrid import BuildingMicrogrid
from mgl2.prosumer.vehicle_rl_prosumer import Vehicle
from mgl2.utils.constants import DAY_LENGTH

class MyEnv(gym.Env): # gym.wrapper
    def __init__(self, env_config):
        prosumer_list = [Vehicle.default() for _ in range(2)]
        building_microgrid = BuildingMicrogrid.default(prosumer_list)
        self.environment = SingleMicrogridE.default(building_microgrid)

        self.action_space = gym.spaces.Box(low=-5.0, high=5.0, shape=(DAY_LENGTH,), dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=-20.0, high=20.0, shape=(DAY_LENGTH,), dtype=np.float32)

    def reset(self):
        return np.zeros(DAY_LENGTH)

    def step(self, action):
        self.environment.step(action)
        metrics = self.environment.state.microgrid.metrics
        obs = metrics.step_demand
        return obs,  metrics.reward, True, {}
        # return <obs>, <reward: float>, <done: bool>, <info: dict>

def test_Vehicle2Grid():
    ray.init()
    algo = ppo.PPO(env=MyEnv, config={
        "env_config": {},  # config to pass to env class
    })

    step = 0
    while True:

        result = algo.train()
        print(step, result['episode_reward_max'], result['episode_reward_mean'])

        if result['episode_reward_mean'] > -10:
            break

        assert step < 50
        step+=1

    print(f"{step} steps required to train.")

if __name__ == "__main__":
    test_Vehicle2Grid()

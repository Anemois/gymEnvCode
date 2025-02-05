import sys
import numpy as np
import gymnasium as gym
import HSREnv

if __name__ == "__main__":
    #env = gymnasium.make("HSREnv-v1")
    gym.pprint_registry()
    env = gym.make('HSREnv-v2')
    obs, info = env.reset()
    for _ in range(1):
        action = env.action_space.sample()

        obs, rwd, term, trunc, info = env.step(action)
        env.render()
        if term or trunc:
            obs, info = env.reset()

env.close()
    
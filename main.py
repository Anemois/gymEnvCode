import sys
import numpy as np
import gymnasium as gym
import HSREnv
from HSREnv.envs.hsr import HSR

if __name__ == "__main__":
    #env = gymnasium.make("HSREnv-v1")
    #way = input("What you wanna do robot/human")
    way = "robot"
    if(way == "robot"):
        gym.pprint_registry()
        env = gym.make('HSREnv-v2')
        obs, info = env.reset()
        for _ in range(1):
            while True:
                action = env.action_space.sample()

                obs, rwd, term, trunc, info = env.step(action)
                env.render()
                if term or trunc:
                    obs, info = env.reset()
                    break
                
    elif(way == "human"):
        game = HSR()
        while True:
            game.view("human")
    
    env.close()
    
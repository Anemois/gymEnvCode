import sys
import numpy as np
import gymnasium as gym
import HSREnv
import time
import pygame
from HSREnv.envs.hsr import HSR
from HSREnv.envs.environment import Environment

from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.env_util import make_vec_env

if __name__ == "__main__":
    #env = gymnasium.make("HSREnv-v1")
    #way = input("What you wanna do robot/human")
    way = "human"
    if(way == "robot"):
        print("im in")
        env = gym.make("HSREnv-v2", render_mode = "robot", charNames = ["Robin", "Adventurine", "Feixiao", "March7"])
        check_env(env)
        print("starting to learn")
        model = PPO("MultiInputPolicy", env, verbose=1)
        model.learn(total_timesteps=25000)
        model.save("HSREnv-v2")

        del model # remove to demonstrate saving and loading

    elif(way == "test"):
        env = gym.make("HSREnv-v2", render_mode = "display", charNames = ["Robin", "Adventurine", "Feixiao", "March7"])
        model = PPO.load("HSREnv-v2", env=env)

        vec_env = model.get_env()
        obs = vec_env.reset()
        print("im in")
        while True:
            action, _states = model.predict(obs)
            obs, rewards, dones, info = vec_env.step(action)
            vec_env.render()
            time.sleep(1)
            print("hi", dones)
            if(dones[0]):
                print("NEWWWW")
                obs = vec_env.reset()

    elif(way == "human"):
        env = gym.make("HSREnv-v2", render_mode = "human", charNames = ["Robin", "Adventurine", "Feixiao", "March7"])
        env.reset()
        #game = HSR(render_mode = "human", charNames = ["Robin", "Adventurine", "Feixiao", "March7"])
        while True:
            #game.view()
            env.render()
         
import sys
import numpy as np
import gymnasium as gym
import HSREnv
from HSREnv.envs.hsr import HSR
from HSREnv.envs.environment import Environment

from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.env_util import make_vec_env

if __name__ == "__main__":
    #env = gymnasium.make("HSREnv-v1")
    #way = input("What you wanna do robot/human")
    way = "robot"
    if(way == "robot"):
        print("im in")
        env = gym.make("HSREnv-v2", render_mode = "robot", charNames = ["Robin", "Adventurine", "Feixiao", "March7"])
        check_env(env)
        print("starting to learn")
        model = PPO("MultiInputPolicy", env, verbose=1)
        model.learn(total_timesteps=25000)
        model.save("HSREnv-v2")

        del model # remove to demonstrate saving and loading

        model = PPO.load("HSREnv-v2")

        obs = env.reset()
        while True:
            action, _states = model.predict(obs)
            obs, rewards, dones, info = env.step(action)
            env.render()
                
    elif(way == "human"):
        game = HSR()
        while True:
            game.view("human")
        
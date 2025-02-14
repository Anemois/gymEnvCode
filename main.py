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
from stable_baselines3.common.evaluation import evaluate_policy

if __name__ == "__main__":
    #env = gymnasium.make("HSREnv-v1")
    #way = input("What you wanna do robot/human")
    way = "test"
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
        env = gym.make("HSREnv-v2", render_mode = "rgb_array", charNames = ["Robin", "Adventurine", "Feixiao", "March7"])
        model = PPO.load(path="HSREnv-v2", env=env)

        vec_env = model.get_env()
        print(type(vec_env))
        obs = vec_env.reset()
        mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
        print("im in", mean_reward, std_reward)
        while True:
            action, _states = model.predict(obs)
            #print(vec_env.render(mode='rgb_array'))
            obs, rewards, dones, info = vec_env.step(action)
            time.sleep(1)
            print("hi", dones, info)
            if(dones[0]):
                print("NEWWWW")
                obs = vec_env.close()

    elif(way == "human"):
        env = gym.make("HSREnv-v2", render_mode = "human", charNames = ["Robin", "Adventurine", "Feixiao", "March7"])
        env.reset()
        #game = HSR(render_mode = "human", charNames = ["Robin", "Adventurine", "Feixiao", "March7"])
        while True:
            #game.view()
            env.render()
         
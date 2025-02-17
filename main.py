import sys
import numpy as np
import gymnasium as gym
import HSREnv
import time
import pygame
from HSREnv.envs.hsr import HSR
from HSREnv.envs.environment import Environment

from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.common.maskable.policies import MaskableMultiInputActorCriticPolicy
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
from sb3_contrib.common.maskable.utils import get_action_masks

def mask_fn(env: gym.Env) -> np.ndarray:
    env = env.unwrapped
    return env.validActionMask()

if __name__ == "__main__":
    #env = gymnasium.make("HSREnv-v1")
    #way = input("What you wanna do robot/human")
    way = "test"
    if(way == "robot"):
        print("im in")
        env = gym.make("HSREnv-v2", render_mode = "robot", charNames = ["Robin", "Adventurine", "Feixiao", "March7"])
        check_env(env)
        env = ActionMasker(env, mask_fn)
        print("starting to learn")
        model = MaskablePPO(MaskableMultiInputActorCriticPolicy, env, verbose=1, n_steps=200)
        model.learn(total_timesteps=50000)
        model.save("HSREnv-v2")

        del model # remove to demonstrate saving and loading

    elif(way == "test"):
        env = gym.make("HSREnv-v2", render_mode = "rgb_array", charNames = ["Robin", "Adventurine", "Feixiao", "March7"])
        model = MaskablePPO.load(path="HSREnv-v2", env=env)

        vec_env = model.get_env()
        print(type(vec_env)) 
        obs = vec_env.reset()
        #mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
        #print("im in", mean_reward, std_reward)
        while True:
            action, _states = model.predict(obs, action_masks=mask_fn(env))
            #print(vec_env.render(mode='rgb_array'))
            obs, rewards, dones, info = vec_env.step(action)
            time.sleep(1)
            print("hi", dones, info)
            if(dones[0]):
                print("NEWWWW")
                obs = vec_env.close()
                break
        print("itsOver")

    elif(way == "human"):
        env = gym.make("HSREnv-v2", render_mode = "human", charNames = ["Robin", "Adventurine", "Feixiao", "March7"])
        env.reset()
        #game = HSR(render_mode = "human", charNames = ["Robin", "Adventurine", "Feixiao", "March7"])
        while True:
            #game.view()
            env.render()
         
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from HSREnv.envs.hsr import HSR
class Environment(gym.Env):
    #metadata = {"render_modes": ["human", "robot"], 'render_fps': 4}
    def __init__(self):
        self.game = HSR()
        #action : [ult1, ult2, ult3, ult4, basic, skill]
        #target : []
        self.action_space = spaces.Dict({"action" : spaces.Discrete(6), "target" : spaces.Discrete(5)})
        #
        self.observation_space = spaces.Dict({"AllyUlts" : spaces.Discrete(4),
                                              "EnemyData": spaces.Discrete(40)})
    
    def reset(self, seed = 0, options = []):
        del self.game
        self.game = HSR(seed= seed)
        obs = self.game.observe()
        return obs, {}

    def step(self, action):
        self.game.action(action)
        obs = self.game.observe()
        reward = self.game.evaluate()
        termination = self.game.is_done()
        truncation = self.game.is_trunc()
        return obs, reward, truncation, termination, {}
    
    def render(self, mode="human"):
        self.game.view(mode= mode)
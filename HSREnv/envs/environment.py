import gymnasium
from gymnasium import spaces
import numpy as np
from HSREnv.envs.hsr import HSR

class Environment(gymnasium.Env):
    metadata = {"render_modes": ["human", "machine"], 'render_fps': 4}
    def __init__(self):
        self.game = HSR()
        self.action_space = spaces.Box()
        self.observation_space = spaces.Box()
    
    def reset(self):
        del self.game
        self.game = HSR
        obs = self.game.observe()
        return obs

    def step(self, action):
        self.game.action(action)
        obs = self.game.observe()
        reward = self.game.evaluate()
        termination = self.game.is_done()
        truncation = self.game.is_trunc()
        return obs, reward, truncation, termination, {}
    
    def render(self, mode="human"):
        self.game.view()
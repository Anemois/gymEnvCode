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
        self.observation_space = spaces.Dict({"AllyUlts" : spaces.MultiBinary(4),
                                              "EnemyHp": spaces.Box(low=0.0, high=1.0,shape=(5,), dtype=np.float64),
                                              "EnemyWeakness" : spaces.MultiBinary([5, 7]),
                                              "Elites" : spaces.MultiBinary(5)})
    
    def reset(self, seed = None, options = []):
        del self.game
        self.game = HSR(seed= seed)
        obs = self.game.observe()
        for i in obs:
            obs[i] = np.array(obs[i])
        return obs, {}

    def actionInterpreter(self, act):
        action = ["ultimate1", "ultimate2", "ultimate3", "ultimate4", "basic", "skill"]
        target = [0, 1, 2, 3, 4]
        return {"action" : action[act["action"]], "target" : target[act["target"]]}

    def step(self, action):
        self.game.action(self.actionInterpreter(action))
        obs = self.game.observe()
        reward = self.game.evaluate()
        termination = self.game.is_done()
        truncation = self.game.is_trunc()
        for i in obs:
            obs[i] = np.array(obs[i])
        return obs, reward, truncation, termination, {}
    
    def render(self, mode="robot"):
        self.game.view(mode= mode)
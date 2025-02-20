import gymnasium
from gymnasium import spaces
import numpy as np
from HSREnv.envs.hsr import HSR
from typing import Optional
class Environment(gymnasium.Env):
    metadata = {"render_modes": ["human", "robot", "rgb_array"], 'render_fps': 10}
    def __init__(self, render_mode: Optional[str] = None, seed = None, charNames = ["Feixiao", "Adventurine", "Robin", "March7"], enemyData = {"waves" : 3, "basicEnemy" : 4, "eliteEnemy" : 1, "basicData" : ["random", "random", "random", "random"], "eliteData" : ["random"]}):
        super(Environment, self).__init__()
        self.kwargs = (render_mode, seed, charNames, enemyData)
        self.game = HSR(render_mode=render_mode, seed=seed, charNames=charNames, enemyData=enemyData)
        #action : [ult1, ult2, ult3, ult4, basic, skill]
        #target : []
        self.action_space = spaces.MultiDiscrete([6,5])
        #
        self.observation_space = spaces.Dict({"AllyUlts" : spaces.MultiBinary(4),
                                              "EnemyHp": spaces.Box(low=0.0, high=1.0,shape=(5,), dtype=np.float64),
                                              "EnemyWeakness" : spaces.MultiBinary([5, 7]),
                                              "Elites" : spaces.MultiBinary(5),
                                              "ActionOrder" : spaces.MultiDiscrete([6, 6]),
                                              "SkillPoints" : spaces.Discrete(7)})

    def reset(self, seed = None, options = []):
        del self.game
        self.game = HSR(render_mode=self.kwargs[0], seed=self.kwargs[1], charNames=self.kwargs[2], enemyData=self.kwargs[3])
        obs = self.getObs()
        for i in obs:
            if(type(obs[i]) == int):
                pass
            elif(i == "EnemyHp" or i == "ActionOrder"):
                obs[i] = np.array(obs[i])
            else:
                obs[i] = np.array(obs[i], dtype = bool)
        return obs, {}

    def getObs(self):
        return self.game.observe()

    def getInfo(self):
        return self.game.getInfo()
    
    def validActionMask(self):
        mask = [[0,0,0,0,1,0],[1,1,1,1,1]]
        obs = self.getObs()
        for i in range(4):
            mask[0][i] = obs["AllyUlts"][i]
        flattenMask = []
        for i in mask:
            for j in i:
                flattenMask.append(j)

        mask[5] = obs["SkillPoints"] > 0

        return flattenMask

    def actionInterpreter(self, act):
        action = ["ultimate1", "ultimate2", "ultimate3", "ultimate4", "basic", "skill"]
        target = [0, 1, 2, 3, 4]
        return {"action" : action[act[0]], "target" : target[act[1]]}

    def step(self, action):
        self.game.action(self.actionInterpreter(action))
        obs = self.getObs()
        reward = self.game.evaluate()
        termination = self.game.is_done()
        truncation = self.game.is_trunc()
        for i in obs:
            if(i == "EnemyHp" or i == "ActionOrder"):
                obs[i] = np.array(obs[i])
            else:
                obs[i] = np.array(obs[i], dtype = bool)
        
        if self.render_mode == "human" or "rgb_array":
            self.render()

        info = self.getInfo()
        info["Action Taken"] = self.actionInterpreter(action)

        return obs, reward, truncation, termination, info
    
    def render(self):
        self.game.view()

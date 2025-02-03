import random
from datetime import datetime
from HSREnv.envs.HSRCharacters.Allies._allyTemplate import AllyTemplate

class Adventurine(AllyTemplate):
    def __init__(self, hp= 3098, atk= 1441, defence= 3976, spd= 113, critRate= 0.435, critDamage= 1.895, energyRegenRate= 1):
        super().__init__(hp, atk, defence, spd, critRate, critDamage)

        self.critRate = critRate + min(max(0, (self.getDefence() - 1600) // 100 * 0.02), 0.48)

        self.name = "Adventurine"
        self.energy = 0
        self.energyCost = 110
        self.energyMax = 110
        self.energyRegenRate = energyRegenRate
        self.blindBet = 0

        random.seed(datetime.now().timestamp())

    def addBlindBet(self, x):
        self.blindBet = min(9, self.blindBet + x)

    def basic(self):
        self.addEnergy(20)
        actionData = {
            "char": "Adventurine",
            "action": "basic",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getDefence(),
            "element": ["imaginary"],
            "break": 10,
            "effects": {}
        }
        self.actionSignal(actionData)    

    def skill(self):
        self.addEnergy(30)
        actionData = {
            "char": "Adventurine",
            "action": "skill",
            "actionType": "shield",
            "target": "Ally",
            "hitType": "all",
            "hits": 1,
            "base": self.getDefence() * 0.24 + 320,
            "element": ["none"],
            "break": 0,
            "effects": {}
        }
        self.actionSignal(actionData)    

    def ultimate(self):
        self.addEnergy(-self.energyCost)
        self.addEnergy(5)
        self.addBlindBet(random.randint(1, 7))

        actionData = {
            "char": "Adventurine",
            "action": "ultimate",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getDefence() * 2.7,
            "element": ["imaginary"],
            "break": 30,
            "effects": [{"name": "AdventurineUltimateDebuff",
                             "type" : "critDamageDebuff",
                             "base" : 0.15,
                             "turnCount" : 3,
                             "maxStack" : 1,
                             "stack" : 1,
                             "deleteOthers" : False,
                             "on/off" : "on"}]
        }
        self.actionSignal(actionData)    

    def talent(self):
        self.addEnergy(7)
        actionData = {
            "char": "Adventurine",
            "action": "talent",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "bounce",
            "hits": 7,
            "base": self.getDefence() * 0.25,
            "element": ["imaginary"],
            "break": 3,
            "effects": {}
        }
        self.actionSignal(actionData)    

    def actionDetect(self, actionType, actionChar):
        if actionType == "hit":
            self.addBlindBet(1)
        if actionChar == "Adventurine":
            self.addBlindBet(1)

        if self.blindBet >= 7:
            self.blindBet -= 7
            self.addAction(["Adventurine", "talent", -1])
import random
from datetime import datetime
from HSREnv.envs.HSRCharacters.Allies._allyTemplate import AllyTemplate

class Feixiao(AllyTemplate):
    def __init__(self, hp= 3311, atk= 2603, defence= 1331, spd= 142, critRate= 82.7, critDamage= 2.40, energyRegenRate= 1):
        super().__init__(hp, atk, defence, spd, critRate, critDamage)

        self.dmgBuff = 1.6

        self.name = "Feixiao"
        self.energy = 3
        self.energyCost = 6
        self.energyMax = 13
        self.energyRegenRate = 1

        self.followUp = False

    def basic(self):    
        self.followUp = True
        actionData = {
            "char": "Feixiao",
            "action": "basic",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 1,
            "element": ["wind"],
            "break": 10,
            "effects": {}
        }
        self.actionSignal(actionData)
    
    def skill(self):
        self.followUp = True
        actionData = {
            "char": "Feixiao",
            "action": "skill",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 2,
            "element": ["wind"],
            "break": 20,
            "effects": {}
        }    
        self.actionSignal(actionData)    
        self.addAction(["Feixiao", "talent", -1])

    def ultimate(self):
        self.addEnergy(-self.energyCost)
        actionData = {
            "char": "Feixiao",
            "action": "ultimate",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 7,
            "element": ["wind"],
            "break": 60,
            "effects": {}
        }
        self.actionSignal(actionData)

    def talent(self):
        actionData = {
            "char": "Feixiao",
            "action": "talent",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 1.1,
            "element": ["wind"],
            "break": 5,
            "effects": {}
        }
        self.actionSignal(actionData) 
    
    def grep(self, grep):
        data = {
            "basic" : {"target" : "Enemy", "hitType" : "single"},
            "skill" : {"target" : "Enemy", "hitType" : "single"},
            "ultimate" : {"target" : "Enemy", "hitType" : "single"}
        }
        return data[grep]

    def actionDetect(self, actionType, actionChar):
        if(actionType == "atk" and actionChar != "Enemy"):
            self.addEnergy(0.5)
            #print("ADDD", self.energy, actionChar)
            if(self.followUp and actionChar != "Feixiao"):
                self.followUp = False
                self.addAction(["Feixiao", "talent", -1])

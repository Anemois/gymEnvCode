import random
from datetime import datetime
from HSREnv.envs.HSRCharacters.Allies._allyTemplate import AllyTemplate

class Robin(AllyTemplate):
    def __init__(self, hp= 4313, atk= 3864, defence= 986, spd= 115, critRate= 0.079, critDamage= 1.733, energyRegenRate= 1.19):
        super().__init__(hp, atk, defence, spd, critRate, critDamage)

        self.energy = 0
        self.energyCost = 160
        self.energyMax = 160
        self.energyRegenRate = energyRegenRate
        self.countdown = 0
        self.singing = False
        
    def basic(self):
        self.countdown -= 1
        if self.countdown <= 0:
            actionData = {
                "char": "Robin",
                "action": "skill",
                "actionType": "buffEnd",
                "target": "Ally",
                "hitType": "all",
                "hits": 1,
                "base": 0,
                "element": ["none"],
                "break": 0,
                "effects": {"RobinSkill": ["dmgBuff", 0.5, 1, -1]}
            }
            self.actionSignal(actionData)

        self.addEnergy(20)
        actionData = {
            "char": "Robin",
            "action": "basic",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 1,
            "element": ["physical"],
            "break": 10,
            "effects": {}
        }
        self.actionSignal(actionData)

    def skill(self):
        self.countdown = 3
        self.addEnergy(30)
        actionData = {
            "char": "Robin",
            "action": "skill",
            "actionType": "buff",
            "target": "Ally",
            "hitType": "all",
            "hits": 1,
            "base": 0,
            "element": ["none"],
            "break": 0,
            "effects": {"RobinSkill": ["dmgBuff", 0.5, 1, 1]}
        }
        self.actionSignal(actionData)

    def ultimate(self):
        self.energy = 5
        self.singing = True
        actionData = {
            "char": "Robin",
            "action": "ultimate",
            "actionType": "buff",
            "target": "Ally",
            "hitType": "all",
            "hits": 1,
            "base": 0,
            "element": ["none"],
            "break": 0,
            "effects": {"RobinUltBuff": ["atkBuff", 0.3, 1, 1], "RobinUltAtk": ["followAtk", self.getAttack() * 1.2, 1, 1]}
        }
        self.actionSignal(actionData)

    def actionDetect(self, actionType, actionChar):
        if actionType == "atk":
            self.addCharge(2)

        if actionType == "start":
            actionData = {
                "char": "Robin",
                "action": "skill",
                "actionType": "buff",
                "target": "Ally",
                "hitType": "all",
                "hits": 1,
                "base": 0,
                "element": ["none"],
                "break": 0,
                "effects": {"RobinTalent": ["critDamage", 0.2, 1, 1]}
            }
            self.actionSignal(actionData)

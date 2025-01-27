import random
from datetime import datetime
from HSREnv.envs.hsr import actionSignal, addAction

class Robin():
    def __init__(self, hp=4313, atk=3864, defence=986, spd=115, critRate=0.079, critDamage=1.733):
        self.buffs = []
        self.hp = hp
        self.atk = atk
        self.defence = defence
        self.spd = spd
        self.critRate = critRate
        self.critDamage = critDamage
        self.atkBuff = 1
        self.defBuff = 1
        self.dmgBuff = 1
        self.speedBuff = 1
        self.actionValue = 10000 / self.spd

        self.countdown = 0
        self.singing = False
        self.energy = 0
        self.energyCost = 160
        self.energyRegenRate = 1.19

        random.seed(datetime.now().timestamp() + 1)

        self.updates = []

    def addEnergy(self, x):
        self.energy = min(self.energyCost, self.energy + x * self.energyRegenRate)

    def addCharge(self, x):
        self.charge = min(10, self.charge + 1)

    def getDefence(self):
        return self.defence * self.defBuff

    def getAttack(self):
        return self.atk * self.atkBuff

    def getSpeed(self):
        return 90 if self.singing else self.spd * self.speedBuff
    
    def addAction(self, dict):
        self.updates.append(["addAction", dict])
    
    def actionSignal(self, dict):
        self.updates.append(["actionSignal", dict])
        
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
            "element": "physical",
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
            "effects": {"RobinUltBuff": ["atkBuff", 0.3, 1, 1], "RobinUltAtk": ["followAtk", self.getAttack() * 1.2, 1, 1]}
        }
        self.actionSignal(actionData)

    def checkUltimate(self):
        return self.energy >= self.energyCost

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
                "effects": {"RobinTalent": ["critDamage", 0.2, 1, 1]}
            }
            self.actionSignal(actionData)

import random
from datetime import datetime

class Adventurine():
    def __init__(self, hp = 3098, atk = 1441, defence = 3976, spd = 113, critRate = 0.435, critDamage = 1.895):
        self.buffs = []
        self.hp = hp
        self.atk = atk
        self.defence = defence
        self.spd = spd
        self.critRate = critRate + min(max(0, (self.getDefence() - 1600) // 100 * 0.02), 0.48)
        self.critDamage = critDamage
        self.atkBuff = 1
        self.defBuff = 1
        self.dmgBuff = 1
        self.speedBuff = 1
        self.actionValue = 10000 / self.spd

        self.energy = 0
        self.energyCost = 110
        self.blindBet = 0
        random.seed(datetime.now().timestamp())

        self.updates = []

    def addEnergy(self, x):
        self.energy = min(self.energyCost, self.energy + x)

    def addBlindBet(self, x):
        self.blindBet = min(9, self.blindBet + x)

    def getDefence(self):
        return self.defence * self.defBuff

    def getAttack(self):
        return self.atk * self.atkBuff

    def getSpeed(self):
        return self.spd * self.speedBuff

    def addAction(self, dict):
        self.updates.append(["addAction", dict])
    
    def actionSignal(self, dict):
        self.updates.append(["actionSignal", dict])
        
    def basic(self):
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
        self.energy = 5
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
            "effects": {"critDamageDebuff": 0.15}
        }
        self.actionSignal(actionData)    

    def checkUltimate(self):
        return self.energy >= self.energyCost

    def talent(self):
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

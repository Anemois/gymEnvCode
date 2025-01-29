import random
from datetime import datetime

class AllyTemplate():
    def __init__(self, hp = 100, atk = 100, defence = 100, spd = 100, critRate = 0.1, critDamage = 1.5):
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

        self.energy = 0
        self.energyCost = 100
        self.energyMax = 100
        self.energyRegenRate = 1
        random.seed(datetime.now().timestamp())

        self.updates = []

    def addEnergy(self, x):
        self.energy = max(min(self.energyMax, self.energy + x), 0)
    
    def checkUltimate(self):
        return self.energy >= self.energyCost

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
        print("TIS EMPTY") 

    def skill(self):
        print("TIS EMPTY")  

    def ultimate(self):
        print("TIS EMPTY")

    def talent(self):
        print("TIS EMPTY")

    def actionDetect(self, actionType, actionChar):
        print("TIS EMPTY")

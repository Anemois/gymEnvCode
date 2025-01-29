import random
from datetime import datetime

class AllyTemplate():
    def __init__(self, hp   = 100, atk= 100, defence= 100, spd= 100, critRate= 0.1, critDamage= 1.5, lv= 80):
        self.buffs = {}
        self.lv = lv
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

        self.defIgnore = 0
        self.resPEN = 0

        random.seed(datetime.now().timestamp())

        self.updates = []

    def addEnergy(self, x):
        self.energy = max(min(self.energyMax, self.energy + x), 0)
    
    def checkUltimate(self):
        return self.energy >= self.energyCost

    def getDefence(self):
        defBuff = 0
        for buff in self.buffs:
            if(buff["type"] == "defBuff"):
                defBuff += buff["base"]
        return self.defence * (self.defBuff + defBuff)

    def getAttack(self):
        atkBuff = 0
        for buff in self.buffs:
            if(buff["type"] == "atkBuff"):
                atkBuff += buff["base"]
        return self.atk * (self.atkBuff + atkBuff)

    def getSpeed(self):
        spdBuff = 0
        for buff in self.buffs:
            if(buff["type"] == "spdBuff"):
                spdBuff += buff["base"]
        return self.spd * (self.speedBuff + spdBuff)
    
    def getCritRate(self):
        critRateBuff = 0
        for buff in self.buffs:
            if(buff["type"] == "critRateBuff"):
                critRateBuff += buff["base"]
        return (self.critRate + critRateBuff)
    
    def getCritDamage(self):
        critDamageBuff = 0
        for buff in self.buffs:
            if(buff["type"] == "critDamageBuff"):
                critDamageBuff += buff["base"]
        return (self.critDamage + critDamageBuff)

    def getDefIgnore(self):
        defIgnoreBuff = 0
        for buff in self.buffs:
            if(buff["type"] == "defIgnoreBuff"):
                defIgnoreBuff += buff["base"]
        return (self.defIgnore + defIgnoreBuff)

    def getResPEN(self):
        resPENBuff = 0
        for buff in self.buffs:
            if(buff["type"] == "resPENBuff"):
                resPENBuff += buff["base"]
        return (self.resPEN + resPENBuff)

    def getUpdate(self):
        if(len(self.updates) == 0):
            return "NULL"
        return self.updates.pop(0)

    def calcDefMultiplier(self, enemyDef):
        return 1 - (enemyDef / (enemyDef + 200 + 10 * self.lv))

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

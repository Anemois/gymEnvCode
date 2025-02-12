import random
from datetime import datetime

class BaseEnemy():
    def __init__(self, name="basic", hp=300000, atk=100, defence=200+10*90, spd=132, weakness = [], toughness = 20):
        self.buffs = {}
        self.debuffs = {}
        self.name = name
        self.hp = hp
        self.maxHp = hp
        self.atk = atk
        self.defence = defence
        self.spd = spd #[132, 158, 227]
        self.spdBuff = 1
        self.atkBuff = 1
        self.defBuff = 1
        self.dmgBuff = 1
        self.spdDebuff = 1
        self.atkDebuff = 1
        self.defDebuff = 1
        self.dmgDebuff = 1
        self.toughness = toughness
        self.maxToughness = toughness
        self.critDamageDebuff = 0
        self.critRateDebuff = 0
        self.actionValue = 10000 / self.spd

        self.weakness = weakness
        self.obsWeakness = []
        weaknesses = ["physical", "fire", "ice", "lightning", "wind", "quantum", "imaginary"]
        for i in range(7):
            self.obsWeakness.append(1 if weaknesses[i] in self.weakness else 0)

        self.moves = ["single", "blast"]
        self.moveptr = 0

        #random.seed(datetime.now().timestamp() + 1)

        self.updates = []

    def getDefence(self, defIgnore = 0):
        return max(0, self.defence * (self.defBuff - (self.defDebuff + defIgnore)))

    def getAttack(self):
        return self.atk * self.atkBuff

    def getSpeed(self):
        return self.spd * self.spdBuff
    
    def getRES(self, charType = [], resPEN = 0):
        return 1 - ((0 if charType in self.weakness else 0.20) - resPEN)

    def getDamageReduction(self):
        return 0.9 if self.toughness > 0 else 1

    def getWeakness(self):
        return self.obsWeakness

    def getCritRateDebuff(self):
        critRateDebuff = 0
        for debuff in self.debuffs:
            debuff = self.debuffs[debuff]
            if(debuff["type"] == "critRateDebuff"):
                critRateDebuff += debuff["base"]
        return (self.critRateDebuff + critRateDebuff)
    
    def getCritDamageDebuff(self):
        critDamageDebuff = 0
        for debuff in self.debuffs:
            debuff = self.debuffs[debuff]
            if(debuff["type"] == "critDamageDebuff"):
                critDamageDebuff += debuff["base"]
        return (self.critDamageDebuff + critDamageDebuff)

    def getUpdate(self):
        if(len(self.updates) == 0):
            return "NULL"
        return self.updates.pop(0)

    def calcActionValue(self):
        return 10000 / self.getSpeed()

    def addDebuffStack(self, effect):
        self.debuffs[effect]["stack"] = min(self.debuffs[effect]["stack"]+1, self.debuffs[effect]["maxStack"])

    def addAction(self, dict):
        self.updates.append(["addAction", dict])
    
    def actionSignal(self, dict):
        self.updates.append(["actionSignal", dict])
        
    def doAction(self):
        action = self.moves[self.moveptr]
        self.moveptr += 1
        if(self.moveptr == len(self.moves)):
            self.moveptr = 0
        return action

    def single(self):
        self.toughness = self.maxToughness
        actionData = {
            "char": "Enemy",
            "action": "basic",
            "actionType": "atk",
            "target": "Ally",
            "hitType": "single",
            "hits": 1,
            "base": 5,
            "element": ["none"],
            "break": 0,
            "effects": {}
        }
        self.actionSignal(actionData)

    def blast(self):
        self.toughness = self.maxToughness
        actionData = {
            "char": "Enemy",
            "action": "basic",
            "actionType": "atk",
            "target": "Ally",
            "hitType": "blast",
            "hits": 1,
            "base": [2, 4, 2],
            "element": ["none"],
            "break": [0, 0, 0],
            "effects": {}
        }
        self.actionSignal(actionData)

    def actionDetect(self, actionType, actionChar):
        pass

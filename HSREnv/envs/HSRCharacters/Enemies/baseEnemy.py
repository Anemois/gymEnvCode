import random
from datetime import datetime

class BaseEnemy():
    def __init__(self, hp=300000, atk=100, defence=200+10*90, spd=132, weakness = []):
        self.buffs = []
        self.hp = hp
        self.atk = atk
        self.defence = defence
        self.spd = spd #[132, 158, 227]
        self.atkBuff = 1
        self.defBuff = 1
        self.dmgBuff = 1
        self.critDamageDebuff = 0
        self.critRateDebuff = 0
        self.speedDebuff = 1
        self.actionValue = 10000 / self.spd

        self.weakness = weakness
        self.moves = ["signle", "blast", "single"]
        self.moveptr = 0

        random.seed(datetime.now().timestamp() + 1)

        self.updates = []

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
        
    def single(self):
        actionData = {
            "char": "Robin",
            "action": "basic",
            "actionType": "atk",
            "target": "Ally",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 1,
            "element": ["none"],
            "break": 0,
            "effects": {}
        }
        self.actionSignal(actionData)

    def blast(self):
        actionData = {
            "char": "Robin",
            "action": "basic",
            "actionType": "atk",
            "target": "Ally",
            "hitType": "blast",
            "hits": 1,
            "base": [self.getAttack() * 0.3, self.getAttack() * 0.5, self.getAttack() * 0.3],
            "element": ["none"],
            "break": 0,
            "effects": {}
        }
        self.actionSignal(actionData)

    def actionDetect(self, actionType, actionChar):
        pass

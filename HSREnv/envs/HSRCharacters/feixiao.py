
class Feixiao():
    def __init__(self, hp = 3311, atk = 2603, defence = 1331, spd = 142, critRate = 82.7, critDamage = 2.40):
        self.buffs = []
        self.atk = atk
        self.spd = spd 
        self.defence = defence
        self.atkBuff = 1
        self.dmgBuff = 1.6
        self.speedBuff = 1
        self.actionValue = 0
        self.critRate = critRate
        self.critDamage = critDamage

        self.energyRegenRate = 1
        self.aureus = 3
        self.followUp = False

        self.actionValue = 10000/self.spd

        self.updates = []

    def addAureus(self, x):
        self.aureus = min(13, self.aureus + x)
    
    def getDefence(self):
        return self.defence * self.defBuff

    def getAttack(self):
        return self.atk * self.atkBuff

    def getSpeed(self):
        return self.speed * self.speedBuff

    def addAction(self, dict):
        self.updates.append(["addAction", dict])
    
    def actionSignal(self, dict):
        self.updates.append(["actionSignal", dict])

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
            "effects": {}
        }
        self.actionSignal(actionData)

    def skill(self):
        self.followUp = True
        actionData = {
            "char": "Feixiao",
            "action": "basic",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 2,
            "effects": {}
        }    
        self.actionSignal(actionData)    
        self.addAction(["Feixiao", "talent", -1])

    def ultimate(self):
        self.aureus -= 6
        actionData = {
            "char": "Feixiao",
            "action": "basic",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 7,
            "effects": {}
        }
        self.actionSignal(actionData)    

    def checkUltimate(self):
        return self.aureus >= 6

    def talent(self):
        actionData = {
            "char": "Feixiao",
            "action": "basic",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 1.1,
            "effects": {}
        }
        self.actionSignal(actionData) 

    def actionDetect(self, actionType, actionChar):
        if(actionType == "atk"):
            self.addAureus(0.5)
            if(self.followUp and actionChar != "Feixiao"):
                self.followUp = False
                self.addAction(["Feixiao", "talent", -1])
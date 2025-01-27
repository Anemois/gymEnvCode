from HSREnv.envs.hsr import actionSignal, addAction

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

        self.actionValue = 10000/self.spd

    def addAureus(self, x):
        self.aureus = min(13, self.aureus + x)
    
    def getDefence(self):
        return self.defence * self.defBuff

    def getAttack(self):
        return self.atk * self.atkBuff

    def getSpeed(self):
        return self.speed * self.speedBuff

    def buffs(self, atk):
        return atk*self.atkBuff*self.dmgBuff

    def basic(self):    
        action_data = {
            "char": "Feixiao",
            "action": "basic",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 1,
            "effects": {}
        }
        return {
            "actionSignal": action_data,
            "addAction": "None"}

    def skill(self):
        action_data = {
            "char": "Feixiao",
            "action": "basic",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 2,
            "effects": {}
        }        
        return {
            "actionSignal": action_data,
            "addAction": ["Feixiao", "talent", -1]}

    def ultimate(self):
        self.aureus -= 6
        action_data = {
            "char": "Feixiao",
            "action": "basic",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 7,
            "effects": {}
        }
        
        return {"actionSignal": action_data,
                "addAction": "None"}

    def checkUltimate(self):
        return self.aureus >= 6

    def talent(self):
        action_data = {
            "char": "Feixiao",
            "action": "basic",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 1.1,
            "effects": {}
        }
        return {"actionSignal": action_data,
                "addAction" : "None"}

    def actionDetect(self, actionType, actionChar):
        if(actionType == "atk"):
            self.addAureus(0.5)
from HSREnv.envs.hsr import actionSignal, addAction

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

    def addEnergy(self, x):
        self.energy = min(self.energyCost, self.energy + x)

    def addBlindBet(self, x):
        self.blindBet = min(9, self.blindBet + 1)

    def getDefence(self):
        return self.defence * self.defBuff

    def getAttack(self):
        return self.atk * self.atkBuff

    def getSpeed(self):
        return self.spd * self.speedBuff

    def basic(self):
        action_data = {
            "char": "Adventurine",
            "action": "basic",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getDefence(),
            "effects": {}
        }
        return {
            "actionSignal": action_data,
            "addAction": "None"
        }

    def skill(self):
        action_data = {
            "char": "Adventurine",
            "action": "skill",
            "actionType": "shield",
            "target": "Ally",
            "hitType": "all",
            "hits": 1,
            "base": self.getDefence() * 0.24 + 320,
            "effects": {}
        }
        return {
            "actionSignal": action_data,
            "addAction": "None"
        }

    def ultimate(self):
        self.energy = 5
        action_data = {
            "char": "Adventurine",
            "action": "ultimate",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getDefence() * 2.7,
            "effects": {"critDamageDebuff": 0.15}
        }
        return {
            "actionSignal": action_data,
            "addAction": "None"
        }

    def checkUltimate(self):
        return self.energy >= self.energyCost

    def talent(self):
        action_data = {
            "char": "Adventurine",
            "action": "talent",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "bounce",
            "hits": 7,
            "base": self.getDefence() * 0.25,
            "effects": {}
        }
        return {
            "actionSignal": action_data,
            "addAction": "None"
        }

    def actionDetect(self, actionType, actionChar):
        if actionType == "hit":
            self.addBlindBet(1)
        if actionChar == "Adventurine":
            self.addBlindBet(1)

        if self.blindBet >= 7:
            self.blindBet -= 7
            return {"actionSignal": "None",
                    "addAction": ["Adventurine", "talent", -1]}

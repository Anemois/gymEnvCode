from HSREnv.envs.hsr import actionSignal, addAction
import random
from datetime import datetime

class March7():
    def __init__(self, hp = 2864, atk = 3222, defence = 908, spd = 115, critRate = 0.716, critDamage = 2.349):
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
        self.energyCost = 110
        self.enchanceBasic = False
        self.SUPERCHARGED = False
        self.charge = 0
        self.shifu = "None"
        self.followUpCharge = True

        random.seed(datetime.now().timestamp() + 1)

    def addEnergy(self, x):
        self.energy = min(self.energyCost, self.energy + x)

    def addCharge(self, x):
        self.charge = min(10, self.charge + 1)

    def getDefence(self):
        return self.defence * self.defBuff

    def getAttack(self):
        return self.atk * self.atkBuff

    def getSpeed(self):
        return self.spd * self.speedBuff

    def basic(self):
        self.followUpCharge = True
        if not self.enchanceBasic:
            self.addEnergy(25)
            self.addCharge(1)
            action_data = {
                "char": "March7",
                "action": "basic",
                "actionType": "atk",
                "target": "Enemy",
                "hitType": "single",
                "hits": 1,
                "base": self.getAttack() * 1,
                "effects": {"m7SwordPlay": 1}
            }
            return {
                "actionSignal": action_data,
                "addAction": "None"
            }
        else:
            self.addEnergy(35)
            actionSignal("March7", "atk")
            hits = 3 if self.SUPERCHARGED else 5
            for i in range(3):
                if (0.6 if self.SUPERCHARGED else 0.8) >= random.random():
                    hits += 1
            supercharge = self.SUPERCHARGED
            self.enchanceBasic = False
            self.SUPERCHARGED = False
            if supercharge:
                self.critDamage += 0.5
            action_data = {
                "char": "March7",
                "action": "basic",
                "actionType": "atk",
                "target": "Enemy",
                "hitType": "single",
                "hits": hits,
                "base": self.getAttack() * 0.8,
                "effects": {"m7SwordPlay": 1}
            }
            if supercharge:
                self.critDamage -= 0.5
            self.charge -= 7
            self.dmgBuff -= 0.8
            return {
                "actionSignal": action_data,
                "addAction": "None"
            }

    def skill(self):
        self.followUpCharge = True
        self.addEnergy(35)
        self.speedBuff += 0.1
        action_data = {
            "char": "March7",
            "action": "skill",
            "actionType": "buff",
            "target": "Ally",
            "hitType": "single",
            "hits": 1,
            "base": 0,
            "effects": {"March7Skill": ["speedBuff", 0.1, 1, 1], "notSelf": 1}
        }
        return {
            "actionSignal": action_data,
            "addAction": "None"
        }

    def ultimate(self):
        self.energy = 5
        self.SUPERCHARGED = True
        action_data = {
            "char": "March7",
            "action": "ultimate",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 2.4,
            "effects": {"m7SwordPlay": 1}
        }
        return {
            "actionSignal": action_data,
            "addAction": "None"
        }

    def checkUltimate(self):
        return self.energy >= self.energyCost

    def talent(self):
        self.addEnergy(5)
        self.addCharge(1)
        action_data = {
            "char": "March7",
            "action": "talent",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 0.6,
            "effects": {"m7SwordPlay": 1}
        }
        return {
            "actionSignal": action_data,
            "addAction": "None"
        }

    def actionDetect(self, actionType, actionChar):
        if actionType == "start":
            self.actionValue = max(0, self.actionValue - 10000 * 0.25)

        if actionType == "atk" and actionChar == self.shifu:
            self.addCharge(1)
            if self.followUpCharge:
                self.followUpCharge = False
                return {"actionSignal": "None",
                    "addAction": ["Adventurine", "talent", -1]}
                
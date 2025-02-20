import random
from datetime import datetime
from HSREnv.envs.HSRCharacters.Allies._allyTemplate import AllyTemplate

class March7(AllyTemplate):
    def __init__(self, hp= 2864, atk= 3222, defence= 908, spd= 115, critRate= 0.716, critDamage= 2.349, energyRegenRate= 1):
        super().__init__(hp, atk, defence, spd, critRate, critDamage)

        self.name = "March7"
        self.energy = 0
        self.energyCost = 110
        self.energyMax = 110
        self.energyRegenRate = energyRegenRate

        self.enchanceBasic = False
        self.SUPERCHARGED = False
        self.charge = 0
        self.shifu = "None"
        self.shifuType = "none"
        self.followUpCharge = True

        random.seed(datetime.now().timestamp())

    def addCharge(self, x):
        self.charge = min(10, self.charge + x)

    def checkCharge(self):
        if(self.charge >= 7):
            self.enchanceBasic = True

    def basic(self):
        self.followUpCharge = True
        if not self.enchanceBasic:
            self.addEnergy(25)
            self.addCharge(1)
            actionData = {
                "char": "March7",
                "action": "basic",
                "actionType": "atk",
                "target": "Enemy",
                "hitType": "single",
                "hits": 1,
                "base": self.getAttack() * 1,
                "element": ["imaginary", self.shifuType],
                "break": 10,
                "effects": [{"name": "m7SwordPlay",
                             "type" : "dmgDebuff",
                             "base" : 0.5,
                             "turnCount" : 1,
                             "maxStack" : 5,
                             "stack" : 1,
                             "deleteOthers" : True,
                             "on/off" : "on"}]
            }
            self.actionSignal(actionData)  
            self.checkCharge()
        else:
            self.addEnergy(35)
            hits = 3 if self.SUPERCHARGED else 5
            for i in range(3):
                if (0.6 if self.SUPERCHARGED else 0.8) >= random.random():
                    hits += 1
            supercharge = self.SUPERCHARGED
            self.enchanceBasic = False
            self.SUPERCHARGED = False
            if supercharge:
                self.critDamage += 0.5
            actionData = {
                "char": "March7",
                "action": "enchancedBasic",
                "actionType": "atk",
                "target": "Enemy",
                "hitType": "single",
                "hits": hits,
                "base": self.getAttack() * 0.8,
                "element": ["imaginary", self.shifuType],
                "break": 5 * hits,
                "effects": [{"name": "m7SwordPlay",
                             "type" : "dmgDebuff",
                             "base" : 0.5,
                             "turnCount" : 1,
                             "maxStack" : 5,
                             "stack" : 1,
                             "deleteOthers" : True,
                             "on/off" : "on"}]
            }
            if supercharge:
                self.critDamage -= 0.5
            self.charge -= 7
            self.dmgBuff -= 0.8
            self.actionSignal(actionData)

    def skill(self):
        self.followUpCharge = True
        self.addEnergy(35)
        self.speedBuff += 0.1
        actionData = {
            "char": "March7",
            "action": "skill",
            "actionType": "buff",
            "target": "Ally",
            "hitType": "single",
            "hits": 1,
            "base": 0,
            "element": ["none"],
            "break": 0,
            "effects": [{"name": "m7SpeedBuff",
                         "type" : "speedBuff",
                         "base" : 0.1,
                         "turnCount" : 100,
                         "maxStack" : 1,
                         "stack" : 1,
                         "deleteOthers" : True,
                         "on/off" : "on"}]
        }
        self.actionSignal(actionData)

    def ultimate(self):
        self.addEnergy(-self.energyCost)
        self.addEnergy(5)
        self.SUPERCHARGED = True
        actionData = {
            "char": "March7",
            "action": "ultimate",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 2.4,
            "element": ["imaginary", self.shifuType],
            "break": 30,
            "effects": [{"name": "m7SwordPlay",
                         "type" : "dmgDebuff",
                         "base" : 0.14,
                         "turnCount" : 1,
                         "maxStack" : 5,
                         "stack" : 1,
                         "deleteOthers" : True,
                         "on/off" : "on"}]
        }
        self.actionSignal(actionData)

    def talent(self):
        self.addEnergy(5)
        self.addCharge(1)
        actionData = {
            "char": "March7",
            "action": "talent",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 0.6,
            "element": ["imaginary", self.shifuType],
            "break": 5,
            "effects": [{"name": "m7SwordPlay",
                         "type" : "dmgDebuff",
                         "base" : 0.14,
                         "turnCount" : 1,
                         "maxStack" : 5,
                         "stack" : 1,
                         "deleteOthers" : True,
                         "on/off" : "on"}]
        }
        self.actionSignal(actionData)
        self.checkCharge()
    
    def grep(self, grep):
        data = {
            "basic" : {"target" : "Enemy", "hitType" : "single"},
            "skill" : {"target" : "Ally", "hitType" : "single"},
            "ultimate" : {"target" : "Enemy", "hitType" : "single"}
        }
        return data[grep]
    
    def actionDetect(self, actionType, actionChar):
        if actionType == "start":
            self.actionValue = max(0, self.actionValue - 10000 * 0.25)

        if actionType == "atk" and actionChar == self.shifu:
            self.addCharge(1)
            self.checkCharge()
            if self.followUpCharge:
                self.followUpCharge = False
                self.addAction(["March7", "talent", -1])
                
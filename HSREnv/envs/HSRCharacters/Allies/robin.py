import random
from datetime import datetime
from HSREnv.envs.HSRCharacters.Allies._allyTemplate import AllyTemplate

class Robin(AllyTemplate):
    def __init__(self, hp= 4313, atk= 3864, defence= 986, spd= 115, critRate= 0.079, critDamage= 1.733, energyRegenRate= 1.19):
        super().__init__(hp, atk, defence, spd, critRate, critDamage)

        self.name = "Robin"
        self.energy = 0
        self.energyCost = 160
        self.energyMax = 160
        self.energyRegenRate = energyRegenRate
        self.countdown = 0
        self.singing = False

        random.seed(datetime.now().timestamp())
        
    def getSpeed(self):
        return 90 if self.singing else self.spd * self.speedBuff

    def getCritRate(self):
        critRateBuff = self.getBuff("critRateBuff")
        return (self.critRate + critRateBuff) if not self.singing else 0.5
    
    def getCritDamage(self):
        critDamageBuff = self.getBuff("critDamageBuff")
        return (self.critDamage + critDamageBuff) if not self.singing else 2

    def getUltName(self):
        if(self.singing):
            return "disable"
        return 'ready' if self.checkUltimate() else 'notready'

    def basic(self):
        self.countdown -= 1
        if(self.singing):
            self.actionSignal(["robinUltDown", "Robin"])
        self.singing = False
        if self.countdown <= 0:
            actionData = {
                "char": "Robin",
                "action": "skill",
                "actionType": "buffEnd",
                "target": "Ally",
                "hitType": "all",
                "hits": 1,
                "base": 0,
                "element": ["none"],
                "break": 0,
                #"effects": {"RobinSkill": ["dmgBuff", 0.5, 1, -1]}
                "effects": [{"name": "RobinSkill",
                             "type" : "dmgBuff",
                             "base" : 0.5,
                             "turnCount" : 100,
                             "maxStack" : 1,
                             "stack" : 1,
                             "deleteOthers" : False,
                             "on/off" : "off"}]}

            self.actionSignal(actionData)

        self.addEnergy(20)
        actionData = {
            "char": "Robin",
            "action": "basic",
            "actionType": "atk",
            "target": "Enemy",
            "hitType": "single",
            "hits": 1,
            "base": self.getAttack() * 1,
            "element": ["physical"],
            "break": 10,
            "effects": {}
        }
        self.actionSignal(actionData)

    def skill(self):
        self.countdown = 3
        self.addEnergy(30)
        if(self.singing):
            self.actionSignal(["robinUltDown", "Robin"])
        self.singing = False
        actionData = {
            "char": "Robin",
            "action": "skill",
            "actionType": "buff",
            "target": "Ally",
            "hitType": "all",
            "hits": 1,
            "base": 0,
            "element": ["none"],
            "break": 0,
            "effects": [{"name": "RobinSkill",
                          "type" : "dmgBuff",
                          "base" : 0.5,
                          "turnCount" : 100,
                          "maxStack" : 1,
                          "stack" : 1,
                          "deleteOthers" : False,
                          "on/off" : "on"}]}
        self.actionSignal(actionData)

    def ultimate(self):
        self.energy = 5
        self.singing = True
        actionData = {
            "char": "Robin",
            "action": "ultimate",
            "actionType": "buff",
            "target": "Ally",
            "hitType": "all",
            "hits": 1,
            "base": 0,
            "element": ["none"],
            "break": 0,
            "effects": [{"name": "RobinUltBuff",
                          "type" : "atkBuff",
                          "base" : 0.3,
                          "turnCount" : 100,
                          "maxStack" : 1,
                          "stack" : 1,
                          "deleteOthers" : False,
                          "on/off" : "on"},
                         {"name": "RobinUltAtk",
                          "type" : "followAtk",
                          "base" : self.getAttack() * 1.2,
                          "turnCount" : 1,
                          "maxStack" : 1,
                          "stack" : 1,
                          "deleteOthers" : False,
                          "on/off" : "on"}]}
        self.actionSignal(actionData)
    
    def grep(self, grep):
        data = {
            "basic" : {"target" : "Enemy", "hitType" : "single"},
            "skill" : {"target" : "Ally", "hitType" : "all"},
            "ultimate" : {"target" : "Ally", "hitType" : "all"}
        }
        return data[grep]
    
    def actionDetect(self, actionType, actionChar):
        if actionType == "atk":
            self.addEnergy(2)

        if actionType == "robinUltDown":
            actionData = {
                "char": "Robin",
                "action": "skill",
                "actionType": "buff",
                "target": "Ally",
                "hitType": "all",
                "hits": 1,
                "base": 0,
                "element": ["none"],
                "break": 0,
                "effects": [{"name": "RobinUltBuff",
                             "type" : "atkBuff",
                             "base" : 0.3,
                             "turnCount" : 100,
                             "maxStack" : 1,
                             "stack" : 1,
                             "deleteOthers" : False,
                             "on/off" : "off"},
                            {"name": "RobinUltAtk",
                             "type" : "followAtk",
                             "base" : self.getAttack() * 1.2,
                             "turnCount" : 1,
                             "maxStack" : 1,
                             "stack" : 1,
                             "deleteOthers" : False,
                             "on/off" : "off"}]}
            self.actionSignal(actionData)

        if actionType == "start":
            actionData = {
                "char": "Robin",
                "action": "skill",
                "actionType": "buff",
                "target": "Ally",
                "hitType": "all",
                "hits": 1,
                "base": 0,
                "element": ["none"],
                "break": 0,
                "effects": [{"name": "RobinTalent",
                             "type" : "critDamageBuff",
                             "base" : 0.2,
                             "turnCount" : 100,
                             "maxStack" : 1,
                             "stack" : 1,
                             "deleteOthers" : False,
                             "on/off" : "on"},
                            {"name": "RobinE1",
                             "type" : "resPENBuff",
                             "base" : 0.24,
                             "turnCount" : 1,
                             "maxStack" : 1,
                             "stack" : 1,
                             "deleteOthers" : False,
                             "on/off" : "on"}]}
            self.actionSignal(actionData)

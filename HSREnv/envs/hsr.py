import HSREnv.envs.HSRCharacters as hsr
import numpy as np
import random
import pygame
import sys
from datetime import datetime

class HSR:
    def __init__(self, charNames = ["Feixiao", "Adventurine", "Robin", "March7"], enemyData = {"waves" : 3, "basicEnemy" : 4, "eliteEnemy" : 1, "basicData" : ["random", "random", "random", "random"], "eliteData" : ["random"]}):
        #init import
        random.seed(datetime.now().timestamp())

        pygame.init()
        self.fps = 60
        self.fpsClock = pygame.time.Clock()
        
        self.width, self.height = 1500, 880
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('image')
        self.pygameImages = {}
        self.initPygameImages()

        #init characters
        self._characters = {
            "Feixiao"     : hsr.Allies.Feixiao(hp=3311, atk=2603, defence=1331, spd=142, critRate=82.7, critDamage=2.4),
            "Adventurine" : hsr.Allies.Adventurine(hp=3098, atk=1441, defence=3976, spd=113, critRate=0.435, critDamage=1.895),
            "Robin"       : hsr.Allies.Robin(hp=4313, atk=3864, defence=986, spd=115, critRate=0.079, critDamage=1.733),
            "March7"      : hsr.Allies.March7(hp=2864, atk=3222, defence=908, spd=115, critRate=0.716, critDamage=2.349)
        }
        self.charNames = ["BLANK"] + charNames
        
        for charName in charNames:
            try:
                self._characters[charName]
            except KeyError:
                print("Character Name Initialization Error\nPlease Give Valid Character Names")
            
        self.team = ["BLANK", self._characters[charNames[1]], self._characters[charNames[2]], 
                     self._characters[charNames[3]], self._characters[charNames[4]]]
        
        #init enemies
        self.wave = 0
        self.enemies = []
        weaknesses = ["physical", "fire", "ice", "lightning", "wind", "quantum", "imaginary"]
        for i in range(enemyData["waves"]):
            thisWave = []
            try:
                for j in range(enemyData["basicEnemy"]):
                    if(enemyData["basicData"][j] == "random"):
                        thisWave.append(hsr.Enemies.BaseEnemy(hp = 50000, atk = 100, spd = random.choice([80, 100, 120]), toughness = random.choice([10, 20]), weakness = random.sample(weaknesses, random.randint(2,3))))
                    else:
                        thisWave.append(hsr.Enemies.BaseEnemy(hp = enemyData[j]["hp"], atk = enemyData[j]["atk"], spd = enemyData[j]["spd"], toughness = enemyData[j]["toughness"], weakness = enemyData[j]["weakness"]))

                for j in range(enemyData["basicEnemy"]):
                    if(enemyData["basicData"][j] == "random"):
                        weaknesses = ["physical", "fire", "ice", "lightning", "wind", "quantum", "imaginary"]
                        thisWave.append(hsr.Enemies.BaseEnemy(hp = 300000, atk = 100, spd = random.choice([100, 132, 150]), toughness = random.choice([100]), weakness = random.sample(weaknesses, random.randint(2,3))))
                    else:
                        thisWave.append(hsr.Enemies.BaseEnemy(hp = enemyData[j]["hp"], atk = enemyData[j]["atk"], spd = enemyData[j]["spd"], toughness = enemyData[j]["toughness"], weakness = enemyData[j]["weakness"]))
            except IndexError:
                print("Enemy number and enemy type is ot lined up, check it please :)")

            random.shuffle(thisWave)

            self.enemies.append(thisWave)

        self._initActionOrder()

        self.lastTarget = 0
        self.lastHp = [0, 0, 0, 0, 0]
        self.reward = 0

    def runAction(self):
        if(self.actionOrder[0][2] > 0):
            k = self.actionOrder[0][2]
            for i in len(self.actionOrder):
                self.actionOrder[i][2] -= k 

    def _initActionOrder(self):
        self.actionOrder = []
        for i in range(1, 5):
            self.actionOrder.append([self.charNames[i], "pending", self.team[i].actionValue])
        for i, enemy in enumerate(self.enemies[self.wave]):
            self.actionOrder.append([enemy, "pending", enemy.actionValue]) #NOT A STRING
        self.lastHp[i] = enemy.hp

        self.actionOrder = sorted(self.actionOrder, key=lambda t: t[2])
        self.runAction()
        
    def debuffEnemy(self, effect, target):
        if(effect["deleteOthers"] == True):
            for enemy in self.enemies[self.wave]:
                enemy.debuffs.pop(effect["name"], None)

        target.debuff[effect["name"]] = effect

    def buffAlly(self, effect, target):
        if(effect["deleteOthers"] == True):
            for ally in self.team:
                ally.buffs.pop(effect["name"], None)

        target.buff[effect["name"]] = effect    

    def doDamage(self, base, element, toughnessDamage, effect, char, target):
        if(isinstance(self.actionOrder[0], str)):
            self.sendSignal(self, "hit", target)
            self._characters[target].addEnergy(base)
        else:
            target.toughness = max(0, target.toughness - toughnessDamage)

            self.debuffEnemy(effect, target)

            dmg = base * char.getDamage() * char.calcDefMultiplier(target.getDefence(char.getDefIgnore())) * \
            target.getRES(element, char.getResPEN()) * target.getDamageReduction()

            if(random.random() >= char.getCritRate() + target.getCritRateDebuff()):
                dmg = dmg * (char.getCritDamage() + target.getCritDamageDebuff()) 

            if(target.hp == 0):
                return

            dmg = round(dmg)
            target.hp = max(0, target.hp - dmg)

            if(target.hp == 0):
                for i in range(4):
                    if(self.enemies[self.wave][i].hp == 0):
                        self.enemies[self.wave][i], self.enemies[self.wave][i+1] = self.enemies[self.wave][i+1], self.enemies[self.wave][i]
                self.reward += 0.1

    def charGoDo(self, charName, action, targetIndex):
        char = self._characters[charName]
        
        getattr(char, action)()
        data = char.getUpdate()
        if(data == "NULL"):
            return
        
        self.sendSignal(self, data["actionType"], data["char"])

        if(data["target"] == "Enemy"):
            if(data["hitType"] == "single"):
                target = self.enemies[self.wave][targetIndex]
                if(target.hp == 0):
                    target = 0
                for i in range(data["hits"]):
                    self.doDamage(data["base"], data["element"], data["break"], data["effect"], char, target)

            elif(data["hitType"] == "blast"):
                targetWave = self.enemies[self.wave]
                if(targetWave[targetIndex].hp == 0):
                    targetIndex = 0
                
                for i in range(data["hits"]):
                    if(targetIndex-1 >= 0):
                        self.doDamage(data["base"][0], data["element"], data["break"][0], data["effect"], char, targetWave[targetIndex-1])
                    self.doDamage(data["base"][1], data["element"], data["break"][0], data["effect"], char, targetWave[targetIndex-1])
                    if(targetIndex+1 <= 4):
                        self.doDamage(data["base"][2], data["element"], data["break"][0], data["effect"], char, targetWave[targetIndex-1])

            elif(data["hitType"] == "bounce"):
                aliveEnemies = []
                for i in range(5):
                    if(self.enemies[self.wave][i].hp > 0):
                        aliveEnemies.append(i)

                for i in range(data["hits"]):
                    target = random.choice(aliveEnemies)
                    self.doDamage(data["base"], data["element"], data["break"], data["effect"], char, self.enemies[self.wave][target])
        
        elif(data["target"] == "Ally"):
            targetIndex = max(1, targetIndex)
            if(data["hitType"] == "single"):
                self.buffAlly(self.team[targetIndex])
            elif(data["hitType"] == "blast"):
                if(targetIndex-1 >= 1):
                    self.buffAlly(self.team[targetIndex-1])
                self.buffAlly(self.team[targetIndex])
                if(targetIndex+1 <= 4):
                    self.buffAlly(self.team[targetIndex+1])
            elif(data["hitType"] == "all"):
                for i in range(1, 5):
                    self.buffAlly(self.team[i])

    def enemyGoDo(self, enemy, action):
        getattr(enemy, action)()
        data = enemy.getUpdate()
        if(data["target"] == "Ally"):
            targetIndex = random.randint(1, 4)
            if(data["hitType"] == "single"):
                if(target.hp == 0):
                    target = 0
                for i in range(data["hits"]):
                    self.doDamage(data["base"], data["element"], data["break"], data["effect"], enemy, self.charNames[targetIndex])

            elif(data["hitType"] == "blast"):
                targetWave = self.enemies[self.wave]
                if(targetWave[targetIndex].hp == 0):
                    targetIndex = 0
                
                for i in range(data["hits"]):
                    if(targetIndex-1 >= 0):
                        self.doDamage(data["base"][0], data["element"], data["break"][0], data["effect"], enemy, self.charNames[targetIndex])
                    self.doDamage(data["base"][1], data["element"], data["break"][0], data["effect"], enemy, self.charNames[targetIndex])
                    if(targetIndex+1 <= 4):
                        self.doDamage(data["base"][2], data["element"], data["break"][0], data["effect"], enemy, self.charNames[targetIndex])

            elif(data["hitType"] == "bounce"):
                aliveEnemies = []
                for i in range(5):
                    if(self.enemies[self.wave][i].hp > 0):
                        aliveEnemies.append(i)

                for i in range(data["hits"]):
                    target = random.choice(aliveEnemies)
                    self.doDamage(data["base"], data["element"], data["break"], data["effect"], enemy, self.charNames[targetIndex])

    def sendSignal(self, actionType, actionChar):
        for i in range(1, 5):
            self.team[i].actionDetect(actionType, actionChar)

    def action(self, action):
        if("ultimate" in action["action"]):
            self.charGoDo(action["action"][8:], "ultimate", action["target"])
            self.actionOrder[0][2] = self._characters[self.actionOrder[0][0]].calcActionValue()
        elif(self.actionOrder[0][1] != "pending"):
            if(isinstance(self.actionOrder[0], str)):
                self.charGoDo(self.actionOrder[0][0], self.actionOrder[0][1], self.lastTarget)
            else:
                self.enemyGoDo(self.actionOrder[0][0], self.actionOrder[0][1])
            del self.actionOrder[0]
            self.runAction()
        else:
            if(isinstance(self.actionOrder[0], str)):
                self.charGoDo(self.actionOrder[0][0], action["action"], action["target"])
                self.actionOrder[0][2] = self._characters[self.actionOrder[0][0]].calcActionValue()
            else:
                self.enemyGoDo(self.actionOrder[0][0], self.actionOrder[0][0].doAction())
                self.actionOrder[0][2] = self.actionOrder[0].calcActionValue()
            
            for i in range(len(self.actionOrder) - 1):
                if(self.actionOrder[i][2] >= self.actionOrder[i+1][2]):
                    self.actionOrder[i], self.actionOrder[i+1] = self.actionOrder[i+1], self.actionOrder[i]
                else:
                    break

    def evaluate(self):
        for i in range(len(self.enemies[self.wave])):#300000
            self.reward += (self.lastHp[i] - self.enemies[self.wave][i].hp)/300000
            self.lastHp[i] = self.enemies[self.wave][i].hp

        rwd = self.reward
        self.reward = 0
        return rwd

    def is_done(self):
        return self.wave >= len(self.enemies)

    def is_trunc(self):
        return False

    def observe(self):
        obs = {
            "AllyUlts" : [],
            "EnemyData" : []
        }
        for i in range(1, 5):
            obs["AllyUlts"].append(self.team[i].checkUltimate())
        for enemy in self.enemies[self.wave]:
            obs["EnemyData"].append(enemy.hp/300000)
            obs["EnemyData"].append(enemy.getWeakness())
        return np.array(obs)

    def _initPygameImages(self):
        self.pygameImages["HSRTitleScreen"] = pygame.image.load("assets/HSRTitleScreen.png").convert()
        self.pygameImages["Feixiaopending"] = pygame.image.load("assets/FeixiaoPending.png").convert()
        self.pygameImages["Feixiaobasic"] = pygame.image.load("assets/FeixiaoBasic.png").convert()
        self.pygameImages["Feixiaoskill"] = pygame.image.load("assets/FeixiaoSkill.png").convert()
        self.pygameImages["Feixiaotalent"] = pygame.image.load("assets/FeixiaoTalent.png").convert()
        self.pygameImages["Feixiaoultimate"] = pygame.image.load("assets/FeixiaoUltimate.png").convert()

        self.pygameImages["Robinpending"] = pygame.image.load("assets/RobinPending.png").convert()
        self.pygameImages["Robinbasic"] = pygame.image.load("assets/RobinBasic.png").convert()
        self.pygameImages["Robinskill"] = pygame.image.load("assets/RobinSkill.png").convert()
        self.pygameImages["Robintalent"] = pygame.image.load("assets/RobinPending.png").convert()
        self.pygameImages["Robinultimate"] = pygame.image.load("assets/RobinUltimate.png").convert()

        self.pygameImages["Adventurinepending"] = pygame.image.load("assets/AdventurinePending.png").convert()
        self.pygameImages["Adventurinebasic"] = pygame.image.load("assets/AdventurineBasic.png").convert()
        self.pygameImages["Adventurineskill"] = pygame.image.load("assets/AdventurineSkill.png").convert()
        self.pygameImages["Adventurinetalent"] = pygame.image.load("assets/AdventurineTalent.png").convert()
        self.pygameImages["Adventurineultimate"] = pygame.image.load("assets/AdventurineUltimate.png").convert()

        self.pygameImages["March7pending"] = pygame.image.load("assets/March7Pending.png").convert()
        self.pygameImages["March7basic"] = pygame.image.load("assets/March7Basic.png").convert()
        self.pygameImages["March7enchancedBasic"] = pygame.image.load("assets/March7Basic.png").convert()
        self.pygameImages["March7skill"] = pygame.image.load("assets/March7Skill.png").convert()
        self.pygameImages["March7talent"] = pygame.image.load("assets/March7Basic.png").convert()
        self.pygameImages["March7ultimate"] = pygame.image.load("assets/March7Ultimate.png").convert()

    def view(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.pygameImages["HSRTitleScreen"])


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # Opposite of pygame.init
                sys.exit()

from HSREnv.envs.HSRCharacters.Allies import *
from HSREnv.envs.HSRCharacters.Enemies import *
import numpy as np
import random
import pygame
import math
import time
import sys
import os
from datetime import datetime
from copy import deepcopy

''' to do list
retake adveturine action and enemy action - done
energy display - done
target choice display better - done
'''
class HSR():
    def __init__(self, seed = None, render_mode = "robot", charNames = ["Feixiao", "Adventurine", "Robin", "March7"], enemyData = {"waves" : 3, "basicEnemy" : 4, "eliteEnemy" : 1, "basicData" : ["random", "random", "random", "random"], "eliteData" : ["random"]}):
        random.seed(datetime.now().timestamp() if seed == None else seed)
        self.DONE = False        
        self.info = []
        self.reward = 0
        self.render_mode = render_mode
        self._initChars(charNames)
        self._initEnemies(enemyData)
        self._initActionOrder()

        self._initPygame()

    def _initChars(self, charNames):
        self._characters = {
            "Feixiao"     : Feixiao(hp=3311, atk=2603, defence=1331, spd=142, critRate=82.7, critDamage=2.4),
            "Adventurine" : Adventurine(hp=3098, atk=1441, defence=3976, spd=113, critRate=0.435, critDamage=1.895),
            "Robin"       : Robin(hp=4313, atk=3864, defence=986, spd=115, critRate=0.079, critDamage=1.733),
            "March7"      : March7(hp=2864, atk=3222, defence=908, spd=115, critRate=0.716, critDamage=2.349)
        }
        self.charNames = charNames
        if(self.charNames[0] != "BLANK"):
            self.charNames.insert(0, "BLANK")
        
        for charName in self.charNames:
            try:
                if(charName != "BLANK"):
                    self._characters[charName]
            except KeyError:
                print("Character Name Initialization Error\nPlease Give Valid Character Names")
            
        self.team = ["BLANK", self._characters[charNames[1]], self._characters[charNames[2]], 
                     self._characters[charNames[3]], self._characters[charNames[4]]]
        
        self.lastTarget = 0
        self.lastHp = [0, 0, 0, 0, 0]
        self.skillPoints = 3
        self.maxSP = 0
        for char in self.team:
            if(char != "BLANK"):
                self.maxSP = max(self.maxSP, char.maxSP)

    def _initEnemies(self, enemyData):
        self.wave = 0
        self.enemies = []
        weaknesses = ["physical", "fire", "ice", "lightning", "wind", "quantum", "imaginary"]
        for i in range(enemyData["waves"]):
            thisWave = []
            try:
                for j in range(enemyData["basicEnemy"]):
                    if(enemyData["basicData"][j] == "random"):
                        thisWave.append(BaseEnemy(name = "basic", hp = 50000, atk = 100, spd = random.choice([80, 100, 120]), toughness = random.choice([10, 20]), weakness = random.sample(weaknesses, random.randint(2,3))))
                    else:
                        thisWave.append(BaseEnemy(name = enemyData[j]["name"], hp = enemyData[j]["hp"], atk = enemyData[j]["atk"], spd = enemyData[j]["spd"], toughness = enemyData[j]["toughness"], weakness = enemyData[j]["weakness"]))

                for j in range(enemyData["eliteEnemy"]):
                    if(enemyData["eliteData"][j] == "random"):
                        weaknesses = ["physical", "fire", "ice", "lightning", "wind", "quantum", "imaginary"]
                        thisWave.append(BaseEnemy(name = "elite", hp = 300000, atk = 100, spd = random.choice([100, 132, 150]), toughness = random.choice([100]), weakness = random.sample(weaknesses, random.randint(2,3))))
                    else:
                        thisWave.append(BaseEnemy(name = enemyData[j]["name"], hp = enemyData[j]["hp"], atk = enemyData[j]["atk"], spd = enemyData[j]["spd"], toughness = enemyData[j]["toughness"], weakness = enemyData[j]["weakness"]))
            except IndexError:
                print("Enemy number and enemy type is ot lined up, check it please :)")

            random.shuffle(thisWave)

            self.enemies.append(thisWave)

    def runAction(self):
        if(self.actionOrder[0][2] > 0):
            k = self.actionOrder[0][2]
            for i in range(len(self.actionOrder)):
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
        try:
            if(effect["deleteOthers"] == True):
                for enemy in self.enemies[self.wave]:
                    if(enemy != target):
                        enemy.debuffs.pop(effect["name"], None)
            if(effect["name"] in target.debuffs):
                target.addDebuffStack(effect["name"])
            else:
                target.debuffs[effect["name"]] = effect

        except KeyError:
            print("No buff")

    def buffAlly(self, effect, target):
        try:
            if(effect["deleteOthers"] == True):
                for ally in self.team:
                    if(ally != target):
                        target.buffs.pop(effect["name"], None)

            if(effect["name"] in target.buffs):
                target.addBuffStack(effect["name"])
            else:
                target.buffs[effect["name"]] = effect    
        except KeyError:
            print("No Buff")

    def isFirstChar(self):
        return isinstance(self.actionOrder[0][0], str)
    
    def getFirstChar(self):
        return self.actionOrder[0][0] if self.isFirstChar() else "Enemy"
    
    def calcDamage(self, base, element, char, target):
        dmg = base * char.getDamage() * char.calcDefMultiplier(target.getDefence(char.getDefIgnore())) * \
            target.getRES(element, char.getResPEN()) * target.getDamageReduction()
        
        if(random.random() >= char.getCritRate() + target.getCritRateDebuff()):
                dmg = dmg * (char.getCritDamage() + target.getCritDamageDebuff()) 
        return dmg

    def doDamage(self, base, element, toughnessDamage, effects, char, target):
        if(isinstance(target, str)):#enemy
            self.sendSignal("hit", target)
            self.reward += -0.01
            if(target != "Feixiao"):
                self._characters[target].addEnergy(base)
            return -1
        else:#char
            dmg = 0
            try:
                if(target.toughness > 0):
                    target.toughness = max(0, target.toughness - toughnessDamage)
                    if(target.toughness == 0):
                        dmg += 5000 
            except AttributeError:
                print(base, element, toughnessDamage, effects, char, target)

            for effect in effects:
                self.debuffEnemy(effect, target)

            dmg += self.calcDamage(base, element, char, target)        

            for buff in char.buffs:
                buff = char.buffs[buff]
                if(buff["type"] == "followAtk"):
                    follow = self.calcDamage(buff["base"], "None", self._characters["Robin"], target)
                    if(random.random() >= char.getCritRate() + target.getCritRateDebuff()):
                        follow += follow * (char.getCritDamage() + target.getCritDamageDebuff())
                    dmg += follow 
                    #print("roibnULT", follow)

            if(target.hp == 0):
                return -1

            dmg = round(dmg)
            target.hp = max(0, target.hp - dmg)

            #print(base, char.getDamage(), char.calcDefMultiplier(target.getDefence(char.getDefIgnore())), \
            #target.getRES(element, char.getResPEN()), target.getDamageReduction())

            if(target.hp == 0):
                for i in range(4):
                    if(self.enemies[self.wave][i].hp == 0):
                        self.enemies[self.wave][i], self.enemies[self.wave][i+1] = self.enemies[self.wave][i+1], self.enemies[self.wave][i]
                self.reward += 0.1
            
            return dmg

    def charGoDo(self, charName, action, targetIndex):
        char = self._characters[charName]
        dmg = 0

        getattr(char, action)()
        update = char.getUpdate()
        data = 0
        if(update == "NULL"):
            return -1
        while(update != "NULL"):
            if(update[0] == "actionSignal"):
                data = update[1]
                if(isinstance(data, dict)):
                    self.sendSignal(data["actionType"], data["char"])
                else:
                    self.sendSignal(data[0], data[1])
                
            elif(update[0] == "addAction"):
                for i in range(len(self.actionOrder)):
                    if(update[1][2] <= self.actionOrder[0][2]):
                        self.actionOrder.insert(i, deepcopy(update[1]))
                        break
            update = char.getUpdate()

        if(data["target"] == "Enemy"):
            if(data["hitType"] == "single"):
                for i in range(data["hits"]):
                    if(self.enemies[self.wave][targetIndex] == 0):
                        targetIndex = 0
                    dmg += self.doDamage(data["base"], data["element"], data["break"], data["effects"], char, self.enemies[self.wave][targetIndex])

            elif(data["hitType"] == "blast"):
                targetWave = self.enemies[self.wave]
                for i in range(data["hits"]):
                    if(targetWave[targetIndex].hp == 0):
                        targetIndex = 0
                    if(targetIndex-1 >= 0):
                        dmg += self.doDamage(data["base"][0], data["element"], data["break"][0], data["effects"], char, targetWave[targetIndex-1])
                    dmg += self.doDamage(data["base"][1], data["element"], data["break"][0], data["effects"], char, targetWave[targetIndex-1])
                    if(targetIndex+1 <= 4):
                        dmg += self.doDamage(data["base"][2], data["element"], data["break"][0], data["effects"], char, targetWave[targetIndex-1])

            elif(data["hitType"] == "bounce"):
                aliveEnemies = []
                for i in range(5):
                    if(self.enemies[self.wave][i].hp > 0):
                        aliveEnemies.append(i)

                for i in range(data["hits"]):
                    target = random.choice(aliveEnemies)
                    dmg += self.doDamage(data["base"], data["element"], data["break"], data["effects"], char, self.enemies[self.wave][target])
        
        elif(data["target"] == "Ally"):
            targetIndex = max(1, targetIndex)
            for effect in data["effects"]:
                if(data["hitType"] == "single"):
                    self.buffAlly(effect, self.team[targetIndex])
                elif(data["hitType"] == "blast"):
                    if(targetIndex-1 >= 1):
                        self.buffAlly(self.team[targetIndex-1])
                    self.buffAlly(effect, self.team[targetIndex])
                    if(targetIndex+1 <= 4):
                        self.buffAlly(effect, self.team[targetIndex+1])
                elif(data["hitType"] == "all"):
                    for i in range(1, 5):
                        self.buffAlly(effect, self.team[i])

        self.skillPoints = max(0, min(self.maxSP, self.skillPoints + data["SP"]))
        return dmg
    
    def enemyGoDo(self, enemy, action):
        getattr(enemy, action)()
        dmg = 0
        update = enemy.getUpdate()
        data = 0
        if(update == "NULL"):
            return -1
        while(update != "NULL"):
            if(update[0] == "actionSignal"):
                data = update[1]
                self.sendSignal(data["actionType"], data["char"])
            elif(update[0] == "addAction"):
                for i in range(len(self.actionOrder)):
                    if(update[1][2] <= self.actionOrder[0][2]):
                        self.actionOrder.insert(i, deepcopy(update[1]))
            update = enemy.getUpdate()

        if(data["target"] == "Ally"):
            targetIndex = random.randint(1, 4)
            if(data["hitType"] == "single"):
                for i in range(data["hits"]):
                    dmg += self.doDamage(data["base"], data["element"], data["break"], data["effects"], enemy, self.charNames[targetIndex])

            elif(data["hitType"] == "blast"):
                for i in range(data["hits"]):
                    if(targetIndex-1 >= 0):
                        dmg += self.doDamage(data["base"][0], data["element"], data["break"][0], data["effects"], enemy, self.charNames[targetIndex])
                    dmg += self.doDamage(data["base"][1], data["element"], data["break"][0], data["effects"], enemy, self.charNames[targetIndex])
                    if(targetIndex+1 <= 4):
                        dmg += self.doDamage(data["base"][2], data["element"], data["break"][0], data["effects"], enemy, self.charNames[targetIndex])

            elif(data["hitType"] == "bounce"):
                aliveChars = [1, 2, 3, 4]

                for i in range(data["hits"]):
                    target = random.choice(aliveChars)
                    dmg += self.doDamage(data["base"], data["element"], data["break"], data["effects"], enemy, self.charNames[target])
            
            return dmg

    def sendSignal(self, actionType, actionChar):
        
        #print(f"{actionChar} did/got {actionType}")
        '''
        for i in self.actionOrder:
            if(not isinstance(i[0], str)):
                print(f", [enemy, {i[1]}, {i[2]}]", end= '')
            else:
                print(f", {i}", end= '')
        print()
        '''
        for i in range(1, 5):
            self.team[i].actionDetect(actionType, actionChar)
            
    def action(self, action):
        self.invalidActionTest(action)
        self.addInfo(f"done? : {self.is_done()}")
        if(self.is_done()):
            return
        if(self.render_mode == "display"):
            self.viewTarget = action["target"]
        if("ultimate" in action["action"]):
            char = self.charNames[int(action["action"][8:])]
            dmg = self.charGoDo(char, "ultimate", action["target"])
            self.charActionImage(char, "ultimate", dmg)
            if(char == "Robin"):
                for i in range(len(self.actionOrder)):
                    if(self.actionOrder[i][0] == "Robin"):
                        del self.actionOrder[i]
                        break
                for i in range(len(self.actionOrder)):
                    if(self._characters[char].calcActionValue() < self.actionOrder[i][2]):
                        self.actionOrder.insert(i, [char, "pending", self._characters[char].calcActionValue()])
                        break
                else:
                    self.actionOrder.append([char, "pending", self._characters[char].calcActionValue()])

        elif(self.actionOrder[0][1] != "pending"):
            #print("NOTPENDING")
            if(self.isFirstChar()):
                dmg = self.charGoDo(self.actionOrder[0][0], self.actionOrder[0][1], self.lastTarget)
                self.charActionImage(self.getFirstChar(), self.actionOrder[0][1], dmg)
            else:
                self.enemyGoDo(self.actionOrder[0][0], self.actionOrder[0][1])
            del self.actionOrder[0]
            self.runAction()
        else:
            if(self.isFirstChar()):
                char = self.actionOrder[0][0]
                #print("----\n" + char)
                del self.actionOrder[0]
                #print(char + "\n--------")
                dmg = self.charGoDo(char, action["action"], action["target"])
                self.charActionImage(char, action["action"], dmg)

                for i in range(len(self.actionOrder)):
                    if(self._characters[char].calcActionValue() < self.actionOrder[i][2]):
                        self.actionOrder.insert(i, [char, "pending", self._characters[char].calcActionValue()])
                        break
                else:
                    self.actionOrder.append([char, "pending", self._characters[char].calcActionValue()])
            else:
                #print("ENEMYYY")
                char = self.actionOrder[0][0]
                del self.actionOrder[0]
                self.enemyGoDo(char, char.doAction())

                for i in range(len(self.actionOrder)):
                    if(char.calcActionValue() < self.actionOrder[i][2]):
                        self.actionOrder.insert(i, [char, "pending", char.calcActionValue()])
                        break
                else:
                    self.actionOrder.append([char, "pending", char.calcActionValue()])
            self.runAction()
        
        if(self.enemies[self.wave][0].hp == 0):
            self.wave = min(self.wave+1, len(self.enemies)-1)
        
    def evaluate(self):
        for i in range(len(self.enemies[self.wave])):#300000
            self.reward += (self.lastHp[i] - self.enemies[self.wave][i].hp)/300000
            self.lastHp[i] = self.enemies[self.wave][i].hp

        rwd = self.reward
        return rwd

    def invalidActionTest(self, action):
        if(self.render_mode == "human"):
            return

        ultWrong = "ultimate" in action["action"] and not self.team[int(action["action"][8:])].checkUltimate()
        selfMarch7 = action["action"] == "skill" and self.actionOrder[0][0] == "March7" and self.charNames[action["target"]] == "March7"
        if(ultWrong or selfMarch7):
            self.DONE = True
            self.reward = -100

    def is_done(self):
        return (self.enemies[self.wave][0].hp == 0 and self.wave == len(self.enemies)-1) or self.DONE

    def is_trunc(self):
        return False

    def observe(self):
        obs = {
            "AllyUlts" : [],
            "EnemyHp" : [],
            "EnemyWeakness" : [],
            "Elites" : [],
            "ActionOrder" : [],
            "SkillPoints" : self.skillPoints
        }
        for i in range(1, 5):
            obs["AllyUlts"].append(self.team[i].checkUltimate())
        for enemy in self.enemies[self.wave]:
            obs["EnemyHp"].append(enemy.hp/enemy.maxHp)
            obs["EnemyWeakness"].append(enemy.getWeakness())
            obs["Elites"].append(1 if enemy.name == "elite" else 0)

        for i in range(2):
            if(self.isFirstChar()):
                obs["ActionOrder"].append(self.charNames.index(self.actionOrder[0][0]))
            else:
                obs["ActionOrder"].append(4 if self.actionOrder[0][0].name == "basic" else 5)
        #print(obs)
        return obs

    def _initPygame(self):
        if(self.render_mode == "robot"):
            return
        pygame.init()

        self.INF = 1000000000
        self.fps = 60
        self.fpsClock = pygame.time.Clock()
        self.deltaTime = 0
        self.font = {"small" : pygame.font.SysFont('Comic Sans MS', 20),
                     "big" : pygame.font.SysFont('Comic Sans MS', 30)}

        self.lockPos = (-100, -100)
        self.hover = {"basic" : True, "skill" : False}
        self.viewTarget = 0

        self.screenWidth, self.screenHeight = 1000, 587
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption('image')
        self.pygameImages = {}

        self.charImagePos = [(0, 0), (10, 307), (190, 307), (370, 307), (550, 307
                                                                         )]
        self.buttonPos = [(765, 460), (865, 360)]
        self.charImageEnergyPos = [(0, 0)]
        self.weaknesses = ["physical", "fire", "ice", "lightning", "wind", "quantum", "imaginary"]
        for i in range(1, 5):
            self.charImageEnergyPos.append((self.charImagePos[i][0] + 90, self.charImagePos[i][1] + 170))

        self.imageTime = {
            "Adventurine" : {"basic":700,"skill":700,"talent":700,"ultimate":1000},
            "Feixiao" : {"basic":700,"skill":700,"talent":1200,"ultimate":1500},
            "Robin" : {"basic":700,"skill":700,"talent":700,"ultimate":1500},
            "March7" : {"basic":700,"skill":700,"talent":700,"ultimate":1000}
        }
        self.charImage = {
            self.charNames[1] : [{"action" : "pending", "to" : -1}],
            self.charNames[2] : [{"action" : "pending", "to" : -1}],
            self.charNames[3] : [{"action" : "pending", "to" : -1}],
            self.charNames[4] : [{"action" : "pending", "to" : -1}]
        }
        self.allImages = []
        self.allRects = []
        self.allTexts = []
        cwd = os.getcwd()        
        directory = os.fsencode(cwd + "/GymEnvCode/HSREnv/envs/assets")
    
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".png") or filename.endswith(".jpg"): 
                flname = filename[:-4]
                self.pygameImages[flname] = pygame.image.load(directory.decode() + "/" + filename).convert()
                #print(flname[:3])
                if(flname[:3] == "HSR"):
                    self.pygameImages[flname] = pygame.transform.scale(self.pygameImages[flname], (self.screenWidth, self.screenHeight))
                elif(flname == "Lock"):
                    self.pygameImages[flname] = pygame.transform.scale(self.pygameImages[flname], (20, 20))
                elif("energy" in flname):
                    self.pygameImages[flname] = pygame.transform.scale(self.pygameImages[flname], (80, 80))
                elif("buttons" in flname):
                    self.pygameImages[f"{flname}_nothover"] = pygame.transform.scale(self.pygameImages[flname], (80, 80))
                    self.pygameImages[f"{flname}_hover"] = pygame.transform.scale(self.pygameImages[flname], (100, 100))
                elif("weakness" in flname):
                    self.pygameImages[f"{flname}"] = pygame.transform.scale(self.pygameImages[flname], (20, 20))
                elif("actionOrder" in flname):
                    if("small" in flname):
                        self.pygameImages[f"{flname}"] = pygame.transform.scale(self.pygameImages[flname], (100, 50))
                    else:
                        self.pygameImages[f"{flname}"] = pygame.transform.scale(self.pygameImages[flname], (120, 60))
                elif("Enemy" in flname):
                    if("basic" in flname):
                        self.pygameImages[flname] = pygame.transform.scale(self.pygameImages[flname], (150, 150))
                    else:
                        self.pygameImages[flname] = pygame.transform.scale(self.pygameImages[flname], (170, 200))
                else:#char
                    self.pygameImages[flname] = pygame.transform.scale(self.pygameImages[flname], (170, 250))
            else:
                continue

    def charActionImage(self, char, action, dmg):
        if(self.render_mode == "robot"):
            return
        self.charImage[char].append({"action" : action, "to" : pygame.time.get_ticks() + self.imageTime[char][action], "dmg" : dmg})
        #print(pygame.time.get_ticks())

    def _checkImageAction(self, char):
        while(len(self.charImage[char]) and pygame.time.get_ticks() > self.charImage[char][0]["to"]):
            self.charImage[char].pop(0)
        if(len(self.charImage[char]) == 0):
            self.charImage[char].append({"action" : "pending", "to" : -1, "dmg" : -1})

    def addImage(self, img, pos, index, name, layer):
        self.allImages.append({"img" : img,
                               "pos" : pos,
                               "index" : index, 
                               "name" : name,
                               "layer" : layer})
    
    def addRect(self, color, rect, layer):
        self.allRects.append({"color" : color,
                              "rect" : rect,
                              "layer" : layer})

    def addText(self, text, layer, pos, size, color = (255, 255, 255)):
        self.allTexts.append({"text" : self.font[size].render(text, True, color), 
                              "pos" : pos,
                              "layer" : layer})

    def addLock(self, index, target, enmCount):
        #print("WAFWUAH")
        if(target == "Enemy"):
            self.lockPos = (120 + (self.screenWidth-120)//(enmCount)*(index) + 65, 40)
            self.addImage(self.pygameImages["Lock"], self.lockPos, index, "Lock", 3)
        else:
            self.lockPos = (self.charImagePos[index][0] + 75, self.charImagePos[index][1] - 20)
            self.addImage(self.pygameImages["Lock"], self.lockPos, index, "Lock", 3)

    def _updateImages(self):
        for i in range(10):
            for data in self.allImages:
                if(data["layer"] == i):
                    self.screen.blit(data["img"], data["pos"])
            for data in self.allRects:
                if(data["layer"] == i):
                    pygame.draw.rect(self.screen, data["color"], data["rect"])
            for data in self.allTexts:
                if(data["layer"] == i):
                    self.screen.blit(data["text"], data["pos"])

    def view(self):
        if(self.render_mode == "robot"):
            return        
        if(self.is_done()):
            #self.addInfo("Ehh Na")
            return      
        
        action = {"target" : "None", "action" : "None"}
        imageRects = []
        for img in self.allImages:
            imageRects.append({"rect" : img["img"].get_rect(topleft=img["pos"]),
                               "pos" : img["pos"],
                               "index" : img["index"], 
                               "name" : img["name"]})
        self.allImages = []
        self.allRects = []
        self.allTexts = []
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit() # Opposite of pygame.init
                sys.exit()
            if(event.type == pygame.MOUSEBUTTONDOWN and self.render_mode == "human"):
                x, y = event.pos
                for data in imageRects:
                    if(data["rect"].collidepoint(x, y)):
                        targetEnemy = (self.isFirstChar() and self._characters[self.getFirstChar()].grep("basic" if self.hover["basic"] else "skill")["target"] == "Enemy")

                        if("Enemy_pose" in data["name"] and targetEnemy):
                            self.viewTarget = data["index"]
                        elif("energy" in data["name"] and self.team[data["index"]].checkUltimate()):
                            action = {"action" : f"ultimate{self.charNames[data['index']]}", "target" : self.viewTarget}
                        elif("button" in data["name"]):
                            if("basic" in data["name"]):
                                if(self.hover["basic"] == False):
                                    self.hover["basic"] = True
                                    self.hover["skill"] = False
                                else:
                                    action = {"action" : f"basic", "target" : self.viewTarget}
                            elif("skill" in data["name"]):
                                if(self.hover["skill"] == False):
                                    self.hover["basic"] = False
                                    self.hover["skill"] = True
                                elif(self.skillPoints > 0):
                                    action = {"action" : f"skill", "target" : self.viewTarget}
                        elif("Enemy" not in data["name"] and "pose" in data["name"] and not targetEnemy):
                            self.viewTarget = data["index"]

        self.screen.fill((0,0,0))
        self.addImage(self.pygameImages["HSR_title_screen"], (0, 0), 0, "HSRTitleScreen", 0)
        
        #Ally Images
        for i in range(1, 5):
            char = self.charNames[i]
            self._checkImageAction(char)
            #print(f"{char}_{self.charImage[char]['action']}")
            name = f"{char}_pose_{self.charImage[char][0]['action']}"
            energyName = f"{char}_energy_{self._characters[char].getUltName()}"
            self.addImage(self.pygameImages[name], self.charImagePos[i], i, name, 1)
            self.addImage(self.pygameImages[energyName], self.charImageEnergyPos[i], i, energyName, 2)
            #display Damage
            dmg = self.charImage[char][0]['dmg']
            if(dmg > 0):
                self.addText(str(dmg), 2, (900, 250), "big")
            #display Energy
            actChar = self._characters[char]
            pos = (self.charImageEnergyPos[i][0]+15, self.charImageEnergyPos[i][1]+80)
            self.addText(f"{math.floor(actChar.energy)}/{math.floor(actChar.energyMax)}", 4, pos, "small")

        nowChar = self.getFirstChar()
        
        if(nowChar != "Enemy"):
            self.addImage(self.pygameImages[f"{nowChar}_buttons_basic_{'' if self.hover['basic'] else 'not'}hover"], self.buttonPos[0], 0, f"{nowChar}_buttons_basic_{'' if self.hover['basic'] else 'not'}hover", 2)
            self.addImage(self.pygameImages[f"{nowChar}_buttons_skill_{'' if self.hover['skill'] else 'not'}hover"], self.buttonPos[1], 1, f"{nowChar}_buttons_skill_{'' if self.hover['skill'] else 'not'}hover", 2)
        
        #Enemy Images      
        enmCount = 0
        for enm in self.enemies[self.wave]:
            if(enm.hp > 0):
                enmCount += 1
        
        #print("[", end='')

        for i in range(enmCount):
            enm = self.enemies[self.wave][i]
            enmName = enm.name
            imgHp = self.pygameImages[f"Enemy_pose_{enmName}"]
            pos = (130 + (self.screenWidth-130)//(enmCount)*(i) - (10 if enmName == "elite" else 0), 60)
            self.addImage(imgHp, pos, i, f"Enemy_pose_{enmName}", 1)
            #Enemy Bars
            ratioHp = enm.hp / enm.maxHp
            ratioToughness = enm.toughness / enm.maxToughness
            add = (10 if enmName=="elite" else 0)
            self.addRect("black", (pos[0] + add, pos[1]-25, 150, 20), 1)
            self.addRect((195, 75, 60), (pos[0] + add, pos[1]-15, 150 * ratioHp, 10), 2)
            self.addRect((255, 255, 255), (pos[0] + add, pos[1]-25, 150 * ratioToughness, 10), 2)
            #Enemy weakness
            cnt = 0
            for i, element in enumerate(self.weaknesses):
                if(enm.obsWeakness[i] == 1):
                    imgToughness = self.pygameImages[f"weakness_{element}"]
                    self.addImage(imgToughness, (pos[0]+cnt*20+add, pos[1]-45), i, f"weakness_{element}", 3)
                    cnt += 1
            #print(enm.hp, ratio, end=', ')
            
        #print("]")

        #Lock Image
        if(self.isFirstChar()):
            char = self._characters[self.getFirstChar()]
            data = char.grep("basic" if self.hover["basic"] else "skill")
            if(data["hitType"] == "single" or data["hitType"] == "bounce"):
                self.addLock(self.viewTarget, data["target"], enmCount)
            elif(data["hitType"] == "blast"):
                if(self.viewTarget-1 >= (0 if data["target"] == "Enemy" else 1)):
                    self.addLock(self.viewTarget-1, data["target"], enmCount)
                self.addLock(self.viewTarget, data["target"], enmCount)
                if(self.viewTarget+1 <= 4):
                    self.addLock(self.viewTarget+1, data["target"], enmCount)
            elif(data["hitType"] == "all"):
                for i in range((0 if data["target"] == "Enemy" else 1), 5):
                    self.addLock(i, data["target"], enmCount)

        if(self.render_mode == "human"):
            if(self.isFirstChar() == False or self.actionOrder[0][1] != "pending"):
                #print("Enemy lol")
                self.action({"action" : "None", "target" : "None"})
            elif(action["action"] != "None"):
                self.action(action)

        if(self.enemies[self.wave][self.viewTarget].hp == 0):
            self.viewTarget = 0

        #Action Order
        first = self.actionOrder[0][0]
        second = self.actionOrder[1][0]
        self.actionOrderPos = [(0, 30), (0, 100)]

        if(isinstance(first, str)):
            self.addImage(self.pygameImages[f"{first}_actionOrder_big"], self.actionOrderPos[0], 0, f"{first}_actionOrder_big", 1)
        else:
            self.addImage(self.pygameImages[f"Enemy_actionOrder_big"], self.actionOrderPos[0], 0, f"Enemy_actionOrder_big", 1)
        if(isinstance(second, str)):
            self.addImage(self.pygameImages[f"{second}_actionOrder_small"], self.actionOrderPos[1], 1, f"{second}_actionOrder_small", 1)
        else:
            self.addImage(self.pygameImages[f"Enemy_actionOrder_small"], self.actionOrderPos[1], 1, f"{second}_actionOrder_small", 1)

        #Skill Points
        self.addText(f"SP : {self.skillPoints}/{self.maxSP}", 3, (905, 480), "small")

        #update
        self._updateImages()
        pygame.display.update()
        if(self.render_mode == "human"):
            self.deltaTime = self.fpsClock.tick(60)
        #self.addInfo("HEY I RENDERED")

    def getInfo(self):
        info = self.info
        self.info = []
        actionInfo = ""
        for char in self.actionOrder:
            if(isinstance(char[0], str)):
                actionInfo += f" - {[char[0], char[2]]}"
            else:
                actionInfo += f" - {[char[0].name, char[2]]}"
        return {"reward" : self.reward,
                "info" : info,
                "------------------------ LEGIT Action Values" : actionInfo}

    def addInfo(self, txt):
        self.info.append(txt)
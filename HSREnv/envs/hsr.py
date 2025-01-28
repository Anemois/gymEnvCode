import HSREnv.envs.HSRCharacters as hsr
import numpy as np
import random
import pygame

class HSR:
    def __init__(self, charNames = ["Feixiao", "Adventurine", "Robin", "March7"], enemyData = {"waves" : 3, "basicEnemy" : 4, "eliteEnemy" : 1, "basicData" : ["random", "random", "random", "random"], "eliteData" : ["random"]}):
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
        self.wave = 1
        self.enemies = ["BLANK"]
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

        self.actionOrder = sorted(self.actionOrder, key=lambda t: t[2])
        self.runAction()
        
    def charGoDo(self, char, action):
        getattr(self._characters[char], action)()

    def action(self, action):
        if(self.actionOrder[0][1] != "pending"):
            if(isinstance(self.actionOrder[0], str)):
                self.charGoDo(self.actionOrder[0][0], self.actionOrder[0][1])
            del self.actionOrder[0]
            self.runAction()
        else:
            pass

    def evaluate(self):
        pass

    def is_done(self):
        pass

    def is_trunc(self):
        pass

    def observe(self):
        pass

    def view(self):
        pass

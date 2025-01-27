import HSREnv.envs.HSRCharacters as hsrChar
import numpy as np
import pygame

class HSR:
    def __init__(self, charNames = ["BLANK", "Feixiao", "Adventurine", "Robin", "March7"]):
        #init characters
        self._characters = {
            "Feixiao" : hsrChar.Feixiao(hp=3311, atk=2603, defence=1331, spd=142, critRate=82.7, critDamage=2.4),
            "Adventurine" : hsrChar.Adventurine(hp=3098, atk=1441, defence=3976, spd=113, critRate=0.435, critDamage=1.895),
            "Robin" : hsrChar.Robin(hp=4313, atk=3864, defence=986, spd=115, critRate=0.079, critDamage=1.733),
            "March7" : hsrChar.March7(hp=2864, atk=3222, defence=908, spd=115, critRate=0.716, critDamage=2.349)
        }
        self.charNames = charNames
        self.team = ["BLANK", self._characters[charNames[1]], self._characters[charNames[2]], 
                     self._characters[charNames[3]], self._characters[charNames[4]]]

        self.actionOrder = []
        for i in range(1, 5):
            self.actionOrder.append([self.charNames[i], "pending", self.team[i].actionValue])

    def action(self):
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

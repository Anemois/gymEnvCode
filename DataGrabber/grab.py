import pyautogui as pg
import numpy as np
import cv2

'''
things to grab:
    "AllyUlts" : spaces.MultiBinary(4),
    "EnemyHp": spaces.Box(low=0.0, high=1.0,shape=(5,), dtype=np.float64),
    "EnemyWeakness" : spaces.MultiBinary([5, 7]),
    "Elites" : spaces.MultiBinary(5),
    "ActionOrder" : spaces.MultiDiscrete([6, 6])
'''

class DataGrabber():
    def __init__(self, chars = ["Feixiao", "Adventurine", "Robin", "March7"]):
        self.initUltPos()
        self.initSPPos()
        self.screen = self.screenshot()

    def initUltPos(self):
        pass

    def initSPPos(self):
        pass

    def screenshot(self, path = None):
        if(path == None):
            self.screen = cv2.cvtColor(np.array(pg.screenshot()),  cv2.COLOR_RGB2BGR)
        else:
            try:
                self.screen = cv2.cvtColor(cv2.imread(path),  cv2.COLOR_RGB2BGR)
            except:
                print("Invalid Path Given")

    def grabAllyUlts(self):
        

    def grabEnemyHp(self):
        pass

    def grabEnemyWeakness(self):
        pass

    def grabElites(self):
        pass

    def grabActionOrder(self):
        pass
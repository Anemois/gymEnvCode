import pyautogui as pg
import numpy as np
import cv2
import os

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
        self.initSpPos()
        self.cwd = os.getcwd()
        self.screen = self.screenshot()
        self.scrX, self.scrY = pg.size()

    def initUltPos(self):
        self.ultPos = [[self.scrX*252//1920, self.scrY*870//1080, self.scrX*50//1920, self.scrY*50//1080], 
                       [self.scrX*480//1920, self.scrY*870//1080, self.scrX*50//1920, self.scrY*50//1080], 
                       [self.scrX*704//1920, self.scrY*870//1080, self.scrX*50//1920, self.scrY*50//1080], 
                       [self.scrX*930//1920, self.scrY*870//1080, self.scrX*50//1920, self.scrY*50//1080]]

    def initSpPos(self):
        self.spPos = [[self.scrX*1448//1920, self.scrY*968//1080], [self.scrX*1466//1920, self.scrY*968//1080], 
                      [self.scrX*1484//1920, self.scrY*968//1080], [self.scrX*1502//1920, self.scrY*968//1080], 
                      [self.scrX*1521//1920, self.scrY*968//1080], 
                      [self.scrX*1448//1920, self.scrY*942//1080], [self.scrX*1466//1920, self.scrY*942//1080]]
        self.spColor = (255, 255, 255)

    def screenshot(self, path = None):
        if(path == None):
            self.screen = cv2.cvtColor(np.array(pg.screenshot()),  cv2.COLOR_RGB2BGR)
        else:
            try:
                self.screen = cv2.cvtColor(cv2.imread(path),  cv2.COLOR_RGB2BGR)
            except:
                print("Invalid Path Given")

    def grabAllyUlts(self):
        pass

    def grabEnemyHp(self):
        pass

    def grabEnemyWeakness(self):
        pass

    def grabElites(self):
        pass

    def grabActionOrder(self):
        pass
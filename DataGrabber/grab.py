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
    def __init__(self, chars = ["Feixiao", "Robin", "Adventurine", "March7"]):
        self.screen = self.screenshot()
        self.scrX, self.scrY = pg.size()
        print(self.scrX, self.scrY)
        self.initImages()
        self.initUltPos()
        self.initSpPos()
        self.cwd = os.getcwd()

        self.chars = chars
        self.ults = [False, False, False, False]
        self.weaknesses = ["physical", "fire", "ice", "lightning", "wind", "quantum", "imaginary"]

    def initImages(self):
        self.images = {}
        cwd = os.getcwd()        
        directory = os.fsencode(cwd + "/DataGrabber/assets")
    
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".png") or filename.endswith(".jpg"): 
                flname = filename[:-4]
                self.images[flname] = cv2.imread(directory.decode() + "/" + filename)
                if(self.images[flname].shape == (1080, 1920, 3)):
                    self.images[flname] = cv2.resize(self.images[flname], (self.scrX, self.scrY))
                else:
                    sh = self.images[flname].shape
                    #print(sh)
                    self.images[flname] = cv2.resize(self.images[flname], (self.scrX*sh[1]//1920, self.scrY*sh[0]//1080))
                    #print(self.images[flname].shape)
    
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

    def showImage(self, img, name = "img"):
        cv2.imshow(name, img)
        cv2.waitKey(0)

    def sameColor(self, c1, c2, diff = 0):
        c = (c1-c2)
        #print(c)
        for i in range(len(c)):
            if(abs(c[i]) > diff):
                return False
        return True

    def mse(self, imageA, imageB, xywhA = None, xywhB = None, debug = False):
        if(xywhA != None):
            imageA = imageA[xywhA[1]:xywhA[1]+xywhA[3],xywhA[0]:xywhA[0]+xywhA[2]]
        if(xywhB != None):
            imageB = imageB[xywhB[1]:xywhB[1]+xywhB[3],xywhB[0]:xywhB[0]+xywhB[2]]

        #imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        #imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        if(debug):
            #self.showImage(imageA, "A")
            #self.showImage(imageB, "B")
            pass#print(err)
        return err

    def screenshot(self, path = None):
        if(path == None):
            self.screen = cv2.cvtColor(np.array(pg.screenshot()),  cv2.COLOR_RGB2BGR)
        else:
            try:
                self.screen = cv2.imread(path)
            except:
                print("Invalid Path Given")

    def _grabUltSpace(self):
        def sv(img, xywh, name):
            cv2.imwrite(f"{name}.png", img[xywh[1]:xywh[1]+xywh[3],xywh[0]:xywh[0]+xywh[2]])
            print("saved", name)

        for i, char in enumerate(self.chars):
            j = 0
            while(f"to_save_ultEnergy_{char}_not_full_{j}" in self.images or f"ultEnergy_{char}_not_full_{j}" in self.images):
                print('not :', j)
                if(f"to_save_ultEnergy_{char}_not_full_{j}" in self.images):
                    sv(self.images[f"to_save_ultEnergy_{char}_not_full_{j}"], self.ultPos[i], f"ultEnergy_{char}_not_full_{j}")
                #print(i)
                j += 1
            j = 0
            while(f"to_save_ultEnergy_{char}_full_{j}" in self.images or f"ultEnergy_{char}_full_{j}" in self.images):
                print('is :', j)
                if(f"to_save_ultEnergy_{char}_full_{j}" in self.images):
                    sv(self.images[f"to_save_ultEnergy_{char}_full_{j}"], self.ultPos[i], f"ultEnergy_{char}_full_{j}")
                #print(i)
                j += 1

    def grabAllyUlts(self, debug = False):
        for i, char in enumerate(self.chars):
            #print(char)
            mseFull = 10000000
            mseNotFull = 10000000
            #print(char)
            j = 0
            while(f"ultEnergy_{char}_not_full_{j}" in self.images):
                mseNotFull = min(mseNotFull, self.mse(self.screen, self.images[f"ultEnergy_{char}_not_full_{j}"], xywhA=self.ultPos[i], debug=debug))
                #print(i)
                j += 1
            j = 0
            while(f"ultEnergy_{char}_full_{j}" in self.images):
                mseFull = min(mseFull, self.mse(self.screen, self.images[f"ultEnergy_{char}_full_{j}"], xywhA=self.ultPos[i], debug=debug))
                j += 1
            if(debug):
                print(char, mseFull, mseNotFull)
            self.ults[i] = mseFull < mseNotFull

    def grabSp(self):
        sp = 0
        for i in range(7):
            #print(self.screen[self.spPos[i][1]][self.spPos[i][0]] - self.spColor)
            if(self.sameColor(self.screen[self.spPos[i][1], self.spPos[i][0]], self.spColor, 3)):
                sp = i+1
            else:
                break
        return sp

    def grabEnemyHp(self):
        pass

    def grabEnemyWeakness(self, debug = False):
        weakPos = []
        screen = self.screen[:500, 600:]
        for weak in self.weaknesses:
            try:        
                for pos in pg.locateAll(self.images[f"weakness_{weak}"], screen, grayscale=True, confidence=0.7):
                    weakPos.append([pos[0], pos[1], weak])
                for pos in pg.locateAll(self.images[f"weakness_{weak}_light"], screen, grayscale=True, confidence=0.7):
                    weakPos.append([pos[0], pos[1], weak])
            except Exception as e:
                if(debug):
                    print("not Found", weak, ":", e, self.images[f"weakness_{weak}"].shape, screen.shape)
        #self.showImage(screen)
        weakPos = sorted(weakPos, key=lambda x: x[0])
        #print(weakPos)
        #self.showImage(screen)
        x = -1000
        i = -1
        enemyWeakness = [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]]
        for data in weakPos:
            i += (1 if (data[0] > x + 100) else 0)
            x = data[0]
            enemyWeakness[i][self.weaknesses.index(data[2])] = 1

        return enemyWeakness

    def grabElites(self):
        pass

    def grabActionOrder(self):
        pass

if __name__ == '__main__':
    src = DataGrabber()

    def testUltGrab(num = 1):
        src.screenshot(path=f'{os.getcwd()}/DataGrabber/assets/ultGrabTest/{num}.png')
        src.grabAllyUlts(debug=True)
        print(src.ults)

    def testGrab(num = 1):
        src.screenshot(path=f'{os.getcwd()}/DataGrabber/assets/ultGrabTest/{num}.png')
        src.grabAllyUlts(debug=False)
        sp = src.grabSp()
        weak = src.grabEnemyWeakness(debug=True)
        print(src.ults, f"sp: {sp}")
        for i in range(5):
            print(f"enemy{i} weak to [", end="")
            for j in range(7):
                if(weak[i][j] == 1):
                    print(src.weaknesses[j], end=(", " if j!=6 else ""))
            print("]")

    #testGrab(5)
    for i in range(1, 7):
        testGrab(num = i)
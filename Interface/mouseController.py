import pyautogui as pg

class MouseController():
    def __init__(self):
        self.scrX, self.scrY = pg.size()
        self.initPos()

    def initPos(self):
        def initUltPos():
            self.ultPos = [[self.scrX*277//1920, self.scrY*895//1080], 
                        [self.scrX*505//1920, self.scrY*895//1080], 
                        [self.scrX*729//1920, self.scrY*895//1080], 
                        [self.scrX*955//1920, self.scrY*895//1080]]

        def initBasicPos():
            self.basicPos = [self.scrX*1645//1920, self.scrY*920//1080]

        def initSkillPos():
            self.skillPos = [self.scrX*1800//1920, self.scrY*840//1080]
        
        initBasicPos()
        initSkillPos()
        initUltPos()
        
    def click(self, button = None):
        if(button == "basic"):
            pg.click(x=self.basicPos[0], y=self.basicPos[1])
        elif(button == "skill"):
            pg.click(x=self.skillPos[0], y=self.skillPos[1])
        elif("ult" in button):
            i = int(button[3])
            pg.click(x=self.ultPos[i][0], y=self.ultPos[i][1])
            

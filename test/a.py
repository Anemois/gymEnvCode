from mid.b import B
class hi:
    def __init__(self):
        self.k = 1
        ok = B()
        ok.go()
    
    def cool(self):
        print("HI")
        self.k = 2
    
    def pp(self):
        print(self.k)

x = hi()
x.pp()
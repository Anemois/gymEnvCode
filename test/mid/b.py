from a import hi

class B:
    def __init__(self):
        self.wow = 1
    
    def go(self):
        self.wow = 0
        hi.cool()
        self.wow = 2
        
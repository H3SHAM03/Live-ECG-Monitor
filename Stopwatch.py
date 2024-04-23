import time

class Stopwatch():
    def __init__(self):
        self.StartTime = 0
        self.EndTime = 0
        self.TimePassed = 0

    def start(self):
        self.StartTime = time.time()

    def secondsPassed(self):
        self.EndTime = time.time()
        self.TimePassed = self.EndTime - self.StartTime
        return self.TimePassed
    
    def reset(self):
        self.StartTime = 0
        self.EndTime = 0
        self.TimePassed = 0
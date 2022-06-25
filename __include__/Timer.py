#!/usr/bin/env python3

import time

class Timer:
    
    def start(self):
        self.s = time.time() * 1000
        self.e = 0
        return self
    
    def end(self):
        self.e = time.time() * 1000
        return self
    
    def printLapse(self, mes):
        differ = self.e - self.s
        
        s = (differ / 1000.0) % 60
        
        s = round(int(s), 2)
        
        m = (differ / (1000 * 60)) % 60
        
        m = round(int(m), 2)
        
        h = round((differ / (1000 * 60 * 60)) % 24)
        
        print("{}: Hours:{}, Minute:{}, Seconds:{}".format(mes, h, m, s))

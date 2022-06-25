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
        
        h = (d / (60 * 60))
        m = ((d / 60) % 60)
        s = (d % 60)
        ms = (d % 100)
        
        print("{}: Hours:%02d, Minute:%02d, Seconds:%02%.%03d" % (mes, h, m, s, ms))

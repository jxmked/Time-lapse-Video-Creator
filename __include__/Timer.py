#!/usr/bin/env python3

import time

class Timer:
    
    def start(self):
        self.s = time.time()
        self.e = 0
        return self
    
    def end(self):
        self.e = time.time()
        return self
    
    def printLapse(self, mes):
        print(mes, end=": ")
        print(time.strftime('%H:%M:%S', time.gmtime(self.e - self.s)))

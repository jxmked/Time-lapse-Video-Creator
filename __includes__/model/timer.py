#!/usr/bin/env python3

from time import gmtime, strftime, perf_counter

class Timer:
    def __init__(self):
        self.name = ""
    
    def start(self):
        self.s = perf_counter()
        self.e = 0
        return self
    
    def stop(self):
        self.e = perf_counter()
        return self
    
    def printLapse(self, mes):
        print(mes, end=": ")
        print(strftime('%H:%M:%S', gmtime(self.e - self.s)))

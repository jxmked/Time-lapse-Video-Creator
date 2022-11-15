#!/usr/bin/env python3
# -*- coding UTF-8 -*-
# 
# @Package Name TLVC (Time Lapse Video Creator)
# 
# Main Controller

from Root import Root

from argparse import ArgumentParser as AP



class Controller(Root):
    # Main Child Object
    # Class Name: Main
    
    def __init__(self):
        Command.__init__(self)
      #  LG.__init__(self)
        
        self.logger("Controller", "logll")
        print("From Controller")
        print(self.config)
        
       # self.fs = Failsafe()
       # print(self.__class__.__name__)
        
       # self.execute([])
    

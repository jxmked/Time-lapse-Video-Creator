#!/usr/bin/env python3
# -*- coding UTF-8 -*-
#
# @Package Name TLVC (Time Lapse Video Creator)
# 
# Main Object

#from os import environ
from os.path import dirname
from atexit import register
from Root import Root
#from __includes__.config import Config
#from Controller import Controller
#from __includes__.video import Video

class Main(Root):
    
    __root__ = dirname(__file__)
    
    SYS_ENV = "development"
    
    def __init__(self) -> None:
        pass
     

if __name__ == '__main__':
    Main()
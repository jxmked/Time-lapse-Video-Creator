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
from __includes__.envres import envRes
#from __includes__.config import Config
#from Controller import Controller
from __includes__.video import Video

class Main(Root):
    
    def __init__(self):
        ## dev | prod
        envRes.set("ENV_MODE", "dev")
        envRes.set("ROOT", dirname(__file__))
        
        vid = Video()
        vid.prepareFiles(vid.files)
     



if __name__ == '__main__':
    Main()


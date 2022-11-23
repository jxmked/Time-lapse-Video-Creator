#!/usr/bin/env python3
# -*- coding UTF-8 -*-
#
# @Package Name TLVC (Time Lapse Video Creator)
# 
# Main Object


from os.path import dirname, join
from atexit import register
from Root import Root
from __includes__.envres import envRes
#from __includes__.config import Config
#from Controller import Controller
from __includes__.model.video import Video
from __includes__.model.get_environment import Get_Environment


class Main(Root):
    
    def __init__(self):
        ## dev | prod
        envRes.set("ENV_MODE", "dev")
        envRes.set("logging", [])
        envRes.set("ROOT", dirname(__file__))
        envRes.set("TMP_FOLDER", join(str(envRes.get("ROOT") or "."), "__includes__", "assets", "temp"))
        

        super().__init__()

        # Set Environment
        Get_Environment()


        # Failure to restore name automatically
        # Use the line below to restore it without rerunning the time-lapse video compiler

        # self.failsafe().restore()
        # return

        
        
        
        
        vid = Video()
        vid.prepareFiles(vid.files)
     



if __name__ == '__main__':
    Main()


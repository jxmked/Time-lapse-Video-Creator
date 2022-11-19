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

        # Set Environment
        Get_Environment()


        # return
        # print("Running on Python Version %s" % sys.version)
        ## dev | prod
        envRes.set("ENV_MODE", "dev")

        envRes.set("ROOT", dirname(__file__))
        envRes.set("TMP_FOLDER", join(envRes.get("ROOT"), "__includes__", "assets", "temp"))
        
        vid = Video()
        vid.prepareFiles(vid.files)
     



if __name__ == '__main__':
    Main()


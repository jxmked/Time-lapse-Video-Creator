#!/usr/bin/env python3
# -*- coding UTF-8 -*-

# @Package Name TLVC (Time Lapse Video Creator)

from __includes__.video import Video as VH
from __includes__.audio import Audio as AH
from __includes__.config import Config as CF
from __includes__.notification import Notification as nf

from argparse import ArgumentParser as AP

from os import dirname, environ


class ENV_VAR_HANDLER(object):
    
    def __init__(self):
        pass
    
    def set(self, key, value):
        

class Main(Config):
    
    __root__ = dirname(__file__)
    
    def __init__(self):
        pass
    
CF()

nf = Notification()
nf.error()
nf.success()
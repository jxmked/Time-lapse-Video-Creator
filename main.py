#!/usr/bin/env python3
# -*- coding UTF-8 -*-


# Package Name TLVC (Time Lapse Video Creator)

from __includes__.failsafe import Failsafe as FS
from __includes__.video import Video as VH
from __includes__.audio import Audio as AH
from __includes__.config import Config as CF

from argparse import ArgumentParser as AP

class TimeLapseVideoCreator(object):
    
    def __init__(self):
        pass
    
CF()
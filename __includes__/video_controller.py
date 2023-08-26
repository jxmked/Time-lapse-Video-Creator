#!/usr/bin/env python3
# -*- coding UTF-8 -*-
#
# Video controller
# Handling Models

from Root import Root
from __includes__.envres import Env
from __includes__.model.video import Video


class Video_Controller(Root):
    def __init__(self) -> None:

        self.video: Video = Video()
        self.files: list[str] = []

    def getVideoFiles(self) -> None:

        pass


"""
- Set config to object Initialize from Config parser object
- Validate Config and print and exit the errors if possible

- Initialize video model
- Get files
- Create Video Object
- Hash video filenames
- Create name backups (Failsafe)
- 



"""

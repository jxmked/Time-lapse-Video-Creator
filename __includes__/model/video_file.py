#!/usr/bin/env python3

#import os

from os import system, remove, rename
from os.path import join, basename, dirname, exists
from json import loads
from __includes__.envres import envRes
from __includes__.helpers import createDir

import subprocess
import re



"""
Extract Video Data Using FFMPEGS' FFPROBE
Requires:
    ffmpeg to be installed in your machine
"""

class VideoFile(object):
    
    __valid_types = ["mp4", "mov", "avi"]
    
    def __init__(self, url):
        assert exists(url), "`%s` does not exists" % url
        assert self.__is_valid(url), "`%s` is not available for this %s object" % (url, self.__class__.__name__)
        
        
        self.path = "" # Path to video
        self.filename = "" # Without Path
        self.fileFormat = "" # Extension
        self.basename = "" # Without Path and Extension
        self.trueName = ""
        self.absolutePath = ""
        self.duration = 0 # Seconds
        self.framerate = 0
        self.bitrate = {"video" : 0, "audio" : 0, "file" : 0} # Hertz
        self.bits_per_sample = {"video":0, "audio":0} # Hertz
        self.resolution = {"width" : 0, "height" : 0}
        self.fileSize = 0
        self.codec = {"video" : 0, "audio" : 0}
        
        
        self.data = {} # For storing some internal/external data that belongs to this object
        
        self.renamed = False # Will Triggered If We
        
        self.__tmp_dir = envRes.get("TMP_FOLDER")
        
        # self.__available_streams = []
        
        createDir(self.__tmp_dir)

        self.trueName = url
        
        self.__set_urls(url)
        
        # Extract Stream-Metadata and metadata from main file
        
        self.__get_json_data()
        
        # Get Video stream and store it to self.data
        assert len(self.data["raw_json"]["streams"]) > 0, "No Video Stream Available in '%s'" % url
        
        self.data["streams"] = {}
        
        for stream in self.data["raw_json"]["streams"]:
            if not stream["codec_type"] in self.data["streams"]:
                self.data["streams"][stream["codec_type"]] = []
            
            self.data["streams"][stream["codec_type"]].append(stream)
        
        self.__get_duration()
        self.__get_bitrate()
        self.__get_bits_per_sample()
        self.__get_filesize()
        self.__get_resolution()
        self.__get_codec()
        self.__get_framerate()
    
    def __set_urls(self, url):
        self.absolutePath = url
        
        self.filename = basename(url)
        self.basename = dirname(url)
        self.path = url.replace(self.filename, "")
    
    def rename(self, name, re_set_urls=False):
        
        res = join(self.path, name)
        
        rename(self.absolutePath, res)
        
        if re_set_urls:
            self.__set_urls(res)
        
    
    def __get_duration(self):
        self.duration = float(self.data["raw_json"]["format"]["duration"])
    
    
    def __get_bits_per_sample(self):
        if "video" in self.data["streams"]:
            self.bits_per_sample["video"] = int(self.data["streams"]["video"][0]["bits_per_raw_sample"])
        
        if "audio" in self.data["streams"]:
            self.bits_per_sample["audio"] = int(self.data["streams"]["audio"][0]["bits_per_sample"])
            
    def __get_bitrate(self):
        if "video" in self.data["streams"]:
            self.bitrate["video"] = int(self.data["streams"]["video"][0]["bit_rate"])
        
        if "audio" in self.data["streams"]:
            self.bitrate["audio"] = int(self.data["streams"]["audio"][0]["bit_rate"])
            
        if "bit_rate" in self.data["raw_json"]["format"]:
            self.bitrate["file"] = int(self.data["raw_json"]["format"]["bit_rate"])
        
    def __get_filesize(self):
        self.fileSize = int(self.data["raw_json"]["format"]["size"])
    
    def __get_resolution(self):
        if "video" in self.data["streams"]:
            self.resolution["width"] = self.data["streams"]["video"][0]["width"]
            self.resolution["height"] = self.data["streams"]["video"][0]["height"]
    
    def __get_codec(self):
        if "video" in self.data["streams"]:
            self.codec["video"] = self.data["streams"]["video"][0]["codec_name"]
        
        if "audio" in self.data["streams"]:
            self.codec["audio"] = self.data["streams"]["audio"][0]["codec_name"]
    
    def __get_framerate(self):
        if "video" in self.data["streams"]:
            self.framerate = eval(self.data["streams"]["video"][0]["avg_frame_rate"])
    
    def __is_valid(self, url):
        for ext in self.__valid_types:
            if url.endswith(".%s" % ext):
                self.fileFormat = ext
                return True
        return False
    
    def __get_json_data(self):
        # Using FFPROBE from FFMPEG, 
        # We can extract metadata from media file
        
        tmp:str = join(self.__tmp_dir, "__%s__%s" % (self.__class__.__name__, "Extracted.json"))
        
        cmd:dict = [
            "ffprobe",
            "-v quiet",
            "-show_format",
            "-show_streams",
            "-print_format",
            "json",
            "\"%s\"" % self.absolutePath
        ]

        res:str|None = None

        # --------------------------
        # I tried this but doesn't work in my case. I don't know why
        # Both of this subprocess returns nothing
        # res = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        # res = res.communicate()[0]
        # --------------------------
        
        # --------------------------
        # Even this one 
        # res = subprocess.run(cmd, capture_output=True, text=True)

        # print(res.stdout)

        # print(res.stderr)
        # res = str(res.stdout)[2:-1] # Convert to string then remove b''
        # res = re.sub(r"\\n", r"\n", res) # Fix New Line Character
        # --------------------------
        
        if envRes.get("ENV") == "linux":
        # --------------------------
        # Exract Data from Video and save it as a text file
            cmd.append("&> '%s'" % tmp)

            system(" ".join(cmd))
            
            # Open the file, load the string
            # Close the file and delete
            
            with open(tmp, "r") as file:
                res = file.read()
            
            try:
                remove(tmp)
            except FileNotFoundError:
                pass
        # --------------------------
        else:
        # Having a problem running on Termux

        # Capture stdout from console???
            cmd = " ".join(cmd)
            res = subprocess.run(cmd, capture_output=True, text=True).stdout
        # --------------------------

        self.data["raw_json"] = loads(res)
    
"""

src = "Video In"
x = VideoFile(os.path.join(src, "a.mp4"))


print(x.bitrate["video"])
print(x.bitrate["audio"])

print(x.codec["video"])
print(x.codec["audio"])
"""


# # # # # # ## # # # # # # #
# Written by Jovan De Guia #
# Github Username: jxmked  #
# # # # # # ## # # # # # # #

#!/usr/bin/env python3
# -*- coding UTF-8 -*-


# Import Functions
from __includes__.helpers import *

from __includes__.model.timer import Timer
from __includes__.model.video_file import VideoFile as VF
from __includes__.envres import envRes

from Root import Root

import json
import sys
import os

class Video(Root):
    
    
    def __init__(self):
        super().__init__()
        
        self.objectName = self.__class__.__name__
        
        self.videoPath = os.path.join(self.__root__, "Video In")
        
        self.validTypes = ["mp4", "avi", "mov", "flv", "wma"]
        
        createDir(self.processed)
        createDir(self.videoPath)
        
        self.storage_manager.setObjectName(self.objectName)
        
        if not os.path.isdir(self.videoPath):
            #nf.error()
            raise Exception("%s looks empty" % self.videoPath)
            
        self.files = getFiles(self.videoPath, self.validTypes)
        self.output = "Output" # Output name
        
        self.fs = self.failsafe(self.objectName)
        
        self.timers = {}
        
        self.mergedFile = os.path.join(self.__root__, "__%s_File_To_Merge.txt" % self.objectName)
        
    
    def prepareFiles(self, files):
        
        l = len(files)
        
        if l == 0:
            #nf.error()
            print("No Video Files to merge")
            exit(0)
        
        files = sortThis(files)
        
        """
        We can use this preset and crf for lower output
        files size and better quality (But not always better quality)
        
        `-preset veryslow -crf 26`
            
        use `-ssim 1 -tune ssim -preset veryslow` to get libx264
        to calculate the SSIM visual quality metric, you'll find
        that veryslow has better quality per bitrate than veryfast
            
        More on this link:
            'https://superuser.com/questions/1556953/why-does-preset-veryfast-in-ffmpeg-generate-the-most-compressed-file-compared'
        """
        
        """
        About Output Quality 
        https://superuser.com/questions/677576/what-is-crf-used-for-in-ffmpeg
        https://stackoverflow.com/questions/39473434/ffmpeg-command-for-faster-encoding-at-a-decent-bitrate-with-smaller-file-size
        """
        
        """
        We're not able to use oneline command if we have only 1 to 3 files.
        It may crash the system in some devices due to lack of memory
        """
        
        # Select on option below
        selected = {
            "quality" : "medium", # Select on`quality` option below 
            "format" : "mp4", # Select on `compression` option below
            
            # The slower the better quality
            # `medium` - default
            "preset" : "fast" # https://trac.ffmpeg.org/wiki/Encode/H.264
        }
        
        # Select Quality
        quality = {
            "depend" : {
                "framerate" : "%s", # Frame rate from video File
                "bitrate" : "%s" # Bit Rate From Video File
            },
            "veryhigh" : {
                "framerate" : "60",
                "bitrate" : "8M"
            },
            "high" : {
                "framerate" : "48",
                "bitrate" : "4M"
            },
            "medium" : {
                "framerate" : "30",
                 "bitrate" : "2.5M"
            },
            "default" : {
                "framerate" : "24",
                "bitrate" : "128k"
            },
            "low" : {
                "framerate" : "16",
                "bitrate" : "500k"
            }
        }
        
        # Compressions Option
        compression = {
            "mp4" : {
                "output" : "%s.mp4" % self.output,
                "codec" : "libx264",
                "format" : "mp4",
                "crf" : "23" # Range 0 - 51 # Default 23
            },
            "ts" : {
                "output" : "%s.ts" % self.output,
                "codec" : "libx264",
                "format" : "mpegts",
                "crf" : "23"
            }
        }
        
        vfs = []
        tmp = {}
        
        print("Encoding Filenames")
        """
        Re-encoding filenames to escape some invalid characters 
        from getting to ffmpeg
        """
        ### Create Video File Object for Each Video ###
        
        for index in range(l):
            vfs.append("")
            vfs[index] = VF(os.path.join(self.__root__, self.videoPath, files[index]))
            file = vfs[index]
            
            fname = file.filename
            
            file.data["hashed"] = "_%s_%s.%s" % (self.objectName, md5(file.absolutePath), "mp4")
            
            file.data["tmp_filename"] = os.path.join(self.videoPath, file.data["hashed"])
            file.data["tmp_processed"] = os.path.join(self.processed, file.data["hashed"])
            
            tmp[file.data["hashed"]] = fname
            
            file.rename(file.data["hashed"])
            
            print("  %s -> %s" % (fname, file.data["hashed"]))
        
        self.fs.createBackup("video list", tmp, self.videoPath, self.videoPath)
        
        try:
            ### Remove Duplicated Frames ###
            
            fmerge = []
            for file in vfs:
                # Using this filters will get out of sync with the audio
                # So, it is better to not to include audio to the process. (I mean removing it)
                
                # https://superuser.com/questions/1706239/using-ffmpeg-mpdecimate-to-get-rid-of-exact-duplicate-frames-i-e-losslessly
                #vf = "mpdecimate=hi=64*12:lo=64*5:frac=0.33:max=0"
               
                # https://stackoverflow.com/questions/37088517/remove-sequentially-duplicate-frames-when-using-ffmpeg#answer-52062421
                #vf = "mpdecimate,setpts=N/FRAME_RATE/TB"
                vf = "mpdecimate,setpts=N/%s/TB" % file.framerate
                
                fmerge.append(file.data["tmp_processed"])
                args = {
                    "title": file.filename,
                    "video_filter": vf
                }
                
                if envRes.get("ENV_MODE") == "dev":
                    args["preset"] = "medium"
                    args["execute"] = 1
                
                self.rmDuplicatedFrames(
                    file.data["tmp_filename"],
                    file.data["tmp_processed"],
                    args
                )
            
            ### Video merge ###
            
            fmergeOut = os.path.join(self.processed, "_Raw_merged.mp4")
            
            args = {
                "title": "Merge (%s) files" % l
            }
            
            if envRes.get("ENV_MODE") == "dev":
                args["preset"] = "medium"
                args["execute"] = 1
            
            self.mergeVideos(fmerge, fmergeOut, args)
            
            # Merge Audio And Video
            
        except BaseException as be:
            # For debug only
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Line Error: %s" % exc_tb.tb_lineno)
            print(be)
            exit(0)
    
    
    def finalMerge(self, video, audio, output, conf=None):
        assert isinstance(video, VF), "Input video must be an instance of VideoFile"
        #assert isinstance(audio, AF), "Input audio must be an instance of AudioFile"
        
        conf = (conf if conf else {})
        
        self.cmd.setInput([video.path, audio])
        self.cmd.setOutput(output)
        self.cmd.setTitle(conf.get("title", "Final Merge: Audio Video"))
        self.execute([
            "-c:v '%s'" % conf.get("video_codec", "copy"),
            "-c:a '%s'" % conf.get("audio_codec", "aac"),
            "-q:v 0",
            "-map 0:v"
            "-vf 'setpts=%s*PTS'" % conf.get("multiplier", "0.5"),
            "-r '%s'" % conf.get("video_framerate", "30"),
            "-f '%s'" % conf.get("video_format", "mp4"),
            "-preset '%s'" % conf.get("preset", "medium"),
            
            # https://superuser.com/questions/908295/ffmpeg-libx264-how-to-specify-a-variable-frame-rate-but-with-a-maximum
            "-fps_mode vfr",
            "-pix_fmt yuv420p",
            "-movflags +faststart" # Playable even it is still downloading
        ], conf.get("execute", 1))
        
    
    def mergeVideos(self, files, o, conf):
        # Write text file contains video to merge and feed it in ffmpeg
        # Since, other method does not work 
        # Due to codec, format and etc. 
        
        with open(self.mergedFile, "w") as f:
            f.write("\n".join(["file '%s'" % file for file in files]))
        
        vc = conf.get("video_codec", "libx264") # Codec
        ff = conf.get("video_force_format", "mp4") # Force Formar
        fr = conf.get("video_framerate", "30") # Framerate
        ps = conf.get("video_preset", "medium") # Preset
        ec = conf.get("execute", 1) # Execute Code
        
        self.cmd.setTitle(conf.get("title", "No Title"))
        self.cmd.setOutput(o)
        
        try:
            self.execute([
                # Import File Manually. Required when using concat format
                "-f concat",
                "-safe 0",
                "-i \"%s\"" % self.mergedFile,
                "-an -sn",
                "-fps_mode vfr",
                "-pix_fmt yuv420p",
                "-c:v %s" % vc,
                "-preset %s" % ps,
                "-r %s" % fr,
                "-f %s" % ff,
                
                # https://stackoverflow.com/questions/25569180/ffmpeg-convert-without-loss-quality
                "-q:v 0" # Keep Quality
            ], ec)
        except AssertionError:
            pass
        
        finally:
            try:
                os.remove(self.mergedFile)
            except FileNotFoundError:
                pass
            
        
    def rmDuplicatedFrames(self, i, o, conf):
        """
        Remove duplicated frames
        Using FFMPEG 'mpdecimate,setpts=N/FRAME_RATE/TB' filter
        To eliminate less busy frames
        """
        
        self.cmd.setTitle(conf.get("title", "Remove Duplicated Frame"))
        self.cmd.setInput(i)
        self.cmd.setOutput(o)
        
        # Remove Duplicated Frame
        vf = conf.get("video_filter", "mpdecimate,setpts=N/FRAME_RATE/TB")
        vc = conf.get("video_codec", "libx264") # Codec
        ff = conf.get("video_force_format", "mp4") # Force Formar
        fr = conf.get("video_framerate", "30") # Framerate
        ps = conf.get("video_preset", "medium") # Preset
        ec = conf.get("execute", 1) # Execute Code
        
        self.execute([
            "-an -sn",
            "-vf '%s'" % vf,
            "-c:v '%s'" % vc,
            "-f '%s'" % ff,
            "-write_xing 0 -id3v2_version 0", # Remove Metadata
            "-map_metadata -1", # Remove Metadata
            
            "-r %s" % fr,
            
            # https://stackoverflow.com/questions/25569180/ffmpeg-convert-without-loss-quality
            "-q:v 0", # Keep Video Quality
                    
            # https://superuser.com/questions/908295/ffmpeg-libx264-how-to-specify-a-variable-frame-rate-but-with-a-maximum
            "-fps_mode vfr",
            "-pix_fmt yuv420p",
            "-movflags +faststart", # Playable even it is still downloading
            
            # For Development Mode
            "-preset %s" % ps
        ], ec)



"""

obj = Video()
obj.prepareFiles(obj.files)



print("\n" * 4)



for log in obj.cmd.getLogs():
    (state, arg) = log
    print("State: %s\nQuery: %s" % (state, arg))
    print()
"""
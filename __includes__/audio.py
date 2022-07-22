#!/usr/bin/bash python3
# -*- coding UTF-8 -*-

import os

# Import Functions
from __includes__.Controller import Controller
from __includes__.helpers import *

class Audio(Controller):
    def __init__(self):
        self.audioPath = "Audio In"
        self.validTypes = ["wav", "mp3", "ogg", "wma", "aac"]
        super().__init__(self.__class__.__name__)
        if not os.path.isdir(self.audioPath):
            createDir(self.audioPath)
            self.notif.error()
            raise Exception("%s looks empty" % self.audioPath)
        
        self.files = getFiles(self.audioPath, self.validTypes)
        
        self.processed = "__Resources__"
        self.output = "Output" # Name
        self.config = {
            "silenceremove" : {
                "start_periods" : 1,
                "start_silence" : 0.1,
                "start_threshold" : "-50dB"
            },
            "crossfading" : {
                "duration" : 0
            },
            "fading" : {
                "in" : 0,
                "out" : 0
            },
            "shortcut" : 1
        }
        
    def prepareFiles(self, files):
        
        l = len(files)
        
        if l == 0:
            self.notif.error()
            print("No Audio Files to merge")
            exit(0)
        
        # Store 
        tmp = {} # Backup Filenames
        im = [] # To Import
        ib = [] # No Absolute Path
        
        files = sortThis(files)
        
        print("Encoding Filenames")
        for file in files:
            
            gh = "_%s_%s" % (self.__class__.__name__, md5(file))
            
            tmp[gh] = file
            
            x = os.path.join(self.audioPath, file)
            y = os.path.join(self.audioPath, gh)
            z = os.path.join(self.processed, gh)
            
            im.append(y)
            ib.append(z)
            os.rename(x, y)
            
            print("  %s -> %s" % (file, gh))
        
        # Steps: Remove Silences, Concat with crossfade, add fading from 
        #    start and before end.
        # Fail at: Executing them all at once with lots of file due to out of memory error.
        # Fail at: Large amount of inputs. Automatically terminating the terminal
        
        selected = "mp3" # Output
        
        selection = {
            "mp3" : { # Best For Final Output. <Size >Speed ~Quality
                "filename" : "%s.mp3" % self.output,
                "codec" : "libmp3lame",
                "forceformat" : "mp3"
            },
            "wav" : { # Best for resourcing. >Size <Speed  <Quality
                "filename" : "%s.wav" % self.output,
                "codec" : "pcm_s16le",
                "forceformat" : "wav"
            },
            "aac" : { # Best for IDK (I don't know. Nothing special). <Size >Speed ~Quality
                "filename" : "%s.aac" % self.output,
                "codec" : "aac",
                "forceformat" : "aac"
            }
        }
        
        self.output = selection[selected]["filename"]
        
        try:
            # Remove Silence from both end of an audio file
            # : Delete after creating bundle
            
            # Incase of unexpected termination which is I experience
            # run `python3 main.py --failsafe` to restore filenames
            self.fs.createBackup("audio list", tmp, self.audioPath, self.audioPath)
            
            createDir(self.processed)
            
            # We cannot escape 1 audio file
            if l == 1 or (self.config['shortcut'] and l <= 3):
                # Set and start timer
                self.timers[0] = Timer()
                self.timers[0].name = "Bundle"
                self.timers[0].start()
                
                self.cmd.setInput(im)
                self.cmd.setOutput(self.output)
                self.execute([
                    "-vn -sn",
                    "-filter_complex '%s'" % self.onlyFor(l),
                    "-map [final]",
                    "-write_xing 0 -id3v2_version 0", # Remove Metadata
                    "-c:a '%s'" % selection[selected]["codec"],
                    "-f '%s'" % selection[selected]["forceformat"],
                    "-max_muxing_queue_size 1024",
                ])
                
                self.timers[0].stop()
            else:
                # I tested it with 30 regular mp3 files and it works fine
                # But I tried 117 files and it crashed. I suspect it in Memory 
                i = 0
                for file in tmp:
                    # Remove Silence from both end
                    
                    self.timers[i] = Timer()
                    self.timers[i].name = tmp[file]
                    self.timers[i].start()
                    
                    # Output it as wav format for fast processing
                    self.cmd.setInput(os.path.join(self.audioPath, file))
                    self.cmd.setOutput(os.path.join(self.processed, file))
                    self.execute([
                        "-vn -sn",
                        "-filter_complex '%s'" % self.createSilenceRemoveFilter(1),
                        "-map [aa]",
                        "-acodec pcm_s16le",
                        "-write_xing 0 -id3v2_version 0", # Remove Metadata
                        "-f wav" ,
                    ])
                    
                    self.timers[i].stop()
                    i += 1
                
                cf = self.createCrossfadeFilter(l - 1)
                fio = self.createFadingFilter("c%s" % createID(l - 1))
                
                self.timers["merging"] = Timer()
                self.timers["merging"].name = "Merging"
                self.timers["merging"].start()
                
                self.cmd.setInput(ib)
                self.cmd.setOutput(self.output)
                self.execute([
                    "-vn -sn",
                    "-max_muxing_queue_size 8",
                    "-filter_complex '%s;%s'" % (cf, fio),
                    "-map [final]",
                    "-map_metadata -1", # Remove Metadata
                    "-c:a '%s'" % selection[selected]["codec"],
                    "-f '%s'" % selection[selected]["forceformat"],
                ])
                
                self.timers["merging"].stop()
                
            
            print("")
            print("---" * 9)
            print("Final Merge Audio File is Ready.")
            print("")
            print("%s file(s) has been merged" % l)
            print("---" * 9)
            print("")
            
            nf.success()
        
        except BaseException as ex:
            
            print("\nError: ")
            print("")
            print(ex)
            print("")
            
            nf.error()
        
        finally:
            self.clear(tmp)
            
    def clear(self, arr):
        print("---" * 9)
        for file in arr:
            afile = os.path.join(self.processed, file)
            os.remove(afile)
            print(" Temporary file '%s' has been deleted." % file)
        print("---" * 9)
    
    ## Filter Builder ##
    
    def onlyFor(self, cnt):
        # Only from 1 to 3 files...
        srf = self.createSilenceRemoveFilter(cnt)
        if cnt == 1:
            return "%s;%s" % ( srf, self.createFadingFilter(createID(1)))
        else:
            return "%s;%s;%s" % ( srf, 
                self.createCrossfadeFilter(cnt - 1, True),
                self.createFadingFilter("c%s" % createID(cnt - 1))
            )
    
    def createSilenceRemoveFilter(self, cnt):
        pat = "{0},{1},{0},{1}".format(
            "silenceremove=start_periods=%s:start_silence=%s:start_threshold=%s" % (
                self.config["silenceremove"]["start_periods"],
                self.config["silenceremove"]["start_silence"],
                self.config["silenceremove"]["start_threshold"]
            ),
            "areverse"
        )
        
        res = []
        for i in range(cnt):
            res.append("[{0}]{1}[{2}]".format(i, pat, createID(i + 1)))
        
        return ";".join(res)
    
    def createCrossfadeFilter(self, cnt, useId=False):
        pat = "acrossfade=d={0}:c1=tri:c2=tri".format(
            self.config["crossfading"]["duration"]
        )
        
        res = []
        
        for i in range(0, cnt):
            if i == 0:
                a1 = (createID(1) if useId else "0:a")
            else:
                a1 = "c%s" % createID(i) # First Audio
            
            a2 = (createID(i + 2) if useId else "%s:a" % (i + 1))
            
            res.append(
                "[{0}][{1}]{2}[c{3}]".format(a1, a2, pat,
                    (createID(i + 1))
                )
            )
        
        return ";".join(res)
    
    def createFadingFilter(self, cid):
        return "[{0}]{1}[final]".format(
            cid,
            "{0},{1},{2},{1}".format(
                ("afade=st=0:d=%s" % self.config["fading"]["in"]),
                "areverse",
                ("afade=st=0:d=%s" % self.config["fading"]["out"]),
            )
        ) 
    

"""
obj = Audio()

obj.prepareFiles(obj.files)

#print(obj.onlyFor(3))

if len(obj.files) > 0:
    for i in obj.timers:
        i = obj.timers[i]
        
        i.printLapse(i.name)
    
"""
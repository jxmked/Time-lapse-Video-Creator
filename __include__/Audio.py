#!/usr/bin/env python3

from os import path, listdir, mkdir

class Audio:
    
    config = {
        "fadeIn" : 5,
        "fadeOut" : 5,
        "crossFade" : 10
    }
    
    def __init__(self):
        self.fInput = "Audio In"
        self.fTrimmed = "Audio Ready File"
        self.fOutput = "Resource Out"
        self.xtl = {}
        self.execute = {}
        self.validFormats = ["mp3", "wav", "aac", "ogg", "wma", "flac"]
        
    def start(self, arg):
        
        self.rawFiles = self.xtl.getFiles(self.xtl.joinPath(self.fInput, ""), self.validFormats)
        self.initTrimMerge(self.rawFiles)
        self.addFadeFilter()
    
    def addFadeFilter(self):
        fname = "merge.wav"
        fpath = self.xtl.joinPath(self.fOutput, fname)
        
        if not self.xtl.fileExists(fpath):
            raise Exception("Audio File %s does not exists" % fpath)
        
        self.aLen = self.xtl.getAudioLength(fpath)
        
        self.execute([
            "-i '%s'" % fpath,
            
            # Set Fading Filter
            "-af 'afade=t=in:st=0:d={},afade=t=out:st={}:d={}'".format(self.config["fadeIn"], self.aLen - self.config["fadeOut"], self.config["fadeOut"]),
            
            "-vn -sn", # Disable Video and Subtitle
            
            "'%s'" % self.xtl.joinPath(self.fOutput, "ReadyToMergeWithVideo.wav")
        ])
    
    
    def initTrimMerge(self, files):
        if len(files) == 0:
            print("No Available Audio to Trim.\nExit...")
            exit(0)
        
        for file in files:
            tmp = self.xtl.getTmpFname()
            tmp = self.xtl.joinPath(self.fInput, tmp)
            tmp += ".%s" % self.xtl.getExt(file)
            
            self.xtl.rename(file, tmp)
            
            try:
                self.execute([
                    ("-i '%s'" % tmp), # Input file
                    "-acodec pcm_s16le", # Audio Codec
                    
                    #"-ar 41000", # Bitrate
                    
                    "-vn -sn", # Disable Video and Subtitle
                    
                    # Set Filter| Trim Both end when Silence
                    "-af 'silenceremove=start_periods=1:start_silence=0.1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_silence=0.1:start_threshold=-50dB,areverse'",
                    
                    # Output
                    ("'%s.wav'" % self.xtl.joinPath(self.fTrimmed, self.xtl.filename(file)))
                ])
            except Exception as err:
                raise Exception(err)
            finally:
                self.xtl.rename(tmp, file)
        
        if len(files) == 1:
            # Since, we have single file...
            
            x = self.xtl.joinPath(self.fTrimmed, ("%s.wav" % self.xtl.filename(files[0])))
            y = self.xtl.joinPath(self.fOutput, "merge.wav")
            self.xtl.copyFile(x, y)
            return 0
        
        # For morethan 1 audio files
        toMerge = {} # To put back audio files previous name
        inp = [] # Input file
        for file in files:
            tmp = self.xtl.getTmpFname()
            tmp = self.xtl.joinPath(self.fTrimmed, tmp)
            tmp += ".%s" % self.xtl.getExt(file)
            
            x = self.xtl.joinPath(self.fTrimmed, self.xtl.filename(file))
            
            self.xtl.rename(x + ".wav", tmp)
            toMerge[tmp] = x
            
            inp.append("-i '%s'" % tmp)
        
        try:
            self.execute([
                #Input files
                ("%s" % (" ".join(inp))),
                
                "-vn -sn", # Disable Video and Subtitle
                
                # Crossfade filter
                self.createCrossFadeFilter(len(files)),
                
                ("'%s'" % (self.xtl.joinPath(self.fOutput, "merge.wav")))
            ])
        except Exception as err:
            raise Exception(err)
        finally:
            for key in toMerge:
                self.xtl.rename(key, toMerge[key])
        
    
    def createCrossFadeFilter(self, count):
        if count == 1:
            raise Exception("Unable to create Crossfade with 1 media file")
            
        x = 2
        y = 97
        
        res = "[0][1]acrossfade=d={}:c1=tri:c2=tri".format(self.config["crossFade"])
        
        for i in range(2, count):
            res += "[{}];[{}][{}]acrossfade=d={}:c1=tri:c2=tri".format(chr(y), chr(y), x, self.config["crossFade"])
            y += 1
            x += 1
        
        return ("-filter_complex '%s'" % res)
    
    def createInlineImport(self, files):
        arr = []
        for file in files:
            arr.append("-i %s" % file)
        
        return " ".join(arr)
    
    def fading(self, param):
        self.config['fadeOut'] = self.isValid(param, "Fade")
        self.config['fadeIn'] = self.isValid(param, "Fade")
        pass
    
    
    def fadeIn(self, param):
        self.config['fadeIn'] = self.isValid(param, "Fade")
        pass
    
    def fadeOut(self, param):
        self.config['fadeOut'] = self.isValid(param, "Fade")
        pass
    
    def isValid(self, num, t):
        try:
            num = int(num)
        except:
            raise Exception("%s value must an integer" % t)
            
        if num >= 1 and num <= 20:
            return num
        
        raise Exception("%s duration '%d' is not valid" % (t, num))
    
    
    def setCrossFadeDuration(self, param):
        self.config["crossFade"] = self.isValid(param, "Crossfade")
        pass
    
    def initialize(self):
        # Check if Folder Exists
        self.xtl.createDir(self.fInput)
        self.xtl.createDir(self.fOutput)
        self.xtl.createDir(self.fTrimmed)
    
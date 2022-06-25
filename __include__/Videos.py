#!/usr/bin/env python3

class Videos:
    
    config = {
        "fadeIn" : 5,
        "fadeOut" : 5,
        "crossFade" : 10
    }
    
    
    def __init__(self):
        self.fInput = "Video In"
        self.fDuplicatedRemoved = "Video Duplicated Frame Removed"
        self.fOutput = "Resource Out"
        self.xtl = {}
        self.execute = {}
        self.mergedFilename = "merge.mp4"
        self.validFormats = ["mp4", "avi", "mov", "flv", "wma"]
       
        self.CONF = {
            "removeDuplicatedFrames" : {
                "frame_rate" : 24,
                "video_codec" : "libx264",
                "force_format" : "mp4"
            }
        }
        
    
    def start(self, arg):
        self.rawFiles = self.xtl.getFiles(self.fInput, self.validFormats)
        
        if len(self.rawFiles) == 0:
            print("No Available Videos to Compile.\nExit...")
            exit(0)
        
        self.initRemoveDuplicatedFrames(arg)
        
        files = []
        for inf in self.rawFiles:
            res = self.xtl.joinPath(self.fDuplicatedRemoved, self.xtl.basename(inf))
            files.append(res)
        
        self.mergeVideoFromDuplicatedFrames(files)
        
        merged = self.xtl.joinPath(self.fOutput, self.mergedFilename)
        if not self.xtl.fileExists(merged):
            raise Exception("File %s not found" % merged)
        
        self.vLen = self.xtl.getVideoLength(merged)
        
        self.aLen = self.A.aLen
        
        # Speed up the video until the duration is same as audio file
        
        self.execute([
            "-i '%s'" % merged,
            
            # Fast Forward Filter and Fade In and Out
            "-filter:v 'setpts={}*PTS,fade=t=in:st=0:d={},fade=t=out:st={}:d={}'".format(
                    self.aLen / self.vLen,
                    self.config['fadeIn'],
                    self.aLen - self.config['fadeOut'],
                    self.config['fadeOut']
                ),
            "-an -sn",
            
            # Frame Rate and Bitrate
            "-r 30 -b:v 4M",
            
            "'{}'".format(self.xtl.joinPath(self.fOutput, "ReadyToMergeWithAudio.mp4"))
        ])
        
        # Final Merge
        self.mergeAudioVideo()
        
    def mergeAudioVideo(self):
        self.execute([
            # Ready Video
            ("-i '%s'" % self.xtl.joinPath(self.fOutput, "ReadyToMergeWithAudio.mp4")),
            # Ready Audio
            ("-i '%s'" % self.xtl.joinPath(self.fOutput, "ReadyToMergeWithVideo.wav")),
            
            #"-c:v libx264",
            "-c:v copy",
            "-c:a aac",
            #"-b:v 4M",
            #"-b:a 44000",
            
            "'Output.mp4'"
        ])
    
        
    def initRemoveDuplicatedFrames(self, arg):
        if not arg:
            # If executed from flag, It will fetch all valid files from input video folder
            self.rawFiles = self.xtl.getFiles(self.fInput, self.validFormats)
            
            if len(self.rawFiles) == 0:
                print("No Available Videos to Compile.\nExit...")
                exit(0)
            
        for file in self.rawFiles:
            # We need to switch the current filename into
            # Something different to prevent 'no file' error for some cases
            
            orig = self.xtl.basename(file)
            
            tmp = "%s.%s" % (self.xtl.getTmpFname(), self.xtl.getExt(orig))
            tmpPath = self.xtl.joinPath(self.fInput, tmp)
            
            self.xtl.rename(file, tmpPath)
            
            # Output path
            out = self.xtl.joinPath(self.fDuplicatedRemoved, orig)
            
            # Init Duplicate Frames Remover
            self.removeDuplicatedFrames(tmpPath, out)
            
            # Put back the original name
            self.xtl.rename(tmpPath, file)
        
        if not arg:
            # If we call from argument
            # Just do the job
            print("Done")
            exit(0)
            
    def removeDuplicatedFrames(self, path, out):
        self.execute([
            "-i '{}'".format(path), # Input file
            
            # Video Codec
            "-c:v libx264",
            
            # Apply filter. Remove Close/Same Frame
            "-vf mpdecimate,setpts=N/FRAME_RATE/TB",
            
            # Disable Audio. Since the output is not sync
            "-an",
            
            "-sn", # Disable Subtitle
            
            # Frame Rate output
            "-r 24",
            
            # Force Output Format
            "-f mp4",
            
            #  I forgot but this is important
            "-movflags +faststart",
            
            "'{}'".format(out) # Output File
        ])
    
    def arg_Merge(self):
        pass
        
        
        
    def mergeVideoFromDuplicatedFrames(self, files):
        if len(files) == 0:
            print("No Available Videos to Compile.\nExit...")
            exit(0)
        
        # Sort files according to it filename to make sure
        # that we merge the videos in their corresponding arrangement
        files.sort()
        
        # Create Txt file for concat
        fname = "toMerge.txt"
        toMerge = []
        
        tmp = {}
        for file in files:
            absPath = self.xtl.joinPath(self.xtl.rmBasename(file), self.xtl.getTmpFname())
            absPath += ".{}".format(self.xtl.getExt(file))
            
            self.xtl.rename(file, absPath)
            toMerge.append("file '%s'" % absPath)
            
            # Backup filename
            tmp[absPath] = file
            
        f = open(fname, "w")
        f.write("\n".join(toMerge))
        f.close()
        
        out = self.xtl.joinPath(self.fOutput, self.mergedFilename)
        
        self.execute([
            # Force format
            "-f concat",
            
            # concat demuxer safe mode option
            "-safe 0",
            
            # List of video in txt file to merge
            ("-i '%s'" % (fname)),
            
            # Disable Audio and Subtitle
            "-an -sn",
            
            # Codec
            "-c copy",
            
            # Output file
            ("'%s'" % out) 
        ])
        
        for key in tmp:
            self.xtl.rename(key, tmp[key])
        
        self.xtl.deleteFile(fname)
        
        
    def fading(self, param):
        self.config['fadeOut'] = self.isValid(param)
        self.config['fadeIn'] = self.isValid(param)
        pass
    
    
    def fadeIn(self, param):
        self.config['fadeIn'] = self.isValid(param)
        pass
    
    def fadeOut(self, param):
        self.config['fadeOut'] = self.isValid(param)
        pass
    
    def isValid(self, num):
        try:
            num = int(num)
        except:
            raise Exception("Fading value must an integer")
            
        if num >= 1 and num <= 20:
            return num
        
        raise Exception("Fading duration '%d' is not valid" % num)
    
    def initialize(self):
        # Check if Folder Exists
        self.xtl.createDir(self.fInput)
        self.xtl.createDir(self.fOutput)
        self.xtl.createDir(self.fDuplicatedRemoved)
    
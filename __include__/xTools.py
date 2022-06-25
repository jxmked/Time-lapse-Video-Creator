#!/usr/bin/env python3


import os
import pathlib
import secrets
import soundfile
import shutil
import subprocess

class xTools:
    
    @staticmethod
    def createDir(path):
        try:
            os.mkdir(path, 0o777)
        except:
            pass
    
    @staticmethod
    def getFiles(path, t):
        
        if not os.path.isdir(os.path.join(path, "")):
            print("`%s` does not exists." % path)
            print("Please execute `-init` or `-i` first.")
            exit(0)
        
        if t == "any":
            return os.listdir(path)
        files = os.listdir(path)
        
        tmp = []
        
        for file in files:
            ext = pathlib.Path(file).suffix[1::].lower()
            
            if ext in t:
                tmp.append(os.path.join(path, file))
            
        return tmp
    
    @staticmethod
    def getExt(name):
        # return extension
        return pathlib.Path(name).suffix[1::].lower()
        
    @staticmethod
    def getTmpFname():
        return secrets.token_hex(15)
    
    @staticmethod
    def basename(path):
        # Return filename.ext
        return os.path.basename(path)
    
    @staticmethod
    def rename(x, y):
        os.rename(str(x), str(y))
        
    @staticmethod
    def joinPath(x, y):
        return os.path.join(x, y)
    
    @staticmethod
    def deleteFile(path):
        os.remove(path)
    
    @staticmethod
    def filename(path):
        return os.path.splitext(os.path.basename(path))[0]
        
    @staticmethod
    def rmBasename(path):
        return pathlib.Path(path).parent.resolve()
    
    @staticmethod
    def getAudioLength(path):
        sfw = soundfile.SoundFile(path)
        return (sfw.frames / sfw.samplerate)
    
    @staticmethod
    def copyFile(f, t):
        # Dont need timestamp to preserve at this tiem
        shutil.copyfile(f, t)
    
    @staticmethod
    def fileExists(path):
        return os.path.exists(path)
    
    @staticmethod
    def getVideoLength(filename):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return float(result.stdout)
    
    @staticmethod
    def isInTermux():
        return subprocess.check_output(['uname', '-o']).strip() == b'Android'
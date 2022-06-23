#!/usr/bin/env python3

import os
import time
import base64
import subprocess
import soundfile

# --- Timer --- #
class Timer:
    
    def start(self):
        self.s = time.time() * 1000
        return self
    
    def end(self):
        self.e = time.time() * 1000
        return self
    
    def printLapse(self, m):
        print("{}: {:.2f}ms".format(m, self.e - self.s))

# !--- Timer ---! #

class Main:
    inputFolder = "in/"
    outputFolder = "out/"
    audioIn = "AudioIn/"
    
    
    # System Varibles
    TMP = ".tmp"
    
    def __init__(self):
        self.inputFiles = os.listdir(self.inputFolder)
        
        # Remove Duplicated Frames
        for file in self.inputFiles:
            x = "{}{}".format(self.inputFolder, file)
            y = "{}{}".format(self.outputFolder, file)
            
            os.system("ffmpeg -i {} -c:v libx264 -vf mpdecimate,setpts=N/FRAME_RATE/TB -an -sn -r 24 -f mp4 -movflags +faststart -y {}".format(x,y))
        
        # Merge 
        self.outpuFiles = os.listdir(self.outputFolder)
        
        self.outpuFiles.sort()
        
        toMerge = []
        for file in self.outpuFiles:
            toMerge.append("file {}{}".format(self.outputFolder, file))
        
        
        f = open("VideoToMerge.txt", "w")
        f.write("\n".join(toMerge))
        f.close()
        
        os.system("ffmpeg -f concat -safe 0 -i {} -an -sn -c copy -y merge.mp4".format("VideoToMerge.txt"))
        
        self.vLen = self.get_length("merge.mp4")
        
        self.processAudio()
        
        # Set Video Duration into the length of an audio file
        os.system("ffmpeg -i merge.mp4 -filter:v 'setpts={}*PTS' -r 30 -an -c:v libx264 -b:v 4M -y noAudio.mp4".format(self.aLen / self.vLen))
        
        # Adding Fading Filter
        os.system("ffmpeg -i noAudio.mp4 -vf 'fade=t=in:st=0:d=10,fade=t=out:st={}:d=5' -y FadingAdded.mp4".format(self.aLen - 5))
        
        # Final Merge 
        os.system("ffmpeg -i FadingAdded.mp4 -i out.wav -c:v copy -c:a aac Output.mp4")
        
    
    def processAudio(self):
        arr = os.listdir(self.audioIn)
        
        # Covert to Wav and Remove Silence in Both Ends
        for x in arr:
            os.system("ffmpeg -y -i AudioIn/{} -acodec pcm_s16le -ar 44100 -af 'silenceremove=start_periods=1:start_silence=0.1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_silence=0.1:start_threshold=-50dB,areverse' -vn AudioOut/out.wav".format(x))
            break
        
        sfw = soundfile.SoundFile("AudioOut/out.wav")
        
        self.aLen = (sfw.frames / sfw.samplerate)
        
        # Add Fade In - Out 
        os.system("ffmpeg -i AudioOut/out.wav -af 'afade=t=in:st=0:d=5,afade=t=out:st={}:d=5' -y out.wav".format(self.aLen - 5))

    
    def get_length(self, filename):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return float(result.stdout)
        
    
    

obj = Main()

print("\n\n")
print(obj.vLen)
print(obj.aLen)


## This is a Beta Version 1.0

"""
Author: Jovan De Guia
Github Username: jxmked
"""

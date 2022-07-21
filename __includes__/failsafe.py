#!/usr/bin/env python3

from os import remove, rename
from os.path import join, isfile, exists, dirname
from json import dumps, loads

from atexit import register as aeRegister

"""
This Object is Self Dependency So Running It Directly is Possible.
 Just for your needs. Hahaha
"""

from __includes__.helpers import slugify, getFiles, createDir

class Failsafe:
    """
    Reverse modified filenames from unexpected exit
    """
    __prename = "__failsafe_"
    __bk_dir = "__includes__/assets/Failsafe"
    __flag = False
    __rData = []
    
    def __init__(self, appname="Runtime"):
        self.appname = slugify(appname)
        
        self.preName = join(self.__bk_dir, self.__prename)
        self.preName = self.joinNames(self.preName, self.appname)
        
        createDir(self.__bk_dir)
        
        self.noAutoFix = False
        
        # Call before exit
        aeRegister(self.checkCalls)
        
    
    def createBackup(self, name, jdata, sourceIn, sourceOut):
        name = slugify(name)
        
        absPath = self.joinNames(self.preName, name) + ".json"
        
        try:
            obj = {
                "data" : dumps(jdata),
                "input" : sourceIn,
                "output" : sourceOut
            }
            
            with open(absPath, "w") as f:
                f.write(dumps(obj))
            
            self.__rData.append(absPath)
            self.__flag = True
            
        except BaseException as be:
            print("- " * 10, end="-\n")
            print("Error: ")
            print(be)
            print("\nUnable to create Backup.")
            print("Safe Exit.")
            exit(0)
        
    
    def restore(self):
        """
        Get all files from backup directory
        then restore names and delete the backup file
        """
        arr = []
        err = []
        files = getFiles(self.__bk_dir, ["json"])
        
        assert len(files) > 0, "No backup file found"
        
        for file in files:
            try:
                absPath = join(self.__bk_dir, file)
                data = None
                with open(absPath, 'r') as f:
                    datas = loads(f.read())
                    parsed = loads(datas["data"])
                
                if self.runRestore(datas, parsed, arr, err):
                    print("Unable to delete %s. Error occur." % file)
                    continue
                
                remove(absPath)
            
            except BaseException as be:
                print("Exception Caught while fetching json file.")
                print("Exception: %s" % be)
            
        self.printErrs(arr, err)
        
        if len(err) == 0 and len(arr) == 0:
            print("Restore Complete")
        
    
    def checkCalls(self):
        if self.noAutoFix:
            return 0
        
        if self.__flag:
            arr = []
            err = []
            hasError = False
            
            for fname in self.__rData:
                data = None
                with open(fname, "r") as f:
                    datas = loads(f.read())
                    parsed = loads(datas["data"])
                
                if not self.runRestore(datas, parsed, arr, err):
                    remove(fname)
            
            self.printErrs(arr, err)
            
        
    def printErrs(self, arr, err):
        if len(arr) > 0:
            print("\nFiles doesn't exists:")
            
            for f in arr:
                print("\t%s" % f)
            
        if len(err) > 0:
            print()
            print("- " * 10, end="-\n")
            print("Error caught while checking temporary files:")
            
            for f in err:
                print("  Current Key: %s" % f["current_key"])
                print("  Current Value: %s" % f["current_value"])
                print("  Error Caught: %s" % f["error"])
                print("")
            
        
    
    def runRestore(self, datas, parsed, arr=[], err=[]):
        hasError = False
        
        for key, data in parsed.items():
            
            # Original Names
            absIn = join(datas["input"], data)
            absOut = join(datas["output"], data)
            
            # Temp Names
            _absIn = join(datas["input"], key)
            _absOut = join(datas["output"], key)
            
            hasError = False
            
            try:
                
                # Attempting to fix if there was an error
                
                if isfile(_absOut):
                    # Error. Temp file should not exists after processing
                    if not exists(dirname(absOut)):
                        absOut = data
                    
                    rename(_absOut, absOut) # Try to rename
                
                if isfile(_absIn):
                    # Error. Temp file should not exists after processing
                    if not isfile(dirname(absIn)):
                        absIn = data
                    
                    rename(_absIn, absIn) # Try to rename
                
            except BaseException as ex:
                hasError = True
                err.append({
                    "current_key" : key,
                    "current_value" : data,
                    "error" : ex
                })
            
        
        return hasError
    
    def joinNames(self, *args):
        return "_".join(args)
    

if __name__ == "__main__":
    obj = Failsafe()
    obj.restore()
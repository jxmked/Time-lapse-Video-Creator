#!/usr/bin/env python3

from os import remove, rename
from os.path import join, isfile, exists, dirname
from json import dumps, loads

from atexit import register as aeRegister

"""
This Object is Self Dependency So Running It Directly is Possible.
just for your needs.
"""

BK_DIR:str = "__includes__/assets/Failsafe"

try:
    from __includes__.helpers import slugify, getFiles, createDir
except:
    from sys import path
    path.append("../")
    from helpers import slugify, getFiles, createDir

    BK_DIR = "../assets/Failsafe"

class Failsafe:
    """
    Reverse modified filenames from unexpected exit
    """
    __prename:str = "__failsafe_"
    __bk_dir:str = BK_DIR
    __flag:bool = False
    __rData:list = []

    def __init__(self, appname:str="Runtime") -> None:
        self.appname:str = slugify(appname)
        
        self.preName:str = join(self.__bk_dir, self.__prename)
        self.preName = self.joinNames(self.preName, self.appname)
        
        createDir(self.__bk_dir)
        
        self.noAutoFix:bool = False
        
        # Call before exit
        aeRegister(self.checkCalls)
        
    
    def createBackup(self, name:str, jdata:dict, sourceIn:str, sourceOut:str) -> None:
        name = slugify(name)
        
        absPath:str = self.joinNames(self.preName, name) + ".json"
        
        try:
            obj:dict[str, str] = {
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
        
    
    def restore(self) -> None:
        """
        Get all files from backup directory
        then restore names and delete the backup file
        """
        arr:list[str] = []
        err:list[dict[str, str|BaseException]] = []
        files:list[str] = getFiles(self.__bk_dir, ["json"])
        
        if len(files) == 0:
            print("No backup file found")
            return
        
        for file in files:
            try:
                absPath:str = join(self.__bk_dir, file)
                
                with open(absPath, 'r') as f:
                    datas:dict = loads(f.read())
                    parsed:dict = loads(datas["data"])
                
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
        
    
    def checkCalls(self) -> None:
        if self.noAutoFix:
            return None
        
        if self.__flag:
            arr:list[str] = []
            err:list[dict[str, str|BaseException]] = []
            
            for fname in self.__rData:
                
                with open(fname, "r") as f:
                    datas:dict = loads(f.read())
                    parsed:dict = loads(datas["data"])
                
                if not self.runRestore(datas, parsed, arr, err):
                    remove(fname)
            
            self.printErrs(arr, err)
            
        
    def printErrs(self, arr, err) -> None:
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
            
        
    
    def runRestore(self, datas, parsed, arr:list[str]=[], err:list[dict[str, str|BaseException]]=[]) -> bool:
        hasError:bool = False
        
        for key, data in parsed.items():
            
            # Original Names
            absIn:str = join(datas["input"], data)
            absOut:str = join(datas["output"], data)
            
            # Temp Names
            _absIn:str = join(datas["input"], key)
            _absOut:str = join(datas["output"], key)
            
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
    Failsafe().restore()



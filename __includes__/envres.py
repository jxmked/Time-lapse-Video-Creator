#!/usr/bin/env python3
# -*- coding UTF-8 -*-
# 
# @Package Name TLVC (Time Lapse Video Creator)
# 
# Global Variables 
# 
# Environment Variables - A Runtime variables

class envRes:
    
    """
    def __init__(self, key):
        self.__envres_key__ = key
        
    """

    __STATIC_GLOBAL_VARIABLE:dict[str, str|int|bool|list|dict] = {}


    @staticmethod
    def set(possibly_key:str, value:str|bool|int) -> None:
        ## Args : possibly_key -> any
        ## Args : value -> any
        
        key:str = possibly_key
        
        if not value:
            value = possibly_key
        #    key = self.__envres_key__
        
        envRes.__STATIC_GLOBAL_VARIABLE.__setitem__(key, value)
        
    @staticmethod
    def get(key:str) -> str|int|bool|list|dict|None:
        ## Args : key -> string
        ## Returns any
        
        try:
            """
            if not key:
                key = self.__envres_key__
            """
            
            return envRes.__STATIC_GLOBAL_VARIABLE.get(key)
        
        except KeyError:
            return None
        
    

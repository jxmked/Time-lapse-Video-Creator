#!/usr/bin/env python3
# -*- coding UTF-8 -*-
# 
# @Package Name TLVC (Time Lapse Video Creator)
# 
# Global Variables 
# 
# Environment Variables - A Runtime variables

from os import environ

environ.__ENVIRONMENT_VARIABLES__ = {}

class envRes:
    
    __envRes_data__ = environ.__ENVIRONMENT_VARIABLES__
    
    """
    def __init__(self, key):
        self.__envres_key__ = key
        
    """
    
    def set(self, possibly_key, value) -> None:
        ## Args : possibly_key -> any
        ## Args : value -> any
        
        key = possibly_key
        
        if not value:
            value = possibly_key
        #    key = self.__envres_key__
            
        self.__envRes_data__[key] = value
        
    
    def get(self, key):
        ## Args : key -> string
        ## Returns any
        
        try:
            """
            if not key:
                key = self.__envres_key__
            """
            
            self.__envRes_data__[key]
        
        except KeyError:
            return None
        
    

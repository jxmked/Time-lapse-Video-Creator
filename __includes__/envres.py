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
    
    """
    def __init__(self, key):
        self.__envres_key__ = key
        
    """
    @staticmethod
    def set(possibly_key, value) -> None:
        ## Args : possibly_key -> any
        ## Args : value -> any
        
        key = possibly_key
        
        if not value:
            value = possibly_key
        #    key = self.__envres_key__
            
        environ.__ENVIRONMENT_VARIABLES__[key] = value
        
    @staticmethod
    def get(key):
        ## Args : key -> string
        ## Returns any
        
        try:
            """
            if not key:
                key = self.__envres_key__
            """
            
            return environ.__ENVIRONMENT_VARIABLES__[key]
        
        except KeyError:
            return None
        
    

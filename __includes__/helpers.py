#!/usr/bin/env python3

import os
import secrets
import unicodedata
import re
from hashlib import md5 as _md5_
from natsort import natsorted

def md5(value):
    m = _md5_()
    m.update(str(value).encode("utf-8"))
    return m.hexdigest()

def sortThis(arr):
    return natsorted(arr)

def createID(n):
    assert (n > 0 and 676 > n), "Cannot generate ID. Max 676, Min 1, Given %s" % n
    
    return str(chr((((n - 1) // 26) % 26) + 97) + chr((( n - 1) % 26) + 97))

def getFiles(dirIn, types):
    """
    Get all contents from given directory.
    Get all selected types of contents
    """
    f = []
    
    if types == "*" or "*" in types:
        return os.listdir(dirIn)
    
    for file in os.listdir(dirIn):
        for ext in types:
            if file.endswith(".%s" % ext):
                f.append(file)
    return f

def generateHex():
    """
    Generate Random 16 char hex
    """
    return secrets.token_hex(15)
    
def createDir(path):
    """
    Create Directory On Writable Path
    """
    try:
        os.mkdir(path, 0o777)
    except BaseException as ex:
        #raise (ex)
        pass
        
    

def slugify(value, allow_unicode=False):
    # https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
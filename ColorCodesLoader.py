#!/usr/bin/env python

"""
BEETFT v0.1

BEETFT creates a simple interface to control basic function of the BEETHEFIRST 3D printer.
BEETFT requires Pygame to be installed. Pygame can be downloaded from http://pygame.org
BEETFT is developed by Marcos Gomes
https://github.com/marcosfg/BEETFT


The MIT License (MIT)

Copyright (c) 2014 Marcos Gomes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,p
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

__author__ = "Marcos Gomes"
__license__ = "MIT"

import pygame
import json

class ColorCodes():
    
    jsonPath = "ColorCodes.json"
    
    colors = None
    
    colorNameList = []
    colorCodeList = []
    colorRGBList = []
    
    """*************************************************************************
                                Init Method 
    
    Loads Json File with color codes and extracts its info
    *************************************************************************"""
    def __init__(self,):
        
        f = open(self.jsonPath,'r')                     #load json as text file
        jsonData = json.load(f)                         #parse the json file
        #self.display = jsonData.get('display')          #get the display list from json file
        #self.leftMenu = jsonData.get('leftMenu')        #get the leftPanel list from json file
        self.colors = jsonData.get('ColorCodes')      #get the color codes list from json file
        f.close()   
        
        for code in self.colors:
            self.colorNameList.append(code['ColorName'])
            self.colorCodeList.append(code['ColorCode'])
            
            rgbColor = code['RGBColor']
            rgbSplit = rgbColor.split(",")
            self.colorRGBList.append(pygame.Color(
                                                int(rgbSplit[0]),
                                                int(rgbSplit[1]),
                                                int(rgbSplit[2])))
            
        
        return
    
    """
    GetColorNameList
    """
    def GetColorNameList(self):
        return self.colorNameList
    
    """
    GetColorCodeList
    """
    def GetColorCodeList(self):
        return self.colorCodeList
    
    """
    GetColorList
    """
    def GetColorList(self):
        return self.colorRGBList
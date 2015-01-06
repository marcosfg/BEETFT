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

class Display():
    
    """
    Display Configuration
    """
    display = []
    displayWidth = 0
    displayHeight = 0
    displayType = ""
    
    """
    Display Appearence
    """
    bgColor = None
    splitLineX = 100
    lineColor = None
    lineThickness = 3
    
    def __init__(self, type="Adafruit PiTFT Resistive", width=320, height=240,
                        bgColor="255,255,255",linePos=100, lineColor="0,0,0", lineThickness=3):
        self.displayWidth = width
        self.displayHeight = height
        self.displayType = type
        self.splitLineX = linePos
        self.lineThickness = lineThickness
        
        bgColorSplit=bgColor.split(",")
        bgR = int(bgColorSplit[0])
        bgG = int(bgColorSplit[1])
        bgB = int(bgColorSplit[2])
        
        self.bgColor = pygame.Color(bgR,bgG,bgB)
        
        lineColorSplit=lineColor.split(",")
        lR = int(lineColorSplit[0])
        lG = int(lineColorSplit[1])
        lB = int(lineColorSplit[2])
        
        self.lineColor = pygame.Color(lR,lG,lB)
    
    
    """
    GetBEEScreen(self)
    
    returns the screen object with the configured dimensions
    """
    def GetBEEScreen(self):
        screen = pygame.display.set_mode((self.displayWidth,self.displayHeight))
        
        return screen
    
    """
    GetbgColor(self)
    
    returns pygame.Color object with the Background color
    """
    def GetbgColor(self):
        
        return self.bgColor
    
    """
    GetLineColor(self)
    
    returns pygame.Color object with the Split Line color
    """
    def GetLineColor(self):
        
        return self.lineColor
    
    """
    DrawLine(self)
    
    Draws the split line
    """
    def DrawLine(self,screen):
        pygame.draw.line(screen, self.lineColor,
                                (self.splitLineX, 0),
                                (self.splitLineX, self.displayHeight),
                                self.lineThickness)
        return
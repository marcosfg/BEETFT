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
import pygbutton

class Button():
    
    """
    pygbutton var
    """
    btn = None
    """
    Button Configuration
    """
    buttonWidth = 0
    buttonHeight = 0
    posX = 0
    posY = 0
    bgColor = None
    fontColor = None
    title = ""
    font = None
    normalSurf = None
    downSurf = None
    highlightSurf = None
    name = None
    
    def __init__(self, x = 0, y = 0, width = 0, height = 0, title="", 
                    bgR=0, bgG=0, bgB=0, fR=0, fG = 0, fB = 0,
                    fontType=None, fontSize = 10,
                    normal=None, down=None, highlight=None, name=""):
                        
        self.buttonWidth = width
        self.buttonHeight = height
        self.posX = x
        self.posY = y
        self.title = title
        self.name = name
        
        if (bgR is not None) or (bgG is not None) or (bgB is not None):
            self.bgColor = pygame.Color(bgR,bgG,bgB)
        
        if (fR is not None) or (fG is not None) or (fB is not None):
            self.fontColor = pygame.Color(fR,fG,fB)
        
        if fontType=="Regular":
            self.font = pygame.font.Font("Fonts/DejaVuSans-Regular.ttf",fontSize)
        elif fontType=="Bold":
            self.font = pygame.font.Font("Fonts/DejaVuSans-Bold.ttf",fontSize)
        elif fontType=="Italic":
            self.font = pygame.font.Font("Fonts/DejaVuSans-Italic.ttf",fontSize)
        elif fontType=="Light":
            self.font = pygame.font.Font("Fonts/DejaVuSans-Light.ttf",fontSize)
        
        if normal is not None:
            self.normalSurf = normal
        if down is not None:
            self.downSurf = down
        if highlight is not None:
            self.highlightSurf = highlight
        
        
    def GetTextButton(self):
        self.btn = pygbutton.PygButton((self.posX,  self.posY, self.buttonWidth, self.buttonHeight),
                                                self.title, self.bgColor, self.fontColor, self.font,
                                                None,None,None,
                                                self.name)
                                                
        
        #caption='', bgcolor=LIGHTGRAY, fgcolor=BLACK, font=None,
        #normal=None, down=None, highlight=None, bName=None
        
        return self.btn
    
    def GetImageButton(self):
        
        self.btn = pygbutton.PygButton((self.posX,  self.posY, self.buttonWidth, self.buttonHeight),
                                                None, None, None, None,
                                                self.normalSurf, self.downSurf, self.highlightSurf,
                                                self.name)
        
        return self.btn

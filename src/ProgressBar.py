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
import math

class ProgressBar():
    
    x = 0
    y = 0
    width = 0
    height = 0
    thickness = 0
    
    lineColor = None
    fillColor = None
    
    rect = None
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, x, y, width, height, lineColor, fillColor,thickness):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.lineColor = lineColor
        self.fillColor = fillColor
        self.thickness = thickness
        
        
        return
    
    """
    GetRect
    """
    def DrawRect(self,screen):
        
        self.rect = pygame.draw.rect(screen, 
                                    self.lineColor,
                                    (self.x,self.y,self.width,self.height),
                                    self.thickness)
        
        return
    
    """
    GetRect
    """
    def GetSurface(self,fillWidth, maxFill):
        
        surf = None
        
        if(maxFill == 0):
            surf = pygame.Surface((0,self.height))
        else:
            if(fillWidth <= 0):
                surf = pygame.Surface((0,self.height))
            else:
                fill = math.ceil(fillWidth*self.width/maxFill)
                surf = pygame.Surface((int(fill),self.height))
        
        surf.fill(self.fillColor)
        
        #fillWidth = int((self.nozzleTemperature/self.targetTemperature)*width)
            
            #self.temperatureBarRect = pygame.draw.rect(self.screen, fontColor, (x,y,width,height), 3)
            #self.temperatureBarSurf = pygame.Surface((fillWidth,height))
            #self.temperatureBarSurf.fill(fontColor)
            #self.screen.blit(self.temperatureBarSurf, (x,y))
        return surf
    
    """
    GetPos
    """
    def GetPos(self):
        return (self.x,self.y)
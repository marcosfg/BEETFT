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

import os
import sys
import pygame
import pygbutton

class WaitScreen():
    """
    @var connected: status of USB connection to the BTF      
    """
    connected = False
    screen = None
    exit = False
    
    lblTop = None
    lblBottom = None
    bgImage = None
    
    """*************************************************************************
                                Init Method 
    
    intis all compoments
    *************************************************************************"""
    def __init__(self, screen):
        """
        .
        """
        self.connected = False
        self.exit = False
        self.screen = screen
        self.currentScreen = 'WaitConnection'
        
        # Start Image
        self.bgImage = pygame.image.load('Images/beeBWVector.png')
        
        
        
        #clear whole screen
        #self.screen.fill( self.color_bg )

        # Draw Image
        self.screen.blit(self.bgImage,(0,0))
        
        #draw top label
        topFont = pygame.font.Font("Fonts/DejaVuSans-Light.ttf",15)
        self.lblTop = topFont.render("Ups... where's the BEE?", 1, (0, 0, 0))
        self.screen.blit(self.lblTop, (10, 10))
        
        #draw Bottom label
        bottomFont = pygame.font.Font("Fonts/DejaVuSans-Light.ttf",10)
        self.lblBottom = bottomFont.render("...please connect your BTF pritner", 1, (0, 0, 0))
        self.screen.blit(self.lblBottom, (140, 210))

        # update screen
        pygame.display.update()
        
        while (not self.connected) and (not self.exit):
            # Handle events
            self.handle_events()
            
        return
    

    """*************************************************************************
                                handle_events
    
    waits for a USB conenction to be stablished
    *************************************************************************"""
    def handle_events(self):
        """handle all events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True

        	# Did the user click on the screen?
            if event.type == pygame.MOUSEBUTTONDOWN:
            	self.connected = True
                
        return
    
    """*************************************************************************
                                KillAll Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def KillAll(self):
        
        self.bgImage = None
        self.lblTop = None
        self.lblBottom = None
        
        return

        





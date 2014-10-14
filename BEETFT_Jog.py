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

class JogScreen():
    """
    @var done: anything can set to True to forcequit
    @var screen: points to: pygame.display.get_surface()        
    """
    btnColor_bg = pygame.Color(168, 168, 168)
    btnFgcolor = pygame.Color(0, 0, 0)
    pygbutton_font = pygame.font.Font('freesansbold.ttf', 10)
    #button sizes
    displacementBtnWidth = 50
    displacementBtnHeigth = 30

    def __init__(self, screen):
        """
        .
        """
        self.currentScreen = 'Jog'

        self.screen = screen

        self.btnMove10 = pygbutton.PygButton((  253,  198, self.displacementBtnWidth, self.displacementBtnHeigth), "10", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font) 
        self.btnMove1 = pygbutton.PygButton((  185,  198, self.displacementBtnWidth, self.displacementBtnHeigth), "1", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font)
        self.btnMove01 = pygbutton.PygButton((  117,  198, self.displacementBtnWidth, self.displacementBtnHeigth), "0.1", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font)

        self.homeSurf = pygame.image.load('Images/Home.png')
        self.btnHomeXY = pygbutton.PygButton((  174,  74, 30, 30), None, None, None, 'Images/Home.png', 'Images/Home.png', 'Images/Home.png')
        self.btnHomeZ = pygbutton.PygButton((  278,  74, 30, 30), None, None, None, 'Images/Home.png', 'Images/Home.png', 'Images/Home.png')

        self.btnX_Minus = pygbutton.PygButton((  112,  74, self.displacementBtnWidth, self.displacementBtnHeigth), "X-", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font)
        self.btnX_Plus = pygbutton.PygButton((  216,  74, self.displacementBtnWidth, self.displacementBtnHeigth), "X+", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font)
        self.btnY_Minus = pygbutton.PygButton((  174,  116, self.displacementBtnHeigth, self.displacementBtnWidth), "Y-", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font)
        self.btnY_Plus = pygbutton.PygButton((  174,  12, self.displacementBtnHeigth, self.displacementBtnWidth), "Y+", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font)
        self.btnZ_Minus = pygbutton.PygButton((  278,  116, self.displacementBtnHeigth, self.displacementBtnWidth), "Z-", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font)
        self.btnZ_Plus = pygbutton.PygButton((  278,  12, self.displacementBtnHeigth, self.displacementBtnWidth), "Z+", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font)

    def Start(self):
        # OctoPiPanel started
        print "BEETFT Jog"
        print "---"
        
        """
        while not self.done:
            # Handle events
            self.handle_events()
            
            # Update buttons visibility, text, graphs etc
            self.update()

            # Draw everything
            self.draw()
        """
       
    def handle_events(self,retVal):
        """handle all events."""
        for event in retVal:
            if 'click' in self.btnMove10.handleEvent(event):
                print 'Button Move 10 pressed'
            if 'click' in self.btnMove1.handleEvent(event):
                print 'Button Move 1 pressed'
            if 'click' in self.btnMove01.handleEvent(event):
                print 'Button Move 0.1 pressed'
            if 'click' in self.btnHomeXY.handleEvent(event):
                print 'Button Home XY'
            if 'click' in self.btnHomeZ.handleEvent(event):
                print 'Button Home Z'
            if 'click' in self.btnX_Minus.handleEvent(event):
                print 'Button X-'
            if 'click' in self.btnX_Plus.handleEvent(event):
                print 'Button X+'
            if 'click' in self.btnY_Minus.handleEvent(event):
                print 'Button Y-'
            if 'click' in self.btnY_Plus.handleEvent(event):
                print 'Button Y+'
            if 'click' in self.btnZ_Minus.handleEvent(event):
                print 'Button Z-'
            if 'click' in self.btnZ_Plus.handleEvent(event):
                print 'Button Z+'

    """
    Update buttons, text, graphs etc.
    """
    def update(self,val):

        self.btnMove10.visible = val
        self.btnMove1.visible = val
        self.btnMove01.visible = val

        self.btnHomeXY.visible = val
        self.btnHomeZ.visible = val

        self.btnX_Minus.visible = val
        self.btnX_Plus.visible = val
        self.btnY_Minus.visible = val
        self.btnY_Plus.visible = val
        self.btnZ_Minus.visible = val
        self.btnZ_Plus.visible = val

        return
               
    def draw(self):
        #clear whole screen
        #self.screen.fill( self.color_bg )

        # Draw buttons
        self.btnMove10.draw(self.screen)
        self.btnMove1.draw(self.screen)
        self.btnMove01.draw(self.screen)

        self.btnHomeXY.draw(self.screen)
        self.btnHomeZ.draw(self.screen)

        self.btnX_Minus.draw(self.screen)
        self.btnX_Plus.draw(self.screen)
        self.btnY_Minus.draw(self.screen)
        self.btnY_Plus.draw(self.screen)
        self.btnZ_Minus.draw(self.screen)
        self.btnZ_Plus.draw(self.screen)

        # update screen
        #pygame.display.update()





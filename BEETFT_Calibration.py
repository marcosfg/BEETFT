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

class CalibrationScreen():
    """
    @var done: anything can set to True to forcequit
    @var screen: points to: pygame.display.get_surface()        
    """
    btnColor_bg = pygame.Color(168, 168, 168)
    btnFgcolor = pygame.Color(0, 0, 0)
    pygbutton_font = pygame.font.Font('freesansbold.ttf', 10)
    pyFont_font = pygame.font.Font('freesansbold.ttf', 10)
    #button sizes
    displacementBtnWidth = 136
    displacementBtnHeigth = 22

    calibrationState = 1

    def __init__(self, screen):
        """
        .
        """
        self.currentScreen = 'Maintenance'

        self.screen = screen

        self.calibrationState = 1

        #draw buttons
        self.btnPlus05 = pygbutton.PygButton((  118,  68, self.displacementBtnWidth, self.displacementBtnHeigth), "+0.5mm", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font) 
        self.btnPlus005 = pygbutton.PygButton((  118,  108, self.displacementBtnWidth, self.displacementBtnHeigth), "+0.05mm", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font) 
        self.btnMinus005 = pygbutton.PygButton((  118,  152, self.displacementBtnWidth, self.displacementBtnHeigth), "-0.05mm", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font) 
        self.btnMinus05 = pygbutton.PygButton((  118,  196, self.displacementBtnWidth, self.displacementBtnHeigth), "-0.5mm", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font)

        #Next Button
        self.btnNext = pygbutton.PygButton((  275,  205, 40, 30), "Next", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font)

   
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
            if 'click' in self.btnPlus05.handleEvent(event):
                print 'Button Move +0.5mm pressed'
            if 'click' in self.btnPlus005.handleEvent(event):
                print 'Button Move +0.05mm pressed'
            if 'click' in self.btnMinus005.handleEvent(event):
                print 'Button Move -0.05mm pressed'
            if 'click' in self.btnMinus05.handleEvent(event):
                print 'Button Move -0.5mm pressed'

            if 'click' in self.btnNext.handleEvent(event):
                print 'Button Next pressed'
                self.calibrationState += 1

            if self.calibrationState > 3:
                self.calibrationState = 1

    """
    Update buttons, text, graphs etc.
    """
    def update(self,val):
        if self.calibrationState == 1:
            self.btnPlus05.visible = val
            self.btnPlus005.visible = val
            self.btnMinus005.visible = val
            self.btnMinus05.visible = val

        self.btnNext.visible = val


        return
               
    def draw(self):
        #clear whole screen
        #self.screen.fill( self.color_bg )

        # Draw buttons
        if self.calibrationState == 1:
            self.btnPlus05.draw(self.screen)
            self.btnPlus005.draw(self.screen)
            self.btnMinus005.draw(self.screen)
            self.btnMinus05.draw(self.screen)
        if self.calibrationState == 2:
            self.lbl1stCalibration = self.pyFont_font.render('Adjust Left Bolt', 1, (220, 12, 0))
            self.screen.blit(self.lbl1stCalibration, (100, 00))
        if self.calibrationState == 3:
            self.lbl2ndCalibration = self.pyFont_font.render('Adjust Rigth Bolt', 1, (220, 12, 0))
            self.screen.blit(self.lbl2ndCalibration, (100, 00))

        #Next Button
        self.btnNext.draw(self.screen)


        # update screen
        #pygame.display.update()
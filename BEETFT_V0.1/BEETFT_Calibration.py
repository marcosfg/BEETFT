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

    def __init__(self, width=320, height=240, caption="OctoPiPanel"):
        """
        .
        """
        self.currentScreen = 'Calibration'

        # init pygame and set up screen
        pygame.init()
        pygame.font.init()

        self.done = False
        #self.color_bg = pygame.Color(254, 193, 0)
        self.color_bg = pygame.Color(255, 255, 255)
        self.btnColor_bg = pygame.Color(254, 193, 0)
        #self.btnColor_bg = pygame.Color(255, 255, 255)
        self.btnFgcolor = pygame.Color(0, 0, 0)
        self.pygbutton_font = pygame.font.Font('freesansbold.ttf', 10)

        # Button settings
        self.buttonWidth = 80
        self.buttonHeight = 25

        

        self.width, self.height = width, height
        self.screen = pygame.display.set_mode( (width,height) )

        # Left buttons
        self.btnJog         = pygbutton.PygButton((  10,  41, self.buttonWidth, self.buttonHeight), "Jog", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font) 
        self.btnMaint       = pygbutton.PygButton((  10,  108, self.buttonWidth, self.buttonHeight), "Maintenance", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font) 
        self.btnCal         = pygbutton.PygButton((  10,  174, self.buttonWidth, self.buttonHeight), "Calibration", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font)

   
    def Start(self):
        # OctoPiPanel started
        print "BEETFT Calibration"
        print "---"
        
        """ game loop: input, move, render"""
        while not self.done:
            # Handle events
            self.handle_events()
            
            # Update buttons visibility, text, graphs etc
            self.update()

            # Draw everything
            self.draw()


        """ Quit """
        pygame.quit()
       
    def handle_events(self):
        """handle all events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print "quit"
                self.done = True

            if 'click' in self.btnJog.handleEvent(event):
                self.currentScreen = 'Jog'
                self.done = True;
            if 'click' in self.btnMaint.handleEvent(event):
                self.currentScreen = 'Maintenance'
                self.done = True;
            if 'click' in self.btnCal.handleEvent(event):
                self.currentScreen = 'Calibration'
                self.done = False;

        	# Did the user click on the screen?
            if event.type == pygame.MOUSEBUTTONDOWN:
            	pass

    """
    Update buttons, text, graphs etc.
    """
    def update(self):

        pass

        return
               
    def draw(self):
        #clear whole screen
        self.screen.fill( self.color_bg )
        pygame.draw.line(self.screen, (0, 0, 0), (100, 0), (100, 240),3)

        # Draw buttons
        self.btnJog.draw(self.screen)
        self.btnMaint.draw(self.screen)
        self.btnCal.draw(self.screen)
        


        # update screen
        pygame.display.update()
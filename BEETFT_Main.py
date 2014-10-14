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
import BEETFT_Start
import BEETFT_Jog
import BEETFT_Maintenance
import BEETFT_Calibration
#import serial
#from serial.tools import list_ports

os.environ["SDL_FBDEV"] = "/dev/fb1"

 
class BEETFT_Main():
    """
    @var done: anything can set to True to forcequit
    @var screen: points to: pygame.display.get_surface()        
    """
    #Init Screen = 'Jog'
    currentScreen = 'Jog'
    #Color & Text Variables
    color_bg = pygame.Color(255, 255, 255)
    btnColor_bg = pygame.Color(168, 168, 168)
    btnFgcolor = pygame.Color(0, 0, 0)
    pygbutton_font = pygame.font.Font('freesansbold.ttf', 10)
    # Button settings
    buttonWidth = 80
    buttonHeight = 25

    #serialPort = None

    def __init__(self, width=320, height=240, caption="OctoPiPanel"):
        """
        .
        """
        self.done = False

        self.currentScreen = 'Jog'

        # init pygame and set up screen
        pygame.init()

        self.width, self.height = width, height
        self.screen = pygame.display.set_mode( (width,height) )

        #print self.currentScreen

   
    def Start(self):
        # OctoPiPanel started
        print "BEETFT Main"
        print "---"

        startScreen = BEETFT_Start.StartScreen(self.screen)
        startScreen.Start()
        #self.serialPort = startScreen.Start()

        # Left buttons
        self.btnJog         = pygbutton.PygButton((  10,  41, self.buttonWidth, self.buttonHeight), "Jog", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font) 
        self.btnMaint       = pygbutton.PygButton((  10,  108, self.buttonWidth, self.buttonHeight), "Maintenance", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font) 
        self.btnCal         = pygbutton.PygButton((  10,  174, self.buttonWidth, self.buttonHeight), "Calibration", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font)

        #Init secondary screens
        self.jogScreen = BEETFT_Jog.JogScreen(self.screen)
        self.maintScreen = BEETFT_Maintenance.MaintScreen(self.screen)
        self.calScreen = BEETFT_Calibration.CalibrationScreen(self.screen)

        """ game loop: input, move, render"""
        while not self.done:
            # Handle events
            self.handle_events()
            
            # Update buttons visibility, text, graphs etc
            self.update()

            # Draw everything
            self.draw()

        pygame.quit()

    def draw(self):
        #clear whole screen
        self.screen.fill( self.color_bg )

        pygame.draw.line(self.screen, (0, 0, 0), (100, 0), (100, 240),3)

        # Draw buttons
        self.btnJog.draw(self.screen)
        self.btnMaint.draw(self.screen)
        self.btnCal.draw(self.screen)

        #Draw Secondary Screens
        if self.currentScreen == 'Jog':
            self.jogScreen.draw()
        elif self.currentScreen == 'Maintenance':
            self.maintScreen.draw()
        elif self.currentScreen == 'Calibration':
            self.calScreen.draw()

        # update screen
        pygame.display.update()


    def update(self):
        #set left buttons visible
        self.btnJog.visible = True
        self.btnMaint.visible = True
        self.btnCal.visible = True

        #Update Secondary Screens
        if self.currentScreen == 'Jog':
            self.jogScreen.update(True)            
            self.maintScreen.update(False)
            self.calScreen.update(False)
        elif self.currentScreen == 'Maintenance':
            self.jogScreen.update(False)
            self.maintScreen.update(True)
            self.calScreen.update(False)
        elif self.currentScreen == 'Calibration':
            self.jogScreen.update(False)
            self.maintScreen.update(False)
            self.calScreen.update(True)



    def handle_events(self):

        retVal = pygame.event.get()
        """handle all events."""
        for event in retVal:
            if event.type == pygame.QUIT:
                print "quit"
                self.done = True

            # Did the user click on the screen?
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

            if 'click' in self.btnJog.handleEvent(event):
                self.currentScreen = 'Jog'
                print self.currentScreen
            if 'click' in self.btnMaint.handleEvent(event):
                self.currentScreen = 'Maintenance'
                print self.currentScreen
            if 'click' in self.btnCal.handleEvent(event):
                self.currentScreen = 'Calibration'
                print self.currentScreen

        if self.currentScreen == 'Jog':
            self.jogScreen.handle_events(retVal)
        elif self.currentScreen == 'Maintenance':
            self.maintScreen.handle_events(retVal)
        elif self.currentScreen == 'Calibration':
            self.calScreen.handle_events(retVal)


if __name__ == '__main__':
    opp = BEETFT_Main(320, 240, "BEETFT")
    opp.Start()

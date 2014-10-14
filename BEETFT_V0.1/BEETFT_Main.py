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
import BEETFT_Start
import BEETFT_Jog
import BEETFT_Maintenance
import BEETFT_Calibration

from pydispatch import dispatcher

os.environ["SDL_FBDEV"] = "/dev/fb1"

 
class BEETFT_Main():
    """
    @var done: anything can set to True to forcequit
    @var screen: points to: pygame.display.get_surface()        
    """

    def __init__(self, width=320, height=240, caption="OctoPiPanel"):
        """
        .
        """
        self.done = False
        #self.color_bg = pygame.Color(254, 193, 0)
        self.color_bg = pygame.Color(255, 255, 255)

        self.currentScreen = 'Jog'

        # init pygame and set up screen
        pygame.init()

        self.width, self.height = width, height
        self.screen = pygame.display.set_mode( (width,height) )

        # Start Image
        #self.asurf = pygame.image.load('Images/beeVector.png')

   
    def Start(self):
        # OctoPiPanel started
        print "BEETFT Main"
        print "---"
        
        startScreen = BEETFT_Start.StartScreen(self.width, self.height, "BEETFT")
        startScreen.Start()

        """ game loop: input, move, render"""
        while not self.done:

            if self.currentScreen == 'Jog':
                self.jogScreen = BEETFT_Jog.JogScreen(self.width, self.height, "BEETFT")
                self.jogScreen.Start()
                self.currentScreen = self.jogScreen.currentScreen;
                self.jogScreen = None
            elif self.currentScreen == 'Maintenance':
                self.maintenanceScreen = BEETFT_Maintenance.MaintenanceScreen(self.width, self.height, "BEETFT")
                self.maintenanceScreen.Start()
                self.currentScreen = self.maintenanceScreen.currentScreen;
                self.maintenanceScreen = None
            elif self.currentScreen == 'Calibration':
                self.calibrationScreen = BEETFT_Calibration.CalibrationScreen(self.width, self.height, "BEETFT")
                self.calibrationScreen.Start()
                self.currentScreen = self.calibrationScreen.currentScreen;
                self.maintenanceScreen = None

            

        """ Quit """
        pygame.quit()



    def handle_events(self):
        """ Check for left button click """


if __name__ == '__main__':
    opp = BEETFT_Main(320, 240, "BEETFT")
    opp.Start()

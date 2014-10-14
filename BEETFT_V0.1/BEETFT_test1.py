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
#from lxml import etree
import xml.etree.ElementTree as etree
from array import array


os.environ["SDL_FBDEV"] = "/dev/fb1"

 
class BEETFT():
    """
    @var done: anything can set to True to forcequit
    @var screen: points to: pygame.display.get_surface()        
    """

    def __init__(self, width=320, height=240, caption="BEETFT"):
        """
        .
        """
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

        # init pygame and set up screen
        pygame.init()

        self.width, self.height = width, height
        self.screen = pygame.display.set_mode( (width,height) )

        # Left buttons
        #self.btnJog         = pygbutton.PygButton((  10,  41, self.buttonWidth, self.buttonHeight), "Jog", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font) 
        #self.btnMaint       = pygbutton.PygButton((  10,  108, self.buttonWidth, self.buttonHeight), "Maintenance", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font) 
        #self.btnCal         = pygbutton.PygButton((  10,  174, self.buttonWidth, self.buttonHeight), "Calibration", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font)

        self.btn = []
        for i in range(1, 4):
            self.btn.append(pygbutton.PygButton((  10,  67*i-26, self.buttonWidth, self.buttonHeight), "Jog"+str(i), self.btnColor_bg, self.btnFgcolor, self.pygbutton_font))

        self.asurf = pygame.image.load('Images/beeVector.png')

   
    def Start(self):
        # OctoPiPanel started
        print "BEETFT start"
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
        #pygame.quit()
       
    def handle_events(self):
        """handle all events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print "quit"
                self.done = True

        # Did the user click on the screen?
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Reset backlight counter
                self.bglight_ticks = pygame.time.get_ticks()

                if self.bglight_on == False and platform.system() == 'Linux':
                    # enable the backlight
                    #os.system("echo '1' > /sys/class/gpio/gpio252/value")
                    self.bglight_on = True
                    print "Background light on."

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print "Got escape key"
                    self.done = True

                # Look for specific keys.
                #  Could be used if a keyboard is connected
                if event.key == pygame.K_a:
                    print "Got A key"

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
        #self.btnJog.draw(self.screen)
        #self.btnMaint.draw(self.screen)
        #self.btnCal.draw(self.screen)

        for i in range(0, 3):
            print i
            btn = self.btn[i]
            btn.draw(self.screen)

        self.screen.blit(self.asurf,(30,30))


        # update screen
        pygame.display.update()


if __name__ == '__main__':
    opp = BEETFT(320, 240, "BEETFT")
    opp.Start()

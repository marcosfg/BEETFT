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

class MaintScreen():
    """
    @var done: anything can set to True to forcequit
    @var screen: points to: pygame.display.get_surface()        
    """
    btnColor_bg = pygame.Color(168, 168, 168)
    btnFgcolor = pygame.Color(0, 0, 0)
    pyFont_font = pygame.font.Font('freesansbold.ttf', 10)
    pygbutton_font = pygame.font.Font('freesansbold.ttf', 10)
    #button sizes
    displacementBtnWidth = 80
    displacementBtnHeigth = 25

    maintState = 'Heating'      # [Heating, Selection, ChangeFilament, CleanNozzle]

    def __init__(self, screen):
        """
        .
        """
        self.currentScreen = 'Maintenance'

        self.screen = screen

        #draw Heating label
        self.lblHeating = self.pyFont_font.render('Heating Nozzle', 1, (220, 12, 0))
        #draw Heating Image
        self.heatingImage = pygame.image.load('Images/bico.png')

        #Next Button
        self.btnNext = pygbutton.PygButton((  275,  205, 40, 30), "Next", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font)

        self.maintState = 'Maintenance'

        #Selection Buttons
        self.btnUnload = pygbutton.PygButton((  170,  41, self.displacementBtnWidth, self.displacementBtnHeigth), "Unload", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font)
        self.btnLoad = pygbutton.PygButton((  170,  108, self.displacementBtnWidth, self.displacementBtnHeigth), "Load", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font)
        self.btnClean = pygbutton.PygButton((  170,  174, self.displacementBtnWidth, self.displacementBtnHeigth), "Clean", self.btnColor_bg, self.btnFgcolor, self.pygbutton_font)

   
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
            if 'click' in self.btnNext.handleEvent(event):
                print 'Button Next pressed'
                self.maintState = 'Selection'

    """
    Update buttons, text, graphs etc.
    """
    def update(self,val):

        self.checkTemp();

        if self.maintState == 'Maintenance':
            self.btnNext.visible = val
            self.btnUnload.visible = False
            self.btnLoad.visible = False
            self.btnClean.visible = False


        if self.maintState == 'Selection':
            self.btnNext.visible = val
            self.btnUnload.visible = True
            self.btnLoad.visible = True
            self.btnClean.visible = True


        return
               
    def draw(self):
        #clear whole screen
        #self.screen.fill( self.color_bg )

        # Draw buttons
        if self.maintState == 'Maintenance':
            self.screen.blit(self.heatingImage,(100, -20))
            self.screen.blit(self.lblHeating, (100, 00))
            pygame.draw.rect(self.screen, (0,0,255), pygame.Rect(120,180,150,15))

        self.btnNext.draw(self.screen)

        self.btnUnload.draw(self.screen)
        self.btnLoad.draw(self.screen)
        self.btnClean.draw(self.screen)


        # update screen
        #pygame.display.update()

    def checkTemp(self):
        pass





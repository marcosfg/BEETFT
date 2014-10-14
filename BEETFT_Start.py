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
import serial
from serial.tools import list_ports

class StartScreen():
    """
    @var done: anything can set to True to forcequit
    @var screen: points to: pygame.display.get_surface()        
    """

    def __init__(self,screen):
        """
        .
        """
        self.waitForConnection = False
        #self.color_bg = pygame.Color(254, 193, 0)
        self.color_bg = pygame.Color(255, 255, 255)

        self.screen = screen

        # Start Image
        #self.bgImage = pygame.image.load('Images/beeVector.png')
        self.bgImage = pygame.image.load('Images/bee.bmp')

   
    def Start(self):
        # OctoPiPanel started
        print "BEETFT start"
        print "---"

        #portList = list_ports.comports()
        #print portList
        #ser = serial.Serial('/dev/tty.usbserial-DA00DDXP', 115200)
        #ser = portList(1)
        #serialPort = 
        
        """ game loop: input, move, render"""
        while not self.waitForConnection:

        	#Wait for start
        	#while ser.inWaiting() == 0:
        	#	pass
        	#res = ser.readline()
        	#if res.find('start') >= 0:
        	#	return ser
        	#	self.waitForConnection = True

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
                self.waitForConnection = True

        	# Did the user click on the screen?
            if event.type == pygame.MOUSEBUTTONDOWN:
            	self.waitForConnection = True

    """
    Update buttons, text, graphs etc.
    """
    def update(self):

        pass

        return
               
    def draw(self):
        #clear whole screen
        self.screen.fill( self.color_bg )

        # Draw Image
        self.screen.blit(self.bgImage,(0,0))


        # update screen
        pygame.display.update()
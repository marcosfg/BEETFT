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

import usb
import usb.core
import usb.util
import sys
import os
import time

class Connection():
    
    READ_TIMEOUT = 2000
    DEFAULT_READ_LENGTH = 512
    
    connected = None
    
    dev = None
    cfg = None
    ep_out = None
    ep_in = None
    
    backend = None

    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self):
        
        
        # find our device
        self.dev = usb.core.find(idVendor=0xffff, idProduct=0x014e)
        
        # was it found? no, try the other device
        if self.dev is None:
            self.dev = usb.core.find(idVendor=0x29c9, idProduct=0x001)
        elif self.dev is None:
            raise ValueError('Device not found')
        
        if self.dev is None:
            print("Can't Find Printer")
            self.connected = False
            return
        
        self.dev.reset()
        # set the active configuration. With no arguments, the first
        # configuration will be the active one
        self.dev.set_configuration()

        # get an endpoint instance
        self.cfg = self.dev.get_active_configuration()
        self.intf = self.cfg[(0,0)]

        self.ep_out = usb.util.find_descriptor(
            self.intf,
            # match the first OUT endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)


        self.ep_in = usb.util.find_descriptor(
            self.intf,
            # match the first in endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN)


        # Verify that the end points exist
        assert self.ep_out is not None
        assert self.ep_in is not None
        
        self.connected = True
        
        return
    
    """*************************************************************************
                                close Method 
    
    returns the connection state
    *************************************************************************"""
    def close(self):
        
        #rm = usb.core._ResourceManager(self.dev,self.backend)
        #rm.release_all_interfaces(self.dev)
        
        #self.dev.reset()
        
        return 
    
    """*************************************************************************
                                dispatch Method 
    
    send a message and read the response
    *************************************************************************"""
    def dispatch(self,message):
        
        time.sleep(0.001)
        self.ep_out.write(message)
        time.sleep(0.009)
        ret = self.ep_in.read(self.DEFAULT_READ_LENGTH, self.READ_TIMEOUT)
        sret = ''.join([chr(x) for x in ret])
        
        return sret
    
    """*************************************************************************
                                isConnected Method 
    
    returns the connection state
    *************************************************************************"""
    def isConnected(self):
        return self.connected
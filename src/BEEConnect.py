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
    
    dev = None
    endpoint = None
    ep_in = None
    ep_out = None
    cfg = None
    intf = None

    READ_TIMEOUT = 500
    DEFAULT_READ_LENGTH = 512

    queryInterval = 0.5
    
    connected = None
    
    backend = None

    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self):
        
        self.findBEE()
        
        return

    """*************************************************************************
                            findBEE Method 

    *************************************************************************"""
    def findBEE(self):
        
        self.connected = False
        
        # find our device
        self.dev = usb.core.find(idVendor=0xffff, idProduct=0x014e)
        # was it found? no, try the other device
        if self.dev is None:
                self.dev = usb.core.find(idVendor=0x29c9, idProduct=0x001)
        elif self.dev is None:
                raise ValueError('Device not found')

        if self.dev is None:
                print("Can't Find Printer")
                return
        
        """
        #DOES NOT WORK IN RPI
        if self.dev.is_kernel_driver_active(0):
            try:
                self.dev.detach_kernel_driver(0)
            except usb.core.USBError as e:
                sys.exit("Could not detatch kernel driver: %s" % str(e))
        """
        # set the active configuration. With no arguments, the first
        # configuration will be the active one
        try:
            self.dev.set_configuration()
            self.dev.reset()
            self.cfg = self.dev.get_active_configuration()
            self.intf = self.cfg[(0,0)]
        except usb.core.USBError as e:
            sys.exit("Could not set configuration: %s" % str(e))
        
        self.endpoint = self.dev[0][(0,0)][0]

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
                            dispatch Method

    *************************************************************************"""
    def dispatch(self,message,to=None,superSpeed=False):
        
        timeout = self.READ_TIMEOUT
        
        if(to is not None):
            timeout = to
        
        if(message == "dummy"):
            pass
        elif(superSpeed):
            #time.sleep(0.001)
            self.ep_out.write(message)
            #time.sleep(0.001)
        else:
            time.sleep(0.001)
            self.ep_out.write(message)
            time.sleep(0.009)
        sret = ""
        
        try:
            #ret = self.dev.read(self.endpoint.bEndpointAddress,self.DEFAULT_READ_LENGTH)
            ret = self.ep_in.read(self.DEFAULT_READ_LENGTH, timeout)
            sret = ''.join([chr(x) for x in ret])
            
            #print(sret)
        except usb.core.USBError as e:
            if ("timed out" in str(e.args)):
                #print("Read Timeout")
                pass
            
        #print("sent: ", message, " received: ", sret)
        return sret

    """*************************************************************************
                            sendCmd Method 

    *************************************************************************"""
    def sendCmd(self,cmd,wait=None,timeout=None):

        #self.findBEE()

        resp = None

        if wait is None:
            resp = self.dispatch(cmd)
        else:
            if(wait == "tog"):
                resp = self.wait4tog(cmd)
            else:
                resp = self.waitFor(cmd,wait,timeout)
            
        return resp

    """*************************************************************************
                            waitFor Method 

    *************************************************************************"""
    def waitFor(self,cmd,s,timeout=None):
        self.dispatch(cmd)
        busy = True
        #nextSend = time.time() + self.queryInterval
        while busy:
            #t = time.time()
            #if t > nextSend:
            try:
                resp = self.dispatch("M625\n",timeout)
                #print(resp)
                str2find = "S:" + str(s)
                if resp.find(str2find) >= 0:
                        busy = False
            except Exception:
                pass
        
        return resp

    """*************************************************************************
                            wait4tog Method 

    *************************************************************************"""
    def wait4tog(self,cmd):
        
        resp = self.dispatch(cmd,500,True)
        str2find = "tog"
        busy = True
        
        while "tog" not in resp:
            try:
                resp += self.dispatch("dummy",500)
            except Exception:
                pass
        
        return resp
    
    """*************************************************************************
                            close Method

    *************************************************************************"""
    def close(self):
        try:
            # release the device
            usb.util.dispose_resources(self.dev)
            usb.util.release_interface(self.dev, self.intf)
        except:
            pass
        
        return
    
    """*************************************************************************
                            startPrinter Method

    *************************************************************************"""
    def startPrinter(self):
        
        self.sendCmd("M625\n")
        self.sendCmd("M630\n")
        
        self.close()
        time.sleep(5)
        self.findBEE()
        
        self.sendCmd("G28\n", "3")
        
        return
    
    """*************************************************************************
                            isConnected Method
    returns the connection state
    *************************************************************************"""
    def isConnected(self):
        
        return self.connected
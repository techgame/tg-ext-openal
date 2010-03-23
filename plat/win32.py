##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2010  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the MIT style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from struct import pack, unpack

import ctypes
from ctypes.util import find_library
from ctypes import POINTER, sizeof, byref, cast
from ctypes import (c_uint32, c_void_p)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_mm_ = ctypes.windll.winmm

DWORD = ctypes.c_uint32
class WindowsMultimediaError(Exception): pass

def getSystemVolume_win32(device=None):
    volume = DWORD(0)
    err = _mm_.waveOutGetVolume(c_void_p(device), byref(volume))
    if err: raise WindowsMultimediaError(err)
    volume = volume.value
    vl = float((volume>> 0) & 0xffff)/0xffff
    vr = float((volume>>16) & 0xffff)/0xffff
    return (vl, vr)

getSystemVolume = getSystemVolume_win32

def setSystemVolume_win32(volume, device=None):
    if isinstance(volume, (int, long, float)):
        volume = (float(volume),)*2

    vl, vr = (max(0, min(0xffff, int(0xffff*v))) for v in volume)
    volume = c_uint32((vr<<16) | (vl<<0))
    err = _mm_.waveOutSetVolume(c_void_p(device), volume)
    if err: raise WindowsMultimediaError(err)

setSystemVolume = setSystemVolume_win32

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    vol = getSystemVolume()
    print 'system volume:', vol
    print 'set system volume'
    setSystemVolume(0.5)
    vol = getSystemVolume()
    print 'system volume:', vol


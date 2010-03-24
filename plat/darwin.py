#!/usr/bin/env python
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
from ctypes import (c_uint32, c_float)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_coreAudio_ = ctypes.cdll.LoadLibrary(find_library('CoreAudio'))

c_appleid = ctypes.c_uint32
AudioDeviceID = c_appleid

def fromAppleId(strAppleId): 
    return unpack('!I', str(strAppleId))[0]
def toAppleId(intAppleId): 
    if isinstance(intAppleId, c_appleid):
        intAppleId = intAppleId.value
    return pack('!I', intAppleId)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variiables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

kAudioHardwarePropertyProcessIsMaster                   = fromAppleId('mast')
kAudioHardwarePropertyIsInitingOrExiting                = fromAppleId('inot')
kAudioHardwarePropertyUserIDChanged                     = fromAppleId('euid')
kAudioHardwarePropertyDevices                           = fromAppleId('dev#')
kAudioHardwarePropertyDefaultInputDevice                = fromAppleId('dIn ')
kAudioHardwarePropertyDefaultOutputDevice               = fromAppleId('dOut')
kAudioHardwarePropertyDefaultSystemOutputDevice         = fromAppleId('sOut')
kAudioHardwarePropertyDeviceForUID                      = fromAppleId('duid')
kAudioHardwarePropertyProcessIsAudible                  = fromAppleId('pmut')
kAudioHardwarePropertySleepingIsAllowed                 = fromAppleId('slep')
kAudioHardwarePropertyUnloadingIsAllowed                = fromAppleId('unld')
kAudioHardwarePropertyHogModeIsAllowed                  = fromAppleId('hogr')
kAudioHardwarePropertyRunLoop                           = fromAppleId('rnlp')
kAudioHardwarePropertyPlugInForBundleID                 = fromAppleId('pibi')
kAudioHardwarePropertyUserSessionIsActiveOrHeadless     = fromAppleId('user')
kAudioHardwarePropertyMixStereoToMono                   = fromAppleId('stmo')

kAudioDevicePropertyJackIsConnected                                 = fromAppleId('jack')
kAudioDevicePropertyVolumeScalar                                    = fromAppleId('volm')
kAudioDevicePropertyVolumeDecibels                                  = fromAppleId('vold')
kAudioDevicePropertyVolumeRangeDecibels                             = fromAppleId('vdb#')
kAudioDevicePropertyVolumeScalarToDecibels                          = fromAppleId('v2db')
kAudioDevicePropertyVolumeDecibelsToScalar                          = fromAppleId('db2v')
kAudioDevicePropertyVolumeDecibelsToScalarTransferFunction          = fromAppleId('vctf')
kAudioDevicePropertyStereoPan                                       = fromAppleId('span')
kAudioDevicePropertyStereoPanChannels                               = fromAppleId('spn#')
kAudioDevicePropertyMute                                            = fromAppleId('mute')
kAudioDevicePropertySolo                                            = fromAppleId('solo')
kAudioDevicePropertyDataSource                                      = fromAppleId('ssrc')
kAudioDevicePropertyDataSources                                     = fromAppleId('ssc#')
kAudioDevicePropertyDataSourceNameForIDCFString                     = fromAppleId('lscn')
kAudioDevicePropertyClockSource                                     = fromAppleId('csrc')
kAudioDevicePropertyClockSources                                    = fromAppleId('csc#')
kAudioDevicePropertyClockSourceNameForIDCFString                    = fromAppleId('lcsn')
kAudioDevicePropertyClockSourceKindForID                            = fromAppleId('csck')
kAudioDevicePropertyPlayThru                                        = fromAppleId('thru')
kAudioDevicePropertyPlayThruSolo                                    = fromAppleId('thrs')
kAudioDevicePropertyPlayThruVolumeScalar                            = fromAppleId('mvsc')
kAudioDevicePropertyPlayThruVolumeDecibels                          = fromAppleId('mvdb')
kAudioDevicePropertyPlayThruVolumeRangeDecibels                     = fromAppleId('mvd#')
kAudioDevicePropertyPlayThruVolumeScalarToDecibels                  = fromAppleId('mv2d')
kAudioDevicePropertyPlayThruVolumeDecibelsToScalar                  = fromAppleId('mv2s')
kAudioDevicePropertyPlayThruVolumeDecibelsToScalarTransferFunction  = fromAppleId('mvtf')
kAudioDevicePropertyPlayThruStereoPan                               = fromAppleId('mspn')
kAudioDevicePropertyPlayThruStereoPanChannels                       = fromAppleId('msp#')
kAudioDevicePropertyPlayThruDestination                             = fromAppleId('mdds')
kAudioDevicePropertyPlayThruDestinations                            = fromAppleId('mdd#')
kAudioDevicePropertyPlayThruDestinationNameForIDCFString            = fromAppleId('mddc')
kAudioDevicePropertyChannelNominalLineLevel                         = fromAppleId('nlvl')
kAudioDevicePropertyChannelNominalLineLevels                        = fromAppleId('nlv#')
kAudioDevicePropertyChannelNominalLineLevelNameForIDCFString        = fromAppleId('lcnl')
kAudioDevicePropertyDriverShouldOwniSub                             = fromAppleId('isub')
kAudioDevicePropertySubVolumeScalar                                 = fromAppleId('svlm')
kAudioDevicePropertySubVolumeDecibels                               = fromAppleId('svld')
kAudioDevicePropertySubVolumeRangeDecibels                          = fromAppleId('svd#')
kAudioDevicePropertySubVolumeScalarToDecibels                       = fromAppleId('sv2d')
kAudioDevicePropertySubVolumeDecibelsToScalar                       = fromAppleId('sd2v')
kAudioDevicePropertySubVolumeDecibelsToScalarTransferFunction       = fromAppleId('svtf')
kAudioDevicePropertySubMute                                         = fromAppleId('smut')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CoreAudioError(Exception): pass

def getSystemVolume_darwin(device=kAudioHardwarePropertyDefaultOutputDevice, channels=(1,2), asDict=False):
    idAudioOutput = getAudioHardwareProperty(device)

    result = []
    key = kAudioDevicePropertyVolumeScalar
    for chanNum in channels:
        v = getAudioDeviceProperty(idAudioOutput, key, chanNum, result=c_float)
        v = v.value
        if asDict: result.append((chanNum, v))
        else: result.append(v)

    if asDict: 
        return dict(result)
    else: return tuple(result)

getSystemVolume = getSystemVolume_darwin

def setSystemVolume_darwin(volume, device=kAudioHardwarePropertyDefaultOutputDevice, channels=(1,2)):
    if isinstance(volume, (int, long, float)):
        volume = (float(volume),)*len(channels)

    result = False
    idAudioOutput = getAudioHardwareProperty(device)
    key = kAudioDevicePropertyVolumeScalar
    for chanNum, volNew in zip(channels, volume):
        volNew = c_float(volNew)
        sz, writable = getAudioDeviceProperty(idAudioOutput, key, chanNum, 
                            False, result=c_float, infoOnly=True)
        if writable: 
            setAudioDeviceProperty(idAudioOutput, key, volNew, chanNum)
            result = True

    return result


def setAudioDeviceProperty(idAudioDevice, idProperty, value, channel=1, section=0, when=None):
    err = _coreAudio_.AudioDeviceSetProperty(
            idAudioDevice, when, 
            channel, section, idProperty, 
            sizeof(value), byref(value))
    if err: raise CoreAudioError(err)

def getAudioDeviceProperty(idAudioDevice, idProperty, channel=1, section=0, result=None, infoOnly=False):
    size = c_uint32(0); writable = c_uint32(0)
    err = _coreAudio_.AudioDeviceGetPropertyInfo(
            idAudioDevice, channel, 
            section, idProperty, 
            byref(size), byref(writable))
    if err: raise CoreAudioError(err)
    if infoOnly:
        return size.value, writable.value

    if result is not None:
        result = result()
    else: result = c_uint32()
    if size.value != sizeof(result):
        raise CoreAudioError("Result size mismatch")

    size.value = sizeof(result)
    err = _coreAudio_.AudioDeviceGetProperty(
            idAudioDevice, channel, section, 
            idProperty, byref(size), byref(result))
    if err: raise CoreAudioError(err)

    return result

def getAudioHardwareProperty(audioHardwarePropertyID, result=None, infoOnly=False):
    size = c_uint32(0); writable = c_uint32(0)
    err = _coreAudio_.AudioHardwareGetPropertyInfo(
            audioHardwarePropertyID, byref(size), byref(writable))
    if err: raise CoreAudioError(err)
    if infoOnly:
        return size.value, writable.value

    if result is not None:
        result = result()
    else: result = c_uint32()
    if size.value != sizeof(result):
        raise CoreAudioError("Result size mismatch")

    size.value = sizeof(result)
    err = _coreAudio_.AudioHardwareGetProperty(
            audioHardwarePropertyID, byref(size), byref(result))
    if err: raise CoreAudioError(err)

    return result

setSystemVolume = setSystemVolume_darwin

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


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2005  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.openAL._properties import *
from TG.openAL.constants import alFormatMap
from TG.openAL.raw import al, alc

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Capture Context
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if not hasattr(alc, 'alcCaptureOpenDevice'):
    Capture = None

else:

    class Capture(ALIDContextObject):
        processEvents = [
            'capturing',
            'sampleCount', 

            'format',
            'frequency',
            'entryCount',
            'entrySize',
            ]

        _buffer = None
        format = None
        frequency = 0
        entryCount = 0
        entrySize = 0

        entrySizeMap = {
            al.AL_FORMAT_MONO8: 1,
            al.AL_FORMAT_MONO16: 2,
            al.AL_FORMAT_STEREO8: 2,
            al.AL_FORMAT_STEREO16: 4,
            }
        name = alcPropertyS(alc.ALC_CAPTURE_DEVICE_SPECIFIER)
        sampleCount = alcPropertyI(alc.ALC_CAPTURE_SAMPLES)

        def __init__(self, name=None, frequency=44100, format=al.AL_FORMAT_STEREO16, count=None):
            if name is not False:
                self.open(name, frequency=frequency, format=format, count=count)

        def __del__(self):
            self.close()

        def __repr__(self):
            return '<%s.%s frequency: %s channels: %s width: %s>' % (
                        self.__class__.__module__, self.__class__.__name__,
                        self.frequency, self.getChannels(), self.getWidth())

        def open(self, name=None, frequency=44100, format=al.AL_FORMAT_STEREO16, count=65536):
            name = name and str(name) or None
            format = alFormatMap.get(format, format)

            self.entrySize = self.entrySizeMap[format]
            self.entryCount = count or 65536
            self.frequency = frequency
            self.format = format
            self._buffer = al.c_buffer(self.entryCount*self.entrySize, 0)
            self._setAsParam(alc.alcCaptureOpenDevice(name, int(frequency), int(format), len(self._buffer)))

            context = self._context
            context.addCapture(self)
            context.device._addContext(self)

        __dealocating = False
        def close(self):
            if self._hasAsParam() and not self.__dealocating:
                self.__dealocating = True
                try:
                    alc.alcCaptureCloseDevice(self)

                    del self.entryCount
                    del self.entrySize
                    del self.frequency
                    del self.format
                    del self._buffer
                finally:
                    self._delAsParam()
        destroy = close

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def getWidth(self):
            return {
                al.AL_FORMAT_MONO8: 1, al.AL_FORMAT_MONO16: 2,
                al.AL_FORMAT_STEREO8: 1, al.AL_FORMAT_STEREO16: 2,
                } [self.format]
        width = property(getWidth)

        def getChannels(self):
            return {
                al.AL_FORMAT_MONO8: 1, al.AL_FORMAT_MONO16: 1,
                al.AL_FORMAT_STEREO8: 2, al.AL_FORMAT_STEREO16: 2,
                } [self.format]
        channels = property(getChannels)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        @classmethod
        def defaultDeviceName(klass):
            cVal = alc.alcGetString(None, alc.ALC_CAPTURE_DEFAULT_DEVICE_SPECIFIER)
            return alc.cast(cVal, alc.c_char_p).value

        @classmethod
        def defaultDevice(klass):
            return klass()

        @classmethod
        def allDeviceNames(klass):
            cVal = alc.alcGetString(None, alc.ALC_CAPTURE_DEVICE_SPECIFIER)
            return multiNullString(cVal)

        @classmethod
        def allDevices(klass):
            devices = [klass(name) for name in klass.allDeviceNames()]
            if not devices:
                devices = [klass()]
            return devices

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _capturing = False
        def getCapturing(self):
            return self._capturing
        isCapturing = getCapturing
        def setCapturing(self, capturing):
            self._capturing = capturing
        capturing = property(getCapturing, setCapturing)

        def start(self):
            alc.alcCaptureStart(self)
            self.setCapturing(True)
        def stop(self):
            alc.alcCaptureStop(self)
            self.setCapturing(False)
        def samples(self, count=None):
            if not self.isCapturing():
                return ''

            count = min(self.sampleCount, count or self.entryCount)
            if count:
                alc.alcCaptureSamples(self, self._buffer, count)
                return self._buffer[:count*self.entrySize]
            else: return ''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Context import
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from device import Device


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

import sys
import time
import threading
from TG.ext.openAL._properties import *
from TG.ext.openAL.raw import al, alc

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Context(ALIDObject):
    def __init__(self, device=None, attrs=[]):
        if device is not False:
            self.create(device, attrs)
        
    def __del__(self):
        try:
            self.destroy()
        except Exception:
            sys.excepthook(*sys.exc_info())
            raise

    _mapping = {}
    def _setAsParam(self, asParam):
        ALIDObject._setAsParam(self, asParam)
        self._mapping[asParam] = self
    
    @classmethod
    def _fromContextPtr(klass, asParam):
        return klass._mapping[asParam]

    def create(self, device=None, attrs=[]):
        """Attrs is a packed list of:
            ALC_FREQUENCY:
                Frequency for mixing output buffer, in units of Hz 
            ALC_REFRESH:
                Refresh intervals, in units of Hz 
            ALC_SYNC:
                Flag, indicating a synchronous context 
            ALC_MONO_SOURCES:
                A hint indicating how many sources should be capable of supporting mono data 
            ALC_STEREO_SOURCES:
                A hint indicating how many sources should be capable of supporting stereo data 
        """
        if self._hasAsParam():
            raise Exception("Context already initialized")

        if attrs:
            attrs = map(int, attrs) + [0]
        else: attrs = None

        self._setAsParam(alc.alcCreateContext(device, attrs))
        self._device = device
        device._addContext(self)
        self._device = device
        self.makeCurrent()

    __dealocating = False
    def destroy(self):
        if self._hasAsParam() and not self.__dealocating:
            self.__dealocating = True
            try:
                self.makeCurrent()
                self.delSources()
                self.delBuffers()

                alc.alcDestroyContext(self)

            finally:
                self._delAsParam()
                self._device = None

    def makeCurrent(self):
        return bool(alc.alcMakeContextCurrent(self))
    select = makeCurrent

    _ctxThread = None
    def stopThread(self, timeout=1):
        t = self._ctxThread 
        if t is not None:
            t.stopProcessing = True
            t.wait(timeout)

    def processInThread(self, start=True):
        ctxThread = threading.Thread(None, self._processForeverInThread, "OpenAL-process-thread")
        ctxThread.setDaemon(True)
        ctxThread.stopThread = False
        if start:
            ctxThread.start()
        self._ctxThread = ctxThread
        return self._ctxThread

    def _processForeverInThread(self, frequency=120):
        sec = 1./frequency
        ctxThread = threading.currentThread()
        while not ctxThread.stopThread:
            self.process()
            time.sleep(sec)

    def process(self):
        self.makeCurrent()
        for src in self.getSources():
            src.process()
        for cap in self.getCaptures():
            cap.process()
        alc.alcProcessContext(self)

    def suspend(self):
        alc.alcSuspendContext(self)

    @classmethod
    def getCurrent(klass):
        return klass._fromContextPtr(alc.alcGetCurrentContext())
    def getDevice(self):
        result = self._device
        if result is None:
            result = Device.fromContext(self)
        return result
    device = property(getDevice)

    def getAttrs(self):
        return self._getAttrsFor(self)
    attrs = property(getAttrs)

    @classmethod
    def getDefaultAttrs(self):
        return self._getAttrsFor(None)

    @classmethod
    def _getAttrsFor(klass, alid):
        bytes = (alc.ALCint*1)()
        alc.alcGetIntegerv(alid, alc.byref(bytes))
        bytes = (alc.ALCint*bytes[0])()
        alc.alcGetIntegerv(alid, alc.byref(bytes))
        return bytes[:]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Source Collection
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _sources = None
    def getSources(self):
        if self._sources is None:
            self.setSources(set())
        return self._sources
    def setSources(self, sources):
        self._sources = sources
    def delSources(self):
        if self._sources is not None:
            while self._sources:
                src = self._sources.pop()
                src.destroy()
            del self._sources
    sources = property(getSources, setSources, delSources)

    def addSource(self, source):
        self.getSources().add(source)
    def removeSource(self, source):
        self.getSources().discard(source)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Capture Collection
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _captures = None
    def getCaptures(self):
        if self._captures is None:
            self.setCaptures(set())
        return self._captures
    def setCaptures(self, captures):
        self._captures = captures
    def delCaptures(self):
        if self._captures is not None:
            while self._captures:
                src = self._captures.pop()
                src.destroy()
            del self._captures
    captures = property(getCaptures, setCaptures, delCaptures)

    def addCapture(self, capture):
        self.getCaptures().add(capture)
    def removeCapture(self, capture):
        self.getCaptures().discard(capture)


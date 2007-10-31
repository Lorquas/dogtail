# -*- coding: utf-8 -*-
"""
Logging facilities

Authors: Ed Rousseau <rousseau@redhat.com>, Zack Cerza <zcerza@redhat.com, David Malcolm <dmalcolm@redhat.com>
"""

__author__ = """Ed Rousseau <rousseau@redhat.com>,
Zack Cerza <zcerza@redhat.com,
David Malcolm <dmalcolm@redhat.com>
"""
import os
import sys
import time
import datetime
from config import config
import codecs

# Timestamp class for file logs
class TimeStamp:
    """
    Generates timestamps tempfiles and log entries
    """
    def __init__(self):
        self.now = "0"
        self.timetup = time.localtime()

    def zeroPad(self, int, width = 2):
        """
        Pads an integer 'int' with zeroes, up to width 'width'.

        Returns a string.

        It will not truncate. If you call zeroPad(100, 2), '100' will be returned.
        """
        if int < 10 ** width:
            return ("0" * (width - len(str(int))) ) + str(int)
        else:
            return str(int)

    # file stamper
    def fileStamp(self, filename, addTime = True):
        """
        Generates a filename stamp in the format of filename_YYYYMMDD-hhmmss.
        A format of filename_YYYYMMDD can be used instead by specifying addTime = False.
        """
        self.now = filename.strip() + "_"
        self.timetup = time.localtime()

        # Should produce rel-eng style filestamps
        # format it all pretty by chopping the tuple
        fieldCount = 3
        if addTime: fieldCount = fieldCount + 3
        for i in range(fieldCount):
            if i == 3: self.now = self.now + '-'
            self.now = self.now + self.zeroPad(self.timetup[i])
        return self.now

    # Log entry stamper
    def entryStamp(self):
        """
        Generates a logfile entry stamp of YYYY.MM.DD HH:MM:SS
        """
        self.timetup = time.localtime()

        # This will return a log entry formatted string in YYYY.MM.DD HH:MM:SS
        for i in range(6):
            # put in the year
            if i == 0:
                self.now = str(self.timetup[i])
            # Format Month and Day
            elif i == 1 or i == 2:
                self.now = self.now + "." + self.zeroPad(self.timetup[i])
            else:
                x = self.timetup[i]
                # make the " " between Day and Hour and put in the hour
                if i == 3:
                    self.now = self.now + " " + self.zeroPad(self.timetup[i])
                # Otherwise Use the ":" divider
                else:
                    self.now = self.now + ":" + self.zeroPad(self.timetup[i])
        return self.now

class IconLogger:
    """
    Writes entries to the tooltip of an icon in the notification area or the desktop.
    """
    trayicon = None
    def __init__(self):
        if not IconLogger.trayicon:
            from trayicon import TrayIcon
            IconLogger.trayicon = TrayIcon()
            if IconLogger.trayicon.proc: self.works = True
            else: self.works = False
            iconName = 'dogtail-tail-48.png'
            iconPath = '/usr/share/icons/hicolor/48x48/apps/' + iconName
            if os.path.exists(iconPath):
                IconLogger.trayicon.set_icon(iconPath)
            self.message('dogtail running...')

    def message(self, msg):
        """
        Display a message to the user
        """
        IconLogger.trayicon.set_tooltip(msg)

    def __del__(self):
        IconLogger.trayicon.close()

class Logger:
    """
    Writes entries to standard out, and to an IconLogger if desired.
    """
    iconLogger = None
    stamper = TimeStamp()
    def __init__(self, logName, file = False, stdOut = True):
        """
        FIXME! make this log to a file based on the name arg.

        name: the name of the log

        file: The file object to log to.

        stdOut: Whether to log to standard out.
        """
        self.logName = logName
        self.stdOut = stdOut
        self.file = file # Handle to the logfile
        if not self.file: return

        logDir = config.logDir
        if not os.path.isdir(logDir): os.makedirs(logDir)

        scriptName = config.scriptName
        if not scriptName: scriptName = 'log'
        self.fileName = scriptName

        # check to see if we can write to the logDir
        if os.path.isdir(logDir):
            # generate a logfile name and check if it already exists
            self.fileName = logDir + self.stamper.fileStamp(self.fileName) + '_' + self.logName
            i = 0
            while os.path.exists(self.fileName):
                # Append the pathname
                if i == 0:
                    self.fileName = self.fileName + "." + str(i)
                else:
                    logsplit = self.fileName.split(".")
                    logsplit[-1] = str(i)
                    self.fileName = ".".join(logsplit)
                i += 1
        else:
            # If path doesn't exist, raise an exception
            raise IOError, "Log path %s does not exist or is not a directory" % logDir

        # Try to create the file and write the header info
        try:
            print "Creating logfile at %s ..." % self.fileName
            self.file = codecs.open(self.fileName, mode = 'wb', encoding = 'utf-8')
            self.file.write("##### " + os.path.basename(self.fileName) + '\n')
            self.file.flush()
            #self.file.close()
        except IOError:
            print "Could not create and write to " + self.fileName
            self.file = False

    def log(self, message):
        """
        Hook used for logging messages. Might eventually be a virtual
        function, but nice and simple for now.
        """
        message = message.decode('utf-8', 'replace')

        # Try to use the IconLogger.
        if self.iconLogger and self.iconLogger.works:
            self.iconLogger.message(message)
        
        # Also write to standard out.
        if self.stdOut and config.logDebugToStdOut: print message

        # Try to open and write the result to the log file.
        if not self.file: return
        try:
            #self.file = open(self.fileName, 'a')
            self.file.write(message + '\n')
            self.file.flush()
            #self.file.close()
        except IOError:
            print "Could not write to file " + self.fileName

class ResultsLogger(Logger):
    """
    Writes entries into the Dogtail log
    """
    def __init__(self, stdOut = True):
        Logger.__init__(self, 'results', file = True, stdOut = stdOut)
        # Set the logDir - maybe we want to use mktemp(1) for this later.

    # Writes the result of a test case comparison to the log
    def log(self, entry):
        """
        Writes the log entry. Requires a 1 {key: value} pair dict for an argument or else it will throw an exception.
        """
        # We require a 1 key: value dict
        # Strip all leading and trailing witespace from entry dict and convert
    # to string for writing

        if len(entry) == 1:
            key = entry.keys()
            value = entry.values()
            key = key[0]
            value = value[0]
            entry = str(key) + ":      " + str(value)
        else:
            raise ValueError, entry
            print "Method argument requires a 1 {key: value} dict. Supplied argument not one {key: value}"

        Logger.log(self, self.stamper.entryStamp() + "      " + entry)

debugLogger = Logger('debug', config.logDebugToFile)

import traceback
def exceptionHook(exc, value, tb):
    tbStringList = traceback.format_exception(exc, value, tb)
    tbString = ''.join(tbStringList)
    debugLogger.log(tbString)
    sys.exc_clear()

sys.excepthook = exceptionHook

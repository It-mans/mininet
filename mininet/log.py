"Logging functions for Mininet."

import logging
from logging import Logger
import types

LEVELS = { 'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL }

# change this to logging.INFO to get printouts when running unit tests
LOGLEVELDEFAULT = logging.WARNING

#default: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGMSGFORMAT = '%(message)s'


# Modified from python2.5/__init__.py
class StreamHandlerNoNewline( logging.StreamHandler ):
    """StreamHandler that doesn't print newlines by default.
       Since StreamHandler automatically adds newlines, define a mod to more
       easily support interactive mode when we want it, or errors-only logging
       for running unit tests."""

    def emit( self, record ):
        """Emit a record.
           If a formatter is specified, it is used to format the record.
           The record is then written to the stream with a trailing newline
           [ N.B. this may be removed depending on feedback ]. If exception
           information is present, it is formatted using
           traceback.printException and appended to the stream."""
        try:
            msg = self.format( record )
            fs = '%s' # was '%s\n'
            if not hasattr( types, 'UnicodeType' ): #if no unicode support...
                self.stream.write( fs % msg )
            else:
                try:
                    self.stream.write( fs % msg )
                except UnicodeError:
                    self.stream.write( fs % msg.encode( 'UTF-8' ) )
            self.flush()
        except ( KeyboardInterrupt, SystemExit ):
            raise
        except:
            self.handleError( record )


class Singleton( type ):
    """Singleton pattern from Wikipedia
       See http://en.wikipedia.org/wiki/SingletonPattern#Python

       Intended to be used as a __metaclass_ param, as shown for the class
       below.

       Changed cls first args to mcs to satisfy pylint."""

    def __init__( mcs, name, bases, dict_ ):
        super( Singleton, mcs ).__init__( name, bases, dict_ )
        mcs.instance = None

    def __call__( mcs, *args, **kw ):
        if mcs.instance is None:
            mcs.instance = super( Singleton, mcs ).__call__( *args, **kw )
            return mcs.instance


class MininetLogger( Logger, object ):
    """Mininet-specific logger
       Enable each mininet .py file to with one import:

       from mininet.log import [lg, info, error]

       ...get a default logger that doesn't require one newline per logging
       call.

       Inherit from object to ensure that we have at least one new-style base
       class, and can then use the __metaclass__ directive, to prevent this
       error:

       TypeError: Error when calling the metaclass bases
       a new-style class can't have only classic bases

       If Python2.5/logging/__init__.py defined Filterer as a new-style class,
       via Filterer( object ): rather than Filterer, we wouldn't need this.

       Use singleton pattern to ensure only one logger is ever created."""

    __metaclass__ = Singleton

    def __init__( self ):

        Logger.__init__( self, "mininet" )

        # create console handler
        ch = StreamHandlerNoNewline()
        # create formatter
        formatter = logging.Formatter( LOGMSGFORMAT )
        # add formatter to ch
        ch.setFormatter( formatter )
        # add ch to lg
        self.addHandler( ch )

        self.setLogLevel()

    def setLogLevel( self, levelname=None ):
        """Setup loglevel.
           Convenience function to support lowercase names.

           levelName: level name from LEVELS"""
        level = LOGLEVELDEFAULT
        if levelname != None:
            if levelname not in LEVELS:
                raise Exception( 'unknown loglevel seen in set_loglevel' )
            else:
                level = LEVELS.get( levelname, level )

        self.setLevel( level )
        self.handlers[ 0 ].setLevel( level )


lg = MininetLogger()
info = lg.info
error = lg.error

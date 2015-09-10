"""
Utilities to manage mongod service
"""
import subprocess as sp
import socket
import sys
import time

class Mongod(object):
    """
    Utility class to manage mongod service
    """
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        if 'mongod_bin' in self.kwargs:
            self.mongod_bin = kwargs['mongod_bin']
        else:
            self.mongod_bin = "mongod"
        if 'port' in self.kwargs:
            self.port = int(kwargs['port'])
        else:
            self.port = 27017
        if 'db_path' in self.kwargs:
            self.db_path = kwargs['db_path']
        else:
            self.db_path = "db"

        self.proc = None

    def is_mongod_running(self):
        """Return True if mongod is up and listening on defined port"""
        
        try:
            _connect_to_mongo_port(int(self.port))
            return True
        except OSError:
            return False
        except Exception:
            return False    

    def did_mongod_start(self, port=0, timeout=60):
        """
        Wait timeout secs trying to connect to mongod defined port.
        Return True as soon as connection succeed or False if could not connect after timeout.
        """
        if port == 0:
            port = self.port
        
        while timeout > 0:
            time.sleep(1)
            try:
                _connect_to_mongo_port(int(port))
                return True
            except OSError as ex:
                print >> sys.stderr, ex
                timeout = timeout - 1
            except Exception as ex:
                print >> sys.stderr, ex
                timeout = timeout - 1
        print >> sys.stderr, "timeout starting mongod"
        return False

    def start(self):
        """Start mongod instance using defined port and db path"""
        
        if self.is_mongod_running():
            return
        
        cmd = self.mongod_bin + " --port " + str(self.port) + " --smallfiles --dbpath " + self.db_path + " > /dev/null &"
        #if self.kwargs.get('noJournal'):
            #argv += ['--nojournal']
        #if self.kwargs.get('noPreallocj'):
            #argv += ['--nopreallocj']
        print "---------- Starting MongoDB"
        print cmd

        try:
            sp.call(cmd, shell=True)
        except OSError as ex:
            print 'Problem in file:' + __file__
            print ex.child_traceback
        except Exception as ex:
            print 'Problem in file:' + __file__
            print ex.child_traceback

        if not self.did_mongod_start(self.port):
            raise Exception("Failed to start mongod")

    def stop(self): # pylint: disable=R0201
        """killall mongod processes"""
        
        if not self.is_mongod_running():
            return
        
        try:
            print "---------- Stopping MongoDB"      
            sp.call('killall mongod', shell=True)
            time.sleep(1)
            sp.call('killall -9 mongod')
        except OSError:
            pass

def _connect_to_mongo_port(port):
    """Try to connect to mongod listening port. Raise exception under failure"""
         
    sock = socket.socket()
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    sock.settimeout(1)
    sock.connect(("localhost", int(port)))
    sock.close()

from abc import ABCMeta, abstractmethod

"""
    Data access objects

    source     - A definition of the source of prefixlist, provides 
                 as-set/as-number and registry
    prefixlist - A list of prefixes and member as-numbers fetched at a
                 point in time from the routing registry
"""

class BaseDAO(metaclass=ABCMeta):

    @abstractmethod
    def store_prefixlist(self, source, prefixlist):
        """ Store a fetched prefixlist in persistent storage """
        pass

    @abstractmethod
    def load_prefixlist(self, source, version=None):
        """ Load prefixlist of specified version from persistent storage """
        pass

    @abstractmethod
    def list_prefixlist(self, source):
        """ List available versions of the specified list """
        pass

    @abstractmethod
    def store_source(self, data):
        """ Store a new source definition """
        pass

    @abstractmethod
    def load_source(self, source):
        """ Load a source definition """
        pass

    @abstractmethod
    def list_source(self):
        """ List all sources """
        pass

    @abstractmethod
    def remove_source(self, source):
        """ Remove source definition """
        pass

    @abstractmethod
    def update_source(self, source, data):
        """ Update source definition """
        pass

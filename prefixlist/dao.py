from abc import ABCMeta, abstractmethod
from . import prefixlist

"""
    Data access objects

    source     - A definition of the source of prefixlist, provides 
                 as-set/as-number and registry
    prefixlist - A list of prefixes and member as-numbers fetched at a
                 point in time from the routing registry
"""

class BaseDAO(metaclass=ABCMeta):

    def store_prefixlist(self, source, prefixlist):
        """ Store a fetched prefixlist in persistent storage """
        if type(source) is not int or source < 1:
            raise ValueError("Attribute source should be a positive integer")
        if type(prefixlist) is not prefixlist.PrefixList:
            raise ValueError("Attribute prefixlist should be a PrefixList instance")

        return self.store_prefixlist_exec(source, prefixlist)

    @abstractmethod
    def store_prefixlist_exec(self, source, prefixlist):
        """ implementation of store_prefixlist """
        pass

    def load_prefixlist(self, source, version=None):
        """ Load prefixlist of specified version from persistent storage """

        if type(source) is not int or source < 1:
            raise ValueError("Attribute source should be a positive integer")
        if version is not None and (type(version) is not int or (type(version) is int and version < 1)):
            raise ValueError("Attribute version should be None or a positive integer")

        return self.load_prefixlist_exec(source, version)

    @abstractmethod
    def load_prefixlist_exec(self, source, version):
        """ Implementation of load_prefixlist """
        pass

    def list_prefixlist(self, source):
        """ List available versions of the specified list """

        if type(source) is not int or source < 1:
            raise ValueError("Attribute source should be a positive integer")

        return self.list_prefixlist_exec(source)


    @abstractmethod
    def list_prefixlist_exec(self, source):
        """ Implementation of list_prefixlist """
        pass

    def store_source(self, data):
        """ Store a new source definition """
        # FIXME: Perform input validation
        return self.store_source_exec(data)

    @abstractmethod
    def store_source_exec(self, data):
        """ Implementation of store_source """
        pass

    def load_source(self, source):
        """ Load a source definition """

        if type(source) is not int or source < 1:
            raise ValueError("Attribute source should be a positive integer")

        return self.load_source_exec(source)

    @abstractmethod
    def load_source_exec(self, source):
        """ Implementation of load_source """
        pass

    def list_source(self):
        """ List all sources """
        return self.list_source_exec()

    @abstractmethod
    def list_source_exec(self):
        """ implementation of list_source """
        pass

    def remove_source(self, source):
        """ Remove source definition """

        if type(source) is not int or source < 1:
            raise ValueError("Attribute source should be a positive integer")

        return self.remove_source_exec(source)

    @abstractmethod
    def remove_source_exec(self, source):
        """ Implementation of remove_source """
        pass

    def update_source(self, source, data):
        """ Update source definition """
        # FIXME: perform input validation
        return self.update_source_exec(source, data)

    @abstractmethod
    def update_source_exec(self, source, data):
        """ Implementation of update_source """
        pass

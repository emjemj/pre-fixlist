from abc import ABCMeta, abstractmethod
from . import prefixlist

"""
    Data access objects

    rpsl_object - A definition of the prefixlist, provides 
                  as-set/as-number and registry
    prefixlist  - A list of prefixes and member as-numbers fetched at a
                  point in time from the routing registry
"""

class BaseDAO(metaclass=ABCMeta):

    def store_prefixlist(self, rpsl_object, prefixlist):
        """ Store a fetched prefixlist in persistent storage """
        if type(rpsl_object) is not int or rpsl_object < 1:
            raise ValueError("Attribute rpsl_object should be a positive integer")
        if type(prefixlist) is not prefixlist.PrefixList:
            raise ValueError("Attribute prefixlist should be a PrefixList instance")

        return self.store_prefixlist_exec(rpsl_object, prefixlist)

    @abstractmethod
    def store_prefixlist_exec(self, rpsl_object, prefixlist):
        """ implementation of store_prefixlist """
        pass

    def load_prefixlist(self, rpsl_object, version=None):
        """ Load prefixlist of specified version from persistent storage """

        if type(rpsl_object) is not int or rpsl_object < 1:
            raise ValueError("Attribute rpsl_object should be a positive integer")
        if version is not None and (type(version) is not int or (type(version) is int and version < 1)):
            raise ValueError("Attribute version should be None or a positive integer")

        return self.load_prefixlist_exec(rpsl_object, version)

    @abstractmethod
    def load_prefixlist_exec(self, rpsl_object, version):
        """ Implementation of load_prefixlist """
        pass

    def list_prefixlist(self, rpsl_object):
        """ List available versions of the specified list """

        if type(rpsl_object) is not int or rpsl_object < 1:
            raise ValueError("Attribute rpsl_object should be a positive integer")

        return self.list_prefixlist_exec(rpsl_object)


    @abstractmethod
    def list_prefixlist_exec(self, rpsl_object):
        """ Implementation of list_prefixlist """
        pass

    def store_rpsl_object(self, data):
        """ Store a new rpsl_object definition """
        # FIXME: Perform input validation
        return self.store_rpsl_object_exec(data)

    @abstractmethod
    def store_rpsl_object_exec(self, data):
        """ Implementation of store_rpsl_object """
        pass

    def load_rpsl_object(self, rpsl_object):
        """ Load a rpsl_object definition """

        if type(rpsl_object) is not int or rpsl_object < 1:
            raise ValueError("Attribute rpsl_object should be a positive integer")

        return self.load_rpsl_object_exec(rpsl_object)

    @abstractmethod
    def load_rpsl_object_exec(self, rpsl_object):
        """ Implementation of load_rpsl_object """
        pass

    def list_rpsl_object(self):
        """ List all rpsl objects """
        return self.list_rpsl_object_exec()

    @abstractmethod
    def list_rpsl_object_exec(self):
        """ implementation of list_rpsl_object """
        pass

    def remove_rpsl_object(self, rpsl_object):
        """ Remove rpsl_object definition """

        if type(rpsl_object) is not int or rpsl_object < 1:
            raise ValueError("Attribute rpsl_object should be a positive integer")

        return self.remove_rpsl_object_exec(rpsl_object)

    @abstractmethod
    def remove_rpsl_object_exec(self, rpsl_object):
        """ Implementation of remove_rpsl_object """
        pass

    def update_rpsl_object(self, rpsl_object, data):
        """ Update rpsl_object definition """
        # FIXME: perform input validation
        return self.update_rpsl_object_exec(rpsl_object, data)

    @abstractmethod
    def update_rpsl_object_exec(self, rpsl_object, data):
        """ Implementation of update_rpsl_object """
        pass

from abc import ABCMeta, abstractmethod
from expandas.model import ASNumber, ASSet

class BaseValidator(metaclass=ABCMeta):
    actions = { "permit": True, "deny": False }

    def __init__(self, config):
        
        if type(config) is not dict:
            raise ValueError("Config should be a dict")

        if "violation_action" not in config:
            raise ValueError("Missing required element violation_action in config")

        if "default_action" in config:
            try:
                self.default_action = self.actions[config["default_action"]]
            except:
                raise ValueError("Invalid default action: {}".format(config["default_action"]))
        else:
                self.default_action = self.actions["permit"]

        self.violation_action = config["violation_action"]
        try:
            self.violation_action = self.actions[config["violation_action"]]
        except:
            raise ValueError("Invalid violation action: {}".format(config["violation_action"]))
        self.config = config

    def validate(self, new, old):
        # FIXME: Add some input checking!
        self.validate_entity(new, old)

    @abstractmethod
    def validate_entity(self, new, old):
        """ Implement your validation logic here """
        pass

    def default(self, obj):
        """ Apply default action on object """
        self.apply_action(obj, self.default_action)

    def violate(self, obj):
        """ Apply violation action on object """
        self.apply_action(obj, self.violation_action)

    def apply_action(self, obj, action):
        """ Apply specified action on object """

        # don't overwrite previous validators.
        if obj["permit"] == False:
            return

        obj["permit"] = action

        # Also set for prefixes if they exist
        if "inet" in obj:
            for pfx in obj["inet"]:
                pfx["permit"] = action

        if "inet6" in obj:
            for pfx in obj["inet6"]:
                pfx["permit"] = action

class MemberASNValidator(BaseValidator):
    """ Validate member asns, apply default action for members not found in list and
        violation action for members found """

    def __init__(self, config):
        super().__init__(config)

        if "asns" not in self.config:
            raise ValueError("Missing required parameter asns in config")

        self.asns = self.config["asns"]

    def validate_entity(self, new, old):
        for member in new:
            if member["asn"] in self.asns:
                self.violate(member)
            else:
                self.default(member)

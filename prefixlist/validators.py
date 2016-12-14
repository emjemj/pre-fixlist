from abc import ABCMeta, abstractmethod
from expandas.model import ASNumber, ASSet

class BaseValidator(metaclass=ABCMeta):
    actions = [ "permit", "deny", "validate" ]

    def __init__(self, config):
        
        if type(config) is not dict:
            raise ValueError("Config should be a dict")

        if "violation_action" not in config:
            raise ValueError("Missing required element violation_action in config")

        if config["violation_action"] not in self.actions:
            raise ValueError("Invalid violation_action {}".format(config["violation_action"]))
        if "default_action" in config:
            self.default_action = config["default_action"]
        else:
            self.default_action = "permit"

        self.config = config
        self.violation_action = config["violation_action"]

    def validate(self, asset):
        if type(asset) is not ASSet:
            raise ValueError("Validation is only possible for ASSets")

        print("Executing validator {}".format(self.config["description"]))

        result = []
        for member in asset:
            result.append({"member": member, "action": self.validate_entity(member) })

        return result


    @abstractmethod
    def validate_entity(self, entity):
        """ Implements logic for validating a specific entry """
        pass

class MemberASNValidator(BaseValidator):

    def __init__(self, config):
        super().__init__(config)

        if "forbidden_asns" not in self.config:
            raise ValueError("Missing required parameter forbidden_asns in config")

        self.forbidden_asns = self.config["forbidden_asns"]

    def validate_entity(self, entity):
        if type(entity) is not ASNumber:
            raise ValueError("Invalid argument type");

        if entity.asn in self.forbidden_asns:
            return self.violation_action
        else:
            return self.default_action

class Validator:
    required_parameters = [ "class", "description", "violation_action" ]
    
    def __init__(self, config):
        self.validators = []

        # Do boring configuration parsing
        if "default" in config:
            if "violation_action" in config["default"]:
                self.default_violation_action = config["default"]["violation_action"]
        else:
                self.default_violation_action = None
        if "validators" in config:
            # Instantiate validators
            for validator in config["validators"]:
                self.__load_validator(validator)


    def __load_validator(self, validator):
        if "violation_action" not in validator:
            if self.default_violation_action is not None:
                validator["violation_action"] = self.default_violation_action

        for param in self.required_parameters:
            if param not in validator:
                raise Exception("Missing required argument {}".format(param))

        klass = self.__load_class(validator["class"])
        instance = klass(validator)

        self.validators.append(instance)


    def __load_class(self, classname):
        mod = __import__("prefixlist.validators", fromlist = [ classname ])
        klass = getattr(mod, classname)

        return klass

    def validate(self, new, old):
        for validator in self.validators:
            validator.validate(new, old)

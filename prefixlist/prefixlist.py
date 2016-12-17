class PrefixList:
    """ The PrefixList holds the data received from routing registries and
        the validation results of this data. """

    def __init__(self, name):
        self.name = name
        self.members = []

    def __iter__(self):
        for member in self.members:
            yield member

    def add_member(self, member):
        memb = {
            "asn": member.asn,
            "permit": None,
            "inet": [],
            "inet6": []
        }

        for prefix in member.inet:
            p = {
                "prefix": prefix,
                "permit": None
            }

            memb["inet"].append(p)

        for prefix in member.inet6:
            p = {
                "prefix": prefix,
                "permit": None
            }
            memb["inet6"].append(p)

        self.members.append(memb)

    @classmethod
    def from_asset(cls, asset):
        obj = PrefixList(asset.name)

        for member in asset:
            obj.add_member(member)

        return obj

    def debug(self):
        for member in self.members:
            print("AS{}: {}".format(member["asn"], member["permit"]))
            for i in member["inet"]:
                print("--{}: {}".format(i["prefix"], i["permit"]))
            for i in member["inet6"]:
                print("--{}: {}".format(i["prefix"], i["permit"]))

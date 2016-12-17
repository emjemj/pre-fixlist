class PrefixList:
    """ The PrefixList holds the data received from routing registries and
        the validation results of this data. """

    def __init__(self, name):
        self.name = name
        self.members = {}

    def __iter__(self):
        for asn in self.members:
            yield self.members[asn]

    def add_member(self, member):

        if member.asn in self.members:
            return

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

        self.members[member.asn] = memb

    @classmethod
    def from_asset(cls, asset):
        obj = PrefixList(asset.name)

        for member in asset:
            obj.add_member(member)

        return obj

    def debug(self):
        for asn in self.members:
            member = self.members[asn]
            print("AS{}: {}".format(asn, member["permit"]))
            for i in member["inet"]:
                print("--{}: {}".format(i["prefix"], i["permit"]))
            for i in member["inet6"]:
                print("--{}: {}".format(i["prefix"], i["permit"]))

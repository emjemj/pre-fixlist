import yaml
from prefixlist import validator
from expandas.loader import RIPERESTLoader

with open("config.yml", "r") as stream:
    config = yaml.load(stream)

ldr = RIPERESTLoader()

vldr = validator.Validator(config["validation"])

data = ldr.load_asset("AS-GLESYS")

res = vldr.validate(data)

for x in res:
    print(x)

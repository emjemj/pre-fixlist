import yaml
from prefixlist import updater

with open("config.yml", "r") as stream:
    config = yaml.load(stream)
    upd = updater.Updater(config)
    upd.run()

#!/usr/bin/env python3

from prefixlist.main import PrefixListMain
from time import sleep

main = PrefixListMain("config.yml")  

sleep(10)
main.stop()

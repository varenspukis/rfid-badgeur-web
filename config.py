from configparser import ConfigParser
from collections import namedtuple
import re
import os
from serial import *

cfg = ConfigParser()
cfg.read("badge.conf")

# Output sqlite file
output = cfg['output']['path']
os.makedirs(os.path.dirname(output), exist_ok=True)

serial_port = Serial(port=cfg['badge']['port'], baudrate=4800)

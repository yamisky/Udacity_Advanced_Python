from .MemeEngine import MemeEngine

import os

TEMP_PATH = './tmp'
STATIC_PATH = './static'

if not os.path.exists(TEMP_PATH):
    os.mkdir(TEMP_PATH)

if not os.path.exists(STATIC_PATH):
    os.mkdir(STATIC_PATH)

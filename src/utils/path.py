import os

DIR_UTIL = os.path.split(os.path.abspath(__file__))[0]
DIR_SRC = os.path.normpath(os.path.join(DIR_UTIL, os.pardir))
DIR_ROOT = os.path.normpath(os.path.join(DIR_SRC, os.pardir))

DIR_KEYS = os.path.join(DIR_ROOT, 'keys')

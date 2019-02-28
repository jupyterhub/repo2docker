#!/bin/python3

import sys
import logging
from urllib.error import URLError
from urllib.request import urlopen

try:
    u = urlopen('http://localhost:{}'.format(sys.argv[1]), timeout=2)
    if u.code == 200:
        sys.exit(0)
    logging.warning('STATUS: %i' % u.code)
except URLError as e:
    logging.warning('ERROR: %s' % str(e))
sys.exit(1)

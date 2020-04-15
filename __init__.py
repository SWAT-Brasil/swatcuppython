__version__ = '0.0.1'

import sys

MIN_PYTHON = (3, 6)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required for swatpython.\n" % MIN_PYTHON)

#IS_PYTHON3 = sys.version_info[0] >= 3

# if IS_PYTHON3:
# exec('from .teste import Teste')
# exec('from .swat import SWAT')
##exec('from .operationalsystem import OperationalSystem')
# exec('from .swatversion import SWATVersion')
# else:
# exec('from .teste import Teste')
# exec('from FortranRecordWriter import FortranRecordWriter')
# exec('from swat import SWAT')
# exec('from operationalsystem import OperationalSystem')
# exec('from swatversion import SWATVersion')

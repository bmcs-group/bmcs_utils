
from bmcs_utils.version import __version__

import collections
try:
    # Python 3.9+ compatibility: import from collections.abc directly
    from collections.abc import Iterable
    collections.Iterable = Iterable
except ImportError:
    # Fallback for older Python versions where collections.Iterable exists
    pass

ENABLE_K3D = True
import os

from app.config import APP_ROOT
from .ip2Region import Ip2Region

ip2region = Ip2Region(os.path.sep.join((APP_ROOT, 'app', 'utils', 'ip2addr', 'ip2region.db')))

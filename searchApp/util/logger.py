import logging
import sys, os, platform
import redis
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from django.conf import settings

'''
Log levels:
https://docs.python.org/3/library/logging.html#logging-levels
Exception is logged with ERROR level
'''

class RedisHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)
        self.redisConnection = redis.StrictRedis(settings.REDIS['host'], settings.REDIS['port'], db=0,
                                                 password=settings.REDIS['password'])
        self.keyName = settings.REDIS["collection_prefix"] + "exceptions"
        try:
            if not self.redisConnection.exists(self.keyName):
                self.redisConnection.lpush(self.keyName, "list start")
                self.redisConnection.expire(self.keyName, 3600*24*5)
        except Exception as e:
            pass

    def emit(self, record):
        try:
            msg = self.format(record)
            self.redisConnection.lpush(self.keyName, msg)
        except Exception as e:
            pass

class HostnameFilter(logging.Filter):
    hostname = platform.node()

    def filter(self, record):
        record.hostname = HostnameFilter.hostname
        return True

# Extra handler (stdout)
stdoutHandler = logging.StreamHandler(sys.stdout)
stdoutHandler.setLevel(logging.DEBUG)
stdoutHandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(pathname)s:%(lineno)d: %(message)s'))

# Redis handler
redisHandler = RedisHandler()
redisHandler.addFilter(HostnameFilter())
redisHandler.setLevel(logging.ERROR)
redisHandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(hostname)s %(pathname)s:%(lineno)d: %(message)s'))

# Add all handlers
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(stdoutHandler)
# log.addHandler(redisHandler)
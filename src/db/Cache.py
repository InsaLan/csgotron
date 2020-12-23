import redis
"""
This class  will hold Cache class and utils, aswell as the logger for the cache
"""
class Cache:
    def __init__(self, host, port, db):
        self.port = port
        self.db = db
        self.host = host
        self.redis = redis.Redis(host=self.host, port=self.port, db=self.db)
    

Revokation_list = Cache('localhost',6379, 10)
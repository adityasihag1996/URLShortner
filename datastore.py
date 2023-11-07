import redis

class DataStore:
    def __init__(self, redis_host = 'localhost', redis_port = 6900):
        self.redis_0 = redis.StrictRedis(
            host = redis_host,
            port = redis_port,
            db = 0,
            decode_responses = True
        )

        self.redis_1 = redis.StrictRedis(
            host = redis_host,
            port = redis_port,
            db = 1,
            decode_responses = True
        )

    def get(self, key, db_id = 0):
        db = self.redis_0 if db_id == 0 else self.redis_1
        if db.exists(key):
            return db.lrange(key, 0, -1)
        else:
            return None
    
    def set(self, key, values, expire = None, db_id = 0):
        db = self.redis_0 if db_id == 0 else self.redis_1

        try:
            for value in values:
                db.rpush(key, value)
            
            if expire:
                db.expire(key, expire)

            return True
        except:
            return False
    
    def exists(self, key, db_id = 0):
        db = self.redis_0 if db_id == 0 else self.redis_1

        return db.exists(key)
    
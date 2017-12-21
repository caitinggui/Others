# coding: utf-8

import redis


class RedisPool(object):
    __pool = None

    def __new__(cls, cfs, *args, **kargs):
        if not cls.__pool:
            cls.__pool = super(RedisPool, cls).__new__(cls, *args, **kargs)
            cls.__pool.pool = redis.ConnectionPool(
                host=cfs.get("HOST"),
                port=int(cfs.get("PORT")),
                db=cfs.get("DB"),
                password=cfs.get("PASSWORD"),
                max_connections=int(cfs.get("MAX_CONNECTIONS"))
            )
        return cls.__pool

    def __init__(self, cfs):
        super(RedisPool, self).__init__(cfs)

    def get_connection(self):
        return redis.StrictRedis(connection_pool=RedisPool.__pool.pool)

    def __getattr__(self, conn):
        return redis.StrictRedis(connection_pool=RedisPool.__pool.pool)


if __name__ = "__main__":
    redis_config = {
        "HOST": "192.168.10.53",
        "PORT": 6002,
        "DB": 3,
        "MAX_CONNECTIONS": 20,
        "PASSWORD": "password"}
    redis = RedisPool(redis_config)
    # 这里conn和redis.conn是等价的，用完之后都会被redispool 自动回收
    conn = redis.get_connection()
    print(redis.conn.dbsize())
    print(conn.dbsize())

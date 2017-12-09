# coding: utf-8

"""
python实现单例模式的多种方法
"""

import redis


class Singleton(object):
    """可作为单例的父类"""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


def singleClass(cls):
    _instance = {}

    def wrapper(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return wrapper


class RedisPool(object):
    """直接就是单例的类"""
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

    def get_connection(self):
        return redis.StrictRedis(connection_pool=RedisPool.__pool.pool)


if __name__ == "__main__":
    class AS(Singleton):
        num = 0

        def __init__(self):
            AS.num += 1

    @singleClass
    class BS(object):
        def __init__(self):
            pass

    a1 = AS()
    print AS.num
    a2 = AS()
    print AS.num
    print "a1 id:", id(a1)
    print "a2 id:", id(a2)

    b1 = BS()
    b2 = BS()
    assert(id(b1) == id(b2))

    pool = RedisPool(configs.get("redis"))
    print pool.get_connection()

# backend/__init__.py
import redis

def clear_redis():
    client = redis.Redis(host='localhost', port=6379, db=0)
    client.flushdb()

clear_redis()

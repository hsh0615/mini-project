# backend/__init__.py
import os
import redis

def clear_redis():
    redis_host = 'redis' if os.getenv('DJANGO_ENV') == 'docker' else 'localhost'
    client = redis.Redis(host=redis_host, port=6379, db=0)
    client.flushdb()

clear_redis()

from redis import Redis

REDIS_SERVER = 'localhost'
REDIS_PORT = 6379

IP_NETWORK_DB_NUM = 1
IP_INDEX_DB_NUM = 0
IP_NETWORK_DB = Redis(host=REDIS_SERVER, port=REDIS_PORT, db=IP_NETWORK_DB_NUM, decode_responses=True)
INDEX_DB = Redis(host=REDIS_SERVER, port=REDIS_PORT, db=IP_INDEX_DB_NUM, decode_responses=True)

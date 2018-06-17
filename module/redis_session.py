#coding:utf-8
from redis import Redis
from uuid import uuid4

import sys
sys.path.append('../../metadata')
import monday_sql_config as config

class RedisSession:
    def __init__(self, config):
        self.prefix = config['prefix']
        self.timeout = config['timeout']
        self.db = Redis(host=config['host'], port=config['port'], db=config['db'], decode_responses=True)

    # 세션이 있으면 타임아웃 만큼 다시 연장해주고 없으면 False 있으면 사용자id 리턴
    def open_session(self, session_key):
        user_name = self.db.get(self.prefix+session_key)
        if user_name is not None:
            self.db.expire(self.prefix+session_key, self.timeout)
        return user_name

    # 신규 세션 요청 시 세션 값을 만들어서 리턴
    def save_session(self, user_name):
        session_key = str(uuid4())
        self.db.setex(self.prefix+session_key, user_name, self.timeout)
        return session_key

if __name__ == "__main__" :
    r = RedisSession(config.REDIS_SESS_CONF)
    session_key = r.save_session('01012345678')
    print(session_key)
    user_name = r.open_session(session_key)
    if user_name:
        print(user_name)

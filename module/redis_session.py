#coding:utf-8
# 작성자 유진세
# redis 를 통해서 세션 관리를 한다.
from redis import Redis
from uuid import uuid4

class redis_session:
    prefix = 'was:session_key:'
    server_ip = '192.168.0.20'
    port = 6379
    timeout = 3600

    def __init__(self):
        self.db = Redis(self.server_ip, self.port)

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
    r = redis_session()
    #session_key = r.save_session()
    if r.open_session('b0b6b52b-1d72-43fe-bdf3-69248a73383d') :
        print "1234"
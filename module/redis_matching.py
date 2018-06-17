#coding:utf-8
from redis import Redis
from twilio.rest import Client
from time import time
import math

import sys
sys.path.append('../../metadata')
import monday_sql_config as config

class RedisMatching:
    def __init__(self, config):
        self.db = Redis(host=config['host'], port=config['port'], db=config['db'], decode_responses=True)
        self.msg_client = Client(config['account_sid'], config['auth_token']).messages
        self.msg_sender = config['sender']

    def set_userdata(self, user_data):
        user_data['timestamp'] = int(time())
        return self.db.hmset(user_data['phone_numb'], user_data)

    def get_userdata(self, user_name):
        return self.db.hgetall(user_name)

    def get_all_user(self):
        return self.db.keys()

    def remove_userdata(self, user_name):
        return self.db.delete(user_name)

    def send_message(self, phone_numb, message):
        phone_numb = '+82'+phone_numb[1:]
        result = self.msg_client.create(to=phone_numb,
                                        from_=self.msg_sender,
                                        body=message
                                        )
        return result

    def initialize(self):
        for key in self.get_all_user():
            self.db.delete(key)

    def match_user(self):
        def make_food_vector(user_data):
            food_vector = [ int(user_data['cutlet']),
                            int(user_data['hamburger']),
                            int(user_data['noodle']),
                            int(user_data['korean_food']) ]
            return food_vector
        def make_message_text(target_name, user_data, similarity=0):
            if user_data['gender'] == 'male' : user_data['gender'] = '남'
            elif user_data['gender'] == 'female' : user_data['gender'] = '여'
            text ='%s님, 혼밥러 매칭완료!\n\n상대 : %s님\n연락처 : %s\n성별 : %s\n유사도 : %0.2f' \
                    %(target_name, user_data['user_name']
                        , user_data['phone_numb'], user_data['gender']
                        , similarity*100)
            return text

        while(len(self.get_all_user()) >= 2):
            user_list = self.get_all_user()
            user_data_list = list(map(self.get_userdata, user_list))
            user_data_list = [[user_data['timestamp'], user_data] for user_data in user_data_list]
            user_data_list = [user_data[1] for user_data in sorted(user_data_list)]
            print(user_data_list)

            target_user = user_data_list[0]
            target_vec = make_food_vector(target_user)

            similarity_list = []
            for user_data in user_data_list[1:]:
                user_vec = make_food_vector(user_data)
                similarity = RedisMatching.cosine_similarity(target_vec, user_vec)
                similarity_list.append( (similarity, user_data) )

            max_val = max(similarity_list)
            print(max_val)
            text = make_message_text(target_user['user_name'], max_val[1], max_val[0])
            self.send_message(target_user['phone_numb'], text)
            print(text)
            text = make_message_text(max_val[1]['user_name'], target_user, max_val[0])
            self.send_message(max_val[1]['phone_numb'], text)
            print(text)

            # self.remove_userdata(target_user['phone_numb'])
            # self.remove_userdata(max_val[1]['phone_numb'])

            return True

    @staticmethod
    def cvt_unit_vec(vector):
        scalar =  math.sqrt(sum([i*i for i in vector]))
        return [idx/scalar for idx in vector]

    @staticmethod
    def cosine_similarity(a, b):
        a = RedisMatching.cvt_unit_vec(a)
        b = RedisMatching.cvt_unit_vec(b)
        return sum([i*j for i,j in zip(a, b)])

    @staticmethod
    def custom_similarity(a, b):
        # a = RedisMatching.cvt_unit_vec(a)
        # b = RedisMatching.cvt_unit_vec(b)
        c = [i-j for i,j in zip(a, b)]
        c = [i*i for i in c]
        return 300 - math.sqrt(sum(c))

if __name__ == "__main__" :
    test_config = config.REDIS_MATCH_CONF
    test_config.update(config.TWILLO_CONFIG)
    print(test_config)
    r = RedisMatching(test_config)
    r.match_user()

    # a = [55,50,90,40]
    # b = [30,25,35,25]
    # c = [30,25,55,25]
    #
    # print()
    # print('=========== 성향 ===========')
    # print('=양식, 패스트푸드, 면, 한식=')
    # print('A :', a)
    # print('B :', b)
    # print('C :', c)
    # print()
    #
    # # print('=====Unit Vector=====')
    # # print( 'a unit vector :', RedisMatching.cvt_unit_vec(a) )
    # # print( 'b unit vector :', RedisMatching.cvt_unit_vec(b) )
    # # print( 'c unit vector :', RedisMatching.cvt_unit_vec(c) )
    # # print()
    #
    # print('===== Custom Similarity =====')
    # print( 'A <-> B :', RedisMatching.custom_similarity(a, b) )
    # print( 'B <-> C :', RedisMatching.custom_similarity(b, c) )
    # print( 'C <-> A :', RedisMatching.custom_similarity(c, a) )
    # print()
    #
    # print('===== Cosine Similarity =====')
    # print( 'A <-> B :', RedisMatching.cosine_similarity(a, b) )
    # print( 'B <-> C :', RedisMatching.cosine_similarity(b, c) )
    # print( 'C <-> A :', RedisMatching.cosine_similarity(c, a) )
    # print()

    # test_config = config.REDIS_MATCH_CONF
    # test_config.update(config.TWILLO_CONFIG)
    # print(test_config)
    # r = RedisMatching(test_config)
    #
    # print( r.set_userdata({'phone_numb':'01073632399', 'test':'한글은?', 'test2':456}) )
    # # data = r.get_userdata('01073632124')
    # print( r.get_all_user() )
    # print( type(r.get_all_user()) )
    # r.initialize()
    # print( r.get_all_user() )
    # print( type(r.get_all_user()) )

    # print( r.send_message(data['phone_numb'], '이렇게 문자 보낼 수 있어여') )
    # print( r.remove_userdata(data['phone_numb']) )
    # if user_name:
    #     print(user_name)

#coding:utf-8
import sys
sys.path.append('../../metadata')
import monday_sql_config as config
import pymysql

# 사용자 정보
class User(object):
    def __init__(self, config):
        self.conn = mysql.connect(host=config['host'],
                             user=config['user'],
                             passwd=config['passwd'],
                             db=config['db'],
                             charset='utf8')

    # /user/register
    def create(self, university, phone_numb, username, password, sex):
        try :
            cursor = self.conn.cursor()
            query = "INSERT INTO student values (%s, %s, %s, %s, %s)"
            value = (university, phone_numb, username, password, sex)
            cursor.execute(query, value)
            cursor.fetchall()
            self.conn.commit()
            cursor.close()
            return None
        except Exception as e :
            self.conn.rollback()
            return_dict = dict()
            return_dict["success"] = False
            return_dict["failure_short"] = "Unknown Failure " + str(e)
            return return_dict

    # /user/register/check_phone_number
    # /user/login/is_exist_phone_number
    def is_exist_phone_number(self, phone_numb):
        try :
            cursor = self.conn.cursor()
            query = "SELECT 1 FROM student WHERE phone_numb = %s"
            value = (phone_numb)
            cursor.execute(query, value)
            data = cursor.fetchall()
            cursor.close()
            if data : return True
            else : return False
        except Exception as e :
            self.conn.rollback()
            return_dict = dict()
            return_dict["success"] = False
            return_dict["failure_short"] = "Unknown Failure " + str(e)
            return return_dict

    # /user/login
    def login(self, phone_numb, password):
        try :
            cursor = self.conn.cursor()
            query = "SELECT 1 FROM student WHERE phone_numb = %s and password = %s"
            value = (phone_numb, password)
            cursor.execute(query, value)
            data = cursor.fetchall()
            cursor.close()
            if data : return True
            else : return False
        except Exception as e :
            self.conn.rollback()
            return_dict = dict()
            return_dict["success"] = False
            return_dict["failure_short"] = "Unknown Failure " + str(e)
            return return_dict

    # /user/delete
    def delete(self, phone_numb):
        try :
            cursor = self.conn.cursor()
            query = "DELETE FROM student WHERE phone_numb = %s"
            value = (phone_numb)
            cursor.execute(query, value)
            cursor.fetchall()
            self.conn.commit()
            cursor.close()
            return None
        except Exception as e :
            self.conn.rollback()
            return_dict = dict()
            return_dict["success"] = False
            return_dict["failure_short"] = "Unknown Failure " + str(e)
            return return_dict

    # def __del__(self):
    #     self.conn.close()


if __name__ == '__main__' :
    test = User(config.MYSQL_CONFIG)
    #test.create_user()
    # test.login()
    #test.delete_user()

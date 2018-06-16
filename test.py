import sys
import time
import os
import pymysql as mysql

sys.path.append('../metadata')
import monday_sql_config as config

import time

if __name__ == '__main__':
    # app.run(port=5000)
    # phone_numb = request.form['mobile']
    # print(phone_numb, file=sys.stderr)
    conn = mysql.connect(host=config.MYSQL_CONFIG['host'],
                         user=config.MYSQL_CONFIG['user'],
                         passwd=config.MYSQL_CONFIG['passwd'],
                         db=config.MYSQL_CONFIG['db'],
                         charset='utf8')
    cursor = conn.cursor()

    # query = "SELECT 1 FROM student WHERE 'phone_numb' = '%s'" %('1231231232')
    # cursor.execute(query)
    # data = cursor.fetchall()
    # conn.commit()
    # if data:
    #     print('phone number is already exist', file=sys.stderr)
    #     print(data, file=sys.stderr)
    # else:
    #     print('phone number is not exist', file=sys.stderr)
    #     print(data, file=sys.stderr)


    try :
        query = "INSERT INTO student values (%s, %s, %s, %s, %s)"
        value = ('seoil', '11111111111', 'number123313', 'dfdfdfdf', 'female')
        cursor.execute(query, value)
        data = cursor.fetchall()
        conn.commit()
    except Exception as e :
        return_dict = dict()
        return_dict["success"] = False
        return_dict["failure_short"] = "Unknown Failure " + str(e)
        print(return_dict)

    cursor.close()
    conn.close()

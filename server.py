from flask import Flask, render_template, request, Response, redirect
import sys
import time
import os
from flask_cors import CORS
import pymysql as mysql

sys.path.append('../metadata')
import monday_sql_config as config

import time

app = Flask(__name__)
CORS(app)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def index(name=None):
    # return render_template('registration.html', name=name)
    return render_template('index.html', name=name)

@app.route('/registration')
def registration(name=None):
    return render_template('registration.html', name=name)

@app.route('/matching')
def matching(name=None):
    return render_template('matching.html', name=name)

@app.route('/register', methods = ['POST'])
def register(name=None):
    print(request.form['university'], file=sys.stderr)
    print(request.form['mobile'], file=sys.stderr)
    print(request.form['username'], file=sys.stderr)
    print(request.form['password'], file=sys.stderr)
    print(request.form['sex'], file=sys.stderr)

    try :
        conn = mysql.connect(host=config.MYSQL_CONFIG['host'],
                             user=config.MYSQL_CONFIG['user'],
                             passwd=config.MYSQL_CONFIG['passwd'],
                             db=config.MYSQL_CONFIG['db'],
                             charset='utf8')
        cursor = conn.cursor()
        query = "INSERT INTO student values (%s, %s, %s, %s, %s)"
        value = (request.form['university'], request.form['mobile'],
                 request.form['username'], request.form['password'],
                 request.form['sex'])
        cursor.execute(query, value)
        data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')
    except Exception as e :
        conn.rollback()
        return_dict = dict()
        return_dict["success"] = False
        return_dict["failure_short"] = "Unknown Failure " + str(e)
        print(return_dict, file=sys.stderr)
        return redirect('/registration', error=return_dict)


@app.route('/register/check_phone_number', methods = ['POST'])
def check_phone_number(name=None):
    # TODO: check phone number
    phone_numb = request.form['mobile']
    print(phone_numb, file=sys.stderr)
    conn = mysql.connect(host=config.MYSQL_CONFIG['host'],
                         user=config.MYSQL_CONFIG['user'],
                         passwd=config.MYSQL_CONFIG['passwd'],
                         db=config.MYSQL_CONFIG['db'],
                         charset='utf8')
    cursor = conn.cursor()

    query = "SELECT 1 FROM student WHERE phone_numb = %s"
    value = (phone_numb)
    cursor.execute(query, value)
    data = cursor.fetchall()

    if data:
        print('phone numb already exist', file=sys.stderr)
        print(data, file=sys.stderr)
        result = 'false'
    else:
        print('phone numb does not exist', file=sys.stderr)
        print(data, file=sys.stderr)
        result = 'true'

    cursor.close()
    conn.close()

    return result

@app.route('/login', methods=['post'])
def login():
    phone_numb = request.form['mobile']
    pw = request.form['password']

    conn = mysql.connect(host=config.MYSQL_CONFIG['host'],
                         user=config.MYSQL_CONFIG['user'],
                         passwd=config.MYSQL_CONFIG['passwd'],
                         db=config.MYSQL_CONFIG['db'],
                         charset='utf8')
    cursor = conn.cursor()

    query = "SELECT 1 FROM student WHERE phone_numb = %s and password = %s"
    value = (phone_numb, pw)
    # cursor.execute("set names utf8")
    cursor.execute(query, value)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    # for row in data:
    #     data = row[0]

    if data:
        print ('login success', file=sys.stderr)
        return redirect('/matching')
    else:
        error = 'Invalid input data detected!'

    #return redirect(url_for('success', name=user))
    return render_template('/', error=error)

@app.route('/login/is_exist_phone_number', methods = ['POST'])
def is_exist_phone_number(name=None):
    # TODO: check phone number
    phone_numb = request.form['mobile']
    print(phone_numb, file=sys.stderr)
    conn = mysql.connect(host=config.MYSQL_CONFIG['host'],
                         user=config.MYSQL_CONFIG['user'],
                         passwd=config.MYSQL_CONFIG['passwd'],
                         db=config.MYSQL_CONFIG['db'],
                         charset='utf8')
    cursor = conn.cursor()

    query = "SELECT 1 FROM student WHERE phone_numb = %s"
    value = (phone_numb)
    cursor.execute(query, value)
    data = cursor.fetchall()

    if data:
        print('phone numb already exist', file=sys.stderr)
        print(data, file=sys.stderr)
        result = 'true'
    else:
        print('phone numb does not exist', file=sys.stderr)
        print(data, file=sys.stderr)
        result = 'false'

    cursor.close()
    conn.close()

    return result


if __name__ == '__main__':
    # app.run(port=5000)
    app.run(debug=True, host='0.0.0.0', port=8000)

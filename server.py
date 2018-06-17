from flask import Flask, render_template, request, redirect, session, flash
import sys
import time
import os
from flask_cors import CORS
# import pymysql as mysql
sys.path.append('../metadata')
import monday_sql_config as config

from module.redis_session import RedisSession
from module.user import User

import time

app = Flask(__name__)
app.secret_key = config.APP_CONFIG['secret_key']
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
def index():
    user_name = check_session()
    if user_name is None:
        return render_template('index.html')

    return redirect('/matching')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/matching')
def matching():
    user_name = check_session()
    if user_name is None:
        return redirect('/')

    return render_template('matching.html')

@app.route('/preference')
def preference():
    user_name = check_session()
    if user_name is None:
        return redirect('/')

    return render_template('preference.html')

@app.route('/user/register', methods = ['POST'])
def register():
    print(request.form['university'], file=sys.stderr)
    print(request.form['mobile'], file=sys.stderr)
    print(request.form['username'], file=sys.stderr)
    print(request.form['password'], file=sys.stderr)
    print(request.form['sex'], file=sys.stderr)

    result = User(config.MYSQL_CONFIG).create(request.form['university'],
                                              request.form['mobile'],
                                              request.form['username'],
                                              request.form['password'],
                                              request.form['sex']
                                              )

    if result == None:
        session_key = RedisSession(config.REDIS_SESS_CONF).save_session(request.form['mobile'])
        session['session_key'] = session_key
        flash('회원가입 완료')
        return redirect('/')
    else:
        print(result, file=sys.stderr)
        flash('알 수 없는 에러')
        return redirect('/registration', error=result)

@app.route('/user/register/check_phone_number', methods = ['POST'])
def check_phone_number():
    print('/user/reg/chk phone numb :', request.form['mobile'], file=sys.stderr)
    result = User(config.MYSQL_CONFIG).is_exist_phone_number(request.form['mobile'])

    if result == True : return 'false'
    elif result == False : return 'true'
    else : return result

@app.route('/user/login', methods=['POST'])
def login():
    print('/user/login :', request.form['mobile'], request.form['password'], file=sys.stderr)
    result = User(config.MYSQL_CONFIG).login(request.form['mobile'], request.form['password'])

    if result == True:
        session_key = RedisSession(config.REDIS_SESS_CONF).save_session(request.form['mobile'])
        session['session_key'] = session_key
        return redirect('/matching')
    elif result == False:
        flash('비밀번호를 잘못 입력하셨습니다.')
        return redirect('/') # not exist password
    else:
        return result

@app.route('/user/login/is_exist_phone_number', methods = ['POST'])
def is_exist_phone_number():
    print(request.form['mobile'], file=sys.stderr)
    result = User(config.MYSQL_CONFIG).is_exist_phone_number(request.form['mobile'])

    if result == True : return 'true'
    elif result == False : return 'false'
    else : return result

@app.route('/user/logout', methods=['GET', 'POST'])
def logout():
    if 'session_key' in session:
        del session['session_key']
        flash('로그아웃 완료')
    return redirect('/')

@app.route('/user/delete', methods=['GET', 'POST'])
def delete():
    result = User(config.MYSQL_CONFIG).delete(request.form['mobile'])

    if result == None:
        if 'session_key' in session:
            del session['session_key']
        flash('회원탈퇴 성공')
        return redirect('/')
    else:
        return redirect('/matching', error=result)

@app.route('/user/matching_apply', methods=['POST'])
def matching_apply():
    print(request.form['cutlet'], file=sys.stderr)
    print(request.form['hamburger'], file=sys.stderr)
    print(request.form['noodle'], file=sys.stderr)
    print(request.form['korean_food'], file=sys.stderr)

    user_name = check_session()
    if user_name == None:
        flash('너무 오래 고민하셨네요. 다시 로그인해 주세요.')
        return redirect('/')

    user_data = User(config.MYSQL_CONFIG).get_userdata(user_name)
    if user_data == None :
        flash('원인 불명의 에러입니다.')
        return redirect('/')

    user_data['cutlet'] = request.form['cutlet']
    user_data['hamburger'] = request.form['hamburger']
    user_data['noodle'] = request.form['noodle']
    user_data['korean_food'] = request.form['korean_food']

    matching_config = config.REDIS_MATCH_CONF
    matching_config.update(config.TWILLO_CONFIG)
    RedisMatching(matching_config).set_userdata(user_data)

    flash('신청 완료. 매칭 결과는 문자로 알려드릴 예정입니다.')
    redirect('/matching')


def check_session():
    if 'session_key' not in session:
        return None
    session_key = session['session_key']
    user_name = RedisSession(config.REDIS_SESS_CONF).open_session(session_key)

    if user_name is None :
        del session['session_key']

    return user_name

if __name__ == '__main__':
    # app.run(port=5000)
    app.run(debug=True, host='0.0.0.0', port=8000)

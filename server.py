from flask import Flask, render_template, request, Response, redirect
import sys
import time
import os
from flask_cors import CORS
# import pymysql as mysql
sys.path.append('../metadata')
import monday_sql_config as config

# from module.redis_session import redis_session
from module.user import User

import time

app = Flask(__name__)
# app.secret_key = 'fjkzm2123kd@32z123fdfzdf'
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
    # return render_template('registration.html', name=name)
    return render_template('index.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/matching')
def matching():
    return render_template('matching.html')

@app.route('/user/register', methods = ['POST'])
def register():
    print(request.form['university'], file=sys.stderr)
    print(request.form['mobile'], file=sys.stderr)
    print(request.form['username'], file=sys.stderr)
    print(request.form['password'], file=sys.stderr)
    print(request.form['sex'], file=sys.stderr)

    result = User(config.MYSQL_CONFIG).create( request.form['university'],
                            request.form['mobile'],
                            request.form['username'],
                            request.form['password'],
                            request.form['sex']
                            )

    if result == None:
        return redirect('/')
    else:
        print(result, file=sys.stderr)
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

    if result == True : return redirect('/matching')
    elif result == False : return render_template('/', error='not exist password') # not exist password
    else : return result

@app.route('/user/login/is_exist_phone_number', methods = ['POST'])
def is_exist_phone_number():
    print(request.form['mobile'], file=sys.stderr)
    result = is_exist_phone_number(request.form['mobile'])

    if result == True : return 'true'
    elif result == False : return 'false'
    else : return result

@app.route('/user/logout', methods=['POST'])
def logout():
    if 'session_key' in session:
        del session['session_key']
    return redirect('/')

@app.route('/user/delete', methods=['POST'])
def delete():
    result = User(config.MYSQL_CONFIG).delete(request.form['mobile'])

    if result == None:
        if 'session_key' in session:
            del session['session_key']
        return redirect('/')
    else:
        return redirect('/matching', error=result)

if __name__ == '__main__':
    # app.run(port=5000)
    app.run(debug=True, host='0.0.0.0', port=8000)

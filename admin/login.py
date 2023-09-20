from flask import request, render_template, g, redirect, url_for
from flask import make_response

def Login():
    if request.method == 'GET':  # 登录页面
        return render_template('login.html')
    # 传递登录数据
    if request.method == 'POST':
        if not g.db.open:
            g.db.ping(reconnect=True)
        DBCONN = g.db.cursor()
        username = request.form['username']
        password = request.form['password']
        CheckSql = "SELECT * FROM user WHERE username = %s and password = %s"
        DBCONN.execute(CheckSql,(username,password))
        results = DBCONN.fetchall()
        if len(results) != 0 :
            #存入cookie
            resp = make_response(redirect('/admin'))
            resp.set_cookie('username', username)
            resp.set_cookie('password', password)
            return resp
        else:
            return "登录失败,用户或密码错误"


def OutLogin():
    resp = make_response(redirect('/admin'))
    resp.delete_cookie('username')
    resp.delete_cookie('password')
    return resp

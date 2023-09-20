from flask import render_template, request,redirect,make_response,g

def AdminIndex():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    if not g.db.open:
        g.db.ping(reconnect=True)
    CheckSql = "SELECT * FROM user WHERE username = %s and password = %s"
    DBCONN = g.db.cursor()
    DBCONN.execute(CheckSql, (username, password))
    results = DBCONN.fetchall()
    if len(results) == 0 and username != None and password != None:
        resp = make_response(redirect('/admin'))
        resp.delete_cookie('username')
        resp.delete_cookie('password')
        print(len(results))
        return resp
    resp = make_response(render_template('index.html', username=username))
    resp.delete_cookie('banners_id')
    resp.delete_cookie('mod')
    resp.delete_cookie('title_id')
    resp.delete_cookie('title_mod')
    print(username)
    return resp
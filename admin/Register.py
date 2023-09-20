from flask import Flask, render_template, request, g, make_response, redirect


def Register():
    IndexID = 1
    if not g.db.open:
        g.db.ping(reconnect=True)
    DBCONN = g.db.cursor()
    if request.method == 'GET':  # 注册页面
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        CheckSql = "SELECT * FROM user where username = %s"
        DBCONN.execute(CheckSql,(username))
        results = DBCONN.fetchall() #得到结果
        if len(results) != 0 :
            return "已经存在用户，请返回重新登录"
    if username != None and password != None:
        IndexIDsql = "SELECT ID FROM user order by ID desc limit 1"
        DBCONN.execute(IndexIDsql)
        IndexIDdemo = DBCONN.fetchall()
        if len(IndexIDdemo) != 0:
            print(IndexIDdemo)
            IndexID = IndexIDdemo[0][0] + 1
        RegisterSql ="INSERT INTO user(ID, username, password) VALUES (%s, %s, %s)"
        try:
            # 执行sql语句
            DBCONN.execute(RegisterSql,(IndexID, username, password))
            # 提交事务，否则数据库中不会出现数据
            g.db.commit()
        except:
            # 发生错误时回滚
            g.db.rollback()
            # 存入cookie
        resp = make_response(redirect('/admin'))
        resp.set_cookie('username', username)
        resp.set_cookie('password', password)
        return resp
    else: return "注册失败"

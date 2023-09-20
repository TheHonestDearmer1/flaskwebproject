from flask import render_template, request, g, redirect, make_response
from werkzeug.utils import secure_filename

URL_POST="http://localhost:5000/"

def Custom():
    if request.method == "GET":
        if not g.db.open:
            g.db.ping(reconnect=True)
        title_id = request.cookies.get('title_id')
        title_mod = request.cookies.get('title_mod')
        defaultCustomList = []
        SREACHSQL = "SELECT * FROM custom_table"
        DBCONN = g.db.cursor()
        DBCONN.execute(SREACHSQL)
        results = DBCONN.fetchall()
        for i in results:
            defaultCustomList.append({
                'ID': i[0],
                'title': i[1],
                'description': i[2],
                'src': i[3]
            })
        return render_template('custom.html',defaultCustomList = defaultCustomList,title_id = title_id,mod = title_mod)
    if request.method == "POST":
        if not g.db.open :
            g.db.ping(reconnect=True)
        IndexID = 1
        TitleIDSQL = "SELECT ID FROM custom_table ORDER BY ID DESC Limit 1"
        DBCONN = g.db.cursor()
        DBCONN.execute(TitleIDSQL)
        results = DBCONN.fetchall()  # 得到结果
        if len(results) != 0:
            IndexID = results[0][0] + 1
        title = request.form['title']
        description = request.form['description']
        file = request.files['file']
        FileName = "{}_{}".format(IndexID, secure_filename(file.filename))
        file.save(f"static/{FileName}")
        SRC = URL_POST + "static/" + FileName
        INSERTTABLE="INSERT INTO custom_table(ID,title,description,src) values (%s,%s,%s,%s)"
        DBCONN.execute(INSERTTABLE,(IndexID,title,description,SRC))
        g.db.commit()
        return redirect('/admin/custom')

def Open_Change_Custom(title_id,title_mod):
    resp = make_response(redirect('/admin/custom'))
    resp.set_cookie('title_id',title_id)
    resp.set_cookie('title_mod',title_mod)
    return resp

#修改操作
def Change_Custom() :
    if request.method == "POST":
        DBCONN = g.db.cursor()
        title_id = request.cookies.get('title_id')
        title = request.form['title']
        description = request.form['description']
        file = request.files['file']
        FileName = "{}_{}".format(title_id, secure_filename(file.filename))
        file.save(f"static/{FileName}")
        SRC = URL_POST + "static/" + FileName
        INSERTTABLE = "UPDATE custom_table SET title = %s, description = %s, src = %s WHERE id = %s;"
        # 更新数据
        DBCONN.execute(INSERTTABLE, (title, description, SRC, title_id))
        g.db.commit()
        # 删除cookie
        resp = make_response(redirect('/admin/custom'))
        resp.delete_cookie('title_id')
        resp.delete_cookie('title_mod')
        return resp
    if request.method == "GET" :
        # 删除cookie
        resp = make_response(redirect('/admin/custom'))
        resp.delete_cookie('title_id')
        resp.delete_cookie('title_mod')
        return resp


def Delete_Custom(id):
    if not g.db.open:
        g.db.ping(reconnect=True)
    SREACHTIDSQL = "DELETE FROM custom_table WHERE ID = %s"
    DBCONN = g.db.cursor()
    DBCONN.execute(SREACHTIDSQL, id)
    g.db.commit()
    return redirect('/admin/custom', 200)
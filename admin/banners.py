from flask import  request,g,render_template,redirect,make_response

DataList = [] #将清单定义为全局变量方便返回
#总返回值
def TotalBanners():
    username = request.cookies.get('username')
    if username == None:
        return redirect('/admin/login')
    mod = request.cookies.get('mod')
    title_id = request.cookies.get('banners_id')
    return render_template('banners.html', banners=DefaultDanners(), mod=mod, title_id=title_id)


def Banners():
   username = request.cookies.get('username')
   if username == None:
      return redirect('admin/login')
   if request.method == 'GET':
            return redirect('/admin/banners')
   #打开数据库
   if not g.db.open:
      g.db.ping(reconnect=True)
   title = request.form['title']
   description = request.form['description']
   href = request.form['href']
   indexId =1
   DBCONN = g.db.cursor()
   CheckIndexIDSql = "SELECT ID FROM banner_table order by ID desc limit 1;"
   DBCONN.execute(CheckIndexIDSql)
   results = DBCONN.fetchall()
   if len(results) != 0:
      indexId = results[0][0] + 1
   data = {
      'ID':indexId,
      'title':title,
      'description' :description,
     'href':href
   }
   INSERTSQL = "INSERT INTO banner_table(ID,title,description,href) values(%s,%s,%s,%s)"
   DBCONN.execute(INSERTSQL,(data['ID'],data['title'],data['description'],data['href']))
   g.db.commit()
   SREACHTSQL = "SELECT * FROM banner_table"
   DBCONN.execute(SREACHTSQL)
   results = DBCONN.fetchall()
   DataList.clear()
   for i in results:
      DataList.append({
       'ID':i[0],
       'title':i[1],
       'description' :i[2],
       'href':i[3]
   })

   return redirect('/admin/banners',200)

#删除
def Delete_Banners(id):
   if not g.db.open:
      g.db.ping(reconnect=True)
   print(id)
   SREACHTIDSQL = "DELETE FROM banner_table WHERE ID = %s"
   DBCONN = g.db.cursor()
   DBCONN.execute(SREACHTIDSQL,id)
   g.db.commit()
   DataList.clear()
   return redirect('/admin/banners',200)

#修改
def Change_Banners(id,mod):
   resp = make_response(redirect('/admin/banners'))
   resp.set_cookie('mod', mod)
   resp.set_cookie('banners_id', id)
   return resp

#激发小窗口修改的时候用的
def Change_Action_Banners():
    title = request.form['title']
    description = request.form['description']
    href = request.form['href']
    if not g.db.open:
       g.db.ping(reconnect=True)
    banners_id = request.cookies.get('banners_id')
    print(banners_id)
    SREACHTSQL = "UPDATE banner_table SET title = %s ,description = %s ,href = %s WHERE ID = %s;"
    DBCONN = g.db.cursor()
    DBCONN.execute(SREACHTSQL,(title,description,href,banners_id))
    g.db.commit()
    resp = make_response(redirect('/admin/banners'))
    resp.delete_cookie('banners_id')
    resp.delete_cookie('mod')
    return  resp

#从数据库读取
def DefaultDanners():
   if not g.db.open:
      g.db.ping(reconnect=True)
   defaultDataList = []
   SREACHSQL = "SELECT * FROM banner_table"
   DBCONN = g.db.cursor()
   DBCONN.execute(SREACHSQL)
   results = DBCONN.fetchall()
   for i in results:
      defaultDataList.append({
          'ID': i[0],
         'title': i[1],
         'description': i[2],
         'href': i[3]
         })
   return defaultDataList




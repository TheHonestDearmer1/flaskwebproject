# 安装

项目依赖安装：

```cmd
pip install Flask
pip install pymysql
pip install cryptography
```

启动项目：

```cmd
flask --app index  run -p 端口号
```

# **项目结构**

项目启动文件包含在index.py中，具体内容实现放在admin文件夹中，router.py中写了路由组，具体函数实现在admin的相对应py文件中实现，建表操作在Table.py中实现，开启服务端的时候会进行删表操作

**文件存储**：static存储上传的图片和前台文件

# 功能

目前项目功能只在admin后台中生效：

## **登录和注册**

注册之后用户信息会保存在cookie中，退出登录清除cookie

**缺点**：目前还没有使用加密组件对cookie和token进行加密

## **banner管理**

正常的修改和删除功能正常运行

## 用户评论管理

正常的图片上传和修改，删除功能已经实现。

缺点：更改后和删除的元组中的图片文件还没有写删除功能，删除之后图片文件仍然存在

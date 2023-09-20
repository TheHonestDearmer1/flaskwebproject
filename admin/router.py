from flask import render_template, Blueprint, request, redirect, make_response, g, send_from_directory, url_for
from admin.Register import Register
from admin.login import Login,OutLogin
from admin.admin import AdminIndex
from admin.banners import Banners,Delete_Banners,Change_Banners,Change_Action_Banners,TotalBanners
from admin.custom import Custom,Open_Change_Custom,Change_Custom,Delete_Custom
def InitRouter(app):
    #前台页面
    @app.route('/interface/<filename>')
    def OtherFile(filename):
        return render_template(f"public/{filename}")

    @app.route('/')
    def IndexFile():
        return render_template('public/index.html')


    #后台页面
    admin_bp = Blueprint('admin', __name__)
    @admin_bp.route('/')
    def admin_home():
        return AdminIndex()

    #登录
    @admin_bp.route('/login',methods=['POST', 'GET'])
    def login():
        return Login()

    #注册
    @admin_bp.route('/register',methods=['POST', 'GET'])
    def register():
        return Register( )

    #登出
    @admin_bp.route('/outlogin')
    def outlogin():
        return OutLogin()
    #banners
    @admin_bp.route('/banners',methods=['POST', 'GET'])
    def banners():
        return TotalBanners()
    #banners增添操作
    @admin_bp.route('/banners/action', methods=['POST', 'GET'])
    def banners_action():
        return Banners()

    #banners删除操作
    @admin_bp.route('/banners/action/delete/<id>', methods=['POST', 'GET'])
    def banners_delete(id):
        return Delete_Banners(id)
    #banners修改界面弹出操作
    @admin_bp.route('/banners/action/change/<id>/<mod>', methods=['POST', 'GET'])
    def banners_change(id,mod):
        return Change_Banners(id,mod)

    # banners修改完成操作
    @admin_bp.route('/banners/action/change', methods=['POST', 'GET'])
    def banners_action_change():
        return Change_Action_Banners()
    #custom
    @admin_bp.route('/custom',methods=['POST', 'GET'])
    def custom():
        return Custom()

    #custom修改弹出操作
    @admin_bp.route('/custom/action/<title_id>/<title_mod>', methods=['POST', 'GET'])
    def open_change_custom(title_id,title_mod):
        return Open_Change_Custom(title_id,title_mod)

    #custom修改操作
    @admin_bp.route('/custom/action/change', methods=['POST', 'GET'])
    def change_custom():
        return Change_Custom()

    # custom删除操作
    @admin_bp.route('/custom/action/delete/<id>', methods=['POST', 'GET'])
    def delete_custom(id):
        return Delete_Custom(id)

    app.register_blueprint(admin_bp, url_prefix='/admin')


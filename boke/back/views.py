
from flask import Blueprint, request, render_template, \
    redirect, url_for, session

# 避免循环引入，删掉没用的导包
# from manage import back

# 第一步: 生成蓝图对象
# 蓝图用于管理路由
from werkzeug.security import check_password_hash, generate_password_hash

from back.models import db, User, ArticleType, Article
from utils.functions import is_login

back_blueprint = Blueprint('back', __name__)



# 第二步: 使用蓝图对象管理路由

@back_blueprint.route('/create_db/', methods=['GET'])
def create_db():
    # 生成数据库中的表
    # 将模型映射成数据库中的表（对第一次使用有用）
    db.create_all()
    return '创建表成功'
@back_blueprint.route('/index/',methods=['GET','POST'])
@is_login
def index():
    user = User.query.filter(User.id == session['user_id'] ).first()
    user1=User.query.all()
    user_count=len(user1)
    return render_template('back/index.html' ,user=user,user_count=user_count)


@back_blueprint.route('/register/',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('back/register.html')
    if request.method=='POST':
        username=request.form.get('username')
        password = request.form.get('password')
        password2= request.form.get('password2')

        if username and password and password2:
            user=User.query.filter(User.username==username).first()
            if user:
                error='该账号已注册，请更换账号'
                return render_template('back/register.html')
            else:
                if password2==password:
                    user=User()
                    user.username=username
                    user.password=generate_password_hash(password)
                    user.save()
                    return redirect(url_for('back.login'))
                else:
                    error='两尺密码不一致'
                    return render_template('back/register.html', error=error)
        else:
            error='请填写完整信息'
            return render_template('back/register.html',error=error)
@back_blueprint.route('/logout/',methods=['GET','POST'])
def logout():
    del session['user_id']

    return redirect(url_for('back.login'))

@back_blueprint.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('back/login.html')
    if request.method=='POST':
        username=request.form.get('username')
        password = request.form.get('password')

        if username and password:
            user=User.query.filter(User.username==username).first()
            if not user:

                error='该账号不存在，请去注册'
                return render_template('back/login.html')
            if not check_password_hash(user.password,password):
                error='密码错误，情修改密码'
                return render_template('back/login.html',error=error)
            session['user_id']=user.id
            return redirect(url_for('back.index'))
        else:
            error='请填写完整的登录信息'
            return render_template('back/login.html', error=error)

@back_blueprint.route('/a_type/',methods=['GET','POST'])
def a_type():
    if request.method=='GET':
        types=ArticleType.query.all()
        count_types = len(types)
        user = User.query.filter(User.id == session['user_id']).first()
        return render_template('back/category_list.html', types=types,user=user,count_types=count_types)
@back_blueprint.route('/add_type/',methods=['GET','POST'])
def add_type():
    if request.method=='GET':
        user = User.query.filter(User.id == session['user_id']).first()
        return render_template('back/category_add.html',user=user)
    if request.method=='POST':
        atype=request.form.get('atype')
        if atype:
            art_type=ArticleType()
            art_type.t_name=atype
            db.session.add(art_type)
            db.session.commit()
            return redirect(url_for('back.a_type'))
            # return render_template('back/category_list.html',user=user)
        else:
            error='请填写分类信息'
            return render_template('back/category_add.html', error=error)


@back_blueprint.route('/del_type/<int:id>/',methods=['GET','POST'])
def del_type(id):

    atype=ArticleType.query.get(id)
    db.session.delete(atype)
    db.session.commit()
    return redirect(url_for('back.a_type'))


@back_blueprint.route('/article_list/',methods=['GET'])
def article_list():
    user = User.query.filter(User.id == session['user_id']).first()
    articles=Article.query.all()
    aritcle_count=len(articles)
    return render_template('back/article_list.html',articles=articles,user=user,aritcle_count=aritcle_count)
@back_blueprint.route('/article_add/',methods=['GET','POST'])
def article_add():
    if request.method=='GET':
        user = User.query.filter(User.id == session['user_id']).first()
        types=ArticleType.query.all()
        return render_template('back/article_detail.html', types=types,user=user)
    if request.method=='POST':

        title=request.form.get('title')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('content')
        if title and desc and category and content:
            art=Article()
            art.title=title
            art.desc=desc
            art.content=content
            art.type=category
            db.session.add(art)
            db.session.commit()
            return redirect(url_for('back.article_list'))
        else:
            error='请填写完整的文章信息'
            return render_template('back/article_detail.html', error=error)
@back_blueprint.route('/del_article/<int:id>/',methods=['GET','POST'])
def del_article(id):
    atype=Article.query.get(id)
    db.session.delete(atype)
    db.session.commit()
    return redirect(url_for('back.article_list'))





































































































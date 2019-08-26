from operator import and_

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:123456@localhost/flask_ems"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from models import User
from models import Info
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/regist/')
def regist():
    return render_template("regist.html")

@app.route('/registlogic/',methods=['get','post'])
def registlogic():
    try:
        username = request.form.get("username")
        if username == "":
            username =None
        name = request.form.get("name")
        if name == "":
            name = None
        password = request.form.get("pwd")
        if password == "":
            password = None
        gender = int(request.form.get("sex"))
        user = User(username=username,name=name,password=password,gender=gender)
        db.session.add(user)
        db.session.commit()
        url = url_for("login")
        return redirect(url)
    except:
        return '注册失败'

@app.route('/login/')
def login():
    return render_template("login.html")

@app.route('/loginlogic/',methods=['get','post'])
def loginlogic():
    usernme = request.form.get("name")
    pssword = request.form.get("pwd")
    user = User.query.filter(and_(User.username == usernme,User.password == pssword)).all()
    if user:
        url = url_for("emplist")
        return redirect(url)
    return '登录失败'

@app.route('/emplist/')
def emplist():
    number = int(request.args.get("number",1))
    tag = request.args.get("tag")
    page = db.session.query(Info).paginate(page=number,per_page=2)
    if tag == "add":
        number = page.pages
        page = db.session.query(Info).paginate(page=number, per_page=2)
    return render_template('emplist.html',page=page,number=number)

@app.route('/addemp/')
def addemp():
    return render_template('addEmp.html')

@app.route('/addemplogic/',methods=['get','post'])
def addemplogic():
    try:
        name = request.form.get("name")
        if name == "":
            name = None
        salary = request.form.get("salary")
        age = request.form.get("age")
        info = Info(name=name,salary=salary,age=age)
        db.session.add(info)
        db.session.commit()
        url = url_for("emplist",tag="add")
        return redirect(url)
    except:
        return '信息添加失败'

@app.route('/updateemp/')
def updateemp():
    number = request.args.get("number")
    id = request.args.get("id")
    info = Info.query.filter(Info.id == id).one()
    return render_template("updateEmp.html",info=info,number=number,id=id)

@app.route('/updateemplogic/',methods=['get','post'])
def updateemplogic():
    number = request.args.get("number")
    id = request.args.get("id")
    name = request.form.get("name")
    salary = request.form.get("salary")
    age = request.form.get("age")
    info = Info.query.filter(Info.id == id).one()
    info.name = name
    info.salary = salary
    info.age = age
    db.session.commit()
    url = url_for("emplist",number=number)
    return redirect(url)

@app.route('/deleteemp/')
def deleteemp():
    number = request.args.get("number")
    id = int(request.args.get("id"))
    info = Info.query.filter(Info.id == id).one()
    db.session.delete(info)
    db.session.commit()
    url = url_for("emplist",number=number)
    return redirect(url)

if __name__ == '__main__':
    app.run()

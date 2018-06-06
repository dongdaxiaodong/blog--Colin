from flask import Flask,render_template,url_for,redirect,request,json,jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1346536639@127.0.0.1/myweb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'aodong'
app.debug=True
db=SQLAlchemy(app)

class Type(db.Model):
    __tablename__='types'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    page=db.relationship('Page', backref='type', lazy=True)
class Page(db.Model):
    __tablename__='pages'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(30),nullable=False)
    content=db.Column(db.Text,nullable=False)
    time=db.Column(db.String(30),nullable=False)
    type_id=db.Column(db.Integer,db.ForeignKey('types.id'),nullable=False)

@app.route('/')
def start():
    return render_template('startit.html')

@app.route('/deletetype',methods=['POST'])
def deletetype():
    if request.method=="POST":
        type=json.loads(request.form.get('deletetype'))
        id=Type.query.filter_by(name=type).first().id
        pages=Page.query.all()
        deletelist=[]
        for i in range(len(pages)):
            if pages[i].type_id==id:
                db.session.delete(pages[i])
                db.session.commit()
        thetype=Type.query.filter_by(name=type).first()
        db.session.delete(thetype)
        db.session.commit()
        print('删除成功')
        return ''


@app.route('/writing/')
def writing():
    return render_template('writing.html')

@app.route('/changepage',methods=['POST'])
def changepage():
    if request.method=='POST':
        title=json.loads(request.form.get('titledata'))
        content=json.loads(request.form.get('contentdata'))
        page=Page.query.filter_by(title=title).first()
        page.content=content
        db.session.commit()
        return ''

@app.route('/returnpage',methods=['POST'])
def returnpage():
    if request.method=="POST":
        title=json.loads(request.form.get('titledata'))
        target=Page.query.filter_by(title=title).first()
        content=target.content
        type_id=target.type_id
        type_name=Type.query.filter_by(id=type_id).first().name
        contentlist=[title,content,type_name]
        return jsonify(contentlist)

@app.route('/returnpages',methods=['POST'])
def returnpages():
    if request.method=="POST":
        title=json.loads(request.form.get('titledata'))
        typeid=Type.query.filter_by(name=title).first()
        id=typeid.id
        pageslist=Page.query.all()
        titlelist=[]
        for i in range(len(pageslist)):
            if pageslist[i].type_id==id:
                titlelist.append([pageslist[i].title,pageslist[i].content,pageslist[i].time])
        return jsonify(titlelist)


@app.route('/addtypes',methods=['POST'])
def addtypes():
    if request.method=="POST":
        adddata=request.form.get("adddata")
        mynewtype=json.loads(adddata)
        newtype=Type(name=mynewtype)
        db.session.add(newtype)
        db.session.commit()
        print("type add ok")
    return ''

@app.route('/gettypes/')
def gettypes():
    alldata=Type.query.all()
    datalist=[]
    for data in alldata:
        datalist.append(data.name)
    return jsonify(datalist)

@app.route('/deletepage',methods=['POST'])
def deletepage():
    if request.method == 'POST':
        title=json.loads(request.form.get('deletetitle'))
        page=Page.query.filter_by(title=title).first()
        db.session.delete(page)
        db.session.commit()
        print("删除成功")
    return ''



@app.route('/upload',methods=['POST'])
def upload():
    if request.method=="POST":
        contentdata=request.form.get("contentdata")
        mydata=json.loads(contentdata)
        title=mydata['title']
        content=mydata['content']
        value=mydata['radiovalue']
        checkedtype=Type.query.filter_by(name=value).first()
        typeid=checkedtype.id
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time = nowTime[:10]
        newpage=Page(title=title,content=content,type_id=typeid,time=time)
        db.session.add(newpage)
        db.session.commit()
        print(title,"以及成功被添加到",value)

    return ""

if __name__ == '__main__':
    db.create_all()
    app.run()
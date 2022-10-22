import json
import os
import re
import traceback
from datetime import timedelta

import pymysql
from flask import Flask, jsonify, request, redirect, render_template, session, flash
from sqlalchemy import false
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from util.forms import LoginForm
from util.utils import mysql_conn, mysql_close, validate
from flask_sqlalchemy import SQLAlchemy
'''render_template 渲染模板'''
import config
import util
import time
import static
# from alipay import AliPay

# 使用flask创建一个app对象，传递__name__属性
app = Flask(__name__)
# 加载flask的配置文件
app.config.from_object(config)
# app.register_blueprint(nur)
global department
department = []
global doctor
global manager
global nurse
global patient
global lists
global mlist_id
global clist_id
global bd_id
global mdl1
# class User(db.Model):
#     __tablename__="user"
#     username=db.Column(db.String(200),primary_key=True)
#     password=db.Column(db.String(200),nullable=False)
#
# db.create_all()
# 设置访问的url 根路径

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

@app.route('/')
def LoRe():
        global department
        conn, cursor = mysql_conn()
        try:
            sql = "select name from department;"
            cursor.execute(sql)
            result = cursor.fetchall()
            for i in range(len(result)):
                a=result[i]
                department.append(a[0])
            conn.commit()
        except:
            traceback.print_exc()
            conn.rollback()
        mysql_close(conn, cursor)
        return render_template('users/LoRe.html')
    # sql = "select * from user where username=" + request.args.get("username") + " and password=" +request.args.get("password")+""
    # engine=db.get_engine()
    # cursor=engine.connect()
    #
    # try:
    #     cursor.execute(sql)
    #     results = cursor.fetchall()
    #     if len(results) == 1:
    #         return render_template("Doctor.html", msg='登陆成功')
    #     else:
    #         return render_template('LoRe.html', msg='用户名或密码有误')
    #     conn.commit()
    # except:
    #     traceback.print_exc()
    #     conn.rollback()
    # conn.close()
    # return render_template('LoRe.html')

    # username=request.form["username"]
    # password=request.form["password"]
    # loginCheck(username,password)
    # return render_template('LoRe.html')


    # engine=db.get_engine()
    # with engine.connect() as conn:
    #     result=conn.execute('select 1')
    #     print(result.fetchone())
    # return("Hello World!")
# @app.route('/useradd', methods=['GET'])
# def userAdd():
#     ret_msg={"status":"401","msg":"登录失败，异常问题"}
#     conn,cursor=mysql_conn()
#     # request.get_json(force=True)
#     data=request.json
#     id=data[0]["id"]
#     password=data[0]["password"]
#     # id=request.args.get("username1")
#     # password=request.args.get("password1")
#     if id=="" :
#         ret_msg["msg"] = "信息不完整"
#         ret_msg["status"] = "403"
#     else:
#         try:
#             sql = "insert into doctor values(%d,'%s');" % (int(id), password)
#             cursor.execute(sql)
#             ret_msg = {"status": "400", "msg": "注册成功"}
#         except:
#             traceback.print_exc()
#             conn.rollback()
#     mysql_close(conn,cursor)
#     return json.dumps(ret_msg)

@app.route('/useradd',methods=['GET','POST'])
def userAdd():

    # req=request.get_json()
    # role=int(req['role'])
    # username=int(req['id'])
    # password=req['password']
        conn,cursor=mysql_conn()
        role=request.args.get("downlist1")
        username=request.args.get("username1")
        password=request.args.get("password1")
        # message=validate(role,username,password)
        # flash(message)
        # return render_template('users/LoRe.html')
        try:
            if role== '3':
                # file=request.files.get('file')
                # img=fin.read()
                # fin.close()
                # if request.method=='GET':
                #     f = request.files['file']
                #     if not (f and allowed_file(f.filename)):
                #         return jsonify({"error": 1001, "msg": "图片类型：png、PNG、jpg、JPG、bmp"})
                # # 当前文件所在路径
                #     basepath = os.path.dirname(__file__)
                # # 一定要先创建该文件夹，不然会提示没有该路径
                #     upload_path = os.path.join(basepath, 'static/img', secure_filename(f.filename))
                # # 保存文件
                #     f.save(upload_path)
                #     fin=open(upload_path,'rb')
                #     img=fin.read()
                #     fin.close()
                # 返回上传成功界面
                    baseimg=request.args.get("baseimg",type=str,default=None)
                    sql1="insert into manager values('%s','%s','%s');"%(username,password,baseimg)
                    cursor.execute(sql1)
                    conn.commit()

            elif role == '1':
                sql2 = "insert into doctor(id,password) values('%s','%s');" % (username, password)
                cursor.execute(sql2)
                conn.commit()

            elif role == '2':
                sql3 = "insert into nurse values('%s','%s');" % (username, password)
                cursor.execute(sql3)
                conn.commit()

        except:
            traceback.print_exc()
            conn.rollback()

        return render_template('users/LoRe.html')

global character

@app.route('/login',methods=['GET','POST'])
def login():
    conn,cursor=mysql_conn()
    global character
    character=request.args.get('downlist')
    d_id=request.args.get('doctor_id')
    password=request.args.get('password')
    # 医生登录
    if character=='1':
        sql="select * from doctor where id='%s' and password='%s';" %(d_id,password)
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) == 1:
                global doctor
                doctor = [result[0][0], result[0][3], department[int(result[0][2])]]
                print(doctor)
                return render_template("users/Doctor.html", results1=doctor,results2=character)
            else:
                return render_template("users/LoRe.html", msg="登陆失败，请重新登陆！")
        except:
            traceback.print_exc()
            conn.rollback()
    # 护士登录
    elif character=='2':
        sql1="select * from nurse where id='%s' and password='%s';" %(d_id,password)
        try:
            cursor.execute(sql1)
            result = cursor.fetchall()
            if len(result) == 1:
                global nurse
                nurse = [result[0][0], result[0][3], department[int(result[0][2])]]
                return render_template("users/Nurse.html", results1=nurse,results2=character)
            else:
                return render_template("users/LoRe.html", msg="登陆失败，请重新登陆！")
        except:
            traceback.print_exc()
            conn.rollback()
    # 管理员登录
    elif character=='3':
        sql2="select * from manager where id='%s' and password='%s';"%(d_id,password)
        try:
            cursor.execute(sql2)
            result1=cursor.fetchall()
            if len(result1)==1:
                global manager
                manager=[result1[0][0]]
                return render_template('users/Manager.html',results1=manager)
            else:
                return render_template("users/LoRe.html", msg="登陆失败，请重新登陆！")
        except:
            traceback.print_exc()
            conn.rollback()

    mysql_close(conn,cursor)
    return "登录失败"
# @app.route("/login",methods=['GET','POST '])
# def login():
#     if request.method=="GET":
#         return render_template("login.html")
#     else:
#         form=LoginForm(request.form)
#         if form.validate():
#             username=form.username.data
#             password=form.password.data
#             user=User.query.filter_by(username=username).first()
#             if user and check_password_hash(user.password,password):
#                 session['username']=user.username
#                 return render_template("Doctor.html")
#             else:
#                 return redirect("/login")
#         else:
#             return redirect("/login")












@app.route('/register',methods=['GET','POST'])
def Register():
    conn,cursor=mysql_conn()
    global character
    global patient
    global blist_id
    global mlist_id
    global clist_id
#     病人信息
    p_id=request.args.get('p_id')
    p_name=request.args.get('p_name')
    p_sex=request.args.get('p_sex')
#     提取病人信息
    sql0="select * from patient where patient_id='%s';"%p_id
    cursor.execute(sql0)
    result=cursor.fetchall()
    # 第一次挂号
    if len(result)==0:
        patient=[str(p_id),str(p_name),str(p_sex)]
        if p_sex=='男':
            p_sex=1
        elif p_sex=='女':
            p_sex=0
        sql1="insert into patient values(%d,'%s',%d);"%(p_id,p_name,p_sex)
        try:
            cursor.execute(sql1)
            conn.commit()
        except:
            traceback.print_exc()
            conn.rollback()
    else:
        patient=[p_id]
        patient.append(result[0][1])
        patient.append(p_sex)

#     生成病例 药单 检查单
    global lists
    sql1="select blist_id from blist where blist_id is not null;"
    sql2="select mlist_id from mlist where mlist_id is not null;"
    sql3="select clist_id from clist where clist_id is not null;"
#     表id自动+1
    cursor.execute(sql1)
    blist_id=cursor.fetchall()[-1][0]+1
    cursor.execute(sql2)
    mlist_id = cursor.fetchall()[-1][0] + 1
    cursor.execute(sql3)
    clist_id = cursor.fetchall()[-1][0] + 1

    lists=list()
    lists.append(blist_id)
    lists.append(mlist_id)
    lists.append(clist_id)

    if character=='1':
        mysql_close(conn, cursor)
        return render_template('users/DoctorMain.html', results0=lists, results1=doctor, results2=patient)
    elif character=='2':
        selection=request.args.get('selectdoctor')
        slist=selection.split()
        try:
            sql4="update doc_time set flag=%d where name='%s' and time='%s';"%(1,slist[1],slist[2])
            cursor.execute(sql4)
            conn.commit()
        except:
            traceback.print_exc()
            conn.rollback()
        mysql_close(conn, cursor)
        return render_template('users/NurseMain.html',results0=lists,results1=nurse,results2=patient)

# 再次挂号返回Doctor界面 只用输入卡号
@app.route('/register1')
def Register1():
    if character=='1':
        return render_template('users/Doctor.html', results1=doctor, results0=patient)
    elif character=='2':
        return render_template('users/Nurse.html',results1=nurse)
# 病历提交
@app.route('/binglitijiao')
def Uploadbl():
    zhusu = request.args.get('zhusu')
    xianbingshi = request.args.get('xianbingshi')
    jiwangshi = request.args.get('jiwangshi')
    yizhu=request.args.get('yizhu')

    conn,cursor=mysql_conn()
    sql0="select * from blist where blist_id=%d" % lists[0]
    cursor.execute(sql0)
    result=cursor.fetchall()
    try:
        if len(result)==0:
            print(type(lists[0]))
            print(type(doctor[0]))
            sql1="insert into blist values(%d,'%s','%s','%s','%s',%d,%d);"%(lists[0],zhusu,xianbingshi,jiwangshi,yizhu,int(patient[0]),doctor[0])
            cursor.execute(sql1)
            conn.commit()
            return '病历提交成功'
        elif len(result)==1:
            return '病历已提交，请重新挂号！！'
    except:
        traceback.print_exc()
        conn.rollback()
        return '提交失败'
    mysql_close(conn,cursor)

# 药品
#第一次添加药品
@app.route('/tmedicine')
def FirMedicine():
    return render_template('medicine/AddMedicine.html', results1=doctor)
# 第一次添加药品后
@app.route('/addmedicine')
def AddMedicine():
    m_name=request.args.get('m_name')
    m_name+=';'
    conn,cursor=mysql_conn()
    sql0='select mlist_id from mlist where mlist_id=%d;'%lists[1]
    cursor.execute(sql0)
    result=cursor.fetchall()
    # 该次挂号第一次添加药品
    try:
        if len(result)==0:
            sql1="insert into mlist(mlist_id,p_id,d_id,status) values(%d,%d,%d,%d);"%(lists[1],int(patient[0]),doctor[0],0)
            cursor.execute(sql1)
            conn.commit()

            sql2="update mlist set m_name='%s' where mlist_id=%d;"%(m_name,lists[1])
            cursor.execute(sql2)
            conn.commit()
            return render_template('medicine/ReAddMe.html', results1=doctor)

        elif len(result)==1:
            sql3="update mlist set m_name=concat(m_name,'%s') where mlist_id=%d"%(m_name,lists[1])
            cursor.execute(sql3)
            conn.commit()
            return render_template('medicine/ReAddMe.html', results1=doctor)
    except:
        traceback.print_exc()
        conn.rollback()
        return '添加失败'

    mysql_close(cursor,conn)

@app.route('/medicinelist')
def MedicineList():
    global mdl1
    conn, cursor = mysql_conn()
    sql1 = 'select m_name from mlist where mlist_id=%d;' % lists[1]
    cursor.execute(sql1)
    result = cursor.fetchall()
    result = result[0][0].split(';')
    del result[-1]
    # 对应前端表格
    mdl1 = []
    mdl2 = []
    mdl3 = []
    try:
        for i in range(len(result)):
            a=result[i]
            print(a)
            sql2="select medicine_id,medicine_name from medicine_item where medicine_name='%s';"%a
            cursor.execute(sql2)
            result1=cursor.fetchall()
            mdl1.append(i+1)
            mdl2.append(result1[0][0])
            mdl3.append(result1[0][1])
        return render_template('medicine/MedicineList.html', results0=lists, results1=doctor, results2=patient, results3=mdl1, results4=mdl3, results5=mdl2)
    except:
        return '药单为空'

# 检查
# 第一次提交检查
@app.route('/tcheck')
def FirCheck():
    return render_template('check/AddCheck.html',results1=doctor)

# 第一次添加药品后
@app.route('/addcheck')
def AddCheck():
    c_name=request.args.get('c_name')
    c_name+=";"
    conn,cursor=mysql_conn()
    sql0='select clist_id from clist where clist_id=%d'%lists[2]
    cursor.execute(sql0)
    result=cursor.fetchall()
    # 该次挂号第一次添加检查
    try:
        if len(result)==0:
            sql1="insert into clist(clist_id,p_id,d_id,status) values(%d,%d,%d,%d);"%(lists[2],int(patient[0]),doctor[0],0)
            cursor.execute(sql1)
            conn.commit()

            sql2="update clist set c_name='%s' where clist_id=%d;"%(c_name,lists[2])
            cursor.execute(sql2)
            conn.commit()
            return render_template('check/ReAddCheck.html', results1=doctor)

        elif len(result)==1:
            sql3="update clist set c_name=concat(c_name,'%s') where clist_id=%d"%(c_name,lists[2])
            cursor.execute(sql3)
            conn.commit()
            return render_template('check/ReAddCheck.html', results1=doctor)
    except:
        traceback.print_exc()
        conn.rollback()
        return '添加失败'

    mysql_close(cursor,conn)

@app.route('/checklist')
def CheckList():
    try:
        conn,cursor=mysql_conn()
        sql1="select c_name from clist where clist_id=%d;"%lists[2]
        cursor.execute(sql1)
        result=cursor.fetchall()
        result=result[0][0].split(';')

        del result[-1]
        # 对应前端表格
        mdl1=[]
        mdl2=[]
        mdl3=[]
        for i in range(len(result)):
            a=result[i]
            sql2="select * from check_item where check_name='%s';"%a
            cursor.execute(sql2)
            result1=cursor.fetchall()
            mdl1.append(i+1)
            mdl2.append(result1[0][0])
            mdl3.append(result1[0][1])

        return render_template('check/CheckList.html', results0=lists, results1=doctor, results2=patient, results3=mdl1, results4=mdl3, results5=mdl2)
    except:
        return '检查单为空'

@app.route('/manager')
def Manage():
    if character=='3':
        return render_template('users/Manager.html',results1=manager)
    elif character=='2':
        return render_template('users/NurseMain.html',results1=nurse)

# 查询
# 查询病历单
@app.route('/searchb')
def SearchB():
    blist_id=int(request.args.get("blist_id"))
    conn,cursor=mysql_conn()
    sql0="select * from blist where blist_id=%d;"%blist_id
    cursor.execute(sql0)
    result=cursor.fetchall()
    if len(result)==0:
        mysql_close(conn, cursor)
        return "查无此病历"
    else:
        sql="select zhusu,xianbingshi,jiwangshi,yizhu from blist where blist_id=%d"%blist_id
        cursor.execute(sql)
        result=cursor.fetchall()[0]
        b=[]
        b.append(result[0])
        b.append(result[1])
        b.append(result[2])
        b.append(result[3])

        sql1 = 'SELECT d_id,p_id FROM blist WHERE blist_id=%d' % blist_id
        cursor.execute(sql1)
        result1=cursor.fetchall()[0]

        sql2="select department,name from doctor where id=%d"%result1[0]
        cursor.execute(sql2)
        result2=cursor.fetchall()[0]
        global d,p
        d=[]
        d.append(result2[1])
        d.append(department[result2[0]])

        sql3="select * from patient where patient_id=%d"%result1[1]
        cursor.execute(sql3)
        result3=cursor.fetchall()[0]
        if result3[2]==1:
            ps="男"
        else:
            ps="女"
        p=[]
        p.append(str(result3[0]))
        p.append(result3[1])
        p.append(ps)
        mysql_close(conn, cursor)
        if character=='3':
            return render_template('search/SearchB.html',results1=manager,results2=d,results3=p,results4=b,results5=str(blist_id),results6=character)
        elif character=='2':
            return render_template('search/NurseSearchB.html',results1=nurse,results2=d,results3=p,results4=b,results5=str(blist_id),results6=character)

@app.route('/delb')
def DelB():
    blist_id = int(request.args.get('db_id'))
    conn,cursor=mysql_conn()
    sql0 = "DELETE FROM blist WHERE blist_id=%d" % blist_id
    try:
        cursor.execute(sql0)
        conn.commit()
        mysql_close(conn, cursor)
        message="删除成功"
    except:
        traceback.print_exc()
        conn.rollback()
        mysql_close(conn, cursor)
        message='删除失败'
    flash(message)
    # return render_template('search/SearchBS.html',results1=manager,results2=d,results3=p,results5='')

    if character == '3':
        return render_template('search/SearchBS.html', results1=manager,results2=d,results3=p,results5='')
    elif character == '2':
        return render_template('users/NurseMain.html', results1=nurse,results2=character)

global sum
# 查询药单
@app.route('/searchm')
def SearchM():
    global character
    global mdl0
    mlist_id = request.args.get('mlist_id')
    db, cursor = mysql_conn()
    sql0 = "SELECT mlist_id FROM mlist WHERE mlist_id='%s';" % mlist_id
    cursor.execute(sql0)
    result = cursor.fetchall()
    try:
        if len(result)==0:
            message='查无此药单'
            flash(message)
            if character=='2':
                return render_template('users/NurseMain.html',results1=nurse,results2=character)
            elif character=='3':
                return render_template('users/Manager.html',results1=manager,results2=character)
        else:
            sum=0
            sql1 = "SELECT m_name FROM mlist WHERE mlist_id='%s';" % mlist_id
            cursor.execute(sql1)
            result = cursor.fetchall()
            result = result[0][0].split(';')
            del result[-1]
            mdl1 = []
            mdl2 = []
            mdl0 = []
            mdl3 = []
            for i in range(len(result)):
                a = result[i]
                sql2 = "SELECT medicine_id,medicine_name,medicine_money FROM medicine_item WHERE medicine_name='%s'" % a
                cursor.execute(sql2)
                result1 = cursor.fetchall()
                mdl1.append(i + 1)
                mdl0.append(result1[0][0])
                mdl2.append(result1[0][1])
                mdl3.append(result1[0][2])
                sum+=result1[0][2]
            sql0="update mlist set total=%d where mlist_id='%s';"%(sum,mlist_id)
            cursor.execute(sql0)
            sql2 = "SELECT d_id,p_id FROM mlist WHERE mlist_id='%s';" % mlist_id
            cursor.execute(sql2)
            result = cursor.fetchall()[0]
            sql3 = "SELECT department,name FROM doctor WHERE id=%d;" % result[0]
            cursor.execute(sql3)
            r = cursor.fetchall()[0]
            global d,p
            d = []
            d.append(r[1])
            d.append(department[r[0]])
            sql4 = "SELECT * FROM patient WHERE patient_id=%d;" % result[1]
            cursor.execute(sql4)
            db.commit()
            r = cursor.fetchall()[0]
            if r[2] == 1:
                ps = '男'
            else:
                ps = '女'
            p = []
            p.append(str(r[0]))
            p.append(r[1])
            p.append(ps)
            if character=='3':
                return render_template('search/SearchM.html', results1=manager,results2=d,results3=p,results5=str(mlist_id),results6=mdl1,results7=mdl2,results8=mdl0)
            elif character=='2':
                return render_template('search/NurseSearchM.html',results1=nurse,results2=d,results3=p,results5=str(mlist_id),results6=mdl1,results7=mdl2,results8=mdl0,results9=mdl3)
    except:
        traceback.print_exc()
        db.rollback()
        return '检索失败'

    mysql_close(db,cursor)

@app.route('/delm')
def DelM():
    mlist_id = int(request.args.get('dm_id'))
    conn,cursor=mysql_conn()
    sql0 = "DELETE FROM mlist WHERE mlist_id=%d" % mlist_id
    try:
        cursor.execute(sql0)
        conn.commit()
        mysql_close(conn, cursor)
        message="删除成功"
    except:
        traceback.print_exc()
        conn.rollback()
        mysql_close(conn, cursor)
        message='删除失败'

    flash(message)
    return render_template('search/SearchMS.html', results1=manager, results2=d, results3=p)
    # if character=='3':
    #     return render_template('search/SearchMS.html',results1=manager,results2=d,results3=p)
    # elif character=='2':
    #     return render_template('search/NurseSearchM.html',results1=nurse,results2=d,results3=p)

@app.route('/delm_i')
def DelMedI():
    global mdl1
    conn, cursor = mysql_conn()
    mlist=[]
    print(len(mdl1))
    sql0 = "select m_name from mlist where mlist_id=%d" % lists[1]
    cursor.execute(sql0)
    result0 = cursor.fetchall()
    result=result0[0][0]
    for i in range(len(mdl1)):
        j=str(i+1)
        mlist.append(request.args.get(j)+";")
        result = result.replace(mlist[i],'')
    try:

        sql1="update mlist set m_name='%s' where mlist_id=%d"%(result,lists[1])
        cursor.execute(sql1)
        conn.commit()
        return render_template('medicine/AddMedicine.html', results1=doctor)
    except:
            traceback.print_exc()
            conn.rollback()
            mysql_close(conn, cursor)
            return '删除失败'

# 查询检查单
@app.route('/searchc')
def SearchC():
    global character
    clist_id = int(request.args.get('clist_id'))
    db, cursor = mysql_conn()
    sql0 = 'SELECT clist_id FROM clist WHERE clist_id=%d' % clist_id
    cursor.execute(sql0)
    result = cursor.fetchall()
    try:
        if len(result) == 0:
            message = '查无此药单'
            flash(message)
            if character == '2':
                return render_template('users/NurseMain.html', results1=nurse, results2=character)
            elif character == '3':
                return render_template('users/Manager.html', results1=manager, results2=character)
        else:
            sum=0
            sql1 = 'SELECT c_name FROM clist WHERE clist_id=%d;' % clist_id
            cursor.execute(sql1)
            result = cursor.fetchall()
            result = result[0][0].split(';')
            del result[-1]
            cdl1 = []
            cdl2 = []
            cdl3 = []
            cdl0 = []
            for i in range(len(result)):
                a = result[i]
                sql2 = "SELECT check_id,check_name,check_money FROM check_item WHERE check_name='%s';" % a
                cursor.execute(sql2)
                result1 = cursor.fetchall()
                cdl0.append(i + 1)
                cdl1.append(result1[0][0])
                cdl2.append(result1[0][1])
                cdl3.append(result1[0][2])
                sum+=result1[0][2]
            sql0 = "update clist set total=%d where clist_id='%s';" % (sum, clist_id)
            cursor.execute(sql0)
            sql2 = "SELECT d_id,p_id FROM clist WHERE clist_id='%s';" % clist_id
            cursor.execute(sql2)
            result = cursor.fetchall()[0]
            sql3 = "SELECT name,department FROM doctor WHERE id=%d;" % result[0]
            cursor.execute(sql3)
            r = cursor.fetchall()[0]
            d = []
            d.append(r[0])
            d.append(department[r[1]])
            sql4 = "SELECT patient_id,patient_name,patient_sex FROM patient WHERE patient_id=%d;" % result[1]
            cursor.execute(sql4)
            r = cursor.fetchall()[0]
            if r[2] == 1:
                ps = '男'
            else:
                ps = '女'
            p = []
            p.append(str(r[0]))
            p.append(r[1])
            p.append(ps)
            if character=='3':
                return render_template('search/SearchC.html', results1=manager, results2=d, results3=p, results5=str(clist_id),
                               results6=cdl0, results7=cdl1, results8=cdl2)
            elif character=='2':
                return render_template('search/NurseSearchC.html', results1=nurse, results2=d, results3=p, results5=str(clist_id),
                               results6=cdl0, results7=cdl1, results8=cdl2,results9=cdl3)
    except:
        traceback.print_exc()
        db.rollback()
        return '检索失败'

    mysql_close(db, cursor)


@app.route('/delc')
def DelC():
    clist_id = int(request.args.get('dc_id'))
    conn, cursor = mysql_conn()
    sql0 = "DELETE FROM clist WHERE clist_id=%d" % clist_id
    try:
        cursor.execute(sql0)
        conn.commit()
        mysql_close(conn, cursor)
        message="删除成功"
    except:
        traceback.print_exc()
        conn.rollback()
        mysql_close(conn, cursor)
        message='删除失败'

    flash(message)
    return render_template('search/SearchCS.html',results1=manager,results2=d,result3=p)
@app.route('/research')
def ReSearch():
    return render_template('users/Manager.html',results1=manager)













@app.route('/editd')
def EditD():
    db, cursor = mysql_conn()
    doctor_id = request.args.get('d_id')
    doctor_p = request.args.get('d_p')
    doctor_n = request.args.get('d_name')
    doctor_d = request.args.get('d_d')
    doctor_t = request.args.get('type')
    sql0 = 'SELECT id FROM doctor WHERE id="%s";' % doctor_id
    cursor.execute(sql0)
    result = cursor.fetchall()
    global index
    index=0
    try:
        if len(result) == 0:
            if doctor_t=='1':
                doctor_t=1
            else:
                doctor_t = 0

            for i in range(len(department)):
                if doctor_d == department[i]:
                    index=i

            sql1 = "INSERT INTO doctor VALUES ('%s','%s',%d,'%s','%s');" % (doctor_id,doctor_p,index,doctor_n,doctor_t)
            try:
                cursor.execute(sql1)
                db.commit()
                return '添加成功'
            except:
                traceback.print_exc()
                db.rollback()
                return '添加失败'

        if len(result) == 1:
            if doctor_t=='1':
                doctor_t=1
            else:
                doctor_t = 0

            for i in range(0,4):
                if doctor_d == department[i]:
                    index=i

            sql2 = "UPDATE doctor SET password='%s',department=%d,type=%d,name='%s' WHERE id='%s';" % (doctor_p,index,doctor_t,doctor_n,doctor_id)
            try:
                cursor.execute(sql2)
                db.commit()
                return "更新成功"
            except:
                traceback.print_exc()
                db.rollback()
                return '更新失败'
    except:
        traceback.print_exc()
        db.rollback()
        return '检索失败'
    mysql_close(db,cursor)
@app.route('/reeditd')
def ReEditD():
    return render_template('edit/EditD.html',results1=manager)

@app.route('/editn')
def EditN():
    db, cursor = mysql_conn()
    doctor_id = request.args.get('d_id')
    doctor_p = request.args.get('d_p')
    doctor_n = request.args.get('d_name')
    doctor_d = request.args.get('d_d')
    sql0 = 'SELECT id FROM nurse WHERE id="%s";' % doctor_id
    cursor.execute(sql0)
    result = cursor.fetchall()
    global index
    try:
        if len(result) == 0:

            for i in range(0,4):
                if doctor_d == department[i]:
                    index=i

            sql1 = "INSERT INTO nurse VALUES ('%s','%s',%d,'%s');" % (doctor_id,doctor_p,index,doctor_n)
            try:
                cursor.execute(sql1)
                db.commit()
                return '添加成功'
            except:
                traceback.print_exc()
                db.rollback()
                return '添加失败'
        index=0
        if len(result) == 1:
            for i in range(len(department)):
                if doctor_d == department[i]:
                    index=i

            sql2 = "UPDATE nurse SET password='%s',department=%d,name='%s' WHERE id='%s';" % (doctor_p,index,doctor_n,doctor_id)
            try:
                cursor.execute(sql2)
                db.commit()
                return "更新成功"
            except:
                traceback.print_exc()
                db.rollback()
                return '更新失败'
    except:
        traceback.print_exc()
        db.rollback()
        return '检索失败'
    mysql_close(db,cursor)

@app.route('/reeditn')
def ReEditN():
    return render_template('edit/EditN.html',results1=manager)

global doctorlist,numlist













@app.route('/nursearch')
def NurSearch():
    return render_template('users/NurseMain.html',results1=nurse,results2=character)
@app.route('/doctorlist')
def DoctorList():
    global doctorlist,numlist
    type=request.args.get("type")
    depart=request.args.get("department")
    global j
    for i in range(len(department)):
        if depart==department[i]:
            j=i
            break
    now_time=time.strftime('%H:%M', time.localtime())
    if type=="1":
        conn,cursor=mysql_conn()
        try:
            sql1="select doctor.name,doc_time.time from doctor,doc_time where doctor.id=doc_time.id and doctor.type=%d and doctor.department=%d and doc_time.time>'%s' and doc_time.flag=%d"%(int(type),j,now_time,0)
            cursor.execute(sql1)
            result=cursor.fetchall()
            doctorlist = []
            numlist = []
            for i in range(len(result)):
                doctorlist.append(result[i])
                numlist.append(i+1)
            sql3="update doc_time set flag=%d where time<'%s';"%(0,now_time)
            cursor.execute(sql3)
            conn.commit()
        except:
            traceback.print_exc()
            conn.rollback()
        mysql_close(conn,cursor)
        return render_template('users/DoctorList1.html', results1=nurse, results2=doctorlist,results3=numlist,results4=depart)

    elif type=="2":
        conn,cursor=mysql_conn()
        try:
            sql2="select doctor.name,doc_time.time from doctor,doc_time where doctor.id=doc_time.id and doctor.type=%d and doctor.department=%d and doc_time.time>'%s' and doc_time.flag=%d"%(int(type),j,now_time,0)
            cursor.execute(sql2)
            result=cursor.fetchall()
            doctorlist = []
            numlist = []
            for i in range(len(result)):
                doctorlist.append(result[i])
                print(numlist)
                numlist.append(i+1)
            sql4="update doc_time set flag=%d where time<'%s';"%(0,now_time)
            cursor.execute(sql4)
            conn.commit()
        except:
            traceback.print_exc()
            conn.rollback()
        mysql_close(conn,cursor)
        return render_template('users/DoctorList2.html', results1=nurse, results2=doctorlist,results=numlist)

@app.route('/remainbed')
def RemainB():
    return render_template('users/RemainBed.html',results1=nurse)

@app.route('/searchbed')
def SearchBed():
    conn,cursor=mysql_conn()
    department=request.args.get('department')
    try:
        sql0="select num from department where name='%s';"%department
        cursor.execute(sql0)
        num=cursor.fetchall()[0]
        conn.commit()
        if num !=0:
            return render_template('users/Hospitalization.html',results1=nurse,results2=num)
        else:
            return '床位已满'
    except:
        traceback.print_exc()
        conn.rollback()
    mysql_close(conn,cursor)
@app.route('/zhuyuan')
def Hospitalization():
    global bd_id
    conn,cursor=mysql_conn()
    department=request.args.get('department')
    sex=request.args.get('p_sex')
    id=request.args.get('p_id')

    try:
        sql1 = "select id from hos where id is not null;"
        cursor.execute(sql1)
        bd_id = cursor.fetchall()[-1][0] + 1
        sql2 = "insert into hos values(%d,'%s','%s','%s');"%(bd_id,id,sex,department)
        cursor.execute(sql2)
        sql3 = "update department set num=num-1 where name ='%s';"%department
        cursor.execute(sql3)
        conn.commit()
    except:
        traceback.print_exc()
        conn.rollback()
    mysql_close(conn, cursor)
    return render_template('users/RemainBed.html',results1=nurse)
global sum
@app.route('/paym')
def PayM():
    mlist_id=request.args.get('mlist_id')
    db, cursor = mysql_conn()
    try:
        sql0="select status from mlist where mlist_id='%s';"%mlist_id
        cursor.execute(sql0)
        flag=cursor.fetchall()[0]
        flag=str(flag)
        status = '(0,)'
        print(type(flag))
        if flag == status:
        # 业务逻辑处理：调用支付宝接口

        # 创建支付宝sdk的工具对象
        # 私钥                                      当前目录(__file__ 代表当前目录路径)
        # app_private_key_path = open(os.path.join(os.path.dirname(__file__), "keys/private_key.pem")).read()  # 私钥
        # alipay_public_key_path = open(os.path.join(os.path.dirname(__file__),
        #                                            "keys/public_key.pem")).read()  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        #
        # alipay = AliPay(
        #     appid=constants.ALIPAY_APP_ID,
        #     app_notify_url=None,  # 默认回调url
        #     app_private_key_string=app_private_key_path,  # 私钥
        #     # 支付宝公钥，验证支付宝回传消息使用，不是你自己的公钥
        #     alipay_public_key_string=alipay_public_key_path,
        #
        #     sign_type="RSA2",  # RSA 或者 RSA2
        #     debug=True  # 默认false, true是沙箱环境
        # )
        #
        # # 手机网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
        # order_string = alipay.api_alipay_trade_wap_pay(
        #     out_trade_no=order_id,  # 订单编号
        #     total_amount=order.amount / 100.0,  # 支付金额
        #     subject="爱租房 %s " % order_id,  # 订单标题
        #     return_url="http://127.0.0.1:5000/orders.html",  # 返回链接地址
        #     notify_url=None  # 可选, 不填则使用默认notify url
        # )
        #
        # pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string
        #
        # return jsonify(errno=RET.OK, errmsg="OK", data={"pay_url": pay_url})

    # try:
    #         sql1 = "SELECT m_name FROM mlist WHERE mlist_id='%s';" % mlist_id
    #         cursor.execute(sql1)
    #         result = cursor.fetchall()
    #         result = result[0][0].split(';')
    #         # mdl1 = []
    #         # mdl2 = []
    #         # mdl0 = []
    #         # mdl3 = []
    #         sum=0
    #         for i in range(len(result)-1):
    #             a = result[i]
    #             sql2 = "SELECT medicine_money FROM medicine_item WHERE medicine_name='%s'" % a
    #             cursor.execute(sql2)
    #             result1 = cursor.fetchall()
    #             sum+=result1[0][0]
    #         sql3="update mlist set total=%d;"%sum
    #         cursor.execute(sql3)
    #         db.commit()
    #             # mdl0.append(i + 1)
    #             # mdl1.append(result1[0][0])
    #             # mdl2.append(result1[0][1])
    #             # mdl3.append(result1[0][2])
            sql1="select total from mlist where mlist_id='%s';"%mlist_id
            cursor.execute(sql1)
            result = cursor.fetchall()
            return render_template('search/NursePay.html',results1=nurse,results4=result,result1=character)
        else:
            return render_template('users/NurseMain.html',results1=nurse,result1=character)
    except:
        traceback.print_exc()
        db.rollback()
        return '检索失败'

    mysql_close(db,cursor)

@app.route('/payc')
def PayC():
    clist_id=request.args.get('clist_id')
    db, cursor = mysql_conn()
    try:
        sql0="select status from clist where clist_id='%s';"%clist_id
        cursor.execute(sql0)
        flag=cursor.fetchall()[0]
        flag=str(flag)
        status = '(0,)'
        print(type(flag))
        if flag == status:
        # 业务逻辑处理：调用支付宝接口

        # 创建支付宝sdk的工具对象
        # 私钥                                      当前目录(__file__ 代表当前目录路径)
        # app_private_key_path = open(os.path.join(os.path.dirname(__file__), "keys/private_key.pem")).read()  # 私钥
        # alipay_public_key_path = open(os.path.join(os.path.dirname(__file__),
        #                                            "keys/public_key.pem")).read()  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        #
        # alipay = AliPay(
        #     appid=constants.ALIPAY_APP_ID,
        #     app_notify_url=None,  # 默认回调url
        #     app_private_key_string=app_private_key_path,  # 私钥
        #     # 支付宝公钥，验证支付宝回传消息使用，不是你自己的公钥
        #     alipay_public_key_string=alipay_public_key_path,
        #
        #     sign_type="RSA2",  # RSA 或者 RSA2
        #     debug=True  # 默认false, true是沙箱环境
        # )
        #
        # # 手机网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
        # order_string = alipay.api_alipay_trade_wap_pay(
        #     out_trade_no=order_id,  # 订单编号
        #     total_amount=order.amount / 100.0,  # 支付金额
        #     subject="爱租房 %s " % order_id,  # 订单标题
        #     return_url="http://127.0.0.1:5000/orders.html",  # 返回链接地址
        #     notify_url=None  # 可选, 不填则使用默认notify url
        # )
        #
        # pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string
        #
        # return jsonify(errno=RET.OK, errmsg="OK", data={"pay_url": pay_url})

    # try:
    #         sql1 = "SELECT m_name FROM mlist WHERE mlist_id='%s';" % mlist_id
    #         cursor.execute(sql1)
    #         result = cursor.fetchall()
    #         result = result[0][0].split(';')
    #         # mdl1 = []
    #         # mdl2 = []
    #         # mdl0 = []
    #         # mdl3 = []
    #         sum=0
    #         for i in range(len(result)-1):
    #             a = result[i]
    #             sql2 = "SELECT medicine_money FROM medicine_item WHERE medicine_name='%s'" % a
    #             cursor.execute(sql2)
    #             result1 = cursor.fetchall()
    #             sum+=result1[0][0]
    #         sql3="update mlist set total=%d;"%sum
    #         cursor.execute(sql3)
    #         db.commit()
    #             # mdl0.append(i + 1)
    #             # mdl1.append(result1[0][0])
    #             # mdl2.append(result1[0][1])
    #             # mdl3.append(result1[0][2])
            sql1="select total from clist where clist_id='%s';"%clist_id
            cursor.execute(sql1)
            result = cursor.fetchall()
            return render_template('search/NursePay.html',results1=nurse,results4=result,result1=character)
        else:
            return render_template('users/NurseMain.html',results1=nurse,result1=character)
    except:
        traceback.print_exc()
        db.rollback()
        return '检索失败'

    mysql_close(db,cursor)


@app.route('/payresult')
def PayRe():
    return render_template('search/NursePay.html',results1=nurse,results2=character)

# 添加路由
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        # 通过file标签获取文件
        f = request.files['file']
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "图片类型：png、PNG、jpg、JPG、bmp"})
        # 当前文件所在路径
        basepath = os.path.dirname(__file__)
        # 一定要先创建该文件夹，不然会提示没有该路径
        upload_path = os.path.join(basepath, 'static/img', secure_filename(f.filename))
        # 保存文件
        f.save(upload_path)
        # 返回上传成功界面
        return render_template('test/upload_ok.html')
    # 重新返回上传界面
    return render_template('test/upload.html')

if __name__ == '__main__':
    app.run()

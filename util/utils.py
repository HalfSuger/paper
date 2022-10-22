import time
import traceback

import pymysql
from flask import jsonify, request, render_template
import static

def mysql_conn():
    conn = pymysql.connect(host="localhost", user="root", password="1234", database="ops")

    cusor = conn.cursor()
    return conn,cusor

def mysql_close(conn, cursor):
    cursor.close()
    conn.close()

def query(sql,*args):
    conn, cursor = mysql_conn()
    cursor.execute(sql,args)
    res = cursor.fetchall()
    mysql_close(conn, cursor)
    return res

def Register(username,password):
    conn, cursor = mysql_conn()
    sql = "insert into doctor VALUES('%s','%s');"%(username,password)
    try:
            cursor.execute(sql)
            results=cursor.fetchall()
            if len(results)==1:
                return render_template("users/Doctor.html", msg='登陆成功')
            else:
                return render_template('users/Doctor.html', msg='用户名或密码有误')
            conn.commit()
    except:
            traceback.print_exc()
            conn.rollback()
            mysql_close(conn,cursor)

def validate(role,id,password):
    conn,cursor=mysql_conn()
    if role=='1':
        sql1="select * from doctor where id='%s'"%id
        cursor.execute(sql1)
        result1=cursor.fetchall()
        if len(result1)==1:
            return '用户已存在'
        elif len(result1)==0:
            try:
                sql11="insert into doctor(id,password) values('%s','%s')"%(id,password)
                cursor.execute(sql11)
                conn.commit()
            except:
                traceback.print_exc()
                conn.rollback()
            mysql_close(conn,cursor)
            return '注册成功'
    elif role=='2':
        sql2="select * from nurse where id='%s'"%id
        cursor.execute(sql2)
        result2=cursor.fetchall()
        if len(result2)==1:
            return '用户已存在'
        elif len(result2)==0:
            try:
                sql21 = "insert into nurse(id,password) values('%s','%s')" % (id, password)
                cursor.execute(sql21)
                conn.commit()
            except:
                traceback.print_exc()
                conn.rollback()
            mysql_close(conn, cursor)
            return '注册成功'
    elif role == '3':
        sql3 = "select * from doctor where id='%s'" % id
        cursor.execute(sql3)
        result3 = cursor.fetchall()
        if len(result3) == 1:
            return '用户已存在'
        elif len(result3) == 0:
            try:
                sql31 = "insert into manager(id,password) values('%s','%s')" % (id, password)
                cursor.execute(sql31)
                conn.commit()
            except:
                traceback.print_exc()
                conn.rollback()
            mysql_close(conn, cursor)
            return '注册成功'


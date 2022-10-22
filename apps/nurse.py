# import traceback
#
# from flask import Blueprint, render_template, request
# from app import nurse
# from util.utils import mysql_conn, mysql_close
#
# nur=Blueprint('nurse',__name__,url_prefix="/nurse")
# global department
# department = ['内科', '外科', '妇科', '儿科']
# global doctor
# global manager
# global patient
# global lists
#
# @nurse.route('/doctorlist')
# def DoctorList():
#     global doctorlist
#     type=request.args.get("type")
#     if type=="1":
#         conn,cursor=mysql_conn()
#         try:
#             sql1="select name from doctor where type=%d"%int(type)
#             cursor.execute(sql1)
#             result=cursor.fetchall()
#             for i in range(len(result)):
#                 doctorlist=[]
#                 doctorlist.append(result[i])
#             conn.commit()
#         except:
#             traceback.print_exc()
#             conn.rollback()
#         mysql_close(conn,cursor)
#     return render_template('users/DoctorList1.html', results1=nurse, results2=doctorlist)
# @nurse.route('/register')
# def NurRegister():
#     conn,cursor=mysql_conn()
#     global patient
#     global blist_id
#     global mlist_id
#     global clist_id
# #     病人信息
#     p_id=request.args.get('p_id')
#     p_name=request.args.get('p_name')
#     p_sex=request.args.get('p_sex')
#
# #     提取病人信息
#     sql0="select * from patient where patient_id='%s';"%p_id
#     cursor.execute(sql0)
#     result=cursor.fetchall()
#     # 第一次挂号
#     if len(result)==0:
#         patient=[str(p_id),str(p_name),str(p_sex)]
#         if p_sex=='男':
#             p_sex=1
#         elif p_sex=='女':
#             p_sex=0
#         sql1="insert into patient values(%d,'%s',%d);"%(p_id,p_name,p_sex)
#         try:
#             cursor.execute(sql1)
#             conn.commit()
#         except:
#             traceback.print_exc()
#             conn.rollback()
#     else:
#         patient=[p_id]
#         patient.append(result[0][1])
#         patient.append(p_sex)
#
# #     生成病例 药单 检查单
#     global lists
#     sql1="select blist_id from blist where blist_id is not null;"
#     sql2="select mlist_id from mlist where mlist_id is not null;"
#     sql3="select clist_id from clist where clist_id is not null;"
# #     表id自动+1
#     cursor.execute(sql1)
#     blist_id=cursor.fetchall()[-1][0]+1
#     cursor.execute(sql2)
#     mlist_id = cursor.fetchall()[-1][0] + 1
#     cursor.execute(sql3)
#     clist_id = cursor.fetchall()[-1][0] + 1
#
#     lists=list()
#     lists.append(blist_id)
#     lists.append(mlist_id)
#     lists.append(clist_id)
#
#     mysql_close(conn,cursor)
#     return render_template('users/DoctorMain.html', results0=lists, results1=nurse, results2=patient)
#
# # 再次挂号返回Doctor界面 只用输入卡号
# @nurse.route('/register1')
# def NurRegister1():
#     return render_template('users/Doctor.html', results1=nurse, results0=patient)
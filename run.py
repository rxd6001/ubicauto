# -*- coding:utf-8 -*-

from UBiC_Rotate_data import gb
from UBiC_Search_def import myasset, ex_item, cnt_p, askper, ticker_per2, one_sell2, perct, de_perct, kwrun, one_buy, linenumber, get_orderi2, t_c2, expa, expr
from flask import Flask, render_template, render_template_string, flash, redirect, \
	session, abort, request, url_for, escape, jsonify				# request, url_for :form에 입력한 정보를 전송해서 다른 페이지에 출력
from flask_login import LoginManager
# from flask.ext.cache import Cache
from subprocess import PIPE, Popen
from markupsafe import escape
# from flask.ext.wtf import Form
# from wtforms import StringField, SubmitField
# from wtforms.validators import Required
import psutil
import os
import ssl
from decimal import Decimal
import pickle
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import secrets
import json
import subprocess
import pyupbit

app = Flask(__name__)	# Flask 객체 생성

app.secret_key = b';\xda\xe7^r\x03j^'
# app.secret_key = secrets.token_bytes(8)
app.config["PERMANENT_SESSION_LIFETIME"] =  timedelta(hours=1)	#로그인 지속 시간 1분
# app.config["PERMANENT_SESSION_LIFETIME"] =  timedelta(minutes=30)	#로그인 지속 시간 1분
app.config['USE_PERMANENT_SESSION'] = True
# login_manager = LoginManager()
# login_manager.init_app(app)

start_time = time.time()                    # 시간 측정 시작

def check_logined():					# 로그인 체크하기
	print(session)
	if 'id' in session:
		print(f'{session["id"]} 계정으로 로그인 되었습니다')
		return True
	return False

def login_upbit(user_id):			# 업비트로 로그인 후 실행하는 함수에 사용
	try:
		f = open(("/root/UBiCauto/Acct/upbit%s.txt") %(acc_name[user_id]))        # 파일 열기
		lines = f.readlines()                       # 라인을 일러들임
		access = lines[0].strip()                   # access key '\n' 0번 행 불러오기
		secret = lines[1].strip()                   # secret key '\n' 1번 행 불러오기
		f.close()                                   # 파일 닫기
		upbit = pyupbit.Upbit(access, secret)      # 업비트 로그인
		return upbit
	except Exception as e:
		print(e)

@app.route("/error/500")			# 에러 이동 페이지
def error():
	return render_template('/error/500.html')

acc_str = {'zenka':'ubic1', 'butysoo':'ubic2', 'liebe':'ubic3'}		# 계정별 string 설정
acc_name = {'ubic1':'1', 'ubic2':'2', 'ubic3':'3' }			# 웹페이지에서 매도버튼 클릭 시 계정별 구분 적용
cal_name = {'ubic1':['/root/UBiCauto/data/mycal1.pickle', '/root/UBiCauto/data/mycal_m1.pickle','/root/UBiCauto/data/add_num1.pickle',\
	'/root/UBiCauto/data/cal_l1.pickle','/root/UBiCauto/data/t_tp1.pickle', '/root/UBiCauto/data/set_cfg1.pickle',\
	'/root/UBiCauto/data/ext_item1.pickle'],\
	'ubic2':['/root/UBiCauto/data/mycal2.pickle', '/root/UBiCauto/data/mycal_m2.pickle', '/root/UBiCauto/data/add_num2.pickle',\
	'/root/UBiCauto/data/cal_l2.pickle', '/root/UBiCauto/data/t_tp2.pickle', '/root/UBiCauto/data/set_cfg2.pickle',\
	'/root/UBiCauto/data/ext_item2.pickle'],\
	'ubic3':['/root/UBiCauto/data/mycal3.pickle', '/root/UBiCauto/data/mycal_m3.pickle', '/root/UBiCauto/data/add_num3.pickle',\
	'/root/UBiCauto/data/cal_l3.pickle', '/root/UBiCauto/data/t_tp3.pickle', '/root/UBiCauto/data/set_cfg3.pickle',\
	'/root/UBiCauto/data/ext_item3.pickle']}					# 자산정보 파일 가져오기위한 경로
# cal_name['ubic'] 설명
	# [0]:일별내역, [1]:월별내역, [2]:추매횟수, [3]:매도리스트, [4]:초기매수금액, [5]:종목평가손익 리스트, [6]:매수,매도 설정값
acc_bal = {'ubic1': 40000000, 'ubic2': 1000000, 'ubic3': 4890000}		# 계정별 원금

@app.route("/")			# 계정 및 세션 체크
def index():
	if check_logined():
		try:			
			acc = session["id"]
			# print(f'세션: {acc_str[acc]}')
			print(f'/(index) (로그인 계정: {acc_str[acc]}, 세션: {session["id"]})')
			return redirect('/'+acc_str[acc])
		except Exception as e:
			print(e)
			return render_template('/login.html')
	else:
		return render_template('/login.html')

@app.route('/ubic_signup')			# 싸인업?
def ubic_signup():
	return render_template("/ubic_signup.html")

@app.route('/login', methods=['POST', 'GET'])			# 로그인
def login_confirm():
	with open('/root/UBiCauto/Acct/members.pickle', 'rb') as mb:
		members = pickle.load(mb)

	try:
		id_ = request.form['id_']
		pw_ = request.form['pw_']
		if members[id_] == pw_:
			session['id'] = id_
			print(acc_str[session['id']])
			# return redirect(url_for('ubic1'))
			session.permanent = True
			return redirect("/" + acc_str[id_])
		else:
			return render_template('/login.html')
	except Exception as e:
		return render_template('/login.html')

@app.route('/logout')			# 로그아웃
def logout():
	session.clear()
	print('계정이 로그아웃 되었습니다')
	return render_template("/login.html")

@app.route("/favicon.ico", methods=['GET'])			# favicon
def favicon():
	return ""

@app.route('/<user_id>/ubic_reps', methods=['GET', 'POST'])			# 프로세스 재시작 수동
def ubic_reps(user_id):
	start_time = time.time()                    # 시간 측정 시작
	if check_logined():
		try:
			print(f'ubic_reps (계정: {user_id}, 세션: {session["id"]})')

			if acc_str[session['id']]:
				if session['id'] == "zenka" or acc_str[session['id']] == user_id:
					pass
				else:
					return redirect(url_for("error"))
		except Exception as e:
			print(e)
	else:
		return redirect(url_for('index'))

	with open('/root/UBiCauto/data/ext_itemB.pickle', 'rb') as fr:      # 신규매수 제외할 코인파일(ext_itemB.pickle)
		ext_itemB = pickle.load(fr)
	ext_B = ext_itemB['ext_b']
	
	System_Check = subprocess.run(['/usr/bin/bash', '/usr/bin/ubicck'], stdout=subprocess.PIPE, universal_newlines=True)
	ob_ck = System_Check.stdout

	if "p /" in ob_ck:			# 감시 프로세스 체크
		ob_ck = True
	else:
		ob_ck = False
	
	System_Check = subprocess.run(['/usr/bin/bash', '/usr/bin/shp'], stdout=subprocess.PIPE, universal_newlines=True)
	all_ckout = System_Check.stdout

	if ("UBiCauto/myc" in all_ckout) and ("UBiCauto/wrun" in all_ckout) and ("UBiCauto/prr" in all_ckout)\
		and ("UBiCauto/pbb" in all_ckout) and ("UBiCauto/pss" in all_ckout):			# 전체 프로세스 체크
		all_ck = True
	else:
		all_ck = False
	if ("UBiCauto/prr" in all_ckout):			# 공통 프로세스 체크
		prr_ck = True
	else:
		prr_ck = False
	if ("UBiCauto/wrun" in all_ckout):			# 웹서버 프로세스 체크
		wrun_ck = True
	else:
		wrun_ck = False
	if ("UBiCauto/pbb" in all_ckout):			# 매수 프로세스 체크
		pbb_ck = True
	else:
		pbb_ck = False
	if ("UBiCauto/pss" in all_ckout):			# 매도 프로세스 체크
		pss_ck = True
	else:
		pss_ck = False
	if ("UBiCauto/myc" in all_ckout):			# 자료생성 프로세스 체크
		myc_ck = True
	else:
		myc_ck = False

	print(f'감시: {ob_ck}, 전체: {all_ck}, 공통: {prr_ck}, 웹서버: {wrun_ck}, 매수: {pbb_ck}, 매도: {pss_ck}, 자료생성: {myc_ck}')
	if request.method == "POST":
		cmdh = request.form['cmdh']
		cmdb = request.form['cmdb']
		xdata = request.form['xdata']
		cndata = request.form['cndata']
		print(request.form)
		# print(f'전송방식:{request.method}, expcn:{expcn}')
		# print(f'전송방식: {request.method}, cmdh: {cmdh}, cmdb: {cmdb}, xdata: {xdata}, cndata: {cndata}')
		try:
			if cmdb == "expa":
				expa(xdata)
				# print(f'종목: {xdata}을 추가')
				rdata = {'response': '200', 'cmdb':cmdb, 'xdata':xdata}
				print(f'{linenumber()}p::id:{id} --- (1) Cycle time: {round((time.time() - start_time), 3)} seconds ---\n')
				return jsonify(rdata)
			elif cmdb == "expr":
				expr(cndata)
				# print("삭제")
				rdata = {'response': '200', 'cmdb':cmdb, 'xdata':x_data}
				print(f'{linenumber()}p::id:{id} --- (1) Cycle time: {round((time.time() - start_time), 3)} seconds ---\n')
				return jsonify(rdata)
			elif cmdh and cmdb:
				# os.system("sh /root/UBiCauto/sh/kwrun.sh")			# 웹서버 재실행
				cmd = cmdh + "_" + cmdb
				print(cmd)
				r = subprocess.Popen(["/usr/bin/bash", cmd])
				# print(r.stdout)
				# print(r.stderr)
				rdata = {'response': '200', 'cmdb':cmdb}
				print(f'{linenumber()}p::id:{id} --- (1) Cycle time: {round((time.time() - start_time), 3)} seconds ---\n')
				return jsonify(rdata)
		except:
			rdata = {'response': '400'}
			return jsonify(rdata)
	else:
		return render_template('/ubic_reps.html', ob_ckw= ob_ck, all_ckw= all_ck, prr_ckw= prr_ck, wrun_ckw= wrun_ck, pbb_ckw= pbb_ck, pss_ckw= pss_ck, myc_ckw= myc_ck, ext_B= ext_B)

@app.route('/<user_id>/ubic_repsck', methods=['POST'])			# 프로세스 재시작 check
def ubic_repsck(user_id):
	start_time = time.time()                    # 시간 측정 시작
	if check_logined():
		try:
			print(f'ubic_reps (계정: {user_id}, 세션: {session["id"]})')

			if acc_str[session['id']]:
				if session['id'] == "zenka" or acc_str[session['id']] == user_id:
					pass
				else:
					return redirect(url_for("error"))
		except Exception as e:
			print(e)
	else:
		return redirect(url_for('index'))
	
	# os.system("ubicck")
	# with open("/root/UBiCauto/sh/ubicck.sh", 'r') as fr:
	# 	ob_ck = fr.read()
	System_Check = subprocess.run(['/usr/bin/bash', '/usr/bin/ubicck'], stdout=subprocess.PIPE, universal_newlines=True)
	ob_ck = System_Check.stdout

	if "p /" in ob_ck:			# 감시 프로세스 체크
		ob_ck = True
	else:
		ob_ck = False

	System_Check = subprocess.run(['/usr/bin/bash', '/usr/bin/shp'], stdout=subprocess.PIPE, universal_newlines=True)
	all_ckout = System_Check.stdout

	if ("UBiCauto/myc" in all_ckout) and ("UBiCauto/wrun" in all_ckout) and ("UBiCauto/prr" in all_ckout)\
		and ("UBiCauto/pbb" in all_ckout) and ("UBiCauto/pss" in all_ckout):			# 전체 프로세스 체크
		all_ck = True
	else:
		all_ck = False
	if ("UBiCauto/prr" in all_ckout):			# 공통 프로세스 체크
		prr_ck = True
	else:
		prr_ck = False
	if ("UBiCauto/wrun" in all_ckout):			# 웹서버 프로세스 체크
		wrun_ck = True
	else:
		wrun_ck = False
	if ("UBiCauto/pbb" in all_ckout):			# 매수 프로세스 체크
		pbb_ck = True
	else:
		pbb_ck = False
	if ("UBiCauto/pss" in all_ckout):			# 매도 프로세스 체크
		pss_ck = True
	else:
		pss_ck = False
	if ("UBiCauto/myc" in all_ckout):			# 자료생성 프로세스 체크
		myc_ck = True
	else:
		myc_ck = False
	if request.method == "POST":
		# print(f'전송방식: {request.method}', request.form['data'])
		try:
			if request.form['data'] == 'AJAX':
				System_Check = subprocess.run(['/usr/bin/bash', '/usr/bin/ubicck'], stdout=subprocess.PIPE, universal_newlines=True)
				ob_ck = System_Check.stdout

				print("ob_ck", ob_ck)
				if "p /" in ob_ck:			# 감시 프로세스 체크
					ob_ck = True
				else:
					ob_ck = False

				System_Check = subprocess.run(['/usr/bin/bash', '/usr/bin/shp'], stdout=subprocess.PIPE, universal_newlines=True)
				all_ckout = System_Check.stdout

				if ("UBiCauto/myc" in all_ckout) and ("UBiCauto/wrun" in all_ckout) and ("UBiCauto/prr" in all_ckout)\
					and ("UBiCauto/pbb" in all_ckout) and ("UBiCauto/pss" in all_ckout):			# 전체 프로세스 체크
					all_ck = True
				else:
					all_ck = False
				if ("UBiCauto/prr" in all_ckout):			# 공통 프로세스 체크
					prr_ck = True
				else:
					prr_ck = False
				if ("UBiCauto/wrun" in all_ckout):			# 웹서버 프로세스 체크
					wrun_ck = True
				else:
					wrun_ck = False
				if ("UBiCauto/pbb" in all_ckout):			# 매수 프로세스 체크
					pbb_ck = True
				else:
					pbb_ck = False
				if ("UBiCauto/pss" in all_ckout):			# 매도 프로세스 체크
					pss_ck = True
				else:
					pss_ck = False
				if ("UBiCauto/myc" in all_ckout):			# 자료생성 프로세스 체크
					myc_ck = True
				else:
					myc_ck = False
				rdata = {'response': '200', 'ob_ckw': ob_ck, 'all_ckw': all_ck, 'prr_ckw': prr_ck, 'wrun_ckw': wrun_ck, 'pbb_ckw': pbb_ck, 'pss_ckw': pss_ck, 'myc_ckw': myc_ck}
				return jsonify(rdata)
		except:
			rdata = {'response': '400'}
			return jsonify(rdata)
	else:
		rdata = {'response': '400'}
		return jsonify(rdata)

@app.route("/<user_id>", methods=['GET', 'POST'])			# 자산정보 페이지 (메인)
def ubic1(user_id):
	start_time = time.time()
	print(session)
	if check_logined():
		try:			
			print(f'ubic번호 (계정: {user_id}, 세션: {session["id"]})')

			if acc_str[session['id']]:
				if session['id'] == "zenka" or acc_str[session['id']] == user_id:
					pass
				else:
					return redirect(url_for("error"))
		except Exception as e:
			print(e)
	else:
		return redirect(url_for('index'))

	with open(cal_name[user_id][0], 'rb') as fr1:			# mycal
		mycal = pickle.load(fr1)
	with open(cal_name[user_id][2], 'rb') as fr:			# add_num
		add_num = pickle.load(fr)
	with open(cal_name[user_id][3], 'rb') as fr1:			# cal_l
		cal_l = pickle.load(fr1)
	with open(cal_name[user_id][5], 'rb') as fr:			# set_cfg1 (ubic_conf)
		ubic_conf = pickle.load(fr)
	b_money = ubic_conf['b_money']							# b_money 호출
	with open(cal_name[user_id][4], 'rb') as fr:
		t_tp = pickle.load(fr)

	try:
		bl = gb(login_upbit(user_id))[0]                                                        	# 자산정보
		tsum, tbidm, tbidp, summ = myasset(login_upbit(user_id))									# 총 자산, 총매수, 수익율, 보유금액
		sum_tp = round(sum(t_tp), 1)												# 평가손익 계산(손실액으로 계산 - 정확)
		tsumm = round((tsum + sum_tp), 1)					# 현재자산(실시간) = 총자산 - 손실액
		summ = round(summ, 1)
		ysum = mycal.iloc[-1]['T_Asset']; roe = round(((tsum) - (ysum)) / tsum * 100, 3)
		roep = round(((sum_tp / tbidm) * 100), 2)								# 수익률
		# roepp = round((allsum + roep), 2)
		calsum = round((tsum - ysum), 1)
		bl_cnt = len(bl)			# 종목수
		adn_cnt = len(add_num)		# add_num 종목수
		msum = round((mycal['Profit'].sum() + calsum), 1)
		allsum = round((tsum - acc_bal[user_id]), 1)
		roepp = round((allsum + sum_tp), 1)					#실손익
		troe = round(mycal['ROE'].sum(), 2)
		if user_id == "ubic1":
			ex_num = 1
			ret_ct = ex_item(bl, ex_num)
			with open('/root/UBiCauto/data/set_cfg1.pickle', 'rb') as fset:				# 1계정 매도 기준 가져오기
				ubic_conf= pickle.load(fset)
			ask_p = round((ubic_conf['ask_p'] * 100), 2)

		elif user_id == "ubic2":
			ex_num = 2
			ret_ct = ex_item(bl, ex_num)
			with open('/root/UBiCauto/data/set_cfg2.pickle', 'rb') as fset:				# 2계정 매도 기준 가져오기
				ubic_conf= pickle.load(fset)
			ask_p = round((ubic_conf['ask_p'] * 100), 2)

		elif user_id == "ubic3":
			ex_num = 3
			ret_ct = ex_item(bl, ex_num)
			with open('/root/UBiCauto/data/set_cfg3.pickle', 'rb') as fset:				# 3계정 매도 기준 가져오기
				ubic_conf= pickle.load(fset)
			ask_p = round((ubic_conf['ask_p'] * 100), 2)

	except TypeError as ubic1_t:
		print(ubic1_t)
	# print(add_num)
	keyname1 = ['금일 수익', '이달 수익', '(실/평가)손익', '전체 자산', '여유 금액', '매수 금액', '누적 수익']
	keyname2 = ['수익률(일/월)', '매수 비중']
	
	mycalt ={'금일 수익': format(calsum, ","), '이달 수익':format(msum, ","), '누적 수익': format(allsum, ','), '(실/평가)손익': f'{format(roepp, ",")} / {format(sum_tp, ",")}', '수익률(일/월)': f'{roe} / {troe}', '전체 자산': f'{format(tsumm, ",")} / {format(tsum, ",")}', \
		'여유 금액': format(summ, ','), '매수 금액': format(tbidm, ","), '매수 비중': f'{b_money} / {tbidp}', '종목 수량': f'{ask_p}% / {bl_cnt} 종목 / ↷ {adn_cnt}', '매도 횟수': len(cal_l)}
	add_cnt = {'추매 횟수': ret_ct}

	try:
		# print(request.form['data'])
		if request.form['data'] == "AJAX":
			rdata = {'response': '200'}
			ret_ct = list(ret_ct)
			# print(type(ret_ct))
			rdata.update(mycalt)
			rdata['추매 횟수'] = ret_ct[0]
			return jsonify(rdata)
	except Exception as e:
		print(e)

	print(f'{linenumber()}p::id:{id} --- (1) Cycle time: {round((time.time() - start_time), 3)} seconds ---\n')
	return render_template('ubic.html', mycalt_info = mycalt, keyname1 = keyname1, keyname2 = keyname2, add_cnt = add_cnt)

@app.route('/<user_id>/ubic_conf', methods=['GET', 'POST'])			# 설정 페이지
def ubic_config(user_id):
	start_time = time.time()                    # 시간 측정 시작
	if check_logined():
		try:
			print(f'ubic_conf (계정: {user_id}, 세션: {session["id"]})')

			if acc_str[session['id']]:
				if session['id'] == "zenka" or acc_str[session['id']] == user_id:
					pass
				else:
					return redirect(url_for("error"))
		except Exception as e:
			print(e)
	else:
		return redirect(url_for('index'))
	# {'sell_count', 'b_money', 'bp', 'b_count', 'blow_money', 'bg', 'gt', 'code', 'y3h3or', 'tho_30r', 'tho_1r', 'tpor', 'p5g', 'p10g', 'p510g', 'p550g', 'p1050g', 'nw', 
	# 'npct', 'ap', 'agt', 'l_money', 'ask_p', 'ask_ug', 'ask_pp', 'adsp', 'u_p', 'yg', 'ag1', 'ag2', 'ag3', 'ag4', 'ag5', 'ag6', 'ag7', 'ag8', 'ag9', 'ag10', 'adp1', 'adp2',
	# 'adp3', 'adp4', 'adp5', 'adp6', 'adp7', 'adp8', 'adp9', 'adp10', 'abptime'} 참고
	perct_item = ['bg', 'npct', 'ask_p', 'ask_ug', 'ask_pp', 'adsp']
	f_item = ['bp', 'bg', 'gt', 'npct', 'agt', 'ask_p', 'ask_ug', 'ask_pp', 'adsp', 'u_p', 'ag1', 'ag2', 'ag3', 'ag4', 'ag5',\
		'ag6', 'ag7', 'ag8', 'ag9', 'ag10', 'adp1', 'adp2', 'adp3', 'adp4', 'adp5', 'adp6', 'adp7', 'adp8', 'adp9', 'adp10', 'abptime']
	i_item = ['sell_count', 'b_money', 'bp', 'b_count', 'blow_money', 'bg', 'gt', 'code', 'y3h3or', 'tho_30r', 'tho_1r', 'tpor',\
		'p5g', 'p10g', 'p510g', 'p550g', 'p1050g', 'nw', 'npct', 'ap', 'agt', 'l_money', 'ask_p', 'ask_ug', 'ask_pp', 'adsp', 'u_p',\
			'yg', 'ag1', 'ag2', 'ag3', 'ag4', 'ag5', 'ag6', 'ag7', 'ag8', 'ag9', 'ag10', 'adp1', 'adp2', 'adp3', 'adp4', 'adp5', 'adp6',\
				'adp7', 'adp8', 'adp9', 'adp10', 'abptime']
	try:			# ajax
		item = request.form['data']				# 설정항목 가져옴
		value = request.form['value']			# 설정값 가져옴
		set = dict(request.form)
		print(set)
		try:
			if "." in value:
				try:
					value = float(value)
					if (item in f_item):
						if item == "bp":
							if (0 <= value <= 5):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "bg":			# 매수대기(분)
							if (0 <= value <= 1):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "gt":			# 매수대기 (분)
							if (0 <= value <= 720):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "npct":			# 
							if (1 <= value <= 90):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ask_p":			# 매도 시 수익률
							if (0.45 <= value  <= 5):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ask_ug":			#
							if (0 <= value  <= 30):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ask_pp":			#
							if (0 <= value  <= 5):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "agt":			# 매도대기(분)
							if (0 <= value <= 720):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adsp":			# 추매 시작 시점
							if (0 <= value <= 10):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag1":			# () 배 추매(1회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag2":			# () 배 추매(2회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag3":			# () 배 추매(3회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag3":			# () 배 추매(3회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag4":			# () 배 추매(3회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag5":			# () 배 추매(5회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag6":			# () 배 추매(6회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag7":			# () 배 추매(7회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag8":			# () 배 추매(8회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag9":			# () 배 추매(9회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag10":			# () 배 추매(10회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp1":			# ()% 시 추매(1회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp2":			# ()% 시 추매(2회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp3":			# ()% 시 추매(3회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp4":			# ()% 시 추매(4회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp5":			# ()% 시 추매(5회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp6":			# ()% 시 추매(6회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp7":			# ()% 시 추매(7회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp8":			# ()% 시 추매(8회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp9":			# ()% 시 추매(9회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp10":			# ()% 시 추매(10회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "abptime":			# 매수 완료 후
							if (0 <= value  <= 60):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)
					else:
						rdata = {'response': '400', 'text': 'string'}
						return jsonify(rdata)
				except:
					rdata = {'response': '400', 'text': 'string'}
					return jsonify(rdata)
			else:
				try:
					value = int(value)
					if item in i_item:
						if item == "sell_count":
							if (0 == value) or (1 == value) or (2 == value) or (3 == value):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "b_money":
							if (5000 <= value <= 30000):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "bp":
							if (0 <= value <= 5):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "b_count":
							if (0 <= value <= 60):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)
						elif item == "blow_money":
							if (5000 <= value <= 30000):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "bg":			# 매수대기(분)
							if (0 <= value <= 1):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "gt":			# 매수대기 (분)
							if (0 <= value <= 720):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "code":			# 종목 검색 기준
							if (1 == value) or (2 == value):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "y3h3or":			# 
							if (1 <= value <= 120):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)
							
						elif item == "tho_30r":			# 
							if (1 <= value <= 120):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "tho_1r":			# 
							if (1 <= value <= 120):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "tpor":			# 
							if (1 <= value <= 120):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "p5g":			# 
							if (1 <= value <= 120):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "p10g":			# 
							if (1 <= value <= 120):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "p510g":			# 
							if (1 <= value <= 120):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "p550g":			# 
							if (1 <= value <= 120):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "p1050g":			# 
							if (1 <= value <= 120):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "nw":			# 
							if (1 <= value <= 90):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "npct":			# 
							if (1 <= value <= 90):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "yg":			# 
							if (1 <= value <= 90):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ask_p":			# 매도 시 수익률
							if (0.45 <= value  <= 5):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ask_ug":			#
							if (0 <= value  <= 30):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ask_pp":			#
							if (0 <= value  <= 5):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "agt":			# 매도대기(분)
							if (0 <= value <= 720):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adsp":			# 추매 시작 시점
							if (0 <= value <= 10):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ap":			# 추매 횟수 제한
							if (0 <= value <= 10):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "u_p":			# ()% 이하 추매 ≦ N_50ma
							if (0 <= value  <= 10):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "l_money":			# 추매 금액 제한(추매 전 금액)
							if (0 <= value <= 1000000):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag1":			# () 배 추매(1회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag2":			# () 배 추매(2회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag3":			# () 배 추매(3회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag3":			# () 배 추매(3회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag4":			# () 배 추매(3회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag5":			# () 배 추매(5회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag6":			# () 배 추매(6회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag7":			# () 배 추매(7회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag8":			# () 배 추매(8회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag9":			# () 배 추매(9회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "ag10":			# () 배 추매(10회)
							if (0 <= value <= 2):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp1":			# ()% 시 추매(1회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp2":			# ()% 시 추매(2회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp3":			# ()% 시 추매(3회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp4":			# ()% 시 추매(4회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp5":			# ()% 시 추매(5회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp6":			# ()% 시 추매(6회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp7":			# ()% 시 추매(7회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp8":			# ()% 시 추매(8회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp9":			# ()% 시 추매(9회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "adp10":			# ()% 시 추매(10회)
							if (-30 <= value  <= 30):
								value = abs((value))
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)

						elif item == "abptime":			# 매수 완료 후
							if (0 <= value  <= 60):
								pass
							else:
								rdata = {'response': '400', 'text': 'string'}
								return jsonify(rdata)					
						
					else:
						rdata = {'response': '400', 'text': 'string'}
						return jsonify(rdata)
				except:
					rdata = {'response': '400', 'text': 'string'}
					return jsonify(rdata)
		except Exception as e:
			rdata = {'response': '400', 'text': 'string'}
			return jsonify(rdata)
		
		# print(f'항목: {item}, 설정값: {type(value)}')
		try:	
			# print(f'항목: {item}, 설정값: {value}')
			with open(cal_name[user_id][5], 'rb') as fset:
				ubic_conf = pickle.load(fset)
			if item in perct_item:
				con_value = perct(value)
				ubic_conf[item]=con_value		# 설정파일에 '항목:설정값' 변경
			else:
				ubic_conf[item]=value		# 설정파일에 '항목:설정값' 변경
			# print('설정후', ubic_conf)
			with open(cal_name[user_id][5], 'wb') as fset:
				pickle.dump(ubic_conf, fset)

			rdata = {'response': '200'}
			return jsonify(rdata)
		except Exception as e:
			print(e)
			rdata = {'response': '400', 'text': 'save'}
			return jsonify(rdata)
	except Exception as e: # call page
		with open(cal_name[user_id][5], 'rb') as fset:
			ubic_conf = pickle.load(fset)
		# print('변경전', ubic_conf)
		test_dict = {'sell_count': ') (0:sxax, 1:soao, 2:soax, 3:sxao)', 'b_money': ')원 = 초기매수값',\
			'bp': ')% 매수(총자산 기준)', 'b_count': ')개 = 매수종목 갯수', 'blow_money': ')원 = 최저 매수금액', \
			'bg': ')% 시 매수(현재가(cp) 기준)', 'gt': ')분 = 매수대기 취소', 'code': ') 종목 검색 기준', \
			'y3h3or': ')% = B_3D(hp-sp)', 'tho_30r': ')% = N_30m(hp-sp)', 'tho_1r': ')% = N_1m(hp-sp)',\
			'tpor': ')% = N(cp-sp)', 'p5g': ')% = (cp-B5Dma)', 'p10g': ')% = (cp-B10Dma)', 'p510g': ')% = (B5Dma-B10Dma)',\
			'p550g': ')% = (B5Dma-B50Dma)', 'p1050g': ')% = (B10Dma-B50Dma)', 'nw': ')ma ≦ cp 시', 'npct': ')% 이상',\
			'yg': ')ma ≦ ep', 'ask_p': ')% = 매도시 수익율', 'ask_ug': ')% 매도(최저기준 이하 시',\
			'ask_pp': ')% 매도대기(지정가 설정시)', 'agt': ')분 = 매도대기 해제시간', 'adsp': ')% 이하(추매시작 시점: 매수평단)',\
			'ap': ')번 = 추매횟수 제한', 'u_p': ')% 이하 추매(cp ≦ N_50ma)', 'l_money': ')원 = 금액제한(추매 전)',\
			'ag1': ')배 추매(1회)', 'ag2': ')배 추매(2회)', 'ag3': ')배 추매(3회)', 'ag4': ')배 추매(4회)',\
			'ag5': ')배 추매(5회)', 'ag6': ')배 추매(6회)', 'ag7': ')배 추매(7회)', 'ag8': ')배 추매(8회)',\
			'ag9': ')배 추매(9회)', 'ag10': ')배 추매(10회)','adp1': ')% 시 추매(1회)', 'adp2': ')% 시 추매(2회)', 'adp3': ')% 시 추매(3회)',\
			'adp4': ')% 시 추매(4회)', 'adp5': ')% 시 추매(5회)', 'adp6': ')% 시 추매(6회)', 'adp7': ')% 시 추매(7회)', 'adp8': ')% 시 추매(8회)',\
			'adp9': ')% 시 추매(9회)', 'adp10': ')% 시 추매(10회)', 'abptime': ')분 = 매수완료 후'}

		for key, value in ubic_conf.items():
			if key in perct_item:
				con_value = de_perct(value)
				try:
					test_list = [con_value, test_dict[key]]
				except:
					test_list = [con_value, ""]
				ubic_conf[key]=test_list
				# ubic_conf[key]=con_value
			else:
				try:
					test_list = [value, test_dict[key]]
				except:
					test_list = [value, ""]
				ubic_conf[key]=test_list

		# print('변경후', ubic_conf)
		return render_template("/ubic_conf.html", ubic_conf_ = ubic_conf)
	print(f'{linenumber()}p::id:{id} --- (1) Cycle time: {round((time.time() - start_time), 3)} seconds ---\n')

@app.route("/<user_id>/ubic_ear")			# 일별내역 페이지
def ubic_ear(user_id):
	start_time = time.time()                    # 시간 측정 시작
	if check_logined():
		try:
			print(f'ubic_ear (계정: {user_id}, 세션: {session["id"]})')
			if acc_str[session['id']]:
				if session['id'] == "zenka" or acc_str[session['id']] == user_id:
					pass
				else:
					return redirect(url_for("error"))
		except Exception as e:
			print(e)
	else:
		return redirect(url_for('index'))

	with open(cal_name[user_id][0], 'rb') as fr1:
		mycal = pickle.load(fr1)
	now = datetime.now()                                                  # 저장 전 현 날짜
	now1 = datetime(now.year, now.month, now.day) + timedelta(0)
	yday1 = now1 + timedelta(-1) 
	# ydaym = ("%s년%s월 합계" %(yday1.strftime("%y"), yday1.month))
	ydaym = (f'총 합 계')
	tsum = myasset(login_upbit(user_id))[0]
	mycalroe = round((mycal['Profit'].sum() / tsum) * 100, 1)
	mycal.loc[ydaym] = [tsum, mycal['Profit'].sum(), mycalroe, mycal['Ct'].sum()]
	mycal.columns = ['총자산','수익','수익률','매도수']
	mycal.columns.name = '날짜'
	date_list = list(mycal.index.values)			# 데이타프레임 > 인덱스만 리스트로 변환
	c_list = []			# 데이타프레임 > 리스트
	for i in date_list:
		f = {}
		f['날짜'] = i			# 리스트 날짜와 병합
		f.update(mycal.loc[i].to_dict())
		c_list.append(f)
	c_list2 = reversed(c_list)			# 월별내역 리스트 정렬을 역으로 바꿈
	c_list_r = list(c_list2)			# 역으로 바꾼 c_list2를 리스트로 지정해줘야 함

	print(f'{linenumber()}p::id:{id} --- (1) Cycle time: {round((time.time() - start_time), 3)} seconds ---\n')
	# return render_template("/ubic_ear.html", tables=[mycal.to_html(classes='data')], titles=mycal.columns.values)	# mycal
	return render_template("/ubic_ear.html", c_list = c_list, c_list_r = c_list_r)	# mycal

@app.route("/<user_id>/ubic_mear")			# 월별내역 페이지
def ubic_mear(user_id):
	start_time = time.time()                    # 시간 측정 시작
	if check_logined():
		try:
			print(f'ubic_mear (계정: {user_id}, 세션: {session["id"]})')
			# print('ubic_mear (계정: %s, 세션: %s)' %(user_id, session['id']))
			if acc_str[session['id']]:
				if session['id'] == "zenka" or acc_str[session['id']] == user_id:
					pass
				else:
					return redirect(url_for("error"))
		except Exception as e:
			print(e)
	else:
		return redirect(url_for('index'))

	with open(cal_name[user_id][1], 'rb') as fr1:
		mycal = pickle.load(fr1)
	now = datetime.now()                                                    # 저장 전 현 날짜
	now1 = datetime(now.year, now.month, now.day) + timedelta(0)
	yday1 = now1 + timedelta(-1) 
	ydaym = (f'총 합 계')
	tsum = myasset(login_upbit(user_id))[0]
	mycalroe = mycal['Profit'].sum() / tsum * 100
	mycal.loc[ydaym] = [round(tsum, 1), mycal['Profit'].sum(), round(mycalroe, 1), mycal['Ct'].sum()]
	mycal.columns = ['총자산','수익','수익률','매도수']
	mycal.columns.name = '날짜'
	date_list = list(mycal.index.values)			# 데이타프레임 > 인덱스만 리스트로 변환
	c_list = []			# 데이타프레임 > 리스트
	for i in date_list:
		f = {}
		f['날짜'] = i			# 리스트 날짜와 병합
		f.update(mycal.loc[i].to_dict())
		c_list.append(f)
	c_list2 = reversed(c_list)			# 월별내역 리스트 정렬을 역으로 바꿈
	c_list_r = list(c_list2)			# 역으로 바꾼 c_list2를 리스트로 지정해줘야 함
	print(f'{linenumber()}p::id:{id} --- (1) Cycle time: {round((time.time() - start_time), 3)} seconds ---\n')
	return render_template("/ubic_mear.html", c_list = c_list, c_list_r = c_list_r)	# mycal

@app.route("/<user_id>/ubic_bal", methods=['GET', 'POST'])			# 종목화면 페이지
def ubic_bal(user_id):
	start_time = time.time()
	if check_logined():
		try:
			print(f'ubic_bal (계정: {user_id}, 세션: {session["id"]})')
			# print('ubic_bal (계정: %s, 세션: %s)' %(user_id, session['id']))
			if acc_str[session['id']]:
				if session['id'] == "zenka" or acc_str[session['id']] == user_id:
					pass
				else:
					return redirect(url_for("error"))
		except Exception as e:
			print(e)
	else:
		return redirect(url_for('index'))
	# print(f'ubic_bal (계정: {user_id}, 세션: {session["id"]})')
	try:
		with open('/root/UBiCauto/data/cp.pickle', 'rb') as fr1:            # mycal 불러오기
			cu_p = pickle.load(fr1)
	except Exception as e:
		print(e)
	with open(cal_name[user_id][2], 'rb') as fr:			# add_num 호출
		add_num = pickle.load(fr)
	with open(cal_name[user_id][6], 'rb') as fset:			# ext_item 제외항목 호출
		ext_item = pickle.load(fset)

	ext_b = ext_item['ext_b']
	ext_s = ext_item['ext_s']
	ext_a = ext_item['ext_a']
	# print(ext_a, ext_s)
	name, avg, tb = gb(login_upbit(user_id))
	my1 = []
	for e, key in avg.items():
		my2 = {}
		tb1 = tb[e]
		t_money = round(tb1 * key)
		if e in cu_p:
			price = cu_p[e]
			tp = round((((price - key) / key) * 100), 2)
			profit = round(t_money * tp /100)

			if e in ext_a:
				my2['chk_a'] = 'on'
			else:
				my2['chk_a'] = 'off'
			if e in ext_b:
				my2['chk_b'] = 'on'
			else:
				my2['chk_b'] = 'off'
			if e in ext_s:
				my2['chk_s'] = 'on'
			else:
				my2['chk_s'] = 'off'
		try:
			my2['Coin(종목)'] = e; my2['수익률(%)'] = tp; my2['평가손익(원)'] = format(profit,",")
			my2['add_num'] = add_num[e][0]; my2['매수금액(원)'] = format(t_money, ",")
			my1.append(my2)		
		except Exception as e:
			print(e)
	my1 = sorted(my1, key = lambda x : (-x['수익률(%)']))	# 리스트 내 다중 딕셔너리 특정key값으로 오름차순 정렬

	BTC_per = ticker_per2(cu_p, "KRW-BTC")					# BTC 전날대비 수익률 호출
	try:
		if request.form['data'] == "AJAX":
			rdata = {'response': '200', 'BTC': BTC_per, 'rtable':render_template("/ubic_bal_table.html", my1 = my1, BP=BTC_per)}
			return jsonify(rdata)
	except Exception as e:
		print(e)

	print(f'{linenumber()}p::id:{id} --- (1) Cycle time: {round((time.time() - start_time), 3)} seconds ---\n')
	return render_template("/ubic_bal.html", my1 = my1, BP=BTC_per)	

@app.route("/<user_id>/ubic_deal", methods=['POST'])		# ubic_bal 웹페이지에서 매수, 매도하는 함수
def ubic_deal(user_id):
	start_time = time.time()                    # 시간 측정 시작
	if check_logined():
		try:
			print(f'ubic_deal (계정: {user_id}, 세션: {session["id"]})')

			if acc_str[session['id']]:
				if session['id'] == "zenka" or acc_str[session['id']] == user_id:
					pass
				else:
					return redirect(url_for("error"))
		except Exception as e:
			print(e)
	else:
		return redirect(url_for('index'))

	e = request.form['data']			# coin_name 받음
	print(e)
	deal_cont = request.form['deal']			# 'b'매수 or 's'매도 인지 확인(deal_cont)
	print(deal_cont)
	if deal_cont == "b":
		try:
			nb_money = int(request.form['money'])			# 매수금액 정수로 받음
			print(nb_money)
			cp = one_buy(login_upbit(user_id), e, nb_money)			# 현재가 매수주문 후 현재가 리턴
			# print('매수완료')
			rdata = {'response': '200', 'cp':format(cp, ','), 'nb_money': format(nb_money, ',')}
			return jsonify(rdata)
		except:
			rdata = {'response': '400'}
			return jsonify(rdata)
	elif deal_cont == "s":
		try:
			one_sell2(login_upbit(user_id), e)			# 매수 ((1))호가에 매도주문
			print('매도완료')
			rdata = {'response': '200'}
			return jsonify(rdata)
		except:
			rdata = {'response': '400'}
			return jsonify(rdata)
	else:
		rdata = {'response': '400'}
		return jsonify(rdata)
	print(f'{linenumber()}p::id:{id} --- (1) Cycle time: {round((time.time() - start_time), 3)} seconds ---\n')

@app.route('/<user_id>/ubic_readd', methods=['POST'])			# 추횟수 수정
def ubic_readd(user_id):
	start_time = time.time()                    # 시간 측정 시작
	if check_logined():
		try:
			print(f'ubic_deal (계정: {user_id}, 세션: {session["id"]})')

			if acc_str[session['id']]:
				if session['id'] == "zenka" or acc_str[session['id']] == user_id:
					pass
				else:
					return redirect(url_for("error"))
		except Exception as e:
			print(e)

	adn_value = int(request.form['data'])			# 추매횟수 int 로 변경
	e = request.form['coin_name']
	# print(adn_value, e)
	try:
		if (adn_value != None) and e:		# 추매횟수가 Null값이 아니고 종목명이 있을때 정상실행
			print(e, adn_value)
			# print(type(e), type(adn_value))
			with open(cal_name[user_id][2], 'rb') as fr:    # add_num 호출
				add_num = pickle.load(fr)
			add_num[e][0]=adn_value
			with open(cal_name[user_id][2], 'wb') as fw:
				pickle.dump(add_num, fw)
			# print(add_num)
			rdata = {'response': '200'}
			return jsonify(rdata)
	except Exception as e:
		print(e)
		rdata = {'response': '400'}
		return jsonify(rdata)
	print(f'{linenumber()}p::id:{id} --- (1) Cycle time: {round((time.time() - start_time), 3)} seconds ---\n')
	return ""

@app.route("/<user_id>/ubic_hty")			# 체결내역 페이지
def ubic_hty(user_id):
	start_time = time.time()                    # 시간 측정 시작
	if check_logined():
		try:
			print(f'ubic_ear (계정: {user_id}, 세션: {session["id"]})')
			if acc_str[session['id']]:
				if session['id'] == "zenka" or acc_str[session['id']] == user_id:
					pass
				else:
					return redirect(url_for("error"))
		except Exception as e:
			print(e)
	else:
		return redirect(url_for('index'))

	trs_hty_l = []
	get_hty = get_orderi2("/root/UBiCauto/Acct/upbit%s.txt" %(acc_name[user_id]))[:80]
	for i in get_hty:
		trs_hty = {}
		trs_hty['created_at'] = t_c2(i['created_at'])
		trs_hty['coin_name'] = i['market']          # 코인명
		trs_hty['side'] = i['side']         # 거래종류
		# trs_hty['price'] = '{:,}'.format(float(i['price']))           # 거래단가
		# trs_hty['price'] = i['price']           # 거래단가
		price = i.get('price')
		if price:
			if '.' in price:
				trs_hty['price'] = float(price)           # 거래단가
			else:
				trs_hty['price'] = '{:,}'.format(int(price))           # 거래단가
		else:
			continue
		# trs_hty['created_at'] = i['created_at']         # 체결시간
		# trs_hty['volume'] = i['volume']         # 입력한 주문양
		# trs_hty['remaining_volume'] = i['remaining_volume']         # 체결 후 남은 주문양
		# trs_hty['paid_fee'] = i['paid_fee']         # 사용된 수수료
		# trs_hty['executed_volume'] = i['executed_volume']           # 체결된 양
		if trs_hty['side'] == 'bid':
			trs_hty['tr_money'] = int(float(i['executed_volume']) * float(price))         # 매수 정산금액
		else:
			trs_hty['tr_money'] = int(float(i['executed_volume']) * float(price) - float(i['paid_fee']))         # 매도 정산금액
		trs_hty_l.append(trs_hty)
	
	print(f'{linenumber()}p::id:{id} --- (1) Cycle time: {round((time.time() - start_time), 3)} seconds ---\n')
	# return render_template("/ubic_ear.html", tables=[mycal.to_html(classes='data')], titles=mycal.columns.values)	# mycal
	return render_template("/ubic_thty.html", thty = trs_hty_l)	# mycal

@app.route("/<user_id>/ubic_chk", methods=['POST'])				# 매도, 추매 상태 체크 및 유지
def ubic_chk(user_id):
	start_time = time.time()                    # 시간 측정 시작
	if check_logined():
		try:
			print(f'ubic_mear (계정: {user_id}, 세션: {session["id"]})')
			# print('ubic_mear (계정: %s, 세션: %s)' %(user_id, session['id']))
			if acc_str[session['id']]:
				if session['id'] == "zenka" or acc_str[session['id']] == user_id:
					pass
				else:
					return redirect(url_for("error"))
		except Exception as e:
			print(e)
	else:
		return redirect(url_for('index'))

	with open(cal_name[user_id][6], 'rb') as feit:
		ext_item = pickle.load(feit)
	ext_a = ext_item['ext_a']
	ext_b = ext_item['ext_b']
	ext_s = ext_item['ext_s']

	coin_name = request.form['coin_name']
	ext_chk = request.form['ext_chk']
	onoff = request.form['onoff']
	print(f'(coin_name): {coin_name}\n(ext_chk): {ext_chk}\n(onoff): {onoff}')

	if coin_name :
		if ext_chk == 'ext_add':
			if onoff == 'true':
				ext_a.append(coin_name)
				set_item = set(ext_a)
				ext_a = list(set_item)
				print(f'on: ext_a: {ext_a}')
			else:
				ext_a.remove(coin_name)
				print(f'off: ext_a: {ext_a}')
		if ext_chk == 'ext_buy':
			if onoff == 'true':
				ext_b.append(coin_name)
				set_item = set(ext_b)
				ext_b = list(set_item)
				print(f'on: ext_b: {ext_b}')
			else:
				ext_b.remove(coin_name)
				print(f'off: ext_b: {ext_b}')
		if ext_chk == 'ext_sell':
			if onoff == 'true':
				ext_s.append(coin_name)
				set_item = set(ext_s)
				ext_s = list(set_item)
				print(f'on: ext_s: {ext_s}')
			else:
				ext_s.remove(coin_name)
				print(f'off: ext_s: {ext_s}')


	with open(cal_name[user_id][6], 'wb') as feit:
		pickle.dump(ext_item, feit)
	try:
		rdata = {'response': '200'}
		return jsonify(rdata)
	except Exception as e:
		print(e)
		rdata = {'response': '400'}
		return jsonify(rdata)
	print(f'{linenumber()}p::id:{id} --- (1) Cycle time: {round((time.time() - start_time), 3)} seconds ---\n')
	return render_template("/ubic_bal.html", my1 = my1, BP=BTC_per)	

@app.route("/<user_id>/<symbol>", methods=['GET'])				# 종목별 차트 출력 페이지
def ubic_chart(user_id, symbol):
	return render_template("/ubic_chart.html", symbol = symbol)



if __name__ == '__main__':   
	ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
	ssl_context.load_cert_chain(certfile='/etc/letsencrypt/live/zenky.duckdns.org/fullchain.pem', keyfile='/etc/letsencrypt/live/zenky.duckdns.org/privkey.pem')
	app.run(host="192.168.0.24", port=5000, ssl_context=ssl_context, threaded=True) # , debug=True)

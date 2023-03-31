# -*- coding:utf-8 -*-

import pyupbit
import time
from datetime import datetime
import os
import pickle
from datetime import datetime, timedelta
import threading
# from UBiC_Search_def import buy_avr_price_5, buy_avr_price_10, buy_avr_price_20, buy_avr_price_30, buy_avr_price_40, \
#     buy_avr_price_50, buy_avr_price_60, buy_avr_price_70, buy_avr_price_80, buy_avr_price_90, ma5_under, s1_bull_m1, \
#     b2_decline_m1, get_orderi, abp_check, get_tick_s, t_c, ex_item, perct, adn_insert, myasset, askper, add_rw0, \
#     add_rw1, add_rw2, add_rw3, add_rw4, add_rw5, add_rw6, add_rw7, add_rw8, add_rw9, add_rw10, add_rwav5, add_rwav10,\
#     add_rwav20, add_rwav30, add_rwav40, add_rwav50, add_rwav60, add_rwav70, add_rwav80, add_rwav90, add_rwinit, add_get,\
#     linenumber, ext_save, get_orderi2
# from UBiC_Rotate_data import gb

user = 3            # 사용자 선택 (1, 2, 3)

''' bsl 에러로 정상 실행 안될 시 ( f_bid0 ) '''
# 설정할  계정 번호 수정 'upbit(계정번호).txt  : p.21, p.73 / add_num 용량이 0이거나 깨졌을 경우 정상 add_num 복사 후 실행

f = open("/root/UBiCauto/Acct/upbit%s.txt" %(user))        # 파일 열기 (불러올 계정 입력)
lines = f.readlines()                       # 라인을 일러들임
access = lines[0].strip()                   # access key '\n' 0번 행 불러오기
secret = lines[1].strip()                   # secret key '\n' 1번 행 불러오기
f.close()                                   # 파일 닫기

upbit = pyupbit.Upbit(access, secret)       # 업비트 로그인
balance = upbit.get_balances()              # 로그인 후 자산내역 불러오기
# ------------------------------------------------------------------------- #

print(f'자산내역: {balance}')
print(f'자산내 총수량: {len(balance)}')

''' 자산에서 종목명만 추출 '''
def gb(upbit):
    bal = []                                        # 보유종목명
    bf_bal = {}                                     # 보유종목과 보유금액
    avg_p = {}                                      # 종목과 평균매수가 dict
    t_bal = {}                                      # 종목과 보유수량                                 
    balance = upbit.get_balances()                 # 자산정보: dict
    for i in balance:                               # 자산('balance') 리스트를 하나씩 'i'로 가져 옴
        if 'KRW' not in i['currency']:              # 영문 종목명에 'KRW-종목명' 형태로 재 저장
            u = i['unit_currency']                  # 'KRW'
            t = i['currency']                       # '영문 종목명'
            # tl = i['locked']                        # locked 된 수량
            tb = float(i['balance']) + float(i['locked'])                      # 종목 보유수량 str 으로 float 로 변경 필요
            avg_buy_price = float(i['avg_buy_price'])      # 매수 평균 추출 str 이라 float 로 변경 필요
            if avg_buy_price != 0:                      # 매수평균이 0이 아닌 종목만 추출
                e = u + '-' + t                         # 'KRW'-'영문 종목명'
                t_money = tb * avg_buy_price            # 종목 보유금액
                bf_bal[e] = t_money                     # 종목과 보유금액을 딕셔너리에 추가
                # bal.append(e)                           # (( 보유 종목명 ))만 bal 리스트에 추가
                avg_p[e] = [0, 0, avg_buy_price]                # 종목과 평단 'avg_price'에 추가
                t_bal[e] = tb                           # 종목과 보유수량 'tb'에 추가 

    # df_bal에 추가 된 종목별 보유금액을 재정렬(적은금액순으로)
    af_bal = sorted(bf_bal.items(), key=lambda x: x[1], reverse=False)  # list(tuple) [('종목', 실수값),...] 로 바인딩 
    """ 매수금액이 적은 종목부터 종목명 재정렬 """
    for j in af_bal:                                # 반복문으로 종목명만 저장
        bal.append(j[0])
    return bal, avg_p, t_bal                        # 종목명(gb(upbit)[0]), 평단(gb(upbit)[1]), 수량(gb(upbit)[2])
# ------------------------------------------------------------------------------------------------------------------- #
    
bal_name = gb(upbit)[0]     # 종목명을 'bal_name'에 저장
print(f'보유종목:수량({len(bal_name)}):{bal_name}')   # 종목명 확인

## add_num = {'KRW-APT': [2, 90, 8806.2], 'KRW-T': [2, 0, 8675.01], 'KRW-BTC': [0, 0, 9463.97], 'KRW-LINK': [0, 0, 10646.96], 'KRW-MANA': [1, 0, 8012.01], 'KRW-XLM': [0, 0, 8806.2]}

# with open('/root/UBiCauto/data/add_num3.pickle', 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
#     pickle.dump(add_num, fw)
# 계정번호 수정 'add_num(계정번호)'

with open('/root/UBiCauto/data/add_num%s.pickle' %(user), 'rb') as fr:    # add_num 호출
    add_num = pickle.load(fr)

''' add_num에서 종목명 추출 '''

key_name =[]
for key in add_num:
    key_name.append(key)
print(f'add_num종목:수량{len(key_name)}, {key_name}')      # add_num 종목 확인

# -------------------------- #

''' add_num 항목에 없는 자산명 확인(집합으로 확인) '''

bal_apd = list(set(bal_name) - set(key_name))       # 차집합
print(f'add_num에서 빠진 종목:수량{len(bal_apd)}, {bal_apd}')        # 차집합 출력
# ----------------------------------------------- #
''' add_num에 없는 종목 확인 > 변환 > 추가 '''

if 0 < len(bal_apd):
    for key in bal_apd:
        add_num[key]=[0, 0, 0]
# ----------------------------------------------- #
with open('/root/UBiCauto/data/add_num%s.pickle' %(user), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
    pickle.dump(add_num, fw)

print(f'add_num: {add_num}')
print(f'add_num수량:{len(add_num)}')
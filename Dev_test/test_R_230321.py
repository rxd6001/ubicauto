# -*- coding:utf-8 -*-

import pyupbit
import pickle
import time
from datetime import datetime
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import os

# sched = BlockingScheduler()               # 단일 함수 스케줄 실행 시 사용
sched = BackgroundScheduler()               # 여러 함수 스케줄 실행 시 사용

# """ ================ my 로그인 ================ """
# f = open("/root/UBiCauto/Acct/upbit_zenky.txt")        # 파일 열기
# lines = f.readlines()                       # 라인을 일러들임
# access = lines[0].strip()                   # access key '\n' 0번 행 불러오기
# secret = lines[1].strip()                   # secret key '\n' 1번 행 불러오기
# f.close()                                   # 파일 닫기

# upbit1 = pyupbit.Upbit(access, secret)      # 업비트 로그인

# """ ================ 로그인 ================ """
# f = open("/root/UBiCauto/Acct/upbit_buty.txt")        # 파일 열기
# lines = f.readlines()                       # 라인을 일러들임
# access = lines[0].strip()                   # access key '\n' 0번 행 불러오기
# secret = lines[1].strip()                   # secret key '\n' 1번 행 불러오기
# f.close()                                   # 파일 닫기

# upbit2 = pyupbit.Upbit(access, secret)      # 업비트 로그인

# """ ================ 로그인 ================ """
# f = open("/root/UBiCauto/Acct/upbit_liebe.txt")        # 파일 열기
# lines = f.readlines()                       # 라인을 일러들임
# access = lines[0].strip()                   # access key '\n' 0번 행 불러오기
# secret = lines[1].strip()                   # secret key '\n' 1번 행 불러오기
# f.close()                                   # 파일 닫기

# upbit3 = pyupbit.Upbit(access, secret)      # 업비트 로그인


""" 프로그램 실행 (하루 한 번 실행 필요) """

# 매일 1분 간격으로 원화마켓 종목 가져 옴
@sched.scheduled_job('cron', minute='*/1', id='rotate5')
def krw_markets():
    # krw_markets1 = pyupbit.get_tickers(fiat="KRW")        # 원화마켓 전체종목 호출
    url = "https://api.upbit.com/v1/market/all"

    querystring = {"isDetails":"true"}
    response = requests.request("GET", url, params=querystring)
    contents = response.json()                              # 호출한 전체 마켓종목에을 리스트로 변환

    if isinstance(contents, list):                          # contents 가 리스트일 경우 ** 유의종목 ** 제외한 원화마켓 종목만 호출 
        krw_markets1 = [x['market'] for x in contents if x['market_warning'] not in 'CAUTION' and x['market'].startswith('KRW')]

    with open('/root/UBiCauto/data/krw_markets.pickle', 'wb') as fw:        # 원화마켓 종목의 데이터를 파일로 저장
        pickle.dump(krw_markets1, fw)          


def km2():
    with open('/root/UBiCauto/data/krw_markets.pickle', 'rb') as fr2:       # 파일로 불러 옴
        km1 = pickle.load(fr2)
    return km1


km = km2()                  # 원화마켓 전 종목 변수로 저장


# 매시간 당 4번 일봉 정보 가져 옴
@sched.scheduled_job('cron', minute='00, 06, 16, 36, 56', second='18', id='rotate25')
def gdf_day():                                                              # krw_markets : 원화마켓, ticker : 종목
    for ticker in km:                                                       # 원화마켓에서 종목을 하나씪 가져옴
        dfd = pyupbit.get_ohlcv(ticker, interval="day", count=100)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
        with open('/root/UBiCauto/data/ohlcvd/%s_df_day.pickle' %(ticker), 'wb') as fw2:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
            pickle.dump(dfd, fw2)
            time.sleep(0.2)
        while True:
            fs = os.path.getsize('/root/UBiCauto/data/ohlcvd/%s_df_day.pickle' %(ticker))
            if fs < 1024 :
                dfd = pyupbit.get_ohlcv(ticker, interval="day", count=100)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
                with open('/root/UBiCauto/data/ohlcvd/%s_df_day.pickle' %(ticker), 'wb') as fw2:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
                    pickle.dump(dfd, fw2)
            else:
                break


def dy(ticker):
    try:
        with open('/root/UBiCauto/data/ohlcvd/%s_df_day.pickle' %(ticker), 'rb') as fr2:                     # df_day 파일로 불러 옴
            df_day = pickle.load(fr2)
        return df_day
    except EOFError as df:
        print('e-time:', datetime.now())
        print('Rot_df:', df)


# dy_%s = dy(%(ticker))                                       # 일봉 1일 1회 호출 위해 변수로 저장(1회 호출 후 안 변함)


# (( 30분봉 정보 갱신 )) 업비트에서 가져와서 파일로 저장 (30분 갱신)
@sched.scheduled_job('cron', minute='01, 31', second='10', id='rotate1')
def gdf_min30():
    for ticker in km:                                                       # 원화마켓에서 종목을 하나씪 가져옴
        dfm30 = pyupbit.get_ohlcv(ticker, interval="minute30", count=50)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
        with open('/root/UBiCauto/data/ohlcvm30/%s_df_min30.pickle' %(ticker), 'wb') as fw3:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
            pickle.dump(dfm30, fw3)
            time.sleep(0.2)
        while True:
            fs = os.path.getsize('/root/UBiCauto/data/ohlcvm30/%s_df_min30.pickle' %(ticker))
            if fs < 1024 :
                dfm30 = pyupbit.get_ohlcv(ticker, interval="minute30", count=50)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
                with open('/root/UBiCauto/data/ohlcvm30/%s_df_min30.pickle' %(ticker), 'wb') as fw3:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
                    pickle.dump(dfm30, fw3)
            else:
                break


def dm30(ticker):
    try:
        with open('/root/UBiCauto/data/ohlcvm30/%s_df_min30.pickle' %(ticker), 'rb') as fr3:    # 30분봉 파일로 불러 옴
            df_min30 = pickle.load(fr3)
        return df_min30
    except EOFError as df1:
        print('e-time:', datetime.now())
        print('Rot_df1:', df1)


# (( 10분봉 정보 갱신 )) 업비트에서 가져와서 파일로 저장 (10분 갱신)
@sched.scheduled_job('cron', minute='00, 10, 20, 30, 40, 50', second='30', id='rotate4')
def gdf_min10():
    for ticker in km:                                                       # 원화마켓에서 종목을 하나씪 가져옴
        dfm10 = pyupbit.get_ohlcv(ticker, interval="minute10", count=55)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
        with open('/root/UBiCauto/data/ohlcvm10/%s_df_min10.pickle' %(ticker), 'wb') as fw10:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
            pickle.dump(dfm10, fw10)
            time.sleep(0.2)
        while True:
            fs = os.path.getsize('/root/UBiCauto/data/ohlcvm10/%s_df_min10.pickle' %(ticker))
            if fs < 1024 :
                dfm10 = pyupbit.get_ohlcv(ticker, interval="minute10", count=55)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
                with open('/root/UBiCauto/data/ohlcvm10/%s_df_min10.pickle' %(ticker), 'wb') as fw10:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
                    pickle.dump(dfm10, fw10)
            else:
                break


def dm10(ticker):
    try:
        with open('/root/UBiCauto/data/ohlcvm10/%s_df_min10.pickle' %(ticker), 'rb') as fr10:    # 30분봉 파일로 불러 옴
            df_min10 = pickle.load(fr10)
        return df_min10
    except EOFError as df10:
        print('e-time:', datetime.now())
        print('Rot_df10:', df10)


# (( 3 분봉 정보 갱신 )) 업비트에서 가져와서 파일로 저장 ( 3분 갱신)
@sched.scheduled_job('cron', minute='00, 03, 06, 09, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, \
    42, 45, 48, 51, 54, 57', second='03', id='rotate2')
def gdf_min3():
    for ticker in km:                                                       # 원화마켓에서 종목을 하나씪 가져옴
        dfm3 = pyupbit.get_ohlcv(ticker, interval="minute3", count=51)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
        with open('/root/UBiCauto/data/ohlcvm3/%s_df_min3.pickle' %(ticker), 'wb') as fw4:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
            pickle.dump(dfm3, fw4)
            time.sleep(0.1)
        while True:
            fs = os.path.getsize('/root/UBiCauto/data/ohlcvm3/%s_df_min3.pickle' %(ticker))
            if fs < 1024 :
                dfm3 = pyupbit.get_ohlcv(ticker, interval="minute3", count=50)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
                with open('/root/UBiCauto/data/ohlcvm3/%s_df_min3.pickle' %(ticker), 'wb') as fw4:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
                    pickle.dump(dfm3, fw4)
            else:
                break


def dm3(ticker):
    try:
        with open('/root/UBiCauto/data/ohlcvm3/%s_df_min3.pickle' %(ticker), 'rb') as fr4:      # 3분봉 파일로 불러 옴
            df_min3 = pickle.load(fr4)
        return df_min3
    except EOFError as df2:
        print('e-time:', datetime.now())
        print('Rot_df2:', df2)


# (( 1분봉 정보 갱신 )) 업비트에서 가져와서 파일로 저장 (1분 갱신)
@sched.scheduled_job('cron', minute='00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, \
    31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59', second='05', id='rotate3')
# @sched.scheduled_job('interval', minutes = 1, id='rotate3')
def gdf_min1():
    # # start = time.time()
    for ticker in km:                                                       # 원화마켓에서 종목을 하나씪 가져옴
        dfm1 = pyupbit.get_ohlcv(ticker, interval="minute1", count=51)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
        with open('/root/UBiCauto/data/ohlcvm1/%s_df_min1.pickle' %(ticker), 'wb') as fw5:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
            pickle.dump(dfm1, fw5)
            time.sleep(0.1)
        while True:
            fs = os.path.getsize('/root/UBiCauto/data/ohlcvm1/%s_df_min1.pickle' %(ticker))
            if fs < 1024 :
                dfm1 = pyupbit.get_ohlcv(ticker, interval="minute1", count=50)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
                with open('/root/UBiCauto/data/ohlcvm1/%s_df_min1.pickle' %(ticker), 'wb') as fw5:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
                    pickle.dump(dfm1, fw5)
            else:
                break   
    # # print("--- %s seconds ---" % round((time.time() - start), 2))  

def dm1(ticker):
    with open('/root/UBiCauto/data/ohlcvm1/%s_df_min1.pickle' %(ticker), 'rb') as fr5:      # 1분봉 파일로 불러 옴
        df_min1 = pickle.load(fr5)
    try:
        if df_min1 is not None:
            return df_min1
        else:
            pass
    except EOFError as dm1:
        print('e-time:', datetime.now())
        print('Rot_dm1:', dm1)


# (( 보유자산정보, 종목정보 갱신 )) 업비트에서 가져와서 ((파일로 저장)) (3.5초 주기: 3.5초 이하는 'skip error' 발생
# @sched.scheduled_job('interval', seconds=2.6, id='rotate2')
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
                avg_p[e] = avg_buy_price                # 종목과 평단 'avg_price'에 추가
                t_bal[e] = tb                           # 종목과 보유수량 'tb'에 추가 

    # df_bal에 추가 된 종목별 보유금액을 재정렬(적은금액순으로)
    af_bal = sorted(bf_bal.items(), key=lambda x: x[1], reverse=False)  # list(tuple) [('종목', 실수값),...] 로 바인딩 
    """ 매수금액이 적은 종목부터 종목명 재정렬 """
    for j in af_bal:                                # 반복문으로 종목명만 저장
        bal.append(j[0])
    return bal, avg_p, t_bal                        # 종목명(gb(upbit)[0]), 평단(gb(upbit)[1]), 수량(gb(upbit)[2])


""" ===== 모든 종목 현재가 가져오기 1 (Buy 종목 검색 시 사용) ===== """
# # 원화종목을 나눠서 가져올 경우
# def cp1():                                          # 원화종목이 100개 이상으로 나눠서 호출 후 합침
#     try:
#         cp1 = pyupbit.get_current_price(km[:100])       # 종목별 현재가를 호출(최대 100개)
#         cp2 = pyupbit.get_current_price(km[100:])       # 100 이후 종목별 현재가 호출
#         cp1.update(cp2)                                 # cp1 + cp2
#         return cp1
#     except TypeError as Rot_cp1:
#         print('Rot_cp1:', Rot_cp1)

# 원화종목을 한번에 모든종목 가져올 경우
@sched.scheduled_job('cron', second='*/1', id='rotatecp1', max_instances=6)
def cp4():                                          # 원화종목이 100개 이상으로 나눠서 호출 후 합침
    try:
        cp1 = pyupbit.get_current_price(km)       # 종목별 현재가를 호출(모든종목)
        # cp2 = pyupbit.get_current_price(km[100:])       # 100 이후 종목별 현재가 호출
        # cp1.update(cp2)                                 # cp1 + cp2 딕셔너리를 합침
        with open('/root/UBiCauto/data/cp.pickle', 'wb') as fw3:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
            pickle.dump(cp1, fw3)
    except TypeError as Rot_cp:
        print('Rot_cpw:', Rot_cp)


""" ===== 모든 종목 현재가 가져오기 2 (Buy 신규매수 시 사용) ===== """
# def cp2():
#     try:
#         cp1 = pyupbit.get_current_price(km[:100])
#         cp2 = pyupbit.get_current_price(km[100:])
#         cp1.update(cp2)
#         return cp1
#     except TypeError as Rot_cp2:
#         print('Rot_cp2:', Rot_cp2)


""" ===== 모든 종목 현재가 가져오기 3 (Sell 매도 시 사용) ===== """
# def cp3():
#     try:
#         cp1 = pyupbit.get_current_price(km[:100])
#         cp2 = pyupbit.get_current_price(km[100:])
#         cp1.update(cp2)
#         return cp1
#     except TypeError as Rot_cp3:
#         print('Rot_cp3:', Rot_cp3)


""" 시작 """
if __name__ == '__main__':              # 자체 실행 시 실행될 메써드...
    print('오늘도 화이팅 시작~')
    sched.start()                       # 스케줄 실행 (다중 쓰레드...?)

    while True:                         # 1초에 한 번씩 자체 실행
        time.sleep(1)

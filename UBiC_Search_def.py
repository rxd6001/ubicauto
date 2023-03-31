# -*- coding:utf-8 -*-

"""
# 모든 코인 최저매매 금액 1,000원 이상 #
# 스텔라루멘, 이더리움, 비트코인, 에이다, 이오스,
스테이터스네트워크토큰, 비트코인캐시, 넴 5,000원 이상
"""
import pyupbit
from UBiC_Rotate_data import dm1, dm3, dm10, dm30, dy
from datetime import datetime, timedelta
from collections import Counter                             # 리스트 중복된 값 갯수 체크
import jwt
import uuid
import hashlib
import math
from decimal import Decimal
from urllib.parse import urlencode, unquote
import requests
import time
import pickle
import os
from inspect import currentframe



""" ((정렬 조건)) G (시가 - 고가 차 (24시간 내) 30m) 매수 조건검색 """

# NoneType error 발생 구간
def rain_market_bho(ticker):                                                        # 1일 고가 - 시가 차 gap, 30m 계산
    try:
        h_max = dm30(ticker)['high'].max()                                          # 종목의 30분봉 최고가 호출
        open0 = dy(ticker).iloc[-1]['open']                                         # 종목 시가
        gap = h_max - open0                                                         # 최고가 - 시가
        gap_r = gap / open0 * 100                                                   # 고가 - 시가 차 시가기준 값 %
        return gap_r                                                                # gap_r 리턴
    except Exception as bho:
        print('def_bho:', bho)


""" ((정렬 조건)) G (시가 - 고가 차 (60분 내) 1m) 매수 조건검색 """

# NoneType error 발생 구간
def rain_market_1ho(ticker):            # 60m 고가 - 시가 차 gap, 1m 계산(2분호출)
    # try:
    mx_1mh = dm1(ticker)['high'].max()                                          # 종목의 1분봉 최고가 호출
    open0 = dy(ticker).iloc[-1]['open']                                         # 종목 시가
    gap = mx_1mh - open0                                                        # 최고가 - 시가
    gap_r = gap / open0 * 100                                                   # 고가 - 시가 차 시가기준 값 %
    return gap_r                                                                # gap_r 리턴
    # except Exception as ho1:
    #     print(f'Error::\nsearch_def::rain_market_1ho:{linenumber()}p::{ho1}\n')


""" Test ~ ((매수 조건)) G (5이 - 10이 위치 (1m)) 매수 조건검색  """

# test 중....1 이평, 상승 시 매수 (1. 매수시점 변경 전)
def r1_m510(ticker, price):         # 미사용 중                                                   # (5이 < 10이) 3분봉 매수시점 조건
    try:
        # open1 = dm1(ticker).iloc[-1]['open']                                        # 현재 1분봉 시가
        close2 = dm1(ticker).iloc[-2]['close']                                      # 2분전 종가
        # open2 = dm1(ticker).iloc[-2]['open']                                        # 2분전 시가
        # close3 = dm1(ticker).iloc[-3]['close']                                      # 3분전 종가
        # open3 = dm1(ticker).iloc[-3]['open']                                        # 3분전 시가

        # last_ma5 = dm1(ticker)['close'].rolling(window=5).mean()[-2]                # 2분 종가의 5평균
        # last_ma53 = dm1(ticker)['close'].rolling(window=5).mean()[-3]                # 3분 종가의 5평균
        # last_ma10 = dm1(ticker)['close'].rolling(window=10).mean()[-2]              # 2분 종가의 10평균
        # last_ma20 = dm1(ticker)['close'].rolling(window=20).mean()[-2]              # 2분 종가의 10평균
        # last_ma50 = dm1(ticker)['close'].rolling(window=50).mean()[-2]              # 2분 종가의 10평균
        # gap_r5 = (last_ma5 - last_ma50) / last_ma50 * 100                            # 5이 <-- gap --> 50이 10이 기준
        # gap_r10 = (last_ma10 - last_ma50) / last_ma50 * 100                            # 10이 <-- gap --> 50이 10이 기준
        # gap_r20 = (last_ma20 - last_ma50) / last_ma50 * 100                            # 20이 <-- gap --> 50이 10이 기준

        last_ma52 = dm1(ticker)['close'].rolling(window=5).mean()[-2]                # 2분 종가의 5평균
        last_ma53 = dm1(ticker)['close'].rolling(window=5).mean()[-3]                # 3분 종가의 5평균
        last_ma102 = dm1(ticker)['close'].rolling(window=10).mean()[-2]              # 2분 종가의 10평균
        last_ma103 = dm1(ticker)['close'].rolling(window=10).mean()[-3]
        last_ma202 = dm1(ticker)['close'].rolling(window=20).mean()[-2]              # 2분 종가의 10평균
        last_ma203 = dm1(ticker)['close'].rolling(window=20).mean()[-3]
        last_ma502 = dm1(ticker)['close'].rolling(window=50).mean()[-2]              # 2분 종가의 10평균
        # gap_r5 = (last_ma52 - last_ma50) / last_ma502 * 100                            # 5이 <-- gap --> 50이 10이 기준
        # gap_r10 = (last_ma102 - last_ma50) / last_ma502 * 100                            # 10이 <-- gap --> 50이 10이 기준
        # gap_r20 = (last_ma202 - last_ma50) / last_ma502 * 100                            # 20이 <-- gap --> 50이 10이 기준
        gap_r520 = (last_ma52 - last_ma202) / last_ma502 * 100  

        # if (last_ma10 <= last_ma5) and (last_ma50 < last_ma5) and (0 <= gap_r5 <= 0.5) and (0 <= gap_r10 <= 0.6) \
        #     and (0 <= gap_r20 <= 0.6) and (last_ma5 <= close2) and (last_ma53 <= close3):  # 조건 and (open1 <= price)
        if (last_ma202 <= last_ma52) and (last_ma202 < last_ma102) \
            and (last_ma53 < last_ma52) and ( last_ma103 < last_ma102) and (last_ma203 < last_ma202) \
                and (last_ma502 < last_ma102) and (0 <= gap_r520 <= 0.5) and (last_ma52 <= close2):  # 조건 and (open1 <= price)
            return True
        else:
            return False
    except Exception as m510:
        print(f'Error::\nsearch_def::r1_m510:{linenumber()}p::{m510}\n')


""" ((추격매도 1조건)) G (1m)) """

# NoneType error 발생 구간
def s1_bull_m1(ticker):                                                              # (5이 < 10이) 3분봉 매수시점 조건
    # try:
    # open1 = dm1(ticker).iloc[-1]['open']                                        # 현재 1분봉 시가
    # close1 = dm1(ticker).iloc[-1]['close']                                       # 1분전 종가
    # open2 = dm1(ticker).iloc[-2]['open']                                        # 2분전 시가
    close2 = dm1(ticker).iloc[-2]['close']                                       # 2분전 종가
    # open3 = dm1(ticker).iloc[-3]['open']                                        # 3분전 시가
    close3 = dm1(ticker).iloc[-3]['close']                                       # 3분전 종가

    last_ma05 = dm1(ticker)['close'].rolling(window=5).mean()[-1]                # 1분 종가의 5평균 현봉
    last_ma010 = dm1(ticker)['close'].rolling(window=10).mean()[-1]              # 1분 종가의 5평균 현봉
    last_ma5 = dm1(ticker)['close'].rolling(window=5).mean()[-2]                 # 2분 종가의 5평균 전봉
    last_ma53 = dm1(ticker)['close'].rolling(window=5).mean()[-3]                # 3분전 종가의 5평균 전전봉
    last_ma10 = dm1(ticker)['close'].rolling(window=10).mean()[-2]               # 2분 종가의 10평균
    # last_ma103 = dm1(ticker)['close'].rolling(window=10).mean()[-3]               # 3분 종가의 10평균
    last_ma20 = dm1(ticker)['close'].rolling(window=20).mean()[-2]               # 2분 종가의 20평균
    last_ma50 = dm1(ticker)['close'].rolling(window=50).mean()[-2]               # 2분 종가의 50평균

    gap = (last_ma05 - last_ma010) * 0.5                                         # 조정 (5평 - 10평)의 3%
    mp = last_ma010 + gap                                                         # 10평가격 - 3% 이상 유지 시
    # mp = last_ma05 - gap                                                         # 10평가격 + 3% 이상 유지 시

    # if (last_ma10 < last_ma5) and (last_ma20 < last_ma10) and (last_ma50 < last_ma20) \
    if (last_ma50 < last_ma20 < last_ma10 < last_ma5) and (last_ma5 <= close2) and (last_ma53 <= close3):   # 조건
    # if (last_ma50 < last_ma20 < last_ma10 < last_ma5) and (last_ma10 <= close2) and (last_ma103 <= close3):   # 조건
        return True, mp             # bull 기준 + mp 하락 시 매도 기준
    else:
        return False, mp
    # except Exception as s1_m1:
    #     print('def_s1_m1:', s1_m1)


""" ((추매지연 1조건)) G (1m)) 매수지연 조건포함(하락 시 적용) """


def b1_decline_m1(ticker):                                                            # 감소 시 추매 시점 체크
    try:
        # open1 = dm1(ticker).iloc[-1]['open']                                        # 현재 1분봉 시가
        # close1 = dm1(ticker).iloc[-1]['close']                                       # 1분전 종가
        # open2 = dm1(ticker).iloc[-2]['open']                                        # 2분전 시가
        close2 = dm1(ticker).iloc[-2]['close']                                       # 2분전 종가
        # open3 = dm1(ticker).iloc[-3]['open']                                        # 3분전 시가
        close3 = dm1(ticker).iloc[-3]['close']                                       # 3분전 종가

        last_ma05 = dm1(ticker)['close'].rolling(window=5).mean()[-1]                # 1분 종가의 5평균 현봉
        last_ma020 = dm1(ticker)['close'].rolling(window=20).mean()[-1]              # 1분 종가의 20평균 현봉
        last_ma5 = dm1(ticker)['close'].rolling(window=5).mean()[-2]                 # 1분 종가의 5평균 전봉
        # last_ma53 = dm1(ticker)['close'].rolling(window=5).mean()[-3]                # 1분 종가의 5평균 전전봉
        last_ma10 = dm1(ticker)['close'].rolling(window=10).mean()[-2]               # 1분 종가의 10평균
        last_ma103 = dm1(ticker)['close'].rolling(window=10).mean()[-3]               # 1분 종가의 10평균
        last_ma20 = dm1(ticker)['close'].rolling(window=20).mean()[-2]               # 1분 종가의 20평균
        last_ma50 = dm1(ticker)['close'].rolling(window=50).mean()[-2]               # 1분 종가의 50평균

        dgap = (last_ma020 - last_ma05) * 0.5                                         # (5평 - 10평)의 5%
        dmp = round((last_ma05 + dgap), 2)                                            # 5평가격 - 5% 이상 유지 시
        """ pass 조건 5,20,50 역배열이고 1분전 , 2분전 종가가 10이평 아래 , 현가가 20이평과 5이평 차의 5% 만큼 5이평에서 더한 값보다 낮을 때"""

        if (last_ma5 <= last_ma20 <= last_ma50) and (close2 <= last_ma10) and (close3 <= last_ma103):   # 조건
            return True, dmp             # decline 기준 + dmp 하락 시 추매 기준
        else:
            return False, dmp
    except Exception as b1_m1:
        print('def_b1_m1:', b1_m1)

""" ((추매지연 2조건)) G (1m)) 매수지연 조건포함(하락 시 적용) """
def b2_decline_m1(ticker):                                                            # 감소 시 추매 시점 체크
    # try:
    # open1 = dm1(ticker).iloc[-1]['open']                                        # 현재 1분봉 시가
    # close1 = dm1(ticker).iloc[-1]['close']                                       # 1분전 종가
    # open2 = dm1(ticker).iloc[-2]['open']                                        # 2분전 시가
    # close2 = dm1(ticker).iloc[-2]['close']                                       # 2분전 종가
    # open3 = dm1(ticker).iloc[-3]['open']                                        # 3분전 시가
    # close3 = dm1(ticker).iloc[-3]['close']                                       # 3분전 종가

    # last_ma5_1 = dm1(ticker)['close'].rolling(window=5).mean()[-1]                # 1분 종가의 5평균 현봉
    last_ma5_2 = dm1(ticker)['close'].rolling(window=5).mean()[-2]
    last_ma5_3 = dm1(ticker)['close'].rolling(window=5).mean()[-3]
    last_ma10_1 = dm1(ticker)['close'].rolling(window=10).mean()[-1]
    last_ma10_2 = dm1(ticker)['close'].rolling(window=10).mean()[-2]              # 1분 종가의 20평균 현봉
    last_ma10_3 = dm1(ticker)['close'].rolling(window=10).mean()[-3]
    # last_ma20_1 = dm1(ticker)['close'].rolling(window=20).mean()[-1]              # 1분 종가의 20평균 현봉
    last_ma20_2 = dm1(ticker)['close'].rolling(window=20).mean()[-2]              # 1분 종가의 20평균 현봉
    last_ma20_3 = dm1(ticker)['close'].rolling(window=20).mean()[-3]

    # last_ma50_2 = dm1(ticker)['close'].rolling(window=50).mean()[-2]               # 1분 종가의 50평균
    
    dgap = (last_ma20_2 - last_ma10_2) * 0.6                                         # 전분(20평 - 10평)의 6%
    dmp = round((last_ma10_1 + dgap), 2)                                            # 5평가격 - 5% 이상 유지 시
    """ pass 조건 5,20,50 역배열이고 1분전 , 2분전 종가가 10이평 아래 , 현가가 20이평과 5이평 차의 5% 만큼 5이평에서 더한 값보다 낮을 때"""

    if (last_ma5_2 <= last_ma5_3) or (last_ma10_2 <= last_ma10_3) or (last_ma20_2 <= last_ma20_3) :   # 조건
        # print(f'last_ma5_2: {last_ma5_2}, last_ma5_3: {last_ma5_3}, dmp:{dmp}, {ticker}:true')
        # print(ticker,'true')
        return True, dmp             # decline 기준 + dmp 하락 시 추매 기준
    else:
        return False, dmp
    # except Exception as b2_m1:
    #     print('def_b2_m1:', b2_m1)


""" ((정렬 조건)) G ((전고가 <-- gap --> 전시가) 전3일 조정값) 매수 조건검색 """


def rain_market_yho(ticker):                                                        # ((전고가 <-- gap --> 전시가) 전3일 조정값), 현재가 위치 지준 계산
    try:
        yhigh = dy(ticker)['high'].iloc[-4:-1]                                          # 전3일 고가 dataframe 
        yopen0 = dy(ticker)['open'].iloc[-4:-1]                                         # 전3일 시가 dataframe
        gap_r = max((yhigh - yopen0) / yopen0 * 100)                                    # gap 제일 큰 값 dataframe 계산값 중 최고치
        return gap_r
    except Exception as yho:
        print('def_yho:', yho)


""" ((정렬 조건)) G (금현가 <-- gap --> 금시가) 매수 조건검색 """


def rain_market_po(ticker, price):                                                  # (금현가 <-- gap --> 금시가) gap 계산
    # try:
    open0 = dy(ticker).iloc[-1]['open']
    gap = price - open0                                                             # 현가 - 시가
    gap_r = gap / open0 * 100                                                       # 현가 - 시가 차 시가기준
    return gap_r
    # except Exception as po:
    #     print('def_po:', po)



""" 적은 종목 집중 투자 시 ((정렬 조건)) (전일)(5이 == 양봉) 조건검색 """


def bull_market_1up(ticker):                                                         # 5이 < 시가 비교
    # try:
    yopen = dy(ticker).iloc[-2]['open']                                             # 전일 시가
    yclose = dy(ticker).iloc[-2]['close']                                           # 전일 종가
    last_ma5 = dy(ticker)['close'].rolling(window=5).mean()[-2]                     # 전일 5이
    if (last_ma5 < yclose) and (yopen < yclose):                                    # 전5이 < 전종가 와 전시 < 전종
        return True
    else:
        return False
    # except Exception as o5:
    #     print('def_o5:', o5)



""" 적은 종목 집중 투자 시 ((정렬 조건)) (전3일)(급상승 후 약세 체크) 조건검색 """


def bull_market_3dup(ticker):                                                         # 5이 < 시가 비교
    # try:
    ylow3 = dy(ticker).iloc[-4]['low']                                             # 전일 시가
    ylow2 = dy(ticker).iloc[-3]['low']                                             # 전일 시가
    ylow1 = dy(ticker).iloc[-2]['low']                                             # 전일 시가
    yhigh3 = dy(ticker).iloc[-4]['high']                                             # 전일 시가
    yhigh2 = dy(ticker).iloc[-3]['high']                                             # 전일 시가
    yhigh1 = dy(ticker).iloc[-2]['high']                                             # 전일 시가
    yopen1 = dy(ticker).iloc[-2]['open']                                           # 전일 종가
    yclose1 = dy(ticker).iloc[-2]['close']                                           # 전일 종가
    gap3 = yhigh3 - ylow3; gap2 = yhigh2 - ylow2; gap1 = yhigh1 - ylow1
    last_ma5 = dy(ticker)['close'].rolling(window=5).mean()[-2]                     # 전일 5이
    if (gap1 < gap2 < gap3) and (yopen1 < yclose1) and (last_ma5 < yclose1):                                    # 전5이 < 전종가 와 전시 < 전종
        return True
    else:
        return False
    # except Exception as o5:
    #     print('def_o5:', o5)


""" ((1번째 정렬 조건 - 1번보다 넓게)) G (yg이평 < 종가) 전일 조정값) 매수 조건검색 """


def bull_market_yc(yg, ticker):                                                         # (전yg이평 <-- gap --> 전종가)인 종목 선택
    # try:
    yclose = dy(ticker)['close'].iloc[-2]                                               # 전일 종가
    last_mayg = dy(ticker)['close'].rolling(window=yg).mean()[-2]                       # 전일 yg이평
    last_mayg = last_mayg - (last_mayg * perct(20))                                     # 전yg이평 - 20% 이상일 경우 검색
    if (last_mayg < yclose):                                                            # 전yg이평 < 전종가
        return True
    else:
        return False
    # except Exception as yg: last_ma = last_ma_nw - (last_ma_nw * npct)
    #     print('def_yg:', yg)


""" ((정렬 조건)) (전90이 < 현가) 조건검색 """


def bull_market_pg(npct, nw, ticker, price):                                  # 전90이 < 현가 비교
    try:
        last_ma_nw = dy(ticker)['close'].rolling(window=nw).mean()[-2]                   # 90일 종가의 평균
        last_ma = last_ma_nw - (last_ma_nw * npct)
        # print(f'종목:{ticker},현재가:{price},90일:{last_ma_nw}, 계산:{last_ma}')
        if price >= last_ma:                                                          # 90이 < 현가
            return True
        else:
            return False
    except Exception as pnw:
        print('def_pnw:', pnw)

""" ((정렬 조건)) (5이 < 시가) 조건검색 """


def bull_market_o5(ticker):                                                         # 5이 < 시가 비교
    # try:
    open0 = dy(ticker).iloc[-1]['open']                                             # 금일 시가
    last_ma5 = dy(ticker)['close'].rolling(window=5).mean()[-2]                     # 5일 종가의 평균
    if last_ma5 < open0:                                                            # 5이 < 시가
        return True
    else:
        return False
    # except Exception as o5:
    #     print('def_o5:', o5)


""" ((정렬 조건)) (금시가 < 현가 ) 조건검색 """


def bull_market_po(ticker, price):                                                  # 금시가 < 현가 비교
    try:
        open0 = dy(ticker).iloc[-1]['open']                                             # 금일 시가
        if open0 <= price:                                                              # 금시가 < 현가
            return True
        else:
            return False
    except Exception as po:
        print('def_po:', po)


""" ((정렬 조건)) (전5이 < 현가) 조건검색 """


def bull_market_p5(ticker, price):                                                  # 전5이 < 현가 비교
    # try:
    last_ma5 = dy(ticker)['close'].rolling(window=5).mean()[-2]                     # 5일 종가의 평균
    if last_ma5 <= price:                                                           # 전5이 < 현가
        return True
    else:
        return False
    # except Exception as p5:
    #     print('def_p5:', p5)


""" ((정렬 조건)) (전10이 < 전5이) 조건검색 """


def bull_market_510(ticker):                                                        # 전10이 < 전5이 비교 함수
    # try:
    last_ma5 = dy(ticker)['close'].rolling(window=5).mean()[-2]                     # 5일 종가의 평균
    last_ma10 = dy(ticker)['close'].rolling(window=10).mean()[-2]                   # 10일 종가의 평균
    if last_ma10 <= last_ma5:                                                       # 10이 < 5이
        return True
    else:
        return False
    # except Exception as bm510:
    #     print('def_bm510:', bm510)


""" ((정렬 조건)) (전50이 < 전5이) 조건검색 """


def bull_market_550(ticker):                                                        # 전5일 이평 > 전50일 이평 비교
    # try:
    last_ma5 = dy(ticker)['close'].rolling(window=5).mean()[-2]                     # 5일 종가의 평균의 전5일 이평
    last_ma50 = dy(ticker)['close'].rolling(window=50).mean()[-2]                   # 50일 종가의 평균의 전50일 이평
    if last_ma50 <= last_ma5:                                                       # 50이 < 5이
        return True
    else:
        return False
    # except Exception as bm550:
    #     print('def_bm550:', bm550)

""" ((정렬 조건)) (전90이 < 전5이) 조건검색 """


def bull_market_590(ticker):                                                        # 전5일 이평 > 전50일 이평 비교
    # try:
    last_ma5 = dy(ticker)['close'].rolling(window=5).mean()[-2]                     # 5일 종가의 평균의 전5일 이평
    last_ma90 = dy(ticker)['close'].rolling(window=90).mean()[-2]                   # 50일 종가의 평균의 전50일 이평
    if last_ma90 <= last_ma5:                                                       # 50이 < 5이
        return True
    else:
        return False
    # except Exception as bm590:
    #     print('def_bm590:', bm590)


""" ((정렬 조건)) (전50이 < 전10이 이평) 조건검색 """


def bull_market_1050(ticker):                                                       # 전50이 < 전10이 비교
    # try:
    last_ma10 = dy(ticker)['close'].rolling(window=10).mean()[-2]                   # 5일 종가의 평균의 전5일 이평
    last_ma50 = dy(ticker)['close'].rolling(window=50).mean()[-2]                   # 50일 종가의 평균의 전50일 이평
    if last_ma50 <= last_ma10:  # 50이 < 10이
        return True
    else:
        return False
    # except Exception as bm1050:
    #     print('def_bm1050:', bm1050)


# -------------------------------------------------------------------- #


""" ((검색 조건)) G ((현가 <-- gap --> 전5이) < 조정값 p) 조건검색 """


def bull_market_p5g(ticker, price):                                                 # ((현가 <-- gap --> 전5이) < 조정값 p) 계산
    try:
        last_ma5 = dy(ticker)['close'].rolling(window=5).mean()[-2]                     # 5일 종가의 평전
        gap = price - last_ma5                                                          # ((현가 <-- gap --> 전5이) < 조정값 p) 차이
        gap_r = gap / last_ma5 * 100                                                    # 5이 기준 현가 몇 %
        return gap_r
    except Exception as p5g:
        print('def_p5g:', p5g)


""" ((검색 조건)) G ((전5이 <-- gap --> 전10이) < 조정값 p) 조건검색 """


def bull_market_510g(ticker):                                                       # ((전5이 <-- gap --> 전10이) < 조정값 p) 계산
    try:
        last_ma5 = dy(ticker)['close'].rolling(window=5).mean()[-2]                     # 5일 종가의 평균의 전일 이평
        last_ma10 = dy(ticker)['close'].rolling(window=10).mean()[-2]                   # 10일 종가의 평균의 전일 이평
        gap = last_ma5 - last_ma10                                                      # 전일 5이 - 전 10이 차이
        gap_r = gap / last_ma10 * 100                                                   # 10이 기준 5이 몇 %
        return gap_r
    except Exception as bm510g:
        print('def_bm510g:', bm510g)


""" ((검색 조건)) G ((전10이 <-- gap --> 전50이) < 조정값 p) 조건검색 """


def bull_market_1050g(ticker):                                                      # ((전10이 <-- gap --> 전50이) < 조정값 p) 계산
    try:
        last_ma10 = dy(ticker)['close'].rolling(window=10).mean()[-2]                   # 5일 종가의 평균의 전일 이평
        last_ma50 = dy(ticker)['close'].rolling(window=50).mean()[-2]                   # 50일 종가의 평균의 전일 이평
        gap = last_ma10 - last_ma50                                                     # 전일 10이 - 전50이 차이
        gap_r = gap / last_ma50 * 100                                                   # 50이 기준 10이 몇 %
        return gap_r
    except Exception as bm1050g:
        print('def_bm1050g:', bm1050g)


# ------------------------------------------------------------------------ #


""" ((정렬 조건)) R (현가 <-- gap -->전5이) 정렬 조건 메인 """


def bull_gap_p5(ticker, price):                                                     # (현가 <-- gap --> 전5이) 계산
    try:
        last_ma5 = dy(ticker)['close'].rolling(window=5).mean()[-2]                     # 5일 종가의 평균의 전5일 이평
        gap = price - last_ma5                                                          # 현가 - 전 5이 차이
        gap_r = gap / last_ma5 * 100                                                    # 5이 기준 현가 % 계산
        return gap_r
    except Exception as bgp5:
        print('def_bgp5:', bgp5)


""" ((정렬 조건)) R (5이 <-- gap --> 50이) 계산 정렬 조건 """


def bull_gap_550(ticker):                                                           # (5이 <-- gap --> 50이) 계산
    try:
        last_ma5 = dy(ticker)['close'].rolling(window=5).mean()[-2]                     # 5일 종가의 평균의 전일 이평
        last_ma50 = dy(ticker)['close'].rolling(window=50).mean()[-2]                   # 50일 종가의 평균의 전일 이평
        gap = last_ma5 - last_ma50                                                      # 5이 - 50이 차이
        gap_r = gap / last_ma50 * 100                                                   # 50이 기준 5이 % 계산
        return gap_r
    except Exception as bg550:
        print('def_bg550:', bg550)


# ------------------------------------------------------------------------ #


""" ((추매 평단)) R (5이 기준 추매 평단) 평단가 낮추기 조건 """


def buy_avr_price_5(ticker):                                                       # 목표가 10이 차이 계산
    try:
        last_ma5 = dy(ticker)['close'].rolling(window=5).mean()[-2]                  # 전일 종가의 10평균        
        buy_goal = last_ma5 + (last_ma5 * 0.02)                                      # 
        return buy_goal, last_ma5
    except Exception as avr5:
        print('def_avr5:', avr5)


""" ((추매 평단)) R (10이 기준 추매 평단) 평단가 낮추기 조건 """


def buy_avr_price_10(ticker):                                                       # 목표가 10이 차이 계산
    try:
        last_ma10 = dy(ticker)['close'].rolling(window=10).mean()[-2]                  # 전일 종가의 10평균        
        buy_goal = last_ma10 + (last_ma10 * 0.02)                                      # 
        return buy_goal, last_ma10
    except Exception as avr10:
        print('def_avr10:', avr10)


""" ((추매 평단)) R (20이 기준 추매 평단) 평단가 낮추기 조건 """


def buy_avr_price_20(ticker):                                                       # 목표가 20이 차이 계산
    try:
        last_ma20 = dy(ticker)['close'].rolling(window=20).mean()[-2]                  # 전일 종가의 20평균
        buy_goal = last_ma20 + (last_ma20 * 0.02)                                       # 
        return buy_goal, last_ma20
    except Exception as avr20:
        print('def_avr20:', avr20)


""" ((추매 평단)) R (30이 기준 추매 평단) 평단가 낮추기 조건 """


def buy_avr_price_30(ticker):                                                       # 목표가 30이 차이 계산
    try:
        last_ma30 = dy(ticker)['close'].rolling(window=30).mean()[-2]                  # 전일 종가의 30평균
        buy_goal = last_ma30 + (last_ma30 * 0.02)                                       # 
        return buy_goal, last_ma30
    except Exception as avr30:
        print('def_avr30:', avr30)


""" ((추매 평단)) R (40이 기준 추매 평단) 평단가 낮추기 조건 """


def buy_avr_price_40(ticker):                                                       # 목표가 30이 차이 계산
    try:
        last_ma40 = dy(ticker)['close'].rolling(window=40).mean()[-2]                  # 전일 종가의 30평균
        buy_goal = last_ma40 + (last_ma40 * 0.02)                                       # 
        return buy_goal, last_ma40
    except Exception as avr40:
        print('def_avr40:', avr40)


""" ((추매 평단)) R (50이 기준 추매 평단) 평단가 낮추기 조건 """


def buy_avr_price_50(ticker):                                                       # 목표가 50이 차이 계산
    try:
        last_ma50 = dy(ticker)['close'].rolling(window=50).mean()[-2]                  # 전일 종가의 50평균
        buy_goal = last_ma50 + (last_ma50 * 0.02)                                       # 
        return buy_goal, last_ma50
    except Exception as avr50:
        print('def_avr50:', avr50)


""" ((추매 평단)) R (60이 기준 추매 평단) 평단가 낮추기 조건 """


def buy_avr_price_60(ticker):                                                       # 목표가 50이 차이 계산
    try:
        last_ma60 = dy(ticker)['close'].rolling(window=60).mean()[-2]                  # 전일 종가의 50평균
        buy_goal = last_ma60 + (last_ma60 * 0.02)                                       # 
        return buy_goal, last_ma60
    except Exception as avr60:
        print('def_avr60:', avr60)


""" ((추매 평단)) R (70이 기준 추매 평단) 평단가 낮추기 조건 """


def buy_avr_price_70(ticker):                                                       # 목표가 50이 차이 계산
    try:
        last_ma70 = dy(ticker)['close'].rolling(window=70).mean()[-2]                  # 전일 종가의 50평균
        buy_goal = last_ma70 + (last_ma70 * 0.02)                                       # 
        return buy_goal, last_ma70
    except Exception as avr70:
        print('def_avr70:', avr70)


""" ((추매 평단)) R (80이 기준 추매 평단) 평단가 낮추기 조건 """


def buy_avr_price_80(ticker):                                                       # 목표가 50이 차이 계산
    try:
        last_ma80 = dy(ticker)['close'].rolling(window=80).mean()[-2]                  # 전일 종가의 50평균
        buy_goal = last_ma80 + (last_ma80 * 0.02)                                       # 
        return buy_goal, last_ma80
    except Exception as avr80:
        print('def_avr80:', avr80)


""" ((추매 평단)) R (90이 기준 추매 평단) 평단가 낮추기 조건 """


def buy_avr_price_90(ticker):                                                       # 목표가 50이 차이 계산
    try:
        last_ma90 = dy(ticker)['close'].rolling(window=90).mean()[-2]                  # 전일 종가의 50평균
        buy_goal = last_ma90 + (last_ma90 * 0.02)                                       # 
        return buy_goal, last_ma90
    except Exception as avr90:
        print('def_avr90:', avr90)


""" ((추매 조건)) (현재가 < 30일간 5이평 추적값 중 2번쨰)조건검색 """


def ma5_under(ticker):  # 30일 5이평 값 비교
    try:
        sorted_nums = (sorted(set(dy(ticker)['close'].rolling(window=5).mean()[-31:-1]), reverse=False))[1]  # 5일 종가의 평균 오름차순(낮은값의 2번째) 2번째

        return sorted_nums                                      # 작은 값 중에 2번째 값
    except Exception as ma5:
        print('def_ma5:', ma5)


""" ====================== 주문상태에 따른 자료 가져오기 ====================== """

""" 주문 정보 확인 """


def get_orderi(state, side, want, ofn1):            # state='wait'대기, 'done'완료, side='bid'매수, 'ask'매도, want='n'이름만,'i'정보 |, ofn1='file 경로'
    f = open(ofn1)
    lines = f.readlines()
    access_key = lines[0].strip()
    secret_key = lines[1].strip()
    f.close()

    server_url = 'https://api.upbit.com'

    query = {'state': state, }
    query_string = urlencode(query)

    query_string = "{0}".format(query_string).encode()
    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + '/v1/orders', params=query, headers=headers)
    want_t = []
    want_name = []
    for i in res.json():
        try:
            if side in i['side']:
                want_t.append(i)
                want_name.append(i['market'])
        except TypeError as orderi:
            print('def_orderi', orderi)
    if want == 'i' :
        return want_t
    elif want == 'n':
        return want_name

""" 주문 정보 확인 """
def get_orderi2(ofn1):
    f = open(ofn1)
    lines = f.readlines()
    access_key = lines[0].strip()
    secret_key = lines[1].strip()
    f.close()
    server_url = 'https://api.upbit.com'

    params = {
    # 'states[]': ['done', 'cancel']
    'states[]': ['done']
    }
    query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
    'Authorization': authorization,
    }

    res = requests.get(server_url + '/v1/orders', params=params, headers=headers)
    res.json()

    return res.json()

""" 입금 정보 확인 """


def get_inmoney(ofn1):
    server_url = 'https://api.upbit.com'

    f = open(ofn1)
    lines = f.readlines()
    access_key = lines[0].strip()
    secret_key = lines[1].strip()
    f.close()


    query = {
        'currency': 'KRW',
    }
    query_string = urlencode(query)

    txids = [
        '9e37c537-6849-4c8b-a134-57313f5dfc5a',
        #...
    ]
    txids_query_string = '&'.join(["txids[]={}".format(txid) for txid in txids])

    query['txids[]'] = txids
    query_string = "{0}&{1}".format(query_string, txids_query_string).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/deposits", params=query, headers=headers)

    return res.json()[0]


""" 매수 시간 변환 후 반환 """


def t_c(tc):
    try:
        tc1 = tc.translate({ord('T'): ' '})                 # time 에서 'T' 제거
        tc2 = tc1[0:19]                                     # tc1 에서 원하는 time 추출
        t = datetime.strptime(tc2, '%Y-%m-%d %H:%M:%S')     # tc2 시간 재 구성
        return t
    except Exception as t_c:
        print('def_tc:', t_c)

""" 매수 시간 변환 """


def t_c2(tc):
    try:
        tc1 = tc.translate({ord('T'): ' '})            # time 에서 'T' 제거
        tc1 = tc1.translate({ord('-'): ":"})            # time에서 '-' > ":" 변환
        tc2 = tc1[0:16]         # tc1 에서 원하는 년월일 추출
        # tc3 = tc1[10:16]            # tc1에서 시간 추출
        # tc4 = f'{tc2}\n{tc3}'           # 표기변경
        return tc2
    except Exception as e:
        print(f'{linenumber()}p::error:search_def:t_c: {datetime.now()}, t_c2: {e}')

""" 매도호가 계산 (올림) """


def get_tick_s(price):
    if price >= 2000000:
        tick_size = math.ceil(price / 1000) * 1000
    elif price >= 1000000:
        tick_size = math.ceil(price / 500) * 500
    elif price >= 500000:
        tick_size = math.ceil(price / 100) * 100
    elif price >= 100000:
        tick_size = math.ceil(price / 50) * 50
    elif price >= 10000:
        tick_size = math.ceil(price / 10) * 10
    elif price >= 1000:
        tick_size = math.ceil(price / 5) * 5
    elif price >= 100:
        tick_size = math.ceil(price / 1) * 1
    elif price >= 10:
        tick_size = float(math.ceil(price / 0.1) * Decimal('0.1'))      # 부동소수점 decimal 계산
    else:
        tick_size = float(math.ceil(price / 0.01) * Decimal('0.01'))    # 부동소수점 decimal 계산
    return tick_size


""" 매도 시 평단 확인 """


def abp_check(ticker, abptime, ofn1):                     # 5분간 매수 종목 데이터 보유 시(여러 종목 체결 시)
    cbid_list = []
    gcbid = get_orderi('done', 'bid', 'i', ofn1)[0]       # 마지막 매수완료 종목 정보
    cbid_list.append(gcbid)
    for i in cbid_list:
        if ticker == i['market']:
            mt = (t_c(gcbid['created_at']) + timedelta(minutes=abptime))
            if (mt <= datetime.now()):
                cbid_list.remove(i)
                return True
                # print(cbid_list)
            else:
                # print(cbid_list)
                return False
                return float(i['price'])

def ext_save(id, bl, ext_item):         # 제외항목 저장
    ext_a = ext_item['ext_a']         # 추매제외종목 리스트
    ext_b = ext_item['ext_b']         # 매수제외종목 리스트
    ext_s = ext_item['ext_s']         # 매도제외종목 리스트
    extia = list(set(ext_a) - set(bl))            # 추매제외리스트에서 보유종목에 없는 종목만 추출
    extib = list(set(ext_b) - set(bl))            # 매수제외리스트에서 보유종목에 없는 종목만 추출
    extis = list(set(ext_s) - set(bl))            # 매도제외리스트에서 보유종목에 없는 종목만 추출

    ext_item['ext_a'] = list(set(ext_a) - set(extia))            # 추매제외리스트에서 보유종목에 없는 종목 제외
    ext_item['ext_b'] = list(set(ext_b) - set(extib))            # 추매제외리스트에서 보유종목에 없는 종목 제외
    ext_item['ext_s'] = list(set(ext_s) - set(extis))            # 추매제외리스트에서 보유종목에 없는 종목 제외

    with open('/root/UBiCauto/data/ext_item%s.pickle' %(id), 'wb') as fw:
        pickle.dump(ext_item, fw)
    with open('/root/UBiCauto/data/ext_item%s.pickle' %(id), 'rb') as fr:
        ext_item = pickle.load(fr)
    return ext_item

""" 매도 후 add_num update 반환, collection counter 함수 사용 추매횟수 출력관련 """

def ex_item(bl, ex_num):
    try:
        with open('/root/UBiCauto/data/add_num%s.pickle' %(ex_num), 'rb') as fr:
            add_num = pickle.load(fr)
        ext_adn = []
        extct_adn = []
        for at, ct in add_num.items():                           # add_num 에 있는 종목 확인
            extct_adn.append(ct[0])
            if (at not in bl):                              # add_num 종목이 보유종목에 없는 종목을 ext_adn 에 생성
                ext_adn.append(at)
        [add_num.pop(key, None) for key in ext_adn]         # add_num 에서 ext_adn 종목을 제외 후 재생성
        with open('/root/UBiCauto/data/add_num%s.pickle' %(ex_num), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
            pickle.dump(add_num, fw)
        ret_ct = Counter(extct_adn)                             # 리스트에서 동일한 값 갯수 체크
        ret_ct = {f'0:{extct_adn.count(0)} | 1:{extct_adn.count(1)} | 2:{extct_adn.count(2)} | 3:{extct_adn.count(3)} | 4:{extct_adn.count(4)} | 5:{extct_adn.count(5)} | 6:{extct_adn.count(6)} | 7:{extct_adn.count(7)} | 8:{extct_adn.count(8)}'}
        # ret_ct = {0:{extct_adn.count(0)}, 1:{extct_adn.count(1)}, 2:{extct_adn.count(2)}, 3:{extct_adn.count(3)}, 4:{extct_adn.count(4)}, 5:{extct_adn.count(5)}, 6:{extct_adn.count(6)}, 7:{extct_adn.count(7)}, 8:{extct_adn.count(8)}}
        return ret_ct
    except Exception as add_num:
        print('def_add_num:', add_num)

# add_num에서 an에 매도횟수 호출 바인딩
def add_get(e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    an = add_num.get(e)[0]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return an

def add_rwinit(e, rwnum, adn1, adn2, fbv):           # 새 종목 매수 시 add_num에 추가 저장
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e] = [adn1, adn2, fbv]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return add_num

def add_rw0(e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:1]=[0]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rw1(e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:1]=[1]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rw2(e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:1]=[2]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rw3(e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:1]=[3]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rw4(e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:1]=[4]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rw5(e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:1]=[5]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rw6(e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:1]=[6]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rw7(e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:1]=[7]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rw8(e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:1]=[8]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rw9(e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:1]=[9]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rw10(e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:1]=[10]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rwav5(an, e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:2]=[(an+1), 5]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rwav10(an, e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:2]=[(an+1), 10]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rwav20(an, e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:2]=[(an+1), 20]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rwav30(an, e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:2]=[(an+1), 30]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rwav40(an, e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:2]=[(an+1), 40]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rwav50(an, e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:2]=[(an+1), 50]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rwav60(an, e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:2]=[(an+1), 60]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rwav70(an, e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:2]=[(an+1), 70]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rwav80(an, e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:2]=[(an+1), 80]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

def add_rwav90(an, e, rwnum):
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'rb') as fr:
        add_num = pickle.load(fr)
    add_num[e][0:2]=[(an+1), 90]
    with open('/root/UBiCauto/data/add_num%s.pickle' %(rwnum), 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)
    return

""" 소수 --> % 변환 """


def perct(pct):
    per = pct / 100
    return per

""" 소수 --> % 변환 """

def de_perct(pct):
    per = pct * 100
    per = round(per, 2)
    return per

""" counter 출력 dic 변환 """

def cnt_p(cnt_dic):
    cntp = {}
    for key, value in cnt_dic.items():
        cntp[key]=value
    return cntp


""" 내 자산 정보 확인 """


def myasset(upbit):
    try:
        # time.sleep(0.5)
        mybal = upbit.get_balance_t()                              # 총 매수 가능 금액 (보유금액)
        # time.sleep(0.5)
        mygmoney = upbit.get_amount('ALL')               # 총 매수 금액
        if mybal and mygmoney :
            sum = (mybal + mygmoney)                          # 총 합계 = 총 매수가능 금액 + 총 매수금액
            bidp = mygmoney/sum * 100                         # 총 매수비율 = 총 매수금액 / 총 합계 
            return (round(sum, 1)), (round(mygmoney, 1)), (round(bidp, 2)), (round(mybal, 1))
    except TypeError as myasset:
        print(myasset)




""" 정수 자릿수 구하기 """


def digit_length(n): 
    return int(math.log10(n)) + 1 if n else 0



""" 수익율 계산하기(매수가 기준) """    # 추매 기준에 따른 수익율 계산으로 매수가를 상회해도 계산 가능


def cal_ask3(ask_p, bcnt):
    addct = []
    addct0 = [1, 3, 6, 18, 36, 72]                      # 0차:1, 1차:*3(2배), 2차:*6(1배), 3차:*18(2배), 4차:*36(1배), 5차:*72(1배), 6차:144(1배)
    # print('bcnt', bcnt)
    for i in addct0:
        a = bcnt * i
        b = round(((ask_p - (ask_p * 0.0005)) - a), 2)
        # print(b)
        if 0 < b:
            addct.append(b)
    # print(addct)
    min_addct = min(addct)
    return min_addct


""" 매수 비중에 따른 매도 기준 ON, OFF 가능 """

def askper(upbit, num):
    tbidp = myasset(upbit)[2]              # 매수가능금액 비율
    global akp                              # 함수 밖의 전역변수를 함수내에서 사용 시 선언필요(별도로 함수명을 바꿔줌)
    akp = 0.0045
    n = 1.0                                 # 최대 매도 기준 설정
    try:
        for s in range(0, 100):                 # 0 ~ 100 반복문
            if s % 5 == 0 :                     # 5의 배수 선택
                if s <= tbidp < (s + 5) :       # 5배수 범위 기준
                    akp = round(perct(n), 5)  # 매수 비중 계산
                    # print(s, s+5, n, akp)
                n -= 0.1  # 0.1, 0.06 , 0.03       # 매수 비중 증감폭 0.03배(값을 올리면 akp가 내려감, 내리면 akp 올라감)
        # print(akp) 
        if akp < 0.0045 :
            akp = 0.0045
        print(f'1053p::Search_def.py:(askper)-{akp}')
        with open('/root/UBiCauto/data/set_cfg%s.pickle' %(num), 'rb') as fset:
            ubic_conf = pickle.load(fset)
        ubic_conf['ask_p'] = akp
        with open('/root/UBiCauto/data/set_cfg%s.pickle' %(num), 'wb') as fset:
            pickle.dump(ubic_conf, fset)
    except Exception as e:
        print(f'1060p::error:search_def: askper: {e}')
    return akp


""" 초기 add_num 생성 함수 """

def adn_insert(b_money, t_money):            # 1.추매 횟수 확인(초기 add_num 생성 함수)
    if (t_money < b_money) and (t_money):
        # ad1 = int(b_money / t_money)
        ad1 = 0
        pass
    elif b_money <= t_money:
        ad1 = int(t_money / b_money)
        # ag_price1
        if ad1 == 1:
            ad1 = 0
        elif 1 < ad1 <= 3:          # 2배
            ad1 = 1
        elif 3 < ad1 <= 6:          # 1배
            ad1 = 2
        elif 6 < ad1 <= 18:         # 2배
            ad1 = 3
        elif 18 < ad1 <= 54:        # 2배:54, 1배:36 
            ad1 = 4
        elif 54 < ad1 <= 108:       # 2배:108, 1배:108
            ad1 = 5
    return ad1

""" 초기 add_num 생성 함수 """

def adn_insert1(b_money, t_money, ap_price1):            # 1.추매 횟수 확인(초기 add_num 생성 함수)
    if (t_money < b_money) and (t_money):
        # ad1 = int(b_money / t_money)
        ad1 = 0
        pass
    elif b_money <= t_money:
        sum1 = b_money + ag_price1 +100
        sum2 = sum1 + ag_price2
        sum3 = sum2 + ag_price3
        sum4 = sum3 + ag_price4
        sum5 = sum4 + ag_price5
        sum6 = sum5 + ag_price6
        sum7 = sum6 + ag_price7
        sum8 = sum7 + ag_price8
        sum9 = sum8 + ag_price9
        sum10 = sum9 + ag_price10
        # ad1 = int(t_money / b_money)
        sum0 = 0
        # ag_price1
        if sum0 < t_money <= sum1 :
            ad1 = 0
        elif sum1 < t_money <= sum2 :
            ad1 = 1
        elif sum2 < t_money <= sum3 :
            ad1 = 2
        elif sum3 < t_money <= sum4 :
            ad1 = 3
        elif sum4 < t_money <= sum5 :
            ad1 = 4
        elif sum5 < t_money <= sum6 :
            ad1 = 5
        elif sum6 < t_money <= sum7 :
            ad1 = 6
        elif sum7 < t_money <= sum8 :
            ad1 = 7
        elif sum8 < t_money <= sum9 :
            ad1 = 8
        elif sum9 < t_money <= sum10 :
            ad1 = 10
    return ad1


""" BTC 수익률 출력 """
def ticker_per(cu_p, ticker):
    for e in cu_p:
        if e == ticker:
            yclose = dy(e)['close'].iloc[-2]                    # 전일종가
            cp = cu_p[e]                                        # 현재가
            cper = round(((cp - yclose) / cp) * 100, 2)         # 전일대비 수익률
            if 0 < cper:
                return(f'현재 {e} 종목 ┆ ' + "가격:" + format(cp,",") + "원 ┆" + '\033[91m' + f' 전일대비:{cper} %' + '\033[0m') # 0보다 크면 빨간색
            elif cper < 0:
                return(f'현재 {e} 종목 ┆ ' + "가격:" + format(cp,",") + "원 ┆" + '\033[94m' + f' 전일대비:{cper} %' + '\033[0m') # 0보다 작으면 파란색

""" 종목 수익률 출력 """
def ticker_per2(cu_p, e):
    if e in cu_p:
        yclose = dy(e)['close'].iloc[-2]                    # 전일종가
        cp = cu_p[e]
        cper = round(((cp - yclose) / cp) * 100, 2)         # 전일대비 수익률

    return (cper)

""" 행번호 출력 """
def linenumber():           # 행번호 출력 함수
    cf = currentframe()
    return cf.f_back.f_lineno

class search_s:         # (사용중)
    # 1분 종목검색 (test 중~)
    def r1_m510(self, ticker, price):                                                         # (5이 < 10이) 1분봉 매수시점 조건
        # try:
        close2 = dm1(ticker).iloc[-2]['close']                                      # 3분전 종가

        last_ma52 = dm1(ticker)['close'].rolling(window=5).mean()[-2]                # 3분 종가의 5평균
        last_ma53 = dm1(ticker)['close'].rolling(window=5).mean()[-3]                # 3분 종가의 5평균
        last_ma102 = dm1(ticker)['close'].rolling(window=10).mean()[-2]              # 3분 종가의 10평균
        last_ma103 = dm1(ticker)['close'].rolling(window=10).mean()[-3]
        last_ma202 = dm1(ticker)['close'].rolling(window=20).mean()[-2]              # 3분 종가의 10평균
        last_ma203 = dm1(ticker)['close'].rolling(window=20).mean()[-3]
        last_ma502 = dm1(ticker)['close'].rolling(window=50).mean()[-2]
        gap_r520 = ((last_ma52 - last_ma202) / last_ma202) * 100                           # 5이 <-- gap --> 50이 10이 기준
        gap_r550 = ((last_ma52 - last_ma502) / last_ma502) * 100

        if (last_ma53 < last_ma52) and (last_ma103 < last_ma102) and (last_ma203 < last_ma202) \
            and (gap_r520 <= 0.3) and (gap_r550 <= 1) and (last_ma52 <= close2):
            # print(gap_r520)
            # return True, gap_r520
            return True
        else:
            # return False, gap_r520
            return False
        # except Exception as e:
        #     print(f'Error::\nsearch_def::r1_m510:{linenumber()}p::{e}\n')

    # 3분 종목검색 (test 중~)
    def r3_m510(self, ticker, price):                                                         # (5이 < 10이) 3분봉 매수시점 조건
        try:
            close2 = dm3(ticker).iloc[-2]['close']                                      # 3분전 종가

            last_ma52 = dm3(ticker)['close'].rolling(window=5).mean()[-2]                # 3분 종가의 5평균
            last_ma53 = dm3(ticker)['close'].rolling(window=5).mean()[-3]                # 3분 종가의 5평균
            last_ma102 = dm3(ticker)['close'].rolling(window=10).mean()[-2]              # 3분 종가의 10평균
            last_ma103 = dm3(ticker)['close'].rolling(window=10).mean()[-3]
            last_ma202 = dm3(ticker)['close'].rolling(window=20).mean()[-2]              # 3분 종가의 10평균
            last_ma203 = dm3(ticker)['close'].rolling(window=20).mean()[-3]
            gap_r520 = ((last_ma52 - last_ma202) / last_ma202) * 100                           # 5이 <-- gap --> 50이 10이 기준

            if (last_ma53 < last_ma52) and (last_ma103 < last_ma102) and (last_ma203 < last_ma202) \
                and (gap_r520 <= 0.5) and (last_ma52 <= close2):
                return True, gap_r520
            else:
                return False, gap_r520
        except Exception as r3m510:
            print('def_r3m510:', r3m510)


""" 웹서버 프로세스 재실행 """
def kwrun(ok):
    # q = input ("정말 실행하시겠습니까? ([y]es/[n]o) : ")
    q = 'y'
    if ok == 'true':
        os.system('kwrun')
        print("true")
    return (True)

""" 신규 매수 제외종목 삭제 """
def expr(e):            # 신규 매수 제외종목에서 종목 삭제
    with open('/root/UBiCauto/data/ext_itemB.pickle', 'rb') as fr:      # 신규매수 제외할 코인파일(ext_itemB.pickle)
        ext_itemB = pickle.load(fr)
    ext_B = ext_itemB['ext_b']
    ext_B.remove(e)
    ext_itemB['ext_b'] = ext_B
    with open('/root/UBiCauto/data/ext_itemB.pickle', 'wb') as fw:
        pickle.dump(ext_itemB, fw)

""" 신규 매수 제외종목 추가 """
def expa(e):            # 신규 매수 제외종목에서 종목 추가
    with open('/root/UBiCauto/data/ext_itemB.pickle', 'rb') as fr:      # 신규매수 제외할 코인파일(ext_itemB.pickle)
        ext_itemB = pickle.load(fr)
    ext_B = ext_itemB['ext_b']
    ext_B.append(e)
    ext_itemB['ext_b'] = ext_B
    with open('/root/UBiCauto/data/ext_itemB.pickle', 'wb') as fw:
        pickle.dump(ext_itemB, fw)

""" 한 종목 즉시 매도 버튼(Emergency~) 상황에 맞게 사용(프로그램의 부족한 부분 수동사용) """
def one_sell(upbit, e):         # 응답을 받고 실행
    tb = upbit.get_balance_t(e)                             # 종목 보유수량
    q = input ("정말 실행하시겠습니까? ([y]es/[n]o) : ")
    while True:
        if q == 'y':                                                # 'y'이면 실행
            ob = pyupbit.get_orderbook(e)                           # 호가 가져오기
            try:
                # bob = ob[0]['orderbook_units'][0]['bid_price']      # 가져온 호가의 1호가(매수호가)
                bob = ob.get('orderbook_units')[0]['bid_price']
            except KeyError as kerror:
                print('k-error값:%s' %(kerror))
            upbit.sell_limit_order(e, bob, tb)                    # 해제 후 매도하면 실행 됨 (주의!!!!)
            print(e, bob, tb, '(%s) - sell order ok' %(e))
            break
        elif q == 'n':
            print("실행을 취소했습니다^^;")
            break
        else:
            q = input ("다시 똑바로 입력해 주세요 ([y]es/[n]o) : ")
    # return print(e, bob, tb, '(%s) - sell order ok' %(e))

""" 한 종목 즉시 현재가 매도주문 버튼(Emergency~) 상황에 맞게 사용 """
def one_sell2(upbit, e):            # 질문없이 매도
    tb = upbit.get_balance_t(e)                             # 종목 보유수량
    # q = input ("정말 실행하시겠습니까? ([y]es/[n]o) : ")
    q = 'y'
    while True:
        if q == 'y':                                                # 'y'이면 실행
            ob = pyupbit.get_orderbook(e)                           # 호가 가져오기
            try:
                # bob = ob.get('orderbook_units')[0]['bid_price']     # 자료형 변경 (리스트 > 딕셔너리), 가져온 호가의 1호가(매수호가)
                with open('/root/UBiCauto/data/cp.pickle', 'rb') as fr1:            # 현재가 불러오기
                    cu_p = pickle.load(fr1)                                       # 전체 종목과 현재가 dict 'cu_p' 로 바인딩
                price = cu_p[e]         # 해당종목(e)의 현개가를 price 에 바인딩
            except KeyError as kerror:
                print('k-error값:%s' %(kerror))
            # upbit.sell_limit_order(e, bob, tb)                    # 매수((1))호가에 매도주문, 해제 후 매도하면 실행 됨 (주의!!!!)
            upbit.sell_limit_order(e, price, tb)                    # 매수((1))호가에 매도주문, 해제 후 매도하면 실행 됨 (주의!!!!)
            # print(e, bob, tb, '(%s) - sell order ok' %(e))
            print(e, price, tb, '(%s) - sell order ok' %(e))

            break
        elif q == 'n':
            print("실행을 취소했습니다^^;")
            break
        else:
            q = input ("다시 똑바로 입력해 주세요 ([y]es/[n]o) : ")

""" 한 종목 즉시 현재가 매수주문 버튼 클릭 시 실행 (종목페이지에서 매수 버튼) """
def one_buy(upbit, e, nb_money):            # 질문없이 매도 (웹페이지에서 버튼으로 즉시 매수 실행부분)
    # tb = upbit.get_balance_t(e)                             # 종목 보유수량
    # q = input ("정말 실행하시겠습니까? ([y]es/[n]o) : ")
    q = 'y'
    while True:
        if q == 'y':                                                # 'y'이면 실행
            try:    # 현재가 가져오기
                with open('/root/UBiCauto/data/cp.pickle', 'rb') as fr1:            # 현재가 불러오기
                    cu_p = pickle.load(fr1)                                       # 전체 종목과 현재가 dict 'cu_p' 로 바인딩
            except Exception as cu_p:
                print('1272_ubic_search_def- Buy_cu_p:', cu_p)
            price = cu_p[e]         # 해당종목(e)의 현개가를 price 에 바인딩
            b_o = pyupbit.get_tick_size(price)                        # 매수 호가 계산(v) 주문가격단위 맞춤
            # bid_p = price - (price * bg)                            # 매수 목표가 계산 ( 현재가의 - 0.1 %)(v)
            # print(price, b_o)
            bid_v = round(nb_money / b_o, 3)                                 # nb_money 금액만큼의 수량 계산
            nb_money = format(nb_money,',')         # 천단위 구분자 표시 후 리턴(웹페이지 알람창 표시위함)
            upbit.buy_limit_order(e, b_o, bid_v)            # 현재가 매수 실행
            print(f'{e}종목: 매수가: {price}, 매수금액: {nb_money}원 매수완료')
            return price
            break
        elif q == 'n':
            print("실행을 취소했습니다^^;")
            break
        else:
            q = input ("다시 똑바로 입력해 주세요 ([y]es/[n]o) : ")

""" 한 종목 즉시 매수, 매도 버튼(Emergency~) 상황에 맞게 사용(프로그램의 부족한 부분 수동사용) """
def one_sell3(upbit, e, n):                 # 매도: n=1, 매수: n=2
    tb = upbit.get_balance_t(e)                             # 종목 보유수량
    # q = input ("정말 실행하시겠습니까? ([y]es/[n]o) : ")
    q = 'y'
    while True:
        if q == 'y':                                                # 'y'이면 실행
            ob = pyupbit.get_orderbook(e)                           # 호가 가져오기
            if n == 1:                                              # 매도
                try:
                    # bob = ob[0]['orderbook_units'][0]['bid_price']     # 가져온 호가의 1호가(매수호가)
                    bob = ob.get('orderbook_units')[0]['bid_price']     # 자료형 변경 (리스트 > 딕셔너리)
                except KeyError as kerror:
                    print('k-error값:%s' %(kerror))
                upbit.sell_limit_order(e, bob, tb)                      # 해제 후 매도하면 실행 됨 (주의!!!!)
                print(e, bob, tb, '(%s) - 매도 order ok' %(e))
            elif n == 2:                                                # 매수
                try:
                    # bob = ob[0]['orderbook_units'][0]['ask_price']     # 가져온 호가의 1호가(매도호가)
                    bob = ob.get('orderbook_units')[0]['ask_price']     # 자료형 변경 (리스트 > 딕셔너리)
                except KeyError as kerror:
                    print('k-error값:%s' %(kerror))
                upbit.buy_limit_order(e, bob, tb)                      # 해제 후 매도하면 실행 됨 (주의!!!!)
                print(e, bob, tb, '(%s) - 매수 order ok' %(e))
            break
        elif q == 'n':
            print("실행을 취소했습니다^^;")
            break
        else:
            q = input ("다시 똑바로 입력해 주세요 ([y]es/[n]o) : ")



""" 대폭락 장 비상 버튼(Emergency~) 사용할 일이 없기를... """
# ================================= 비상 시  모든 자산 즉시 매도 ================================= #

def e_ask(upbit):
    bal = []                                        # 보유종목명                            
    balance = upbit.get_balances()                 # 자산정보: dict
    q = input ("정말 실행하시겠습니까? ([y]es/[n]o) : ")
    # q = 'y'
    while True:
        if q == 'y':
            for i in balance:                               # 자산('balance') 리스트를 하나씩 'i'로 가져 옴
                if 'KRW' not in i['currency']:              # 영문 종목명에 'KRW-종목명' 형태로 재 저장
                    u = i['unit_currency']                  # 'KRW'
                    t = i['currency']                       # '영문 종목명'
                    tb = i['balance']                       # 종목 보유수량 str 으로 float 로 변경 필요
                    e = u + '-' + t                         # 'KRW'-'영문 종목명'
                    bal.append(e)                           # (( 보유 종목명 ))만 bal 리스트에 추가
                    # avg_p[e] = float(avg_buy_price)                   # 종목과 평단 'avg_price'에 추가
                    # t_bal[e] = float(tb)                              # 종목과 보유수량 'tb'에 추가 
                    tb = float(tb)                                      # 종목 보유수량 실수로 변환
                    # if e in cu_p:                                     # 현재가 매도 시
                    #     price = cu_p[e]                               # 종목 현재가
                    ob = pyupbit.get_orderbook(e)           # 호가 가져오기
                    try:
                        bob = ob[0]['orderbook_units'][0]['bid_price']      # 가져온 호가의 1호가(매수호가)
                    except KeyError as kerror:
                        print('k-error값:%s' %(kerror))
                    upbit.sell_limit_order(e, bob, tb)                    # 해제 후 매도하면 실행 됨 (주의!!!!)
                    print(e, bob, tb, '(%s) - sell order ok' %(e))
                    time.sleep(0.1)
            break
        elif q == 'n':
            print("실행을 취소했습니다^^;")
            break
        else:
            q = input ("다시 똑바로 입력해 주세요 ([y]es/[n]o) : ")
    return print('(( Sell complete Everything )) ~ !!  %s종목' %(len(bal)))


# ========================================================================================== #



# ============================================================================================================================ #


""" 매도 후 add_num update 반환 """


# def ex_item(add_num, bl):
#     try:
#         ext_adn = []
#         for at in add_num.keys():                           # add_num 에 있는 종목 확인
#             if (at not in bl):                              # add_num 종목이 보유종목에 없는 종목을 ext_adn 에 생성
#                 ext_adn.append(at)
#         [add_num.pop(key, None) for key in ext_adn]         # add_num 에서 ext_adn 종목을 제외 후 재생성
#         return add_num
#     except Exception as add_num:
#         print('def_add_num:', add_num)


""" m1 candle 데이터 저장 및 확인 """


# def m1_check():
#     for ticker in km:                                                       # 원화마켓에서 종목을 하나씪 가져옴
#         cdf = pyupbit.get_ohlcv(ticker, interval="minute1", count=51)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
#         with open('/root/UBiCauto/data/ohlcvm1/%s_df_min1.pickle' %(ticker), 'wb') as fw2:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
#             pickle.dump(cdf, fw2)
#         while True:
#             fs = os.path.getsize('/root/UBiCauto/data/ohlcvm1/%s_df_min1.pickle' %(ticker))
#             if fs < 1024 :
#                 cdf = pyupbit.get_ohlcv(ticker, interval="day", count=60)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
#                 with open('/root/UBiCauto/data/ohlcvm1/%s_df_min1.pickle' %(ticker), 'wb') as fw2:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
#                     pickle.dump(cdf, fw2)
#             else:
#                 break


""" 매도 시 평단 확인 """


# def abp_check(ticker, abptime):                   # 최종매수 1종목에 대한 실행(아주 천천히 거래 시)
#     gcbid = get_cbid_i()[0]
#     if ticker == gcbid['market']:
#         mt = (t_c(gcbid['created_at']) + timedelta(minutes=abptime))
#         if (mt <= datetime.now()):
#             pass
#         else:
#             return float(gcbid['price'])


""" X ((검색 조건)) G ((전5이 <-- gap --> 전50이) < 조정값 p) 조건검색 """


# def bull_market_550g(ticker):                                                       # ((전5이 <-- gap --> 전50이) < 조정값 p) 계산
#     # try:
#     last_ma5 = dy(ticker)['close'].rolling(window=5).mean()[-2]                     # 5일 종가의 평균의 전일 이평
#     last_ma50 = dy(ticker)['close'].rolling(window=50).mean()[-2]                   # 50일 종가의 평균의 전50일 이평
#     gap = last_ma5 - last_ma50                                                      # 전일 5이 - 전 50이 차이
#     gap_r = gap / last_ma50 * 100                                                   # 50이 기준 5이 몇 %
#     return gap_r
#     # except Exception as bm550g:
#     #     print('def_bm550g:', bm550g)



""" X ((검색 조건)) G ((현재가 <-- gap --> 10이) < 조정값 p) 조건검색 """


# def bull_market_p10g(ticker, price):                                                # ((현재가 <-- gap --> 10이) < 조정값 p) 계산
#     # try:
#     last_ma10 = dy(ticker)['close'].rolling(window=10).mean()[-2]                   # 10일 종가의 평균
#     gap = price - last_ma10                                                         # 현가 - 10이 차이
#     gap_r = gap / last_ma10 * 100                                                   # 10이 기준 현가 몇 %
#     return gap_r
#     # except Exception as p10g:
#     #     print('def_p10g:', p10g)


""" Test 중 ~ 2 """


# def r1_m510(ticker, price):                                                         # (5이 < 10이) 3분봉 매수시점 조건
#     try:
#         # open1 = dm1(ticker).iloc[-1]['open']                                        # 현재 1분봉 시가
#         close2 = dm1(ticker).iloc[-2]['close']                                      # 2분전 종가
#         # open2 = dm1(ticker).iloc[-2]['open']                                        # 2분전 시가
#         close3 = dm1(ticker).iloc[-3]['close']                                      # 3분전 종가
#         # open3 = dm1(ticker).iloc[-3]['open']                                        # 3분전 시가

#         last_ma5 = dm1(ticker)['close'].rolling(window=5).mean()[-2]                # 2분 종가의 5평균
#         last_ma53 = dm1(ticker)['close'].rolling(window=5).mean()[-3]                # 3분 종가의 5평균
#         last_ma10 = dm1(ticker)['close'].rolling(window=10).mean()[-2]              # 2분 종가의 10평균
#         last_ma20 = dm1(ticker)['close'].rolling(window=20).mean()[-2]              # 2분 종가의 10평균
#         last_ma50 = dm1(ticker)['close'].rolling(window=50).mean()[-2]              # 2분 종가의 10평균
#         gap_r5 = (last_ma5 - last_ma50) / last_ma50 * 100                            # 5이 <-- gap --> 50이 10이 기준
#         gap_r10 = (last_ma10 - last_ma50) / last_ma50 * 100                            # 10이 <-- gap --> 50이 10이 기준
#         gap_r20 = (last_ma20 - last_ma50) / last_ma50 * 100                            # 20이 <-- gap --> 50이 10이 기준

#         if (last_ma10 <= last_ma5) and (last_ma50 < last_ma5) and (0 <= gap_r5 <= 0.5) and (0 <= gap_r10 <= 0.5) \
#             and (0 <= gap_r20 <= 0.5) and (last_ma5 <= close2) and (last_ma53 <= close3):  # 조건 and (open1 <= price)
#             return True
#         else:
#             return False
#     except Exception as m510:
#         print('def_m510:', m510)


""" ((매수 조건)) G (5이 - 10이 위치 (3m)) 매수 조건검색 """

# # NoneType error 발생 구간
# def r3_m510(ticker, price):                                                         # (5이 < 10이) 3분봉 매수시점 조건
#     try:
#         open1 = dm3(ticker).iloc[-1]['open']                                        # 현재 3분봉 시가
#         close2 = dm3(ticker).iloc[-2]['close']                                      # 3분전 종가
#         open2 = dm3(ticker).iloc[-2]['open']                                        # 3분전 시가
#         close3 = dm3(ticker).iloc[-3]['close']                                      # 6분전 종가
#         open3 = dm3(ticker).iloc[-3]['open']                                        # 6분전 시가

#         last_ma5 = dm3(ticker)['close'].rolling(window=5).mean()[-2]                # 3분 종가의 5평균
#         last_ma10 = dm3(ticker)['close'].rolling(window=10).mean()[-2]              # 3분 종가의 10평균
#         # last_ma20 = dm3(ticker)['close'].rolling(window=20).mean()[-2]              # 3분 종가의 10평균
#         # last_ma50 = dm3(ticker)['close'].rolling(window=50).mean()[-2]              # 3분 종가의 10평균
#         gap_r = (last_ma5 - last_ma10) / last_ma10 * 100                            # 5이 <-- gap --> 10이 10이 기준
#         # gap_r2 = (last_ma5 - last_ma50) / last_ma50 * 100
#         # if (last_ma10 <= last_ma5) and (last_ma50 <= last_ma5) and (0 <= gap_r <= 0.1) \
#         #     and (open2 < close2) and (open3 < close3) and (open1 < price):  # 조건
#         if (last_ma10 <= last_ma5) and (0 <= gap_r <= 0.4) \
#             and (open2 <= close2) and (open3 <= close3) and (open1 <= price):  # 조건
#             return True
#         else:
#             return False
#     except Exception as m510:
#         print('def_m510:', m510)


""" ((매수 조건)) G (5이 - 10이 위치 (1m)) 매수 조건검색 """

# # NoneType error 발생 구간
# def r1_m510(ticker, price):                                                         # (5이 < 10이) 3분봉 매수시점 조건
#     try:
#         open1 = dm1(ticker).iloc[-1]['open']                                        # 현재 3분봉 시가
#         close2 = dm1(ticker).iloc[-2]['close']                                      # 3분전 종가
#         open2 = dm1(ticker).iloc[-2]['open']                                        # 3분전 시가
#         close3 = dm1(ticker).iloc[-3]['close']                                      # 6분전 종가
#         open3 = dm1(ticker).iloc[-3]['open']                                        # 6분전 시가

#         last_ma5 = dm1(ticker)['close'].rolling(window=5).mean()[-2]                # 3분 종가의 5평균
#         last_ma10 = dm1(ticker)['close'].rolling(window=10).mean()[-2]              # 3분 종가의 10평균
#         # last_ma20 = dm1(ticker)['close'].rolling(window=20).mean()[-2]              # 3분 종가의 10평균
#         last_ma50 = dm1(ticker)['close'].rolling(window=50).mean()[-2]              # 3분 종가의 10평균
#         gap_r = (last_ma5 - last_ma10) / last_ma10 * 100                            # 5이 <-- gap --> 10이 10이 기준
#         # gap_r2 = (last_ma5 - last_ma50) / last_ma50 * 100
#         # if (last_ma10 <= last_ma5) and (last_ma50 <= last_ma5) and (0 <= gap_r <= 0.1) \
#         #     and (open2 < close2) and (open3 < close3) and (open1 < price):  # 조건
#         if (last_ma10 <= last_ma5) and (last_ma50 < last_ma5) and (0 <= gap_r <= 0.4) \
#             and (open2 <= close2) and (open3 <= close3) and (open1 <= price):  # 조건
#             return True
#         else:
#             return False
#     except Exception as m510:
#         print('def_m510:', m510)


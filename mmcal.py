import pyupbit
from UBiC_Rotate_data import dy, km, upbit1, gb
import pickle
import time, os
from datetime import datetime, timedelta
import pandas as pd
from UBiC_Search_def import get_orderi, t_c, myasset, cal_ask3, ex_item, cnt_p
from set_config import b_money, ofn1
from decimal import Decimal
from pandas import DataFrame as df
import numpy as np

print("gethering start ~")

cal = 0
while True:
    # start = time.time()
    cask = get_orderi('done', 'ask', 'i', ofn1)         # 매도완료 정보 호출
    cal_l = []
    # ==================== 자산 확인용 추가 ========================= #
    try:
        bl = gb(upbit1)[0]                                                        # 자산정보
        tsum, tbidm, tbidp, su = myasset(upbit1)
        # tsum = myasset(upbit1)[0]
        # tbidm = myasset(upbit1)[1]                                             # 총 매수 금액
        # tbidp = myasset(upbit1)[2]
        now = datetime.now()                                                  # 저장 전 현 날짜
        now1 = datetime(now.year, now.month, now.day) + timedelta(0)           # 현 날짜 재구성
        day = ("%s년%s월%s일" %(now1.year, now1.month, now1.day))               # 2021년3월3일
        yday1 = now1 + timedelta(-1)                                           # 하루 전날짜 생성
        yday = ("%s년%s월%s일" %(yday1.year, yday1.month, yday1.day))           # 2021년3월3일
        ydaym = ("%s년%s월" %(yday1.year, yday1.month))
    except TypeError as mycal:
        print(mycal)
    # ============================================================ #
    try:
        if os.path.isfile('/root/UBiCauto/data/mycal.pickle'):
            with open('/root/UBiCauto/data/mycal.pickle', 'rb') as fr1:
                mycal = pickle.load(fr1)
        else:
            mycal = df(index = range(0), columns = ['T_Asset','Profit','ROE','Ct'])       # 빈 mycal 생성

        if os.path.isfile('/root/UBiCauto/data/mycal_m.pickle'):
            with open('/root/UBiCauto/data/mycal_m.pickle', 'rb') as fr1:
                mycal_m = pickle.load(fr1)
        else:
            mycal_m = df(index = range(0), columns = ['T_Asset','Profit','ROE','Ct'])     # 빈 mycal_m 생성

        if os.path.isfile('/root/UBiCauto/data/cal_l.pickle'):
            with open('/root/UBiCauto/data/cal_l.pickle', 'rb') as fr1:
                cal_l = pickle.load(fr1)
        else:
            cal_l = []

        if os.path.isfile('/root/UBiCauto/data/add_num.pickle'):                            # 매수가를 가져오기 위해 추매 dict 호출
            with open('/root/UBiCauto/data/add_num.pickle' , 'rb') as fr:
                add_num = pickle.load(fr)

        if os.path.isfile('/root/UBiCauto/data/cal_d.pickle'):
            with open('/root/UBiCauto/data/cal_d.pickle', 'rb') as fr2:
                cal_d = pickle.load(fr2)
            # now = datetime.now()
            # now1 = datetime(now.year, now.month, now.day) + timedelta(0)    # 금일 자정 데이터 취합시작 날짜,시간 설정
            bf_mid = datetime(now.year, now.month, now.day, hour=23, minute=31, second=1) + timedelta(0)     # 자정 데이터 취합완료 날짜,시간 설정59 56
            mid = datetime(now.year, now.month, now.day) + timedelta(1)     # 익일 자정 데이터 취합완료 날짜,시간 설정
            first_day1 = datetime(now.year, now.month, 1, second=1)          
            mkt = cask[0]['market'] 
            uid = cask[0]['uuid']                                               # uuid 호출
            ct = cask[0]['created_at']                                          # 시간 호출
            volr = float(cask[0]['remaining_volume'])                                  # 매도 후 남은 잔량
            c_time = t_c(ct)                                                    # 시간 변환
            cal_day = c_time.year, c_time.month, c_time.day                     # 매일 check 날짜 생성            
            if uid == cal_d['uuid']:                                            # 최종매도 uuid와 현재매도 uuid 비교
                # print('uid = uuid')
                pass
            elif (now1 < c_time < mid) and (uid != cal_d['uuid']) and (float(volr) <= 0.1):              # 자정전 저장 시간범위 포함되면 uuid가 틀릴경우 추가
                ask_p = float(cask[0]['price'])                                 # 매도금액
                vol = float(cask[0]['volume'])                                 # 매도수량
                ask_p = round(ask_p * vol, 2)                                   # 매도 총액 
                bcnt = add_num.get(mkt)[2]                                            # 마지막 매수종목의 매수가 호출
                adc = add_num.get(mkt)[0]
                if ask_p < bcnt:
                    pass                
                else:
                    # print(ask_p, bcnt)
                    # print(cal_ask3(ask_p, bcnt))
                    cal = round(cal_ask3(ask_p, bcnt), 1)                           # 매도 후 수익금액
                    # print(cal)
                    cal_l.insert(0, cal)                                            # list 추가
                    cal_d = cask[0]                                                 # 최종 매도종목 정보 저장
                    with open('/root/UBiCauto/data/cal_l.pickle', 'wb') as fw:        # 매도 리스트 파일로 저장
                        pickle.dump(cal_l, fw)
                    # print(cal)
                    with open('/root/UBiCauto/data/cal_d.pickle', 'wb') as fw:        # 최종매도 종목 데이터를 파일로 저장
                        pickle.dump(cal_d, fw)
            
            if bf_mid <= now <= bf_mid + timedelta(minutes=7):                          # 데이터 저장 시간 범위 포함여부 확인

                while True:                                                             # 금일 데이터 저장시 까지 반복
                    # tsum = myasset(upbit1)[0]                                             # 보유자산 총계
                    day = ("%s년%s월%s일" %(now.year, now.month, now.day))               # 형식:2021년3월3일
                    yday0 = now1 + timedelta(-1)                                        # 하루 전
                    yday = ("%s년%s월%s일" %(yday0.year, yday0.month, yday0.day))        # 날짜 변경                
                    ysum = mycal.iloc[-1]['T_Asset']; roe = round(((tsum - ysum) / tsum) * 100, 2)  # 계산
                    calsum = round((tsum-ysum), 1)
                    if day not in mycal.index:
                        mycal.loc[day] = [tsum, calsum, roe, len(cal_l)]                            # 변수 저장                
                        with open('/root/UBiCauto/data/mycal.pickle', 'wb') as fw:           # 자산 데이터를 파일로 저장
                            pickle.dump(mycal, fw)
                    else:
                        break

                cal_l = []
                with open('/root/UBiCauto/data/cal_l.pickle', 'wb') as fw:                                             # 매도금 초기화
                    pickle.dump(cal_l, fw)
            if first_day1 <= now <= (first_day1 + timedelta(minutes=7)): 
                while True:
                    yday0 = now1 + timedelta(-1)                                                                        # 하루 전
                    yday1m = ("%s년%s월" %(yday0.year, yday0.month))                                                 # 년,월 계
                    yday2m = ("%s%s" %(yday0.year, yday0.month))
                    if yday1m not in mycal_m.index:
                        mycal_m.loc[yday1m] = [tsum, mycal['Profit'].sum(), mycal['ROE'].sum(), mycal['Ct'].sum()]
                        with open('/root/UBiCauto/data/mycal_m.pickle', 'wb') as fw:                                    # 자산 데이터를 파일로 저장
                            pickle.dump(mycal_m, fw)
                    else:
                        break
                with open('/root/UBiCauto/data/mycalz_%s.pickle' %(yday2m), 'wb') as fw:           # 월말 결산 저장
                    pickle.dump(mycal, fw)
                # mycal = df(index = range(0), columns = ['T_Asset','Profit','ROE','Ct'])        # mycal 초기화
                mycal = mycal.iloc[-1:]
                mycal.iloc[-1,1:4] = 0.0                                                         # 마지막 행의 첫번째열 부터 3번째 열까지 '0' 초기화
                with open('/root/UBiCauto/data/mycal.pickle', 'wb') as fw:                       # 빈 자산 데이터를 파일로 저장
                    pickle.dump(mycal, fw)
        else:
            with open('/root/UBiCauto/data/cal_d.pickle', 'wb') as fw:        # 데이터를 파일로 저장
                pickle.dump(cask[0], fw)  
        # ==================== 자산 확인용 추가 ========================= #
        ysum = mycal.iloc[-1]['T_Asset']; roe = round(((tsum) - (ysum)) / tsum * 100, 2)    # 전일 자산, 수익률
        calsum = round((tsum - ysum), 1)
        mycal.columns.name = '날짜'  
        mycal.loc[ydaym] = [tsum, mycal['Profit'].sum(), mycal['ROE'].sum(), mycal['Ct'].sum()]

        ret_ct = ex_item(add_num, bl)
        ret_ct = ret_ct[1]
        rctt = sorted(cnt_p(ret_ct).items(), key=lambda x: x[1], reverse=True)
        print('\n')

        print("금일수익: %s원     /  횟수: %s     /  보유종목수: %s" %(format(calsum, ','), len(cal_l), len(add_num)))
        print("보유자산: %s원  /  ROE : %s%% \n매수금액: %s원   /  매수: %s%%\n추매현황: %s\n" %(format(tsum, ','), roe, format(tbidm, ','), format(tbidp, ','), rctt))

        display(mycal.iloc[-6:,:])                  # 끝에서 5번째 이후로만 표시    
        print('\n')

        # ============================================================ #
    except Exception as mycal:
        pass
    # print("--- %s seconds ---" % round((time.time() - start), 2))
    time.sleep(0.3)

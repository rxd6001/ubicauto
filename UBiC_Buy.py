# -*- coding:utf-8 -*-

import pyupbit
import operator
# ========================= 조건 함수 호출 ========================= #
from UBiC_Search_def import bull_market_590, bull_market_pg, bull_market_3dup, b1_decline_m1, b2_decline_m1

""" ========================================================================== """
from UBiC_Search_def import bull_market_p5g, bull_market_510g, bull_market_1050g

# from UBiC_Search_def import bull_market_p10g, bull_market_550g

""" ============================================================ """
# from UBiC_Search_def import bull_gap_550

from UBiC_Search_def import bull_gap_p5

from UBiC_Search_def import search_s, linenumber

""" ================================================== """
from UBiC_Search_def import buy_avr_price_10, buy_avr_price_20, buy_avr_price_50, ma5_under, t_c, perct

""" ============================================================================================= """
from UBiC_Search_def import rain_market_po, rain_market_yho, rain_market_bho, rain_market_1ho

""" ======================================================================== """
from UBiC_Search_def import get_orderi, myasset      # 매수, 매도 정보

""" ======================================================================== """
# from UBiC_Rotate_data import cp1, cp2, gb
from UBiC_Rotate_data import gb

""" =============================================================================== """
from datetime import datetime, timedelta     # 시간 계산에 필요

import pickle
import math
import time
import os
import threading

def ubic_buy(id):

    f = open(("/root/UBiCauto/Acct/upbit%s.txt") %(id))        # 파일 열기
    lines = f.readlines()                       # 라인을 일러들임
    access = lines[0].strip()                   # access key '\n' 0번 행 불러오기
    secret = lines[1].strip()                   # secret key '\n' 1번 행 불러오기
    f.close()                                   # 파일 닫기

    upbit = pyupbit.Upbit(access, secret)      # 업비트 로그인

    now = datetime.now()
    s_time = 1        # 1cycle 주기
    
    # """ 매수 종목 검색  """
    r_tho_1_dic = {}; s2s_dic = {}
    while True:
        start_time = time.time()                    # 시간 측정 시작

        # with open('/root/UBiCauto/data/ext_item%s.pickle' %(id), 'rb') as feit:       # 보유종목 중 매수제외 종목 불러오기
        #     ext_item1 = pickle.load(feit)
        # ext_b = ext_item1['ext_b']

        with open('/root/UBiCauto/data/ext_itemB.pickle', 'rb') as feit:        # 신규 매수제외종목 불러와서 적용
            ext_itemB = pickle.load(feit)
        ext_b = ext_itemB['ext_b']

        with open('/root/UBiCauto/data/set_cfg%s.pickle' %(id), 'rb') as fset:
            ubic_conf = pickle.load(fset)

        bp = ubic_conf['bp']; b_count = ubic_conf['b_count']; blow_money = ubic_conf['blow_money']; bg = ubic_conf['bg']
        gt = ubic_conf['gt']; code = ubic_conf['code']; y3h3or = ubic_conf['y3h3or']; tho_30r = ubic_conf['tho_30r']; tho_1r = ubic_conf['tho_1r']
        tpor = ubic_conf['tpor']; p5g = ubic_conf['p5g']; p10g = ubic_conf['p10g']; p510g = ubic_conf['p510g']; p550g = ubic_conf['p550g']
        p1050g = ubic_conf['p1050g']; nw = ubic_conf['nw']; npct = ubic_conf['npct']; yg = ubic_conf['yg']


        # mybal = round(myasset(upbit)[3], 1)          # 예전 코드

        mybal = upbit.get_balance_t()                  # 매수가능금액
        mb1 = math.trunc(mybal / 10000) * 10000         # 10000자리까지 0으로

        b_money = int((mb1 * perct(bp)) / b_count)    # 매수금액 계산


        if b_money < 5100 :
            b_money = blow_money
        
        if b_money < blow_money:                        # 최소 매수금액 'blow_money' 로 제한
            b_money = blow_money                        # 최저 매수금액 설정

        ubic_conf['b_money']= b_money

        with open('/root/UBiCauto/data/set_cfg%s.pickle' %(id), 'wb') as fw:
            pickle.dump(ubic_conf, fw)

        s2 = search_s()                             # 종목검색 클래스

        bull_dict = {}                              # 종목, g550값 : dict
        order_list = []                             # 주문 리스트
        sbl = []                                    # 실제 매수가능한 리스트

        try:    # 종목 및 현재가 가져오기
            with open('/root/UBiCauto/data/cp_e.pickle', 'rb') as fr1:
                cu_p = pickle.load(fr1)                                       # 전체 종목과 현재가 dict 'cu_p' 로 바인딩
            [cu_p.pop(key, None) for key in ext_b]                # 종목 전체 현재가에서 ext 에 있는 종목 제외, None 시 넘어감, 현재 불필요
        except Exception as cu_p:
            print(f'{linenumber()}p::error:현재가: {cu_p}')

        """ (( 종목 검색 시작 )) """
        """ 조건에 맞는 모든 원화코인 종목을 ticker, g550 값으로 하나씩 바인딩 bull_list 만듦(dict) """
        # try:
        if cu_p:                                                            # 현재가에 값이 있을 때만 실행
            # if code ==1:                                                  # 기본설정 실행(약상승장)  
            for ticker, price in cu_p.items():
                # ============================== day == check ================================ #
                """ # --------------------- (안정적) 정렬 기준 값 (적극적) --------------------- # """
                try:            # None type 시 이전 값으로 대체
                    r_tho_1 = rain_market_1ho(ticker)                     # 금일 (고가 - 시가) 차 : 30(%) (금일) (기준 60분: 시가)
                    if r_tho_1:
                        r_tho_1_dic[ticker] = r_tho_1
                except Exception as e:
                    r_tho_1 = r_tho_1_dic.get(ticker)
                    # print(f'id:({id}), {len(r_tho_1_dic)}')
                    print(f'{linenumber()}p::id:{id}:error:r_tho_1: {e}\n {ticker}: {r_tho_1}')
                r_y3h3o = rain_market_yho(ticker)                     # 전3일(고가 - 시가) 차 : 60(%) (기준전: 시가)
                r_tho_30 = rain_market_bho(ticker)                    # 금일 (고가 - 시가) 차 : 30(%) (금일) (기준 24시간: 시가)
                r_tpo = rain_market_po(ticker, price)                 # 금일 (현가 - 시가) 차 : 30(%) (기준금 : 시가)
                # print(ticker, r_tho_30, r_y3h3o, r_tpo)                # 확인 시
                """ # -------------------------------- 매수 범위(현 yg이평 - 20% 이하일 경우 매수 ) 조정 ----------------------- # """
                # b_yc = bull_market_yc(yg, ticker)                       # 전일(yg이평 < 종가) 첫번째 기준 보다 넓게

                # r_5up = bull_market_1up(ticker)                       # 적은종목 투자시 전일 양봉, 5이상
                # b_o5 = bull_market_o5(ticker)                       # 정렬 : 5이 (전일) < 시가(금일)
                # b_po = bull_market_po(ticker, price)                # 정렬 : 시가(금일) < 현가(금일)
                """ ---------------------------------- 매수 범위(현가가 nw이평 이상일 경우 매수) 조정 ---------------------------------------- """
                b_pg = bull_market_pg(npct, nw, ticker, price)              # 정렬 : nw(90)이평(전일) < 현가(금일) (기준 : 전일)

                """ --------------------------------------------------------------------------------------- """
                # b_510 = bull_market_510(ticker)                     # 정렬 : (전일)(10이 < 5이)  (기준 : 전일)
                # b_590 = bull_market_590(ticker)                     # 정렬 : (전일)(50이 < 5이)  (기준 : 전일)
                # b_1050 = bull_market_1050(ticker)                   # 정렬 : (전일)(50이 < 10이) (기준 : 전일)
                """ # ---------------- (상승폭 저) 정렬 기준 조건 (상승폭 고) ----------------- # """
                b_p5g = bull_market_p5g(ticker, price)              # 6%  현가 -  5이(전일) 차이 (기준 : 전5이)
                # b_p10g = bull_market_p10g(ticker, price)            # 현가 - 10이(전일) 차이 5(%) 전기준 : 10이)
                b_510g = bull_market_510g(ticker)                  # 15%  전일(5이 - 10이) 차이 (기준 : 10이)
                # b_550g = bull_market_550g(ticker)                   # 전일(5이 - 50이) 차이 10(%) (기준 : 50이)
                b_1050g = bull_market_1050g(ticker)                 # 60%  전일(10이 - 50이) 차이 (기준 : 50이)
                # print(f'{linenumber()}p::종목:{ticker}, b_yc:{b_yc}, b_pg:{b_pg}, price:{price}')

                """ 검색 조건 : 시작가 < 현재가 < 시가의 5%, 50일 < 5일, 고가 <= 시작가 10% """
                # if b_pg and b_590 and (b_p5g <= p5g) and (b_510g <= p510g) and (b_1050g <= p1050g) : # 매수종목 검색           
                if b_pg and (b_p5g <= p5g) and (b_510g <= p510g) and (b_1050g <= p1050g) : # 매수종목 검색  
                    if (r_tpo < tpor) and (r_y3h3o < y3h3or) and (r_tho_30 < tho_30r) and (r_tho_1 < tho_1r):       # 조건값 설정
                        try:            # None type 시 이전 값으로 대체
                            s2s = s2.r1_m510(ticker, price)
                            if s2s:
                                s2s_dic[ticker] = s2s
                        except Exception as e:    
                            s2s = s2s_dic.get(ticker)
                            print(f'id:({id}),{s2s}')
                            print(f'{linenumber()}p::error:s2s: {e}\n {ticker}: {s2s}')
                        gp5 = bull_gap_p5(ticker, price)                        # '현재가 - 5' 바인딩
                        if code == 2 and s2s:                                
                            bull_dict[ticker] = round(gp5, 4)                       # dict volume 값 소수 4자리까지 저장
                        elif code == 1:                                
                            # g550 = bull_gap_550(ticker)                             # '5 - 5 바인딩
                            bull_dict[ticker] = round(gp5, 4)                       # dict volume 값 소수 4자리까지 저장

                        # 새로운 종목이 추가 시 2일전 데이터가 없기 때문에 "single positional indexer is out-of-bounds" 발생
                        # dataframe 이 비어있던지 이상이 있을 때 나타남 ( 이평 데이터 취합 후 error 예상)

            s_bull_list = sorted(bull_dict.items(), key=lambda x: x[1], reverse=False)  # True : 높은 순 정렬, False : 낮은 순 정렬, list(tuple) [('종목', 실수값),...] 로 바인딩 
            # 미적용
                # s_bull_list = sorted(bull_dict.items(), key=operator.itemgetter(1))
                # 검색 종목의 'gp50' or 'g550'값 기준 내림차순 정렬 목록

                # elif code == 2:                                               # 여러 종목 검색 기준(3분)                  
                #     # print('code = 2')
                #     # pass
                #     for ticker, price in cu_p.items():
                #         # r_y3h3o = rain_market_yho(ticker)                     # 전3일(고가 - 시가) 차 : 25(%) (기준전: 시가)
                #         s2s = s2.r1_m510(ticker, price)
                #         # if (r_y3h3o < y3h3or) and s2s[0]:
                #         if s2s[0]:
                #             bull_dict[ticker] = round(s2s[1], 4)
                #     s_bull_list = sorted(bull_dict.items(), key=lambda x: x[1], reverse=False)  # list(tuple) value 로 정렬
        # except Exception as code:
        #     print(f'{linenumber()}p::error:e-time: {datetime.now()}, code:{code}')
        time.sleep(s_time)
        try:    # 보유종목에 없는 종목을 확인 후 종목리스트 저장
            bl = gb(upbit)[0]                                                        # 보유종목 가져오기
            for sn in s_bull_list:                                                    #
                b_name = sn[0]
                if b_name not in bl:                                                  # 보유종목에 없는 종목을 확인 후 종목리스트 저장
                    sbl.append(b_name)
        except Exception as sbl:
            print(f'{linenumber()}p::error:sbl: {sbl}')

        blcnt = len(bl)                                                           # 거래불가 종목 제외 후 blcnt로 조건문에 수량 적용
        try:                # 종목검색조건 자동 s/w 
            # if (blcnt < b_count) and (len(s_bull_list) == 0) and code == 1:
            if (blcnt < b_count) and (len(sbl) == 0) and code == 2:                   # 설정수이하, sbl = 0, code = 2, 수량부족이고 2번일 때 검색 안 됨 => 1로 변경
                code = 1

                ubic_conf['code'] = 1
                with open('/root/UBiCauto/data/set_cfg%s.pickle' %(id), 'wb') as fset:
                    pickle.dump(ubic_conf, fset)
                print(f'{linenumber()}p::보유종목수 ≦ 매수가능종목수(설정값), 매수가능수량 = 0, code(2):수량부족 ⇨ ({code}) 변경')
            elif (blcnt < b_count) and (0 < len(sbl)) and code == 2:                   # 설정수이하, 0 < sbl, code = 2, 수량부족이고 2번일 때 검색 될 때 2번으로 매수
                code = 1           

                ubic_conf['code'] = 1
                with open('/root/UBiCauto/data/set_cfg%s.pickle' %(id), 'wb') as fset:
                    pickle.dump(ubic_conf, fset)
                print(f'{linenumber()}p::보유종목수 ≪ 매수가능종목수(설정값), 매수가능수량 ≪ 0, code(2):수량부족 ⇨ ({code}) 변경')
            elif (blcnt == b_count) and code ==1 :                                    # 설정수동일, code = 1, 수량가득이고 1번일 때 => 2로 변경
                code = 2

                ubic_conf['code'] = 2
                with open('/root/UBiCauto/data/set_cfg%s.pickle' %(id), 'wb') as fset:
                    pickle.dump(ubic_conf, fset)

                print(f'{linenumber()}p::보유종목수 = 매수가능종목수(설정값), code(1):수량충족 ⇨ ({code}) 변경')
            elif (blcnt == b_count) and (len(sbl) == 0) and code == 2 :                                    # 설정수동일, code = 2, 수량가득이고 2번일 때 => 1로 변경
                code = 1

                ubic_conf['code'] = 1
                with open('/root/UBiCauto/data/set_cfg%s.pickle' %(id), 'wb') as fset:
                    pickle.dump(ubic_conf, fset)

                print(f'{linenumber()}p::보유종목수 = 매수가능종목수(설정값), 매수가능수량 없음, code(2):수량충족 ⇨ ({code}) 변경')
            elif (blcnt < b_count) and (len(sbl) == 0) and code == 1 :                                    # 설정수동일, code = 2, 수량가득이고 1번일 때 => 2로 변경
                code = 2

                ubic_conf['code'] = 2
                with open('/root/UBiCauto/data/set_cfg%s.pickle' %(id), 'wb') as fset:
                    pickle.dump(ubic_conf, fset)

                print(f'{linenumber()}p::보유종목수 ≪ 매수가능종목수(설정값), 매수가능수량 없음, code(1):수량충족 ⇨ ({code}) 변경')

            time.sleep(1)   # 종목검색 조건 자동 선택
        except Exception as error:
            print(f'{linenumber()}p::error:code: {error}')


        """ (( 신규 매수 검색 시작 )) ( g550 오름차순 정렬값) """

        try:    # 매수대기 종목명 가져오기
            # bid_w_list = get_order_bid()                    # 매수 대기 종목명 리스트 가져오기 (미사용)
            bid_w_list = get_orderi('wait', 'bid', 'n', "/root/UBiCauto/Acct/upbit%s.txt" %(id))            # 매수 대기 종목명 리스트 가져오기
        except Exception as bid:
            print(f'{linenumber()}p::error:Buy_bid: {bid}')


        """ ==============================  신규 매수 감시 ============================== """
        
        try:    # 보유종목 리스트 호출
            cbid = get_orderi('done', 'bid', 'n', "/root/UBiCauto/Acct/upbit%s.txt" %(id))                        # 보유종목명 list  
            with open('/root/UBiCauto/data/cp_e.pickle', 'rb') as fr1:            
                cu_p = pickle.load(fr1)                                       # 전체 종목과 현재가 dict 'cu_p' 로 바인딩
            [cu_p.pop(key, None) for key in ext_b]                # 종목 전체 현재가에서 ext 에 있는 종목 제외, None 시 넘어감, 현재 불필요
        except Exception as cu_p:
            print(f'{linenumber()}p::error:Buy_cu_p: {cu_p}')


        try:    # 조건검색 후 신규종목 매수
            if cu_p:                                           # 현재가에 값이 있을 때만 실행
                for b_name in sbl:                              # 검색 종목을 buy_name 에 바인딩
                    # b_name = sn[0]                              # b_name 생성(검색 된 추천 종목)
                    # print(b_name)
                    """ b_name 이 보유종목 에 없고 보유수량 보다 적고 시가-현재가 차이 5% 아래 """
                    # b_name 이 '(검색종목에 없고) & (검색종목 수 < 보유제한수) & (매수종목 리스트가 비었거나 매수종목에 없거나)'
                    
                    if (b_name not in bl) and (b_name not in order_list) and (blcnt < b_count) and (b_name not in bid_w_list) and (mybal >= b_money) :       # 검색종목이 bl에 없고, 매수제한수 이하, 매수대기에 없을 시 
                        # 미적용
                            # print(b_name, "신규 매수 대기 시작...")
                            # upbit.buy_market_order(b_name, b_money)      # (( 시장가 )) 매수
                            # time.sleep(0.2)
                            # sbl.append(b_name)

                        """ (원화마켓 전 종목의 현재가) 가져오기 """
                        if b_name in cu_p.keys():                                      # 보유종목의 현재가 가져오기
                            price = cu_p[b_name]                                       # 해당종목(b_name)의 현개가를 price 에 바인딩
                            b2_bm1 = b2_decline_m1(b_name)                                   # 매수지연 조건     ***
                            # 미적용 
                                # gr_m510 = r3_m510(b_name, price)                            # 매수조건 계산(3m)
                                # gr_m510 = r1_m510(b_name, price)                            # 매수조건 계산(1m)
                                # if True == gr_m510:                                         # 조건 == True 일 경우 매수 대기
                            if b2_bm1[0] and (price < b2_bm1[1]):                       # decline + 매수지연기준   ***
                                pass
                                """ ===================== 지정가 매수 주문 ===================== """
                            else:
                                bid_p = price - (price * bg)                            # 매수 목표가 계산 ( 현재가의 - 0.1 %)(v)
                                b_o = pyupbit.get_tick_size(bid_p)                      # 매수 호가 계산(v)
                                bid_v = b_money / bid_p                                 # 매수 수량 계산(목표가) (매수금액 기준)(v)
                                # b_order = upbit.buy_limit_order(b_name, b_o, bid_v)  # 지정가 매수 실행 (목표가)(v)
                                b_order = upbit.buy_limit_order(b_name, price, bid_v)  # 지정가 매수 실행 (현재가)(v)
                                with open('/root/UBiCauto/find%s.log' %(id),'a') as fw:
                                    print(f'{linenumber()}p::{now}: 종목:{b_name}, 매수가:{price}', file=fw)

                                order_list.append(b_name)                               #  매수 오더리스트 추가
                                time.sleep(5)
                                # 미적용
                                    # b_o = pyupbit.get_tick_size(price)                      # 매수 호가 계산 (미적용)
                                    # bid_v = b_용oney / price                                 # 매수 수량 계산(현재가) (매수금액 기준) (미적용)
                                    # b_order = upbit.buy_limit_order(b_name, price, bid_v)  # 지정가 매수 실행(현재가) (미적용)
                                    # upbit.buy_market_order(b_name, b_money)                # (( 시장가 )) 매수 미적용
                    time.sleep(5)
                    bll = gb(upbit)[0]                 # 보유종목 수량 재호출 위함
                    bllcnt = len(bll)                   # 매도 불가종목 6개 제외
                    print(f'{linenumber()}p::보유종목수: {blcnt}, 보유종목수(매도제외수량적용): {bllcnt}')
                    if (b_count <= bllcnt):             # 종목수 체크 후 매수 정지
                        break
        except Exception as b2:
            print(f'{linenumber()}p::error:e-time: {datetime.now()}, buy_b2: {b2}')

        time.sleep(s_time)
        try:    #매수대기 정보 호출
            bid_w_i = get_orderi('wait', 'bid', 'i', "/root/UBiCauto/Acct/upbit%s.txt" %(id))                            # 매수 대기목록 정보 리스트
        except Exception as wbid_i:
            print(f'{linenumber()}p::error:Buy_wbid: {wbid_i}')


        """ 매수 조건을 만족하지 못하면 아래 조건을 비교하여 매수대기 취소 절차를 진행 """
        try:    # 매수대기 취소
            for bn in range(len(bid_w_list)):                                   # list 에서 매수대기 종목(dict) 항목 추출
                uuids_m = bid_w_i[bn]['market']                                 # 매수대기종목정보에서 가져 온 종목이름
                if uuids_m in ext_b:
                    pass
                else:
                    uuids_id = bid_w_i[bn]['uuid']                                  # bid_w_i[bn] 번째 종목의 'uuid' 의 값
                    a_time1 = bid_w_i[bn]['created_at']                             # 매수대기종목 order 시간
                    a_time = t_c(a_time1)                                           # 계산을 위해 order 시간 형식 변환
                    mt = (a_time + timedelta(minutes=gt))                           # 매수대기 시간 10분 지난 시간 계산
                    # 지정시간이 지났거나, 자산목록에 종목이 있는지,  보유수량 < 제한수량 인지 확인(조건)
                    if (mt <= datetime.now()) or (uuids_m in bl) or (b_count <= blcnt):
                        b_cancel = upbit.cancel_order(uuids_id)                    # 매수 대기 취소
        except Exception as b3:                                                 # TypeError 예외처리 구간
            print(f'{linenumber()}p::error:e-time: {datetime.now()}, buy_b3: {b3}')


        # os.system('clear')
        print(f'{linenumber()}p::code: {code}\n')       

        print(f'{linenumber()}p::' + '\033[1m' + f'id : {id}, 매수대기종목수: {len(bid_w_i)}' + '\033[0m' + f'\n보유종목수(매수제외적용): {blcnt} :  매수가능종목수: {len(sbl)}\n')      # 조건검색 종목의 'g550'값 기준 내림차순 정렬 목록  **
        print(f'{linenumber()}p::실제매수가능한종목:⚜\n{sbl}')
        print(f'{linenumber()}p::id:{id} --- (1) Cycle time: {round((time.time() - start_time), 3)} seconds ---\n')          # 1Cycle 시간

if __name__ == '__main__':
    id_lists = ['1', '2', '3']
    thread_dicts = {}
    for id in id_lists:         # thread 실행
        t = threading.Thread(target=ubic_buy, args=(id, ))
        t.daemon = True
        t.start()
        thread_dicts[id] = t
        print(t)

    while True:         # health check
        for id in id_lists:
            if thread_dicts[id].is_alive():
                print(f'{linenumber()}p::id:( {id} )-{thread_dicts[id].is_alive}')
            else:
                t = threading.Thread(target=ubic_buy, args=(id, ))
                t.daemon = True
                t.start()
                thread_dicts[id] = t
        time.sleep(30)
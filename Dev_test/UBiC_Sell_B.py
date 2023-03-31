# -*- coding:utf-8 -*-

import pyupbit
import time
from datetime import datetime
import os
import pickle
from UBiC_Search_def import buy_avr_price_5, buy_avr_price_10, buy_avr_price_20, buy_avr_price_30, buy_avr_price_40, \
    buy_avr_price_50, buy_avr_price_60, buy_avr_price_70, buy_avr_price_80, buy_avr_price_90, ma5_under, s1_bull_m1, \
    b2_decline_m1, get_orderi, abp_check, get_tick_s, t_c, ex_item, perct, adn_insert, myasset, askper, add_rw0, \
    add_rw1, add_rw2, add_rw3, add_rw4, add_rw5, add_rw6, add_rw7, add_rw8, add_rw9, add_rw10, add_rwav5, add_rwav10,\
    add_rwav20, add_rwav30, add_rwav40, add_rwav50, add_rwav60, add_rwav70, add_rwav80, add_rwav90, add_rwinit

from UBiC_Rotate_data import gb, upbit2
from datetime import datetime, timedelta

""" ======= 추매파일이 경로에 있으면 불러오고 없으면 통과 ======== """
if os.path.isfile('/root/UBiCauto/data/add_num2.pickle'):
    with open('/root/UBiCauto/data/add_num2.pickle', 'rb') as fr:
        add_num = pickle.load(fr)    

now = datetime.now()    # 현재시간 호출
rwnum = 2           # add_num에 필요한 변수
ex_num = 2          # add_num 종목제외 시 필요(ex_item(bl, ex_num))

while True:

    start_time = time.time()                                                  # time check

    with open('/root/UBiCauto/data/set_cfg2.pickle', 'rb') as fset:
        ubic_conf = pickle.load(fset)

    with open('/root/UBiCauto/data/ext_item2.pickle', 'rb') as fset:
        ext_item = pickle.load(fset)

    ext_s = ext_item['ext_s']
    ext_a = ext_item['ext_a']

    ask_p = ubic_conf['ask_p']; ask_ug = ubic_conf['ask_ug']; ask_pp = ubic_conf['ask_pp']; agt = ubic_conf['agt']; sell_cont = ubic_conf['sell_cont']
    adsp = ubic_conf['adsp']; ap = ubic_conf['ap']; u_p = ubic_conf['u_p']; l_money = ubic_conf['l_money']; ag1 = ubic_conf['ag1']; ag2 = ubic_conf['ag2']
    ag3 = ubic_conf['ag3']; ag4 = ubic_conf['ag4']; ag5 = ubic_conf['ag5']; ag6 = ubic_conf['ag6']; ag7 = ubic_conf['ag7']; ag8 = ubic_conf['ag8']
    ag9 = ubic_conf['ag9']; ag10 = ubic_conf['ag10']; adp1 = ubic_conf['adp1']; adp2 = ubic_conf['adp2']; adp3 = ubic_conf['adp3']; adp4 = ubic_conf['adp4']
    adp5 = ubic_conf['adp5']; adp6 = ubic_conf['adp6']; adp7 = ubic_conf['adp7']; adp8 = ubic_conf['adp8']; adp9 = ubic_conf['adp9']; adp10 = ubic_conf['adp10']
    abptime = ubic_conf['abptime']; blow_money = ubic_conf['blow_money']

    ofn2 = '/root/UBiCauto/Acct/upbit2.txt'

    t_tp = []                                             # 평가손익(리스트)

    try:
        bl, abp1, tb1 = gb(upbit2)                              # 보유종목명, 평단, 보유수량 호출                        
        tsum, tbidm, tbidp, summ = myasset(upbit2)              # 자산정보 한 번에 호출
        summ = round(summ, 1)
    except Exception as up:
        print('sell_up:', up)

    # """ ================ UBiC_Rotate_data 에서 보유종목 가져오기 ================ """

    try:    # 보유종목 현재가 호출
        with open('/root/UBiCauto/data/cp.pickle', 'rb') as fr1:            # mycal 불러오기
            cu_p = pickle.load(fr1)                                       # 전체 종목과 현재가 dict 'cu_p' 로 바인딩
        # [cu_p.pop(key, None) for key in ext_s]                # 종목 전체 현재가에서 ext 에 있는 종목 제외, None 시 넘어감, 현재 불필요
        # [bl.remove(key) for key in ext_s if key in bl]        # 매도 제외 종목 설정 
    except Exception as s_cu_p:
        print(s_cu_p)

    # """ ================ 매도 시작 ================ """
    try:
        # if cu_p:                                                    # 현재가에 값이 있는 경우만 이하 실행
        for e in bl:                                            # 자산('bl') 리스트를 하나씩 'e'로 가져 옴
            if abp_check(e, abptime, ofn2):                           # 매수 평단 선택 (체크)
                abp = abp_check(e, abptime, ofn2)                     # 매수평단 최근 매수완료 정보에서 가져 옴
            else:
                abp = abp1[e]                                   # 매수 평균 "자산정보"(업비트)에서 호출                                                       
            tb = tb1[e]                                         # 종목 보유수량 호출
            """ S ~~~ 추매 시점 (소수점 5자리에서 반올림) """

            addprice_1 = round((abp - (abp * perct(adp1))), 6)       # 추매 시 평단의 -3 # 5% 지점 (코인장 변동폭이 적을 때 적용?)
            addprice_2 = round((abp - (abp * perct(adp2))), 6)
            addprice_3 = round((abp - (abp * perct(adp3))), 6)
            addprice_4 = round((abp - (abp * perct(adp4))), 6)
            addprice_5 = round((abp - (abp * perct(adp5))), 6)
            addprice_6 = round((abp - (abp * perct(adp6))), 6)
            addprice_7 = round((abp - (abp * perct(adp7))), 6)
            addprice_8 = round((abp - (abp * perct(adp8))), 6)
            addprice_9 = round((abp - (abp * perct(adp9))), 6)
            addprice_10 = round((abp - (abp * perct(adp10))), 6)

            """ E ~~~ 추매시점 지정 %(adsp %) 이하 시 (소수 5자리에서 반올림) """
            addprice = abp - round((abp * adsp), 6)             # 매수 시 매수평단의 adsp % 이하 일 경우 추매 진행 (평단가)

            if (e in cu_p):                                     # 한 종목에 대한 현재가 추출
                price = cu_p[e]                                 # '종목' 현재가 가져 옴
                tp = round(((price - abp) / abp * 100), 2)                  # '종목' 별 수익율 계산                                       
                t_money = tb * abp
                p_money = price * tb
                loss = p_money - t_money
                t_tp.append(loss)
                goal = abp + (abp * ask_p)                      # 지정가 시 목표 매도가(매수 평균가 기준) 설정 ( 평단가의 - 2.1 % )
                add_ug = abp - (abp * ask_ug)                   # ma5_under 이하 매수 시 매도 및 추매 조건 데이터(-10% 마다 추매)
                # 미적용
                    # goal_s = abp + (abp * ask_pp)                   # 지정가 시 예비 매도걸기
                    # a_o = get_tick_s(goal)                          # 지정가 시 매도 호가 계산(매도 지정가)

                s1_bm1, s1_bm2 = s1_bull_m1(e)                          # bulling~ check
                
                """    매수금액 변경 시 일부 적용    """
                with open('/root/UBiCauto/data/set_cfg2.pickle', 'rb') as fset:
                    ubic_conf = pickle.load(fset)
                b_money = ubic_conf['b_money']          # set_cfg2.pickle에서 b_money 값을 호출

                if t_money <= 5000:     # 매도 후 잔금이 5000원 이하 남을 시 추매
                    bid_money = (b_money + 200) - t_money
                    upbit2.buy_market_order(e, bid_money)   # 현매수금액과 차액만큼 매수
                    add_rw0(e, rwnum)                     # 매수 후 애드넘 횟수 초기화(0번)
                    # 미적용
                        # elif (0.01 < t_money) and (price <= (abp - (abp * perct(2)))) and (t_money <= (b_money - 1000)):    # 현재가 < 매수가, 종목보유금액 < 매수금액(-1000) , (price < (abp + (abp * perct(1))) and
                        #     g_money = b_money - t_money
                        #     if 5000 < g_money:
                        #         upbit2.buy_market_order(e, g_money)
                        #     elif g_money <= 5000:
                        #         g1_money = (5000 - g_money) + 500
                        #         g_money = (g_money + g1_money)
                        #         upbit2.buy_market_order(e, g_money)

                if sell_cont == 0:                                      # 전체 매도 제외, 전체 추매 제외
                    pass
                else:
                    if (sell_cont == 1) or (sell_cont == 2):            # 매도기능
                        if s1_bm1 and (s1_bm2 < price):                 # bulling + 매도기준 만족 시
                            pass
                        elif goal < price:  # 목표가 < 현재가 되면 ((매도)) 실행
                            if e in ext_s:
                                pass
                            else:
                                a_order = upbit2.sell_limit_order(e, price, tb)       # '지정가 < 현재가' 조건 시 현재가 매도 실행

                                # 미적용
                                    # print(j, "판매완료")                        
                                    # upbit2.sell_market_order(e, tb)  # '종목' 을 시장가로 매도
                                    # a_order = upbit2.sell_limit_order(e, a_o, tb)       # '지정가 < 현재가' 조건 시 지정가 매도 실행

                    if (sell_cont == 1) or (sell_cont == 3):          # 추매기능
                        if e in ext_a:
                            pass
                        elif price < goal:                                      #  현재가 < 목표가 price < goal:                                      #  현재가 < 목표가
                            """ ================ (( 보유 종목 추매 감시 )) ================ """
                            buy_goal5 = buy_avr_price_5(e)              # 1차 추매 기준 시작
                            buy_goal10 = buy_avr_price_10(e)            # 1차 추매 목표값 가져 옴 3.5
                            buy_goal20 = buy_avr_price_20(e)            # 2차 추매 목표값 가져 옴 3
                            buy_goal30 = buy_avr_price_30(e)            # 3차 추매 목표값 가져 옴 3
                            buy_goal40 = buy_avr_price_40(e)            # 4차 추매 목표값 가져 옴 3
                            buy_goal50 = buy_avr_price_50(e)            # 5차 추매 목표값 가져 옴 3
                            buy_goal60 = buy_avr_price_60(e)            # 6차 추매 목표값 가져 옴 3
                            buy_goal70 = buy_avr_price_70(e)            # 7차 추매 목표값 가져 옴 3
                            buy_goal80 = buy_avr_price_80(e)            # 8차 추매 목표값 가져 옴 3
                            buy_goal90 = buy_avr_price_90(e)            # 9차 추매 목표값 가져 옴 3
                            # buy_goal50under = buy_goal50[1] - (buy_goal50[1] * u_p / 100)          # 현재 사용 안 함
                            # ma5_u = ma5_under(e)                        # 30일 5이평 값 비교          # 현재 사용 안 함
                            # b1_bm1 = b1_decline_m1(e)                   # 추매지연 조건
                            b2_bm1, b2_bm2 = b2_decline_m1(e)                   # 추매지연 조건 2
                            t_money = tb * abp  # 해당 종목 보유 금액
                            # time.sleep(0.05)
                            ag_price1 = b_money * ag1       # 1(0.5)배 추매
                            ag_price2 = t_money * ag2       # 1(0.3)배 추매
                            ag_price3 = t_money * ag3       # 1(0.4)배 추매
                            ag_price4 = t_money * ag4       # 1(1.0)배 추매
                            ag_price5 = t_money * ag5       # 1(1.0)배 추매
                            ag_price6 = t_money * ag6       # 1(1.0)배 추매
                            ag_price7 = t_money * ag7       # 1(1.0)배 추매
                            ag_price8 = t_money * ag8       # 1(1.0)배 추매
                            ag_price9 = t_money * ag9       # 1(1.0)배 추매
                            ag_price10 = t_money * ag10      # 1(1.0)배 추매


                            """ ======== 보유종목이 추매종목에 없으면 추매 횟수 dict 에 종목 추가한다 ========"""
                            if e not in add_num :
                                cbid = get_orderi('done', 'bid', 'i', ofn2)         # 매수완료 정보 가져오기
                                cprice = cbid[0]['price']                           # 매수완료 정보 중 마지막 종목의 매수금액
                                cvolume = cbid[0]['volume']                         # 매수완료 정보 중 마지막 종목의 매수수량
                                f_bidv0 = float(cprice) * float(cvolume)            # 매수 금액
                                f_bidv = round((f_bidv0 + (f_bidv0 * 0.0005)), 2)   # 매수 금액 + 수수료
                                adn1 = adn_insert(b_money, t_money)                 # 추매 횟수 확인(초기 add_num 생성)
                                print(f'추매종목포함시:{e}, 매수가: {b_money},  adn1: {adn1}')                         # 매수 후 추매 횟수 생성 확인
                                if adn1 == 0:                                       # 추매 횟수 '0'이면
                                    adn2 = 0                                        # 매수 위치 '0'
                                elif 1 <= adn1:                                     # 추매 횟수 '1' 이상이면
                                    if (buy_goal5[1] < abp):                        # 위치 '10' 이하 동일
                                        adn2 = 5 
                                    elif (buy_goal10[1] < abp < buy_goal5[1]):
                                        adn2 = 10
                                    elif (buy_goal20[1] < abp < buy_goal10[1]):
                                        adn2 = 20
                                    elif (buy_goal30[1] < abp < buy_goal20[1]):
                                        adn2 = 30
                                    elif (buy_goal40[1] < abp < buy_goal30[1]):
                                        adn2 = 40
                                    elif (buy_goal50[1] < abp < buy_goal40[1]):
                                        adn2 = 50
                                    elif (buy_goal60[1] < abp < buy_goal50[1]):
                                        adn2 = 60
                                    elif (buy_goal70[1] < abp < buy_goal60[1]):
                                        adn2 = 70
                                    elif (buy_goal80[1] < abp < buy_goal70[1]):
                                        adn2 = 80
                                    elif (buy_goal90[1] < abp < buy_goal90[1]):
                                        adn2 = 90
                                    else:
                                        adn2 = 90
                                # add_num[e] = [adn1, adn2, f_bidv]          # 추매 시 목록 추가 (매수완료 종목명을 dict 에 [추매횟수, 추매위치, 첫 매수가]으로 추가, 처음 매수시)
                                add_rwinit(e, rwnum, adn1, adn2, f_bidv)            # 새 종목 매수 시 목록 추가 (매수완료 종목명을 dict 에 [추매횟수, 추매위치, 첫 매수가]으로 추가, 처음 매수시수
                                print(e, rwnum, adn1, adn2, f_bidv)

                            if b_money < blow_money:                        # 최소 매수금액 'blow_money' 로 제한
                                b_money = blow_money                        # 최저 매수금액 설정

                            an = add_num[e][0]         # {'보유종목': [매수횟수, 매수시점]}, 보유종목의 매수 횟수를 'an' 에 바인딩
                            
                            # print('종목 [' + '\033[1m' + f'{e}' + '\033[0m' + '] ┆\0 ' + f'종목금액 ({format(round(t_money, 3),",")}) ┆ 수익률 (' + '\033[1m' + f'{tp}' + '\033[0m' + ') ┆ 추매횟수 (' + '\033[1m' + f'{an}' + '\033[0m' + ') ┆\n' + f'보유수량 {tb} ┆ b_money({b_money})')
                            """ === 추매 횟수(an), 제한횟수(ap), 현가(price), 평단가(abp), 1차 목표가(buy_goal10), 보유금액(t_money), 제한가(l_money) ==="""

                            """ S ~~ test 중 ~~ S """
                            if ag_price1 < 5000 :       # 추매 시 원금의 몇 배(ag_price1)
                                ag_price1 == 5000
                            if ag_price2 < 5000 :
                                ag_price2 == 5000
                            """ 위 2개 if 문 추가 함 """
                            
                            if b2_bm1 and (price < b2_bm2):           # decline + 추매지연기준 2    
                                pass

                            elif an == 0 and 5000 <= t_money < (b_money * 1.1) and (price < addprice_1) and (0.1 < addprice_2) :     # 1.5
                                # elif t_money < (b_money * 1.2) and (price < addprice_1) :     # -3% (-3%)
                                upbit2.buy_market_order(e, ag_price1)   # 1, 20,000 (1)
                                with open('/root/UBiCauto/find_s1.log','a') as fw:
                                    print(f'{now}: (205) 종목-1:{e}, 매수금액:{ag_price1}, 추매수:{add_num[e][0:1]}, t:{t_money}, b:{b_money}, p:{price}, addp:{addprice_1}', file=fw)
                                if 5000 <= addprice_1:
                                    add_rw1(e, rwnum); time.sleep(5)

                            elif t_money < (b_money * 1.7) and (price < addprice_2) and (0.1 < addprice_3) :     # 2.5
                                upbit2.buy_market_order(e, ag_price2)   # 1, 40,000 (2)
                                with open('/root/UBiCauto/find_s1.log','a') as fw:
                                    print(f'{now}: (205) 종목-2:{e}, 매수금액:{ag_price1}, 추매수:{add_num[e][0:1]}, t:{t_money}, b:{b_money}, p:{price}, addp:{addprice_1}', file=fw)
                                if 5000 <= addprice_1:
                                    add_rw2(e, rwnum); time.sleep(5)

                            elif t_money < (b_money * 2.2) and (price < addprice_3) and (0.1 < addprice_3) :   # 4.5
                                upbit2.buy_market_order(e, ag_price3)   # 1, 80,000 (3)
                                with open('/root/UBiCauto/find_s1.log','a') as fw:
                                    print(f'{now}: (205) 종목-3:{e}, 매수금액:{ag_price1}, 추매수:{add_num[e][0:1]}, t:{t_money}, b:{b_money}, p:{price}, addp:{addprice_1}', file=fw)
                                if 5000 <= addprice_1:
                                    add_rw3(e, rwnum); time.sleep(5)

                            elif t_money < (b_money * 3) and (price < addprice_4) and (0.1 < addprice_4):   # 8.5
                                upbit2.buy_market_order(e, ag_price4)   # 1, 160,000 (4)
                                with open('/root/UBiCauto/find_s1.log','a') as fw:
                                    print(f'{now}: (205) 종목-4:{e}, 매수금액:{ag_price1}, 추매수:{add_num[e][0:1]}, t:{t_money}, b:{b_money}, p:{price}, addp:{addprice_1}', file=fw)
                                if 5000 <= addprice_1:
                                    add_rw4(e, rwnum); time.sleep(5)

                            elif t_money < (b_money * 7) and (price < addprice_5) and (0.1 < addprice_5):   # 16.5
                                upbit2.buy_market_order(e, ag_price5)   # 1배 추매 1회
                                with open('/root/UBiCauto/find_s1.log','a') as fw:
                                    print(f'{now}: (205) 종목-5:{e}, 매수금액:{ag_price1}, 추매수:{add_num[e][0:1]}, t:{t_money}, b:{b_money}, p:{price}, addp:{addprice_1}', file=fw)
                                if 5000 <= addprice_1:
                                    add_rw5(e, rwnum); time.sleep(5)

                                """ E ~~ test 중 ~~ E """

                            elif (addprice < price) and (0.1 < addprice) :                            # 매수평단 (10)% 이하 만족 시(현재가가 ()이하 시 추매 들어감)
                                pass
                            
                                # ---------------------------------------------# 추매 (0 > 1)회 시 #---------------------------------------------------- #
                                
                            elif (an == 0) and (an < ap) and (summ >= (t_money * 1.1)) :
                                
                                if (buy_goal5[1] < abp) and (price < buy_goal10[0]) and (t_money < l_money):
                                    upbit2.buy_market_order(e, ag_price1)   # 0.7배 추매
                                    with open('find_s1.log','a') as fw:
                                        print(f'{now}: (241) 종목:{e}, 매수금액:{ag_price1}, 추매수:{add_num[e][0:1]}', file=fw)
                                    if 5000 <= addprice_1:
                                        add_rwav5(an, e, rwnum)

                                elif (buy_goal10[1] < abp) and (price < buy_goal20[0]) and (t_money < l_money): 

                                    upbit2.buy_market_order(e, ag_price1)
                                    if 5000 <= addprice_1:
                                        add_rwav10(an, e, rwnum)

                                elif (buy_goal20[1] < abp) and (price < buy_goal30[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price1)
                                    if 5000 <= addprice_1:
                                        add_rwav20(an, e, rwnum)

                                elif (buy_goal30[1] < abp) and (price < buy_goal40[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price1)
                                    if 5000 <= addprice_1:
                                        add_rwav30(an, e, rwnum)

                                elif (buy_goal40[1] < abp) and (price < buy_goal50[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price1)
                                    if 5000 <= addprice_1:
                                        add_rwav40(an, e, rwnum)

                                elif (buy_goal50[1] < abp) and (price < buy_goal60[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price1)
                                    if 5000 <= addprice_1:
                                        add_rwav50(an, e, rwnum)

                                elif (buy_goal60[1] < abp) and (price < buy_goal70[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price1)
                                    if 5000 <= addprice_1:
                                        add_rwav60(an, e, rwnum)

                                elif (buy_goal70[1] < abp) and (price < buy_goal80[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price1)
                                    if 5000 <= addprice_1:
                                        add_rwav70(an, e, rwnum)

                                elif (buy_goal80[1] < abp) and (price < buy_goal90[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price1)
                                    if 5000 <= addprice_1:
                                        add_rwav80(an, e, rwnum)

                                elif (buy_goal90[1] < abp) and (price < add_ug) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price1)
                                    if 5000 <= addprice_1:
                                        add_rwav90(an, e, rwnum)

                                elif (buy_goal90[1] > abp) and (price < add_ug) and (t_money < l_money):
                                    # buy_goal90[1] 이하 추매 시 add_ug: 10% 이하 시에 추매
                                    upbit2.buy_market_order(e, ag_price1)
                                    if 5000 <= addprice_1:
                                        add_rwav90(an, e, rwnum)

                                time.sleep(5)

                                    # --------------------------------------------# 추매 (1 > 2)회 시 #---------------------------------------------------- #
                            elif (an == 1) and (an < ap) and (summ >= (t_money * 1.1)) :

                                if (buy_goal5[1] < abp) and (price < buy_goal10[0]) and (t_money < l_money):

                                    upbit2.buy_market_order(e, ag_price2)   # 1배 추매
                                    if 5000 <= addprice_2:
                                        add_rwav5(an, e, rwnum)

                                elif (buy_goal10[1] < abp) and (price < buy_goal20[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price2)
                                    if 5000 <= addprice_2:
                                        add_rwav10(an, e, rwnum)

                                elif (buy_goal20[1] < abp) and (price < buy_goal30[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price2)
                                    if 5000 <= addprice_2:
                                        add_rwav20(an, e, rwnum)

                                elif (buy_goal30[1] < abp) and (price < buy_goal40[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price2)
                                    if 5000 <= addprice_2:
                                        add_rwav30(an, e, rwnum)

                                elif (buy_goal40[1] < abp) and (price < buy_goal50[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price2)
                                    if 5000 <= addprice_2:
                                        add_rwav40(an, e, rwnum)

                                elif (buy_goal50[1] < abp) and (price < buy_goal60[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price2)
                                    if 5000 <= addprice_2:
                                        add_rwav50(an, e, rwnum)

                                elif (buy_goal60[1] < abp) and (price < buy_goal70[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price2)
                                    if 5000 <= addprice_2:
                                        add_rwav60(an, e, rwnum)

                                elif (buy_goal70[1] < abp) and (price < buy_goal80[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price2)
                                    if 5000 <= addprice_2:
                                        add_rwav70(an, e, rwnum)

                                elif (buy_goal80[1] < abp) and (price < buy_goal90[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price2)
                                    if 5000 <= addprice_2:
                                        add_rwav80(an, e, rwnum)

                                elif (buy_goal90[1] < abp) and (price < add_ug) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price2)
                                    if 5000 <= addprice_2:
                                        add_rwav90(an, e, rwnum)

                                elif (buy_goal90[1] > abp) and (price < add_ug) and (t_money < l_money):
                                    # buy_goal90[1] 이하 추매 시 add_ug: 10% 이하 시에 추매
                                    upbit2.buy_market_order(e, ag_price2)
                                    if 5000 <= addprice_2:
                                        add_rwav90(an, e, rwnum)

                                time.sleep(5)

                                    # --------------------------------------------# 추매 (2 > 3)회 시 #---------------------------------------------------- #
                            elif (an == 2) and (an < ap) and (summ >= (t_money * 1.1)):

                                if (buy_goal5[1] < abp) and (price < buy_goal10[0]) and (t_money < l_money):

                                    upbit2.buy_market_order(e, ag_price3)   # 1배 추매
                                    if 5000 <= addprice_3:
                                        add_rwav5(an, e, rwnum)

                                elif (buy_goal10[1] < abp) and (price < buy_goal20[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price3)
                                    if 5000 <= addprice_3:
                                        add_rwav10(an, e, rwnum)

                                elif (buy_goal20[1] < abp) and (price < buy_goal30[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price3)
                                    if 5000 <= addprice_3:
                                        add_rwav20(an, e, rwnum)
                                
                                elif (buy_goal30[1] < abp) and (price < buy_goal40[0]) and (t_money < l_money):
                                    
                                    upbit2.buy_market_order(e, ag_price3)
                                    if 5000 <= addprice_3:
                                        add_rwav30(an, e, rwnum)

                                elif (buy_goal40[1] < abp) and (price < buy_goal50[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price3)
                                    if 5000 <= addprice_3:
                                        add_rwav40(an, e, rwnum)

                                elif (buy_goal50[1] < abp) and (price < buy_goal60[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price3)
                                    if 5000 <= addprice_3:
                                        add_rwav50(an, e, rwnum)

                                elif (buy_goal60[1] < abp) and (price < buy_goal70[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price3)
                                    if 5000 <= addprice_3:
                                        add_rwav60(an, e, rwnum)

                                elif (buy_goal70[1] < abp) and (price < buy_goal80[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price3)
                                    if 5000 <= addprice_3:
                                        add_rwav70(an, e, rwnum)

                                elif (buy_goal80[1] < abp) and (price < buy_goal90[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price3)
                                    if 5000 <= addprice_3:
                                        add_rwav80(an, e, rwnum)

                                elif (buy_goal90[1] < abp) and (price < add_ug) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price3)
                                    if 5000 <= addprice_3:
                                        add_rwav90(an, e, rwnum)

                                elif (buy_goal90[1] > abp) and (price < add_ug) and (t_money < l_money):
                                    # buy_goal90[1] 이하 추매 시 add_ug: 7% 이하 시에 추매
                                    upbit2.buy_market_order(e, ag_price3)
                                    if 5000 <= addprice_3:
                                        add_rwav90(an, e, rwnum)

                                time.sleep(5)
                            

                                    # --------------------------------------------# 추매 (3 > 4)회 시 #---------------------------------------------------- #
                                    # ********************************************************************************* #
                            elif (an == 3) and (an < ap) and (summ >= (t_money * 1.1)):

                                if (buy_goal5[1] < abp) and (price < buy_goal10[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price4)   # ** 1.5배 추매 **
                                    if 5000 <= addprice_4:
                                        add_rwav5(an, e, rwnum)

                                elif (buy_goal10[1] < abp) and (price < buy_goal20[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price4)   # ** 1.5배 추매 **
                                    if 5000 <= addprice_4:
                                        add_rwav10(an, e, rwnum)

                                elif (buy_goal20[1] < abp) and (price < buy_goal30[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price4)   # ** 1.5배 추매 **
                                    if 5000 <= addprice_4:
                                        add_rwav20(an, e, rwnum)

                                elif (buy_goal30[1] < abp) and (price < buy_goal40[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price4)   # ** 1.5배 추매 **
                                    if 5000 <= addprice_4:
                                        add_rwav30(an, e, rwnum)

                                elif (buy_goal40[1] < abp) and (price < buy_goal50[0]) and (t_money < l_money):
                                    
                                    upbit2.buy_market_order(e, ag_price4)
                                    
                                    if 5000 <= addprice_4:
                                        add_rwav40(an, e, rwnum)

                                elif (buy_goal50[1] < abp) and (price < buy_goal60[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price4)
                                    if 5000 <= addprice_4:
                                        add_rwav50(an, e, rwnum)

                                elif (buy_goal60[1] < abp) and (price < buy_goal70[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price4)
                                    if 5000 <= addprice_4:
                                        add_rwav60(an, e, rwnum)

                                elif (buy_goal70[1] < abp) and (price < buy_goal80[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price4)
                                    if 5000 <= addprice_4:
                                        add_rwav70(an, e, rwnum)

                                elif (buy_goal80[1] < abp) and (price < buy_goal90[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price4)
                                    if 5000 <= addprice_4:
                                        add_rwav80(an, e, rwnum)

                                elif (buy_goal90[1] < abp) and (price < add_ug) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price4)
                                    if 5000 <= addprice_4:
                                        add_rwav90(an, e, rwnum)

                                elif (buy_goal90[1] > abp) and (price < add_ug) and (t_money < l_money):
                                    # buy_goal90[1] 이하 추매 시 add_ug: 7% 이하 시에 추매
                                    upbit2.buy_market_order(e, ag_price4)
                                    if 5000 <= addprice_4:
                                        add_rwav90(an, e, rwnum) 

                                time.sleep(5)                  

                                    # --------------------------------------------# 추매 (4 > 5)회 시 #---------------------------------------------------- #

                            elif (an == 4) and (an < ap) and (summ >= (t_money * 1.1)):

                                if (buy_goal5[1] < abp) and (price < buy_goal10[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price5)   # ** 2배 추매 **
                                    if 5000 <= addprice_5:
                                        add_rwav5(an, e, rwnum)

                                elif (buy_goal10[1] < abp) and (price < buy_goal20[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price5)   # ** 2배 추매 **
                                    if 5000 <= addprice_5:
                                        add_rwav10(an, e, rwnum)

                                elif (buy_goal20[1] < abp) and (price < buy_goal30[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price5)   # ** 2배 추매 **
                                    if 5000 <= addprice_5:
                                        add_rwav20(an, e, rwnum)

                                elif (buy_goal30[1] < abp) and (price < buy_goal40[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price5)   # ** 2배 추매 **
                                    if 5000 <= addprice_5:
                                        add_rwav30(an, e, rwnum)

                                elif (buy_goal40[1] < abp) and (price < buy_goal50[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price5)   # ** 2배 추매 **
                                    if 5000 <= addprice_5:
                                        add_rwav40(an, e, rwnum)

                                elif (buy_goal50[1] < abp) and (price < buy_goal60[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price5)
                                    if 5000 <= addprice_5:
                                        add_rwav50(an, e, rwnum)

                                elif (buy_goal60[1] < abp) and (price < buy_goal70[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price5)
                                    if 5000 <= addprice_5:
                                        add_rwav60(an, e, rwnum)

                                elif (buy_goal70[1] < abp) and (price < buy_goal80[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price5)
                                    if 5000 <= addprice_5:
                                        add_rwav70(an, e, rwnum)

                                elif (buy_goal80[1] < abp) and (price < buy_goal90[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price5)
                                    if 5000 <= addprice_5:
                                        add_rwav80(an, e, rwnum)

                                elif (buy_goal90[1] < abp) and (price < add_ug) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price5)
                                    if 5000 <= addprice_5:
                                        add_rwav90(an, e, rwnum)

                                elif (buy_goal90[1] > abp) and (price < add_ug) and (t_money < l_money):

                                    upbit2.buy_market_order(e, ag_price5)
                                    if 5000 <= addprice_5:
                                        add_rwav90(an, e, rwnum)

                                time.sleep(5)

                                # --------------------------------------------# 추매 (5 > 6)회 시 #---------------------------------------------------- #

                            elif (an == 5) and (an < ap) and (summ >= (t_money * 1.1)) : 

                                if (buy_goal5[1] < abp) and (price < buy_goal10[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price6)   # 1배 추매 **
                                    if 5000 <= addprice_6:
                                        add_rwav5(an, e, rwnum)

                                elif (buy_goal10[1] < abp) and (price < buy_goal20[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price6)   # 1배 추매 **
                                    if 5000 <= addprice_6:
                                        add_rwav10(an, e, rwnum)

                                elif (buy_goal20[1] < abp) and (price < buy_goal30[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price6)   # 1배 추매 **
                                    if 5000 <= addprice_6:
                                        add_rwav20(an, e, rwnum)

                                elif (buy_goal30[1] < abp) and (price < buy_goal40[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price6)   # 1배 추매 **
                                    if 5000 <= addprice_6:
                                        add_rwav30(an, e, rwnum)

                                elif (buy_goal40[1] < abp) and (price < buy_goal50[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price6)   # 1배 추매 **
                                    if 5000 <= addprice_6:
                                        add_rwav40(an, e, rwnum)

                                elif (buy_goal50[1] < abp) and (price < buy_goal60[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price6)  # 1배 추매
                                    if 5000 <= addprice_6:
                                        add_rwav50(an, e, rwnum)

                                elif (buy_goal60[1] < abp) and (price < buy_goal70[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price6)
                                    if 5000 <= addprice_6:
                                        add_rwav60(an, e, rwnum)

                                elif (buy_goal70[1] < abp) and (price < buy_goal80[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price6)
                                    if 5000 <= addprice_6:
                                        add_rwav70(an, e, rwnum)

                                elif (buy_goal80[1] < abp) and (price < buy_goal90[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price6)
                                    if 5000 <= addprice_6:
                                        add_rwav80(an, e, rwnum)

                                elif (buy_goal90[1] < abp) and (price < add_ug) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price6)
                                    if 5000 <= addprice_6:
                                        add_rwav90(an, e, rwnum)

                                elif (buy_goal90[1] > abp) and (price < add_ug) and (t_money < l_money):
                                    # buy_goal90[1] 이하 추매 시 add_ug: 7% 이하 시에 추매
                                    upbit2.buy_market_order(e, ag_price6)
                                    if 5000 <= addprice_6:
                                        add_rwav90(an, e, rwnum)

                                time.sleep(5)

                                # --------------------------------------------# 추매 (6 > 7)회 시 #---------------------------------------------------- #

                            elif (an == 6) and (an < ap) and (summ >= (t_money * 1.1)):

                                if (buy_goal5[1] < abp) and (price < buy_goal10[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price7)   # 1배 추매 **
                                    if 5000 <= addprice_7:
                                        add_rwav5(an, e, rwnum)

                                elif (buy_goal10[1] < abp) and (price < buy_goal20[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price7)   # 1배 추매 **
                                    if 5000 <= addprice_7:
                                        add_rwav10(an, e, rwnum)

                                elif (buy_goal20[1] < abp) and (price < buy_goal30[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price7)   # 1배 추매 **
                                    if 5000 <= addprice_7:
                                        add_rwav20(an, e, rwnum)

                                elif (buy_goal30[1] < abp) and (price < buy_goal40[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price7)   # 1배 추매 **
                                    if 5000 <= addprice_7:
                                        add_rwav30(an, e, rwnum)

                                elif (buy_goal40[1] < abp) and (price < buy_goal50[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price7)   # 1배 추매 **
                                    if 5000 <= addprice_7:
                                        add_rwav40(an, e, rwnum)

                                elif (buy_goal50[1] < abp) and (price < buy_goal60[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price7)  # 1배 추매
                                    if 5000 <= addprice_7:
                                        add_rwav50(an, e, rwnum)

                                elif (buy_goal60[1] < abp) and (price < buy_goal70[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price7)  # 1배 추매
                                    if 5000 <= addprice_7:
                                        add_rwav60(an, e, rwnum)

                                elif (buy_goal70[1] < abp) and (price < buy_goal80[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price7)
                                    if 5000 <= addprice_7:
                                        add_rwav70(an, e, rwnum)

                                elif (buy_goal80[1] < abp) and (price < buy_goal90[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price7)
                                    if 5000 <= addprice_7:
                                        add_rwav80(an, e, rwnum)

                                elif (buy_goal90[1] < abp) and (price < add_ug) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price7)
                                    if 5000 <= addprice_7:
                                        add_rwav90(an, e, rwnum)

                                elif (buy_goal90[1] > abp) and (price < add_ug) and (t_money < l_money):
                                    # buy_goal90[1] 이하 추매 시 add_ug: 7% 이하 시에 추매
                                    upbit2.buy_market_order(e, ag_price7)
                                    if 5000 <= addprice_7:
                                        add_rwav90(an, e, rwnum)

                                time.sleep(5)

                                    # --------------------------------------------# 추매 (7 > 8)회 시 #---------------------------------------------------- #

                            elif (an == 7) and (an < ap) and (summ >= (t_money * 1.1)):
                                
                                if (buy_goal5[1] < abp) and (price < buy_goal10[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price8)   # 1배 추매 **
                                    if 5000 <= addprice_8:
                                        add_rwav5(an, e, rwnum)

                                elif (buy_goal10[1] < abp) and (price < buy_goal20[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price8)   # 1배 추매 **
                                    if 5000 <= addprice_8:
                                        add_rwav10(an, e, rwnum)

                                elif (buy_goal20[1] < abp) and (price < buy_goal30[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price8)   # 1배 추매 **
                                    if 5000 <= addprice_8:
                                        add_rwav20(an, e, rwnum)

                                elif (buy_goal30[1] < abp) and (price < buy_goal40[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price8)   # 1배 추매 **
                                    if 5000 <= addprice_8:
                                        add_rwav30(an, e, rwnum)

                                elif (buy_goal40[1] < abp) and (price < buy_goal50[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price8)   # 1배 추매 **
                                    if 5000 <= addprice_8:
                                        add_rwav40(an, e, rwnum)

                                elif (buy_goal50[1] < abp) and (price < buy_goal60[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price8)  # 1배 추매
                                    if 5000 <= addprice_8:
                                        add_rwav50(an, e, rwnum)

                                elif (buy_goal60[1] < abp) and (price < buy_goal70[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price8)  # 1배 추매
                                    if 5000 <= addprice_8:
                                        add_rwav60(an, e, rwnum)

                                elif (buy_goal70[1] < abp) and (price < buy_goal80[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price8)  # 1배 추매
                                    if 5000 <= addprice_8:
                                        add_rwav70(an, e, rwnum)

                                elif (buy_goal80[1] < abp) and (price < buy_goal90[0]) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price8)
                                    if 5000 <= addprice_8:
                                        add_rwav80(an, e, rwnum)

                                elif (buy_goal90[1] < abp) and (price < add_ug) and (t_money < l_money):
                                
                                    upbit2.buy_market_order(e, ag_price8)
                                    if 5000 <= addprice_8:
                                        add_rwav90(an, e, rwnum)

                                elif (buy_goal90[1] > abp) and (price < add_ug) and (t_money < l_money):
                                    # buy_goal90[1] 이하 추매 시 add_ug: 7% 이하 시에 추매
                                    upbit2.buy_market_order(e, ag_price8)
                                    if 5000 <= addprice_8:
                                        add_rwav90(an, e, rwnum)

                                time.sleep(5)

            time.sleep(0.9)

        with open('/root/UBiCauto/data/t_tp2.pickle', 'wb') as fw:    # 보유종목 평가손익(list 로 저장)
            pickle.dump(t_tp, fw)
    except Exception as s1:
        print('e-time:', datetime.now())
        print('s1_매도및추매 프로세스', s1)
    
    sum_tp = sum(t_tp)              # 총 보유 평가손익 계산금액
    ask_p = askper(upbit2, 2)                  # 매도기준 조정 및 저장

    """ 매도 후 매수 횟수 항목 갱신 """

    try:    # 매도 후 매수횟수 갱신
        ex_item(bl, ex_num)                                 # 매수 횟수 항목 갱신 함수 사용
    except Exception as add_num_r:
        print('매도후 adn갱신:', add_num_r)

    """=== 매도대기 취소 절차 진행 (매도 조건을 만족하지 못하면 아래 조건을 비교하여 매도대기 취소) === """
    try:    # 매도대기 취소
        ask_w_i = get_orderi('wait', 'ask', 'i', ofn2)                                    # 매도대기 목록 정보 리스트
        ask_w_list = get_orderi('wait', 'ask', 'n', ofn2)                             # 매도대기 종목 리스트

        for an in range(len(ask_w_list)):                               # list 에서 매도대기 종목(dict) 항목 추출
            uuids_an = ask_w_i[an]['market']                            # 매도대기 종목 정보에서 가져 온 종목이름
            if (uuids_an in ext_s) or ("KRW-BTT" == uuids_an):             # 매도제외 종목에 대기종목이 있을 경우 또는 KRW-BTT 
                pass
            else:
                uuids_aid = ask_w_i[an]['uuid']                             # bid_w_i[bn] 번째 종목의 'uuid' 의 값
                a1_time1 = ask_w_i[an]['created_at']                        # 매도대기 종목 order 시간
                a1_time = t_c(a1_time1)                                     # 계산을 위해 order 시간 형식 변환
                mt = (a1_time + timedelta(seconds=agt))                     # 매도대기 시간 10분 지난 시간 계산
                # if (mt <= datetime.now()) or (uuids_an not in bl):          # 지정시간이 지났는지, 자산목록에 종목이 있는지 확인 후
                if (mt <= datetime.now()):                                  # 지정시간이 지났는지, 자산목록에 종목이 있는지 확인 후
                    b_cancel = upbit2.cancel_order(uuids_aid)               # 매도 대기 취소
    except Exception as s3:
        print('e-time:', datetime.now())
        print('s3_매도대기', s3)

    if os.path.isfile('/root/UBiCauto/data/add_num2.pickle') and os.path.getsize('/root/UBiCauto/data/add_num2.pickle') > 5:
        os.system('clear')
        print(f'보유종목수:[{len(bl)}] | 애드넘: [{len(add_num)}], add_num={add_num}')

    print("--- %s seconds ---" % round((time.time() - start_time), 3))
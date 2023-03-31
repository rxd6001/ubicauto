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
    add_rwav20, add_rwav30, add_rwav40, add_rwav50, add_rwav60, add_rwav70, add_rwav80, add_rwav90, add_rwinit, add_get,\
    linenumber, ext_save
from UBiC_Rotate_data import gb
from datetime import datetime, timedelta
import threading

def ubic_sell(id):
    """ 23p(e) upbit login - s """
    f = open(("/root/UBiCauto/Acct/upbit%s.txt") %(id))        # 파일 열기
    lines = f.readlines()                       # 라인을 일러들임
    access = lines[0].strip()                   # access key '\n' 0번 행 불러오기
    secret = lines[1].strip()                   # secret key '\n' 1번 행 불러오기
    f.close()                                   # 파일 닫기

    upbit = pyupbit.Upbit(access, secret)      # 업비트 로그인
    """ 18p(s) ----------- e """
    s1_bm1_dic = {}; s1_bm2_dic = {}
    b2_bm1_dic = {}; b2_bm2_dic = {}
    now = datetime.now()    # 현재시간 호출
    while True:

        start_time = time.time()                            # time check
                                    
        with open('/root/UBiCauto/data/set_cfg%s.pickle' %(id), 'rb') as fset:          # 계정별 설정값 불러오기
            ubic_conf = pickle.load(fset)

        with open('/root/UBiCauto/data/ext_item%s.pickle' %(id), 'rb') as fset:         # 계정별 제외항목 불러오기
            ext_item = pickle.load(fset)
        
        ext_a = ext_item['ext_a']         # 추매제외종목 리스트
        ext_b = ext_item['ext_b']         # 매수제외종목 리스트
        ext_s = ext_item['ext_s']         # 매도제외종목 리스트
        # print(f'{linenumber()}p::ubic_conf: {ubic_conf}')           # 설정 값들 확인
        ask_p = ubic_conf['ask_p']; ask_ug = ubic_conf['ask_ug']; ask_pp = ubic_conf['ask_pp']; agt = ubic_conf['agt']; sell_cont = ubic_conf['sell_count']
        adsp = ubic_conf['adsp']; ap = ubic_conf['ap']; u_p = ubic_conf['u_p']; l_money = ubic_conf['l_money']; ag1 = ubic_conf['ag1']; ag2 = ubic_conf['ag2']
        ag3 = ubic_conf['ag3']; ag4 = ubic_conf['ag4']; ag5 = ubic_conf['ag5']; ag6 = ubic_conf['ag6']; ag7 = ubic_conf['ag7']; ag8 = ubic_conf['ag8']
        ag9 = ubic_conf['ag9']; ag10 = ubic_conf['ag10']; adp1 = ubic_conf['adp1']; adp2 = ubic_conf['adp2']; adp3 = ubic_conf['adp3']; adp4 = ubic_conf['adp4']
        adp5 = ubic_conf['adp5']; adp6 = ubic_conf['adp6']; adp7 = ubic_conf['adp7']; adp8 = ubic_conf['adp8']; adp9 = ubic_conf['adp9']; adp10 = ubic_conf['adp10']
        abptime = ubic_conf['abptime']; blow_money = ubic_conf['blow_money']
        
        t_tp = []                                             # 평가손익(리스트 생성)

        try:
            bl, abp1, tb1 = gb(upbit)                              # 보유종목명, 평단, 보유수량 호출                       
            tsum, tbidm, tbidp, summ = myasset(upbit)              # 자산정보 한 번에 호출(총합계, 총매수금액, 총매수비율, 총매수가능금액)
            summ = round(summ, 1)
        except Exception as up:
            print(f'{linenumber()}p::error시- 보유종목, 평단, 자산정보, sell_up:, {up}')

        try:    # 보유종목 현재가 호출
            with open('/root/UBiCauto/data/cp.pickle', 'rb') as fr1:            # 현재가 불러오기
                cu_p = pickle.load(fr1)                                         # 전체 종목과 현재가 dict 'cu_p' 로 바인딩
            # [cu_p.pop(key, None) for key in ext_s]                              # 종목 전체 현재가에서 ext 에 있는 종목 제외, None 시 넘어감, 현재 불필요
            # [bl.remove(key) for key in ext_s if key in bl]                      # ##### 매도 제외 종목 설정 #####
        except Exception as s_cu_p:
            print(f'{linenumber()}p::error--현재가: {s_cu_p}')

        # """ ================ 매도 시작 ================ """
        # try:
        for e in bl:                                            # 자산('bl') 리스트를 하나씩 'e'로 가져 옴
            if abp_check(e, abptime, '/root/UBiCauto/Acct/upbit%s.txt' %(id)):                           # 매수 평단 선택 (체크)
                # abp = abp_check(e, abptime, '/root/UBiCauto/Acct/upbit%s.txt' %(id))                     # 매수평단 최근 매수완료 정보에서 가져 옴
                # print(abp_check)
                pass    # 대기시간 적용 테스트
            else:
                abp = abp1[e]                                   # 매수 평균 "자산정보"(업비트)에서 호출                                                       
                tb = tb1[e]                                         # 종목 보유수량 호출
                """ ~87p 추매 시점 (소수점 2자리에서 반올림) - s """
                addprice = round((abp - (abp * adsp)), 4)           # 추매시점 지정 %, 매수 시 매수평단의 adsp % 이하 일 경우 추매 진행 (평단가)
                addprice_1 = round((abp - (abp * perct(adp1))), 4)       # 추매 시 평단의 -3 # 5% 지점 (코인장 변동폭이 적을 때 적용?)
                addprice_2 = round((abp - (abp * perct(adp2))), 4)
                addprice_3 = round((abp - (abp * perct(adp3))), 4)
                addprice_4 = round((abp - (abp * perct(adp4))), 4)
                addprice_5 = round((abp - (abp * perct(adp5))), 4)
                addprice_6 = round((abp - (abp * perct(adp6))), 4)
                addprice_7 = round((abp - (abp * perct(adp7))), 4)
                addprice_8 = round((abp - (abp * perct(adp8))), 4)
                addprice_9 = round((abp - (abp * perct(adp9))), 4)
                addprice_10 = round((abp - (abp * perct(adp10))), 4)
                """ 75p~ ---------- e """

                if (e in cu_p):                                     # 한 종목에 대한 현재가 추출
                    price = cu_p[e]                                 # '종목' 현재가 가져 옴

                    tp = round(((price - abp) / abp * 100), 2)                  # '종목' 별 수익율 계산                                       
                    t_money = tb * abp                              # 종목 총 매수 금액
                    p_money = price * tb                            # 종목 현재 평가금액
                    loss = p_money - t_money                        # 종목 손실액
                    t_tp.append(loss)                               # 종목 수익률 리스트에 추가
                    goal = abp + (abp * ask_p)                      # 지정가 시 목표 매도가(매수 평균가 기준) 설정 ( 평단가의 - 2.1 % )
                    add_ug = abp - (abp * ask_ug)                   # ma5_under 이하 매수 시 매도 및 추매 조건 데이터(-10% 마다 추매)
                    # 미적용
                        # goal_s = abp + (abp * ask_pp)                   # 지정가 시 예비 매도걸기
                        # a_o = get_tick_s(goal)                          # 지정가 시 매도 호가 계산(매도 지정가)

                    # s1_bm1, s1_bm2 = s1_bull_m1(e)                          # bulling~ check
                    try:
                        s1_bm1 = s1_bull_m1(e)[0]
                        if s1_bm1:
                            s1_bm1_dic[e] = s1_bm1
                    except Exception as error:
                        s1_bm1 = s1_bm1_dic.get(e)
                        print(f'{linenumber()}p::id:{id}:error:s1_bm1: {error}\n {e}: {s1_bm1}')
                    try:
                        s1_bm2 = s1_bull_m1(e)[1]                          # bulling~ check
                        if s1_bm2:
                            s1_bm2_dic[e] = s1_bm2
                    except Exception as error:
                        s1_bm2 = s1_bm2_dic.get(e)
                        print(f'{linenumber()}p::id:{id}:error:s1_bm2: {error}\n {e}: {s1_bm2}')
                    
                    """ ~122p  매수금액 변경 시 일부 적용 - s """
                    with open('/root/UBiCauto/data/set_cfg%s.pickle' %(id), 'rb') as fset:
                        ubic_conf = pickle.load(fset)
                    b_money = ubic_conf['b_money']          # set_cfg1.pickle에서 b_money 값을 호출

                    if t_money <= 5000:     # 매도 후 잔금이 5000원 이하 남을 시 추매 (0.01 -> 0.1로 변경 3/15)
                        bid_money = (b_money + 200)- t_money
                        upbit.buy_market_order(e, bid_money)   # 현매수금액과 차액만큼 매수
                        add_rw0(e, id)                  # 매수 후 애드넘 횟수 초기화(0번)
                        
                        if os.path.isfile('/root/UBiCauto/data/add_num%s.pickle' %(id)):
                            with open('/root/UBiCauto/data/add_num%s.pickle' %(id), 'rb') as fr:
                                add_num = pickle.load(fr)
                        with open('/root/UBiCauto/find_s%s.log' %(id),'a') as fw:
                            print(f'{linenumber()}p::잔금 5천원 이하 추매 됨-{now}:종목:{e}, 총계: {t_money}, 매수금액:{ag_price1}, 추매수:{add_num[e][0:1]}, tb: {tb}, abp:{abp}', file=fw)
                    """ 109p~ ---------- e """

                    if sell_cont == 0:          # (0) 전체 매도 제외, 전체 추매 제외
                        pass
                    else:
                        """ ~141p 매도 기능 - s """
                        if (sell_cont == 1) or (sell_cont == 2):            # (1) 매도(o) 추매(o): (2) 매도(o), 추매(x) 
                            if s1_bm1 and (s1_bm2 < price):                 # bulling + 매도기준 만족 시
                                pass
                            elif goal < price:  # 목표가 < 현재가 되면 ((매도)) 실행
                                if e in ext_s:
                                    pass
                                else:
                                    a_order = upbit.sell_limit_order(e, price, tb)       # '지정가 < 현재가' 조건 시 현재가 매도 실행
                                    
                                    ext_save(id, bl, ext_item)            # 제외종목 매도 후 제외리스트에서 삭제 후 저장
                                    with open('/root/UBiCauto/find_ask%s.log' %(id),'a') as fw:
                                        print(f'{linenumber()}p::-{now}:매도종목-1:{e}, 목표가:{goal}, 현재가:{price}, 평단가:{abp}, 수량:{tb}', file=fw)
                                    # 미적용
                                        # print(j, "판매완료")                        
                                        # upbit.sell_market_order(e, tb)  # '종목' 을 시장가로 매도
                                        # a_order = upbit.sell_limit_order(e, a_o, tb)       # '지정가 < 현재가' 조건 시 지정가 매도 실행
                        """ 128p~ ---------- e """
                        """ ~740p 추매 기능 - s """
                        if (sell_cont == 1) or (sell_cont == 3):          # 추매기능
                            if e in ext_a:
                                pass
                            elif price < goal:                                      #  현재가 < 목표가
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
                                # b2_bm1, b2_bm2 = b2_decline_m1(e)                   # 추매지연 조건 2
                                try:
                                    b2_bm1 = b2_decline_m1(e)[0]
                                    if b2_bm1:
                                        b2_bm1_dic[e] = b2_bm1
                                except Exception as error:
                                    b2_bm1 = b2_bm1_dic.get(e)
                                    print(f'{linenumber()}p::id:{id}:error:b2_bm1: {error}\n {e}: {b2_bm1}')
                                try:
                                    b2_bm2 = b2_decline_m1(e)[1]                   # 추매지연 조건 2
                                    if b2_bm2:
                                        b2_bm2_dic[e] = b2_bm2
                                except Exception as error:
                                    b2_bm2 = b2_bm2_dic.get(e)
                                    print(f'{linenumber()}p::id:{id}:error:b2_bm2: {error}\n {e}: {b2_bm2}')    
                                t_money = tb * abp  # 해당 종목 보유 금액

                                """ b_money = 20,000 일 경우의 예 """
                                plus_m = 100            # b_money 금액에 조금의 여유금액을 더함
                                # print(f'{linenumber()}p::plus_m: {plus_m}')            # b_money 금액에 조금의 여유금액을 더함

                                ag_price1 = b_money * ag1                       # ag_price1 : 10,000
                                sum1 = b_money + ag_price1 + plus_m             # 1차 총계 : 30,000
                                ag_price2 = (sum1 - plus_m) * ag2               # ag_price2 : 9,000
                                sum2 = (sum1 - plus_m) + ag_price2 + plus_m     # 2차 총계 : 39,000
                                ag_price3 = (sum2 - plus_m) * ag3               # ag_price3 : 15,600
                                sum3 = (sum2 - plus_m) + ag_price3 + plus_m     # 3차 총계 : 54,600
                                ag_price4 = (sum3 - plus_m) * ag4               # ag_price4 : 54,600
                                sum4 = (sum3 - plus_m) + ag_price4 + plus_m     # 4차 총계 : 109,200
                                ag_price5 = (sum4 - plus_m) * ag5               # ag_price5 : 109,200
                                sum5 = (sum4 - plus_m) + ag_price5 + plus_m     # 5차 총계 : 218,400
                                ag_price6 = (sum5 - plus_m) * ag6               # ag_price6 : 218,400
                                sum6 = (sum5 - plus_m) + ag_price6 + plus_m     # 6차 총계 : 436,800
                                ag_price7 = (sum6 - plus_m) * ag7               # ag_price7 : 436,800
                                sum7 = (sum6 - plus_m) + ag_price7 + plus_m     # 7차 총계 : 873,600
                                ag_price8 = (sum7 - plus_m) * ag8               # ag_price8 : 873,600
                                sum8 = (sum7 - plus_m) + ag_price8 + plus_m     # 8차 총계 : 1,747,200
                                ag_price9 = (sum8 - plus_m) * ag9               # ag_price9 : 1,747,200
                                sum9 = (sum8 - plus_m) + ag_price9 + plus_m    # 9차 총계 : 3,494,400
                                ag_price10 = (sum9 - plus_m) * ag10             # ag_price10 : 3,494,400
                                sum10 = (sum9 - plus_m) + ag_price10 + plus_m  # 10차 총계 : 6,988,800

                                # print(ag_price1, ag_price2, ag_price3, ag_price4, ag_price5, ag_price6, ag_price7, ag_price8, ag_price9, ag_price10 )
                                # print("%s" %(id), f'sum1:({sum1}), sum2:({sum2}), sum3:({sum3}), sum4:({sum4}), sum5:({sum5}), sum6:({sum6}), sum7:({sum7}), sum8:({sum8}), sum9:({sum9}), sum10:({sum10})')

                                """ ======== 보유종목이 추매종목에 없으면 추매 횟수 dict 에 종목 추가한다 ========"""
                                """ ======= 추매파일이 경로에 있으면 불러오고 없으면 통과 ======== """
                                if os.path.isfile('/root/UBiCauto/data/add_num%s.pickle' %(id)):
                                    with open('/root/UBiCauto/data/add_num%s.pickle' %(id), 'rb') as fr:
                                        add_num = pickle.load(fr)
                                if e not in add_num :           # add_num에 종목이 없을 때 실행
                                    cbid = get_orderi('done', 'bid', 'i', '/root/UBiCauto/Acct/upbit%s.txt' %(id))         # 매수완료 정보 가져오기
                                    for i in cbid:
                                        if e == i['market']:
                                            cprice = i['price']                           # 매수완료 정보 중 마지막 종목의 매수금액
                                            cvolume = i['volume']                         # 매수완료 정보 중 마지막 종목의 매수수량
                                            f_bidv0 = float(cprice) * float(cvolume)            # 매수 금액
                                            print(f'{linenumber()}p::매수금액-f_bidv0: {f_bidv0}')
                                            global f_bidv 
                                            f_bidv = round((f_bidv0 + (f_bidv0 * 0.0005)), 2)   # 매수 금액 + 수수료
                                    
                                    if (t_money < b_money) and (t_money):           # 초기 매수 시 횟수 0 입력
                                        adn1 = 0
                                    elif b_money <= t_money:            # t_money 가 초기매수가보다 클 때 추매 횟수 선택
                                        sum0 = 0
                                        if sum0 < t_money <= sum1 :
                                            adn1 = 0
                                        elif sum1 < t_money <= sum2 :
                                            adn1 = 1
                                        elif sum2 < t_money <= sum3 :
                                            adn1 = 2
                                        elif sum3 < t_money <= sum4 :
                                            adn1 = 3
                                        elif sum4 < t_money <= sum5 :
                                            adn1 = 4
                                        elif sum5 < t_money <= sum6 :
                                            adn1 = 5
                                        elif sum6 < t_money <= sum7 :
                                            adn1 = 6
                                        elif sum7 < t_money <= sum8 :
                                            adn1 = 7
                                        elif sum8 < t_money <= sum9 :
                                            adn1 = 8
                                        elif sum9 < t_money <= sum10 :
                                            adn1 = 10

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
                                    print(f'{linenumber()}p::addnum-신규종목발생-id: {id}, 추매종목포함시:{e}, 매수가: {b_money},  adn1: {adn1}')                         # 매수 후 추매 횟수 생성 확인        
                                    add_rwinit(e, id, adn1, adn2, f_bidv)            # 새 종목 매수 시 목록 추가 (매수완료 종목명을 dict 에 [추매횟수, 추매위치, 첫 매수가]으로 추가, 처음 매수시수
                                    print(f'{linenumber()}p::애드넘추가-({e}, {id}, {adn1}, {adn2}, {f_bidv}')

                                if b_money < blow_money:                        # 최소 매수금액 'blow_money' 로 제한
                                    b_money = blow_money                        # 최저 매수금액 설정
                                    
                                an = add_get(e, id)         # add_num 호출 및 매도횟수 불러와서 an에 바인딩

                                # print('종목 [' + '\033[1m' + f'{e}' + '\033[0m' + '] ┆\0 ' + f'종목금액 ({format(round(t_money, 3),",")}) ┆ 수익률 (' + '\033[1m' + f'{tp}' + '\033[0m' + ') ┆ 추매횟수 (' + '\033[1m' + f'{an}' + '\033[0m' + ') ┆\n' + f'보유수량 {tb} ┆ b_money({b_money})')
                                """ === 추매 횟수(an), 제한횟수(ap), 현가(price), 평단가(abp), 1차 목표가(buy_goal10), 보유금액(t_money), 제한가(l_money) ==="""

                                """ test 중 ~~ S """
                                if ag_price1 < 5000 :       # 추매 시 원금의 몇 배(ag_price1)
                                    ag_price1 == 5000
                                if ag_price2 < 5000 :
                                    ag_price2 == 5000
                                """ 위 2개 if 문 추가 함 """
                                
                                if b2_bm1 and (price < b2_bm2):           # decline + 추매지연기준 2    
                                    pass

                                # elif (an == 0) and (an < ap) and (5000 < t_money < (b_money * 1.1)) and (price < addprice_1) and (0.1 < addprice_1) and (5000 <= ag_price1) and (t_money < l_money) and (ag_price1 < summ):     # price: 종목현재가
                                elif (an < ap) and (5000 < t_money <= (b_money * 1.1)) and (price < addprice_1) and (0.1 < addprice_1) and (5000 <= ag_price1) and (t_money < l_money) and (ag_price1 < summ):     # price: 종목현재가
                                    # elif t_money < (b_money * 1.2) and (price < addprice_1) :     # -3% (-3%)
                                    # upbit.buy_market_order(e, ag_price1) 1차 추매
                                    tb = ag_price1 / price          # volume : 매수수량 = 매수금액 / 현재가
                                    upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                    add_rw1(e, id); time.sleep(1)
                                    with open('/root/UBiCauto/find_s%s.log' %(id),'a') as fw:
                                        print(f'{linenumber()}p::an(1)-{now}:종목-1:{e}, 추매금액:{ag_price1}, 추매수:{add_num[e][0:1]}, t:{t_money}, b:{b_money}, 현재가:{price}, 1차추매가격:{addprice_1}', file=fw)

                                # elif (an == 1) and (an < ap) and (t_money < sum2) and (price < addprice_2) and (0.1 < addprice_2) and (5000 <= ag_price2) and (t_money < l_money) and (ag_price2 < summ):
                                elif (an < ap) and (t_money <= sum2) and (price < addprice_2) and (0.1 < addprice_2) and (5000 <= ag_price2) and (t_money < l_money) and (ag_price2 < summ):
                                    # upbit.buy_market_order(e, ag_price2) 2차 추매
                                    tb = ag_price2 / price          # volume : 매수수량 = 매수금액 / 현재가
                                    upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                    add_rw2(e, id); time.sleep(1)
                                    with open('/root/UBiCauto/find_s%s.log' %(id),'a') as fw:
                                        print(f'{linenumber()}p::an(2)-{now}:종목-2:{e}, 추매금액:{ag_price2}, 추매수:{add_num[e][0:1]}, t:{t_money}, b:{b_money}, p:{price}, 2차추매가격:{addprice_2}', file=fw)

                                # elif (an == 2) and (an < ap) and (t_money < sum3) and (price < addprice_3) and (0.1 < addprice_3) and (5000 <= ag_price3) and (t_money < l_money)  and (ag_price3 < summ):
                                elif (an < ap) and (t_money <= sum3) and (price < addprice_3) and (0.1 < addprice_3) and (5000 <= ag_price3) and (t_money < l_money)  and (ag_price3 < summ):
                                    # upbit.buy_market_order(e, ag_price3) 3차 추매
                                    tb = ag_price3 / price          # volume : 매수수량 = 매수금액 / 현재가
                                    upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                    add_rw3(e, id); time.sleep(1)
                                    with open('/root/UBiCauto/find_s%s.log' %(id),'a') as fw:
                                        print(f'{linenumber()}p::an(3)-{now}:종목-3:{e}, 추매금액:{ag_price3}, 추매수:{add_num[e][0:1]}, t:{t_money}, b:{b_money}, p:{price}, 3차추매가격{addprice_3}', file=fw)

                                elif (an < ap) and (t_money <= sum4) and (price < addprice_4) and (0.1 < addprice_4) and (5000 <= ag_price4) and (t_money < l_money)  and (ag_price4 < summ):
                                    # upbit.buy_market_order(e, ag_price4) 4차 추매
                                    tb = ag_price4 / price          # volume : 매수수량 = 매수금액 / 현재가
                                    upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                    add_rw4(e, id); time.sleep(1)
                                    with open('/root/UBiCauto/find_s%s.log' %(id),'a') as fw:
                                        print(f'{linenumber()}p::an(4)-{now}:종목-4:{e}, 추매금액:{ag_price4}, 추매수:{add_num[e][0:1]}, t:{t_money}, b:{b_money}, p:{price}, 4차추매가격{addprice_4}', file=fw)

                                elif (an < ap) and (t_money <= sum5) and (price < addprice_5) and (0.1 < addprice_5) and (5000 <= ag_price5) and (t_money < l_money)  and (ag_price5 < summ):
                                    # upbit.buy_market_order(e, ag_price5) 5차 추매
                                    tb = ag_price5 / price          # volume : 매수수량 = 매수금액 / 현재가
                                    upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                    add_rw5(e, id); time.sleep(1)
                                    with open('/root/UBiCauto/find_s%s.log' %(id),'a') as fw:
                                        print(f'{linenumber()}p::an(5){now}:종목-5:{e}, 추매금액:{ag_price5}, 추매수:{add_num[e][0:1]}, t:{t_money}, b:{b_money}, p:{price}, 5차추매가격{addprice_5}', file=fw)

                                elif (an < ap) and (t_money <= sum6) and (price < addprice_6) and (0.1 < addprice_6) and (5000 <= ag_price6) and (t_money < l_money)  and (ag_price6 < summ):
                                    # upbit.buy_market_order(e, ag_price6) 6차 추매
                                    tb = ag_price6 / price          # volume : 매수수량 = 매수금액 / 현재가
                                    upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                    add_rw6(e, id); time.sleep(1)
                                    with open('/root/UBiCauto/find_s%s.log' %(id),'a') as fw:
                                        print(f'{linenumber()}p::an(6){now}:종목-6:{e}, 추매금액:{ag_price6}, 추매수:{add_num[e][0:1]}, t:{t_money}, b:{b_money}, p:{price}, 6차추매가격{addprice_6}', file=fw)

                                elif (an < ap) and (t_money <= sum7) and (price < addprice_7) and (0.1 < addprice_7) and (5000 <= ag_price7) and (t_money < l_money) and (ag_price7 < summ):
                                    # upbit.buy_market_order(e, ag_price7) 7차 추매
                                    tb = ag_price7 / price          # volume : 매수수량 = 매수금액 / 현재가
                                    upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                    add_rw7(e, id); time.sleep(1)
                                    with open('/root/UBiCauto/find_s%s.log' %(id),'a') as fw:
                                        print(f'{linenumber()}p::an(7){now}:종목-7:{e}, 추매금액:{ag_price7}, 추매수:{add_num[e][0:1]}, t:{t_money}, b:{b_money}, p:{price}, 7차추매가격{addprice_7}', file=fw)

                                elif (an < ap) and (t_money <= sum8) and (price < addprice_8) and (0.1 < addprice_8) and (5000 <= ag_price8) and (t_money < l_money) and (ag_price8 < summ):
                                    # upbit.buy_market_order(e, ag_price8) 8차 추매
                                    tb = ag_price8 / price          # volume : 매수수량 = 매수금액 / 현재가
                                    upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                    add_rw8(e, id); time.sleep(1)
                                    with open('/root/UBiCauto/find_s%s.log' %(id),'a') as fw:
                                        print(f'{linenumber()}p::an(8){now}:종목-8:{e}, 추매금액:{ag_price8}, 추매수:{add_num[e][0:1]}, t:{t_money}, b:{b_money}, p:{price}, 8차추매가격{addprice_8}', file=fw)

                                elif (an < ap) and (t_money <= sum9) and (price < addprice_9) and (0.1 < addprice_9) and (5000 <= ag_price9) and (t_money < l_money) and (ag_price9 < summ):
                                    # upbit.buy_market_order(e, ag_price9) 9차 추매
                                    tb = ag_price9 / price          # volume : 매수수량 = 매수금액 / 현재가
                                    upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                    add_rw9(e, id); time.sleep(1)
                                    with open('/root/UBiCauto/find_s%s.log' %(id),'a') as fw:
                                        print(f'{linenumber()}p::an(8){now}:종목-9:{e}, 추매금액:{ag_price9}, 추매수:{add_num[e][0:1]}, t:{t_money}, b:{b_money}, p:{price}, 9차추매가격{addprice_9}', file=fw)

                                elif (an < ap) and (t_money <= sum10) and (price < addprice_10) and (0.1 < addprice_10) and (5000 <= ag_price10) and (t_money < l_money) and (ag_price10 < summ):
                                    # upbit.buy_market_order(e, ag_price10) 10차 추매 
                                    tb = ag_price10 / price          # volume : 매수수량 = 매수금액 / 현재가
                                    upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                    add_rw10(e, id); time.sleep(1)
                                    with open('/root/UBiCauto/find_s%s.log' %(id),'a') as fw:
                                        print(f'{linenumber()}p::an(9){now}:종목-10:{e}, 추매금액:{ag_price10}, 추매수:{add_num[e][0:1]}, t:{t_money}, b:{b_money}, p:{price}, 10차추매가격{addprice_10}', file=fw)

                                    # ---------------------------------------------####################---------------------------------------------------- #
                                    """ E ~~ test 중 ~~ E """

                                elif (addprice < price) and (0.1 < addprice) :          # 매수평단 (adsp값)% 이하 만족 시(현재가가 ()이하 시 추매 들어감), addprice에 터무니없이 낮은값이 들어올경우대비(0.1 초과조건)
                                    pass
                                
                                    # ---------------------------------------------# 추매 (0 > 1)회 시 #---------------------------------------------------- #
                                    
                                elif (an == 0) and (an < ap) and (summ >= (t_money * 1.1)) and (t_money <= sum1) and (t_money < l_money) and (5000 <= ag_price1) and (0.1 < addprice_1) and (ag_price1 < summ):            # abp(평단가)
                                    
                                    if (buy_goal5[1] < abp) and (price < buy_goal10[0]):
                                        # upbit.buy_market_order(e, ag_price1)
                                        tb = ag_price1 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav5(an, e, id)
                                        with open('find_s%s.log' %(id),'a') as fw:
                                            print(f'{linenumber()}p::an(0){now}:종목:{e}, 추매금액:{ag_price1}, 추매수:{add_num[e][0:1]}', file=fw)

                                    elif (buy_goal10[1] < abp) and (price < buy_goal20[0]): 
                                        # upbit.buy_market_order(e, ag_price1)
                                        tb = ag_price1 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav10(an, e, id)

                                    elif (buy_goal20[1] < abp) and (price < buy_goal30[0]): 
                                        # upbit.buy_market_order(e, ag_price1)
                                        tb = ag_price1 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav20(an, e, id)
                                    
                                    elif (buy_goal30[1] < abp) and (price < buy_goal40[0]): 
                                        # upbit.buy_market_order(e, ag_price1)
                                        tb = ag_price1 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav30(an, e, id)
                                    
                                    elif (buy_goal40[1] < abp) and (price < buy_goal50[0]): 
                                        # upbit.buy_market_order(e, ag_price1)
                                        tb = ag_price1 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav40(an, e, id)

                                    elif (buy_goal50[1] < abp) and (price < buy_goal60[0]): 
                                        # upbit.buy_market_order(e, ag_price1)
                                        tb = ag_price1 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav50(an, e, id)

                                    elif (buy_goal60[1] < abp) and (price < buy_goal70[0]): 
                                        # upbit.buy_market_order(e, ag_price1)
                                        tb = ag_price1 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav60(an, e, id)
                                    
                                    elif (buy_goal70[1] < abp) and (price < buy_goal80[0]): 
                                        # upbit.buy_market_order(e, ag_price1)
                                        tb = ag_price1 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav70(an, e, id)

                                    elif (buy_goal80[1] < abp) and (price < buy_goal90[0]): 
                                        # upbit.buy_market_order(e, ag_price1)
                                        tb = ag_price1 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav80(an, e, id)

                                    elif (buy_goal90[1] < abp) and (price < add_ug): 
                                        # upbit.buy_market_order(e, ag_price1)
                                        tb = ag_price1 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav90(an, e, id)

                                    elif (buy_goal90[1] > abp) and (price < add_ug): 
                                        # upbit.buy_market_order(e, ag_price1)
                                        tb = ag_price1 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav90(an, e, id)

                                    time.sleep(1)

                                        # --------------------------------------------# 추매 (1 > 2)회 시 #---------------------------------------------------- #
                                elif (an == 1) and (an < ap) and (summ >= (t_money * 1.1)) and (t_money <= sum2) and (t_money < l_money) and (5000 <= ag_price2) and (0.1 < addprice_2) and (ag_price2 < summ):
                                    if (buy_goal5[1] < abp) and (price < buy_goal10[0]): 
                                        # upbit.buy_market_order(e, ag_price2) 
                                        tb = ag_price2 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav5(an, e, id)

                                    elif (buy_goal10[1] < abp) and (price < buy_goal20[0]): 
                                        # upbit.buy_market_order(e, ag_price2)
                                        tb = ag_price2 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav10(an, e, id)

                                    elif (buy_goal20[1] < abp) and (price < buy_goal30[0]): 
                                        # upbit.buy_market_order(e, ag_price2)
                                        tb = ag_price2 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav20(an, e, id)

                                    elif (buy_goal30[1] < abp) and (price < buy_goal40[0]): 
                                        # upbit.buy_market_order(e, ag_price2)
                                        tb = ag_price2 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav30(an, e, id)

                                    elif (buy_goal40[1] < abp) and (price < buy_goal50[0]): 
                                        # upbit.buy_market_order(e, ag_price2)
                                        tb = ag_price2 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav40(an, e, id)

                                    elif (buy_goal50[1] < abp) and (price < buy_goal60[0]): 
                                        # upbit.buy_market_order(e, ag_price2)
                                        tb = ag_price2 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav50(an, e, id)

                                    elif (buy_goal60[1] < abp) and (price < buy_goal70[0]): 
                                        tb = ag_price2 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav60(an, e, id)

                                    elif (buy_goal70[1] < abp) and (price < buy_goal80[0]): 
                                        tb = ag_price2 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav70(an, e, id)

                                    elif (buy_goal80[1] < abp) and (price < buy_goal90[0]): 
                                        tb = ag_price2 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav80(an, e, id)

                                    elif (buy_goal90[1] < abp) and (price < add_ug): 
                                        tb = ag_price2 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav90(an, e, id)

                                    elif (buy_goal90[1] > abp) and (price < add_ug): 
                                        tb = ag_price2 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav90(an, e, id)

                                    time.sleep(1)

                                        # --------------------------------------------# 추매 (2 > 3)회 시 #---------------------------------------------------- #
                                elif (an == 2) and (an < ap) and (summ >= (t_money * 1.1)) and (t_money <= sum3) and (t_money < l_money) and (5000 <= ag_price3) and (0.1 < addprice_3) and (ag_price3 < summ):

                                    if (buy_goal5[1] < abp) and (price < buy_goal10[0]): 
                                        tb = ag_price3 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매 
                                        add_rwav5(an, e, id)

                                    elif (buy_goal10[1] < abp) and (price < buy_goal20[0]): 
                                        tb = ag_price3 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav10(an, e, id)

                                    elif (buy_goal20[1] < abp) and (price < buy_goal30[0]): 
                                        tb = ag_price3 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav20(an, e, id)
                                    
                                    elif (buy_goal30[1] < abp) and (price < buy_goal40[0]): 
                                        tb = ag_price3 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav30(an, e, id)

                                    elif (buy_goal40[1] < abp) and (price < buy_goal50[0]): 
                                        tb = ag_price3 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav40(an, e, id)

                                    elif (buy_goal50[1] < abp) and (price < buy_goal60[0]): 
                                        tb = ag_price3 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav50(an, e, id)

                                    elif (buy_goal60[1] < abp) and (price < buy_goal70[0]): 
                                        tb = ag_price3 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav60(an, e, id)

                                    elif (buy_goal70[1] < abp) and (price < buy_goal80[0]): 
                                        tb = ag_price3 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav70(an, e, id)

                                    elif (buy_goal80[1] < abp) and (price < buy_goal90[0]): 
                                        tb = ag_price3 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav80(an, e, id)

                                    elif (buy_goal90[1] < abp) and (price < add_ug): 
                                        tb = ag_price3 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav90(an, e, id)

                                    elif (buy_goal90[1] > abp) and (price < add_ug): 
                                        # buy_goal90[1] 이하 추매 시 add_ug: ()% 이하 시에 추매
                                        tb = ag_price3 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav90(an, e, id)

                                    time.sleep(1)                            

                                        # --------------------------------------------# 추매 (3 > 4)회 시 #---------------------------------------------------- #
                                        # ********************************************************************************* #
                                elif (an == 3) and (an < ap) and (summ >= (t_money * 1.1)) and (t_money <= sum4) and (t_money < l_money) and (5000 <= ag_price4) and (0.1 < addprice_4) and (ag_price4 < summ):

                                    if (buy_goal5[1] < abp) and (price < buy_goal10[0]): 
                                        tb = ag_price4 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav5(an, e, id)

                                    elif (buy_goal10[1] < abp) and (price < buy_goal20[0]): 
                                        tb = ag_price4 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav10(an, e, id)

                                    elif (buy_goal20[1] < abp) and (price < buy_goal30[0]): 
                                        tb = ag_price4 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav20(an, e, id)

                                    elif (buy_goal30[1] < abp) and (price < buy_goal40[0]): 
                                        tb = ag_price4 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav30(an, e, id)

                                    elif (buy_goal40[1] < abp) and (price < buy_goal50[0]): 
                                        tb = ag_price4 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav40(an, e, id)

                                    elif (buy_goal50[1] < abp) and (price < buy_goal60[0]): 
                                        tb = ag_price4 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav50(an, e, id)

                                    elif (buy_goal60[1] < abp) and (price < buy_goal70[0]): 
                                        tb = ag_price4 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav60(an, e, id)

                                    elif (buy_goal70[1] < abp) and (price < buy_goal80[0]): 
                                        tb = ag_price4 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav70(an, e, id)

                                    elif (buy_goal80[1] < abp) and (price < buy_goal90[0]): 
                                        tb = ag_price4 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav80(an, e, id)

                                    elif (buy_goal90[1] < abp) and (price < add_ug): 
                                        tb = ag_price4 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav90(an, e, id)

                                    elif (buy_goal90[1] > abp) and (price < add_ug): 
                                        tb = ag_price4 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav90(an, e, id)

                                    time.sleep(1)                  

                                        # --------------------------------------------# 추매 (4 > 5)회 시 #---------------------------------------------------- #
                                elif (an == 4) and (an < ap) and (summ >= (t_money * 1.1)) and (t_money <= sum5) and (t_money < l_money) and (5000 <= ag_price5) and (0.1 < addprice_5) and (ag_price5 < summ):

                                    if (buy_goal5[1] < abp) and (price < buy_goal10[0]): 
                                        tb = ag_price5 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav5(an, e, id)

                                    elif (buy_goal10[1] < abp) and (price < buy_goal20[0]): 
                                        tb = ag_price5 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav10(an, e, id)

                                    elif (buy_goal20[1] < abp) and (price < buy_goal30[0]): 
                                        tb = ag_price5 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav20(an, e, id)

                                    elif (buy_goal30[1] < abp) and (price < buy_goal40[0]): 
                                        tb = ag_price5 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav30(an, e, id)

                                    elif (buy_goal40[1] < abp) and (price < buy_goal50[0]): 
                                        tb = ag_price5 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav40(an, e, id)

                                    elif (buy_goal50[1] < abp) and (price < buy_goal60[0]): 
                                        tb = ag_price5 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav50(an, e, id)

                                    elif (buy_goal60[1] < abp) and (price < buy_goal70[0]): 
                                        tb = ag_price5 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav60(an, e, id)

                                    elif (buy_goal70[1] < abp) and (price < buy_goal80[0]): 
                                        tb = ag_price5 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav70(an, e, id)

                                    elif (buy_goal80[1] < abp) and (price < buy_goal90[0]): 
                                        tb = ag_price5 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav80(an, e, id)

                                    elif (buy_goal90[1] < abp) and (price < add_ug): 
                                        tb = ag_price5 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav90(an, e, id)

                                    elif (buy_goal90[1] > abp) and (price < add_ug):
                                        tb = ag_price5 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav90(an, e, id)

                                    time.sleep(1)

                                    # --------------------------------------------# 추매 (5 > 6)회 시 #---------------------------------------------------- #
                                elif (an == 5) and (an < ap) and (summ >= (t_money * 1.1)) and (t_money <= sum6) and (t_money < l_money) and (5000 <= ag_price6) and (0.1 < addprice_6) and (ag_price6 < summ):
                                    if (buy_goal5[1] < abp) and (price < buy_goal10[0]): 
                                        tb = ag_price6 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav5(an, e, id)

                                    elif (buy_goal10[1] < abp) and (price < buy_goal20[0]): 
                                        tb = ag_price6 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav10(an, e, id)

                                    elif (buy_goal20[1] < abp) and (price < buy_goal30[0]): 
                                        tb = ag_price6 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav20(an, e, id)

                                    elif (buy_goal30[1] < abp) and (price < buy_goal40[0]): 
                                        tb = ag_price6 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav30(an, e, id)

                                    elif (buy_goal40[1] < abp) and (price < buy_goal50[0]): 
                                        tb = ag_price6 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav40(an, e, id)

                                    elif (buy_goal50[1] < abp) and (price < buy_goal60[0]): 
                                        tb = ag_price6 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav50(an, e, id)

                                    elif (buy_goal60[1] < abp) and (price < buy_goal70[0]): 
                                        tb = ag_price6 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav60(an, e, id)

                                    elif (buy_goal70[1] < abp) and (price < buy_goal80[0]): 
                                        tb = ag_price6 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav70(an, e, id)

                                    elif (buy_goal80[1] < abp) and (price < buy_goal90[0]): 
                                        tb = ag_price6 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav80(an, e, id)

                                    elif (buy_goal90[1] < abp) and (price < add_ug): 
                                        tb = ag_price6 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav90(an, e, id)

                                    elif (buy_goal90[1] > abp) and (price < add_ug): 
                                        tb = ag_price6 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav90(an, e, id)

                                    time.sleep(1)

                                    # --------------------------------------------# 추매 (6 > 7)회 시 #---------------------------------------------------- #
                                elif (an == 6) and (an < ap) and (summ >= (t_money * 1.1)) and (t_money <= sum7) and (t_money < l_money) and (5000 <= ag_price7) and (0.1 < addprice_7) and (ag_price7 < summ):
                                    if (buy_goal5[1] < abp) and (price < buy_goal10[0]): 
                                        tb = ag_price7 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav5(an, e, id)

                                    elif (buy_goal10[1] < abp) and (price < buy_goal20[0]): 
                                        tb = ag_price7 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav10(an, e, id)

                                    elif (buy_goal20[1] < abp) and (price < buy_goal30[0]): 
                                        tb = ag_price7 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav20(an, e, id)

                                    elif (buy_goal30[1] < abp) and (price < buy_goal40[0]): 
                                        tb = ag_price7 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav30(an, e, id)

                                    elif (buy_goal40[1] < abp) and (price < buy_goal50[0]): 
                                        tb = ag_price7 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav40(an, e, id)

                                    elif (buy_goal50[1] < abp) and (price < buy_goal60[0]): 
                                        tb = ag_price7 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav50(an, e, id)

                                    elif (buy_goal60[1] < abp) and (price < buy_goal70[0]): 
                                        tb = ag_price7 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav60(an, e, id)

                                    elif (buy_goal70[1] < abp) and (price < buy_goal80[0]): 
                                        tb = ag_price7 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav70(an, e, id)

                                    elif (buy_goal80[1] < abp) and (price < buy_goal90[0]): 
                                        tb = ag_price7 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav80(an, e, id)

                                    elif (buy_goal90[1] < abp) and (price < add_ug): 
                                        tb = ag_price7 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav90(an, e, id)

                                    elif (buy_goal90[1] > abp) and (price < add_ug): 
                                        tb = ag_price7 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav90(an, e, id)

                                    time.sleep(1)

                                        # --------------------------------------------# 추매 (7 > 8)회 시 #---------------------------------------------------- #
                                elif (an == 7) and (an < ap) and (summ >= (t_money * 1.1)) and (t_money <= sum8) and (t_money < l_money) and (5000 <= ag_price8) and (0.1 < addprice_8) and (ag_price8 < summ):
                                    if (buy_goal5[1] < abp) and (price < buy_goal10[0]):
                                        tb = ag_price8 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav5(an, e, id)

                                    elif (buy_goal10[1] < abp) and (price < buy_goal20[0]): 
                                        tb = ag_price8 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav10(an, e, id)

                                    elif (buy_goal20[1] < abp) and (price < buy_goal30[0]): 
                                        tb = ag_price8 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav20(an, e, id)

                                    elif (buy_goal30[1] < abp) and (price < buy_goal40[0]):
                                        tb = ag_price8 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav30(an, e, id)

                                    elif (buy_goal40[1] < abp) and (price < buy_goal50[0]): 
                                        tb = ag_price8 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav40(an, e, id)

                                    elif (buy_goal50[1] < abp) and (price < buy_goal60[0]): 
                                        tb = ag_price8 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav50(an, e, id)

                                    elif (buy_goal60[1] < abp) and (price < buy_goal70[0]): 
                                        tb = ag_price8 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav60(an, e, id)

                                    elif (buy_goal70[1] < abp) and (price < buy_goal80[0]):
                                        tb = ag_price8 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav70(an, e, id)

                                    elif (buy_goal80[1] < abp) and (price < buy_goal90[0]): 
                                    
                                        tb = ag_price8 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav80(an, e, id)

                                    elif (buy_goal90[1] < abp) and (price < add_ug):
                                        tb = ag_price8 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav90(an, e, id)

                                    elif (buy_goal90[1] > abp) and (price < add_ug): 
                                        tb = ag_price8 / price          # volume : 매수수량 = 매수금액 / 현재가
                                        upbit.buy_limit_order(e, price, tb)         # 현재가 추매
                                        add_rwav90(an, e, id)
                        """ 143p~ ---------- e """

        # print(f'{linenumber()}p::id:{id},추매 후-{now}:종목:{e}, 총계: {t_money}, 남은금액:{summ} 매수금액a_p1:{ag_price1}, a_p2:{ag_price2},  a_p3:{ag_price3} 추매수:{add_num[e][0:1]}, tb: {tb}, abp:{abp}')

        with open('/root/UBiCauto/data/t_tp%s.pickle' %(id), 'wb') as fw:    # 보유종목 평가손익(list 로 저장)
            pickle.dump(t_tp, fw)
        # except Exception as s1:
            # print(f'{linenumber()}p::error:e-time:{datetime.now()}, s1_매도및추매 프로세스:{s1}')

        sum_tp = sum(t_tp)                         # 총 보유 평가손익 계산금액
        ask_p = askper(upbit, 1)                   # 매도기준 조정 및 저장

        """ 755P 매도 후 매수 횟수 항목 갱신 """

        try:    # 매도 후 매수횟수 갱신 (add_num파일 불러와서 제외항목 제거 후 재저장)
            ex_item(bl, id)                                  # 매수 횟수 항목 갱신 함수 사용
        except Exception as add_num_r:
            print(f'{linenumber()}p::error-매수횟수 항목 갱신:매도후 adn갱신: {add_num_r}')

        """ ~777p 매도대기 취소 절차 진행 (매도 조건을 만족하지 못하면 아래 조건을 비교하여 매도대기 취소) - s """
        try:    # 매도대기 취소
            ask_w_i = get_orderi('wait', 'ask', 'i', '/root/UBiCauto/Acct/upbit%s.txt' %(id))                                # 매도대기 목록 정보 리스트
            ask_w_list = get_orderi('wait', 'ask', 'n', '/root/UBiCauto/Acct/upbit%s.txt' %(id))                             # 매도대기 종목 리스트

            for an in range(len(ask_w_list)):                               # list 에서 매도대기 종목(dict) 항목 추출
                uuids_an = ask_w_i[an]['market']                            # 매도대기 종목 정보에서 가져 온 종목이름
                if (uuids_an in ext_s):             # 매도제외 종목에 대기종목이 있을 경우 또는 KRW-BTT 
                    pass
                else:
                    uuids_aid = ask_w_i[an]['uuid']                             # bid_w_i[bn] 번째 종목의 'uuid' 의 값
                    a1_time1 = ask_w_i[an]['created_at']                        # 매도대기 종목 order 시간
                    a1_time = t_c(a1_time1)                                     # 계산을 위해 order 시간 형식 변환
                    mt = (a1_time + timedelta(minutes=agt))                     # 매도대기 시간 10분 지난 시간 계산
                    # if (mt <= datetime.now()) or (uuids_an not in bl):          # 지정시간이 지났는지, 자산목록에 종목이 있는지 확인 후
                    if (mt <= datetime.now()):                                  # 지정시간이 지났는지, 자산목록에 종목이 있는지 확인 후
                        b_cancel = upbit.cancel_order(uuids_aid)               # 매도 대기 취소
        except Exception as s3:
            print(f'{linenumber()}p::error:매도대기 취소:e-time:, {datetime.now()}, {s3}')
        """ 760p~ ---------- e """

        """ ~789p 종목 갯수별 시간지연 적용 - s """
        if len(bl) <= 10:
            time.sleep(6)
        elif len(bl) <= 30:
            time.sleep(4)
        elif len(bl) <= 40:
            time.sleep(3)
        elif len(bl) <= 50:
            time.sleep(1)
        """ 780p~ ---------- e """

        if os.path.isfile('/root/UBiCauto/data/add_num%s.pickle' %(id)) and os.path.getsize('/root/UBiCauto/data/add_num1.pickle') > 5:
            # os.system('clear')
            print(f'{linenumber()}p::id:( {id} )\n보유종목수:[{len(bl)}] | 애드넘: [{len(add_num)}]\nadd_num={add_num}\n')
            
        # print("--- %s seconds ---" % round((time.time() - start_time), 3))          # 1Cycle 시간
        print(f'{linenumber()}p::id:( {id} ) --- (1) Cycle time: {round((time.time() - start_time), 3)} seconds ---\n')          # 1Cycle 시간

if __name__ == '__main__':
    id_lists = ['1', '2', '3']          # 계정별 구분자
    thread_dicts = {}
    for id in id_lists:         # thread 실행
        t = threading.Thread(target=ubic_sell, args=(id, ))         # ubic_sell 함수를 실행(문자열 id로 구분)
        t.daemon = True         # UBiC_Sell.py(main process)가 종료되면 각각의 프로세스(daemon) 데몬도 같이 실행 종료
        t.start()               # thread 시작
        thread_dicts[id] = t
        print(t)

    while True:         # health check
        for id in id_lists:
            if thread_dicts[id].is_alive():         # thread daemon이 실행되고 있는지 확인 후 출력
                print(f'{linenumber()}p::id:( {id} )-{thread_dicts[id].is_alive}')
            else:
                t = threading.Thread(target=ubic_sell, args=(id, ))         # thread daemon 종료 확인 시 재실행
                t.daemon = True
                t.start()
                thread_dicts[id] = t
        time.sleep(30)
# -*- coding:utf-8 -*-

from UBiC_Search_def import one_sell
# from UBiC_Rotate_data import gb, cp1, upbit2
from UBiC_Rotate_data import gb, upbit2
import time
import keyboard
import pickle


# 한 종목(제일 높은 수익) 수동 즉시 매도 실행

# def plus_profit(upbit2):
while True:
    # start_time = time.time()                    # 시간 측정 시작
    bl, avg_p, tb = gb(upbit2)
    # bl = gb(upbit2)[0]
    # avg_p = gb(upbit2)[1]
    # tb = gb(upbit2)[2]
    plus_profit = {}
    # try:
    #     cu_p = cp1()   
    #     ext_s = ['KRW-VTHO', 'KRW-XYM', 'KRW-APENFT']  # 전체 종목과 현재가 dict 'cu_p' 로 바인딩
    #     [cu_p.pop(key, None) for key in ext_s]                # 종목 전체 현재가에서 ext 에 있는 종목 제외, None 시 넘어감, 현재 불필요
    #     [bl.remove(key) for key in ext_s if key in bl]        # 매도 제외 종목 설정 
    # except Exception as p:
    #     print("cu_p", p)
    with open('/root/UBiCauto/data/add_num2.pickle', 'rb') as fr:
        add_num = pickle.load(fr)

    try:
        with open('/root/UBiCauto/data/cp.pickle', 'rb') as fr1:            # mycal 불러오기
            cu_p = pickle.load(fr1)  
        ext_s = []  # 전체 종목과 현재가 dict 'cu_p' 로 바인딩
        [cu_p.pop(key, None) for key in ext_s]                # 종목 전체 현재가에서 ext 에 있는 종목 제외, None 시 넘어감, 현재 불필요
        [bl.remove(key) for key in ext_s if key in bl]        # 매도 제외 종목 설정 
    except Exception as p:
        print("cu_p", p)

    try:
        for e, avg in avg_p.items():
            if e in cu_p:
                price = cu_p[e]
                tp = round((((price - avg) / avg) * 100), 2)            # '종목' 별 수익율 계산
                tn = tb[e] 
                t_money = round((avg * tn), 2)
                tbp = [tp, format(t_money, ",")]                        # 각종목 (수익율, 매수금액)을 리스트로 추가

            if 0 < tp :                
                plus_profit[e] = tbp
        plus_profit = sorted(plus_profit.items(), key=lambda x: x[1][0], reverse=True)

        if 0 < (len(plus_profit)) :
            print(f'────────────────────────────────────────────────────────────\n\
👍 \0 {e} ┆〚 {plus_profit[0][1][0]} 〛┆ {plus_profit[0][1][1]} ┆ cp:⟮{cu_p[e]}⟯ ┆ ADN:⟮{add_num[e][0]}⟯\n\
────────────────────────────────────────────────────────────\n')
            print(f'({len(plus_profit)}) ⇪ 종목 상승 중 ∽\0  ⇪ \n {plus_profit} \n')
            # print(f'first {plus_profit[0]}')
            # e = plus_profit[0][0]
            
            time.sleep(1)

            """ 수동 종목 매도 시 """
            # e = "KRW-STORJ"                    # 수동 종목 매도 시 사용
            """ ----------------- """
            # one_sell(upbit2,e)              # 종목 즉시 매도
            #     break
            # else:
            #     pass
        else:
            print("──────────────────\n ⇩ 종목 없음 ⇩ ⨶ \n──────────────────")
            time.sleep(1)

    except Exception as p:
        print(p) 
    # print("-- %s seconds --" % round((time.time() - start_time), 2))        # time check
    # return e




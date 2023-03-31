# -*- coding:utf-8 -*-

from UBiC_Search_def import one_sell, ticker_per
# from UBiC_Rotate_data import gb, cp1, upbit1, upbit2, upbit3
from UBiC_Rotate_data import gb, upbit1, upbit2, upbit3
import time
import keyboard
import pickle
import os


# 한 종목(제일 높은 수익) 수동 즉시 매도 실행

# def plus_profit(upbit1):
while True:
    # start_time = time.time()                    # 시간 측정 시작
    bl, avg_p, tb = gb(upbit1)
    # bl = gb(upbit1)[0]
    # avg_p = gb(upbit1)[1]
    # tb = gb(upbit1)[2]
    plus_profit = {}

    # try:
    #     cu_p = cp1()   
    #     ext_s = ['KRW-VTHO', 'KRW-XYM', 'KRW-APENFT']  # 전체 종목과 현재가 dict 'cu_p' 로 바인딩
    #     [cu_p.pop(key, None) for key in ext_s]                # 종목 전체 현재가에서 ext 에 있는 종목 제외, None 시 넘어감, 현재 불필요
    #     [bl.remove(key) for key in ext_s if key in bl]        # 매도 제외 종목 설정 
    # except Exception as p:
    #     print("cu_p", p)
    with open('/root/UBiCauto/data/add_num.pickle', 'rb') as fr:
        add_num = pickle.load(fr)

    try:
        with open('/root/UBiCauto/data/cp.pickle', 'rb') as fr1:            # mycal 불러오기
            cu_p = pickle.load(fr1)  
        ext_s = []  # 전체 종목과 현재가 dict 'cu_p' 로 바인딩
        [cu_p.pop(key, None) for key in ext_s]                # 종목 전체 현재가에서 ext 에 있는 종목 제외, None 시 넘어감, 현재 불필요
        [bl.remove(key) for key in ext_s if key in bl]        # 매도 제외 종목 설정 
    except Exception as p:
        print("cu_p", p)
    time.sleep(0.5)
    try:
        for e, avg in avg_p.items():
            if e in cu_p:
                price = cu_p[e]
                tp = round((((price - avg) / avg) * 100), 2)            # '종목' 별 수익율 계산
                tn = tb[e] 
                t_money = round((avg * tn), 1)
                tbp = [tp, format(t_money, ",")]
                
                if 0 <= tp :         
                    plus_profit[e] = tbp                                    # 각종목 (수익율, 매수금액)을 리스트로 추가
                    if e == "KRW-CRO":
                        tbp0 = ('\033[91m' + f'{tbp[0]} %' + '\033[0m') 
                elif tp < 0 and e == "KRW-CRO":
                    tbp0 = ('\033[94m' + f'mybal :{tbp[0]} %' + '\033[0m') 
                        
        # print(tbp)
        plus_profit = sorted(plus_profit.items(), key=lambda profit: profit[1][0], reverse=True)
        # print(plus_profit)
        if 0 < (len(plus_profit)) :
            e = plus_profit[0][0]
            os.system('clear')
            print('\033[1m' + f'{ticker_per(cu_p, "KRW-BTC")}' + '\033[0m' + f'\n{ticker_per(cu_p, "KRW-CRO")} {tbp0} \n')     # 비트코인 현재상황 출력 찐하게
            print('\r' f'────────────────────────────────────────────────────────────\n\
👍' + f'\0 {e} ┆ ' + '\033[1m' + f'〚 {plus_profit[0][1][0]} 〛┆ ' + '\033[0m' + f'{plus_profit[0][1][1]} ┆ cp:⟮{cu_p[e]}⟯ ┆ ADN:⟮{add_num[e][0]}⟯\n\
────────────────────────────────────────────────────────────\n')
            print(f'({len(plus_profit)}) ⇪ 종목 상승 중 ∽\0  ⇪ \n {plus_profit} \n')
            
            time.sleep(1)
            # print("\033c")                     # 화면 삭제
            """ 수동 종목 매도 시 """
            # e = "KRW-STORJ"                    # 수동 종목 매도 시 사용
            """ ----------------- """
            # one_sell(upbit1,e)              # 종목 즉시 매도
            #     break
            # else:
            #     pass
        else:
            os.system('clear')
            print(f'{ticker_per(cu_p, "KRW-BTC")}\n{ticker_per(cu_p, "KRW-CRO")} ┆ {tbp0}\n \
──────────────────\n ⇩ 종목 없음 ⇩\0  ⨶ \n──────────────────')
            time.sleep(1)

    except Exception as p:
        print(p)
        
    # print(f'-- {round((time.time() - start_time), 2)} --\n')        # time check
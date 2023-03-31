# -*- coding:utf-8 -*-

from UBiC_Search_def import one_sell2
# from UBiC_Rotate_data import gb, cp1, upbit1, upbit2, upbit3
from UBiC_Rotate_data import gb, upbit1, upbit2, upbit3
import time
import keyboard
import pickle


# 한 종목(제일 높은 수익) 수동 즉시 매도 실행


while True:
    start_time = time.time()                    # 시간 측정 시작
    bl, avg_p, tb = gb(upbit1)
    # bl = gb(upbit1)[0]
    # avg_p = gb(upbit1)[1]
    plus_profit = {}
    # cu_p = cp1()   
    # ext_s = ['KRW-VTHO', 'KRW-XYM', 'KRW-APENFT']  # 전체 종목과 현재가 dict 'cu_p' 로 바인딩
    # [cu_p.pop(key, None) for key in ext_s]                # 종목 전체 현재가에서 ext 에 있는 종목 제외, None 시 넘어감, 현재 불필요
    # [bl.remove(key) for key in ext_s if key in bl]        # 매도 제외 종목 설정 

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

                tp = ((price - avg) / avg) * 100          # '종목' 별 수익율 계산 

                if 0 < tp :                               # 수익률 + 발생 시
                    plus_profit[e] = tp                   # 종목 추가 저장
        plus_profit = sorted(plus_profit.items(), key=lambda x: x[1], reverse=True)
        # print(plus_profit)
        if 0 < (len(plus_profit)) :
            e = plus_profit[0][0]
            # print(f'({len(plus_profit)}) 종목 상승 중!!, {plus_profit}')
            print(f'매도종목: {plus_profit[0][0]} | {plus_profit[0][1]}')
            
            time.sleep(0.5)

            """ 수동 종목 매도 시 """
            # e = "KRW-XLM"                   # 수동 종목 매도 시 사용
            """ ----------------- """
            one_sell2(upbit1,e)              # 종목 즉시 매도
            print("✌ \0 ok 매도완료")
            break

        else:
            print("⇩ 종목 없음 ⇩  \0⨶")
            break

            time.sleep(1)

    except Exception as p:
        print(p) 
    print("-- %s seconds --" % round((time.time() - start_time), 2))        # time check
    # return e
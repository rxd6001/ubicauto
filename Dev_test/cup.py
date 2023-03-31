# import pyupbit
import time
from datetime import datetime
import os
import pickle

e = "KRW-ZRX"

while True:

    start_time = time.time()  
    try:
        with open('/root/UBiCauto/data/config_buy.pickle', 'rb') as fbuy:           # b_money > bp 로 변경
            bp = pickle.load(fbuy); b_count = pickle.load(fbuy); bg = pickle.load(fbuy)
            gt = pickle.load(fbuy); tpor = pickle.load(fbuy); y3h3or = pickle.load(fbuy)
            tho_30r = pickle.load(fbuy); tho_1r = pickle.load(fbuy); p5g = pickle.load(fbuy)
            p10g = pickle.load(fbuy); p510g = pickle.load(fbuy); p550g = pickle.load(fbuy)
            p1050g = pickle.load(fbuy); ext_b = pickle.load(fbuy); ofn1 = pickle.load(fbuy)
            blow_money = pickle.load(fbuy); nw = pickle.load(fbuy); yg = pickle.load(fbuy)
            npct = pickle.load(fbuy)

            with open('/root/UBiCauto/data/cp.pickle', 'rb') as fr1:            # mycal 불러오기
                cu_p = pickle.load(fr1)                                       # 전체 종목과 현재가 dict 'cu_p' 로 바인딩
            # [cu_p.pop(key, None) for key in ext_b]                # 종목 전체 현재가에서 ext 에 있는 종목 제외, None 시 넘어감, 현재 불필요


        ks = cu_p.get(e)
        # print(cu_p.get('KRW-STX'))
        print(f'[{e}] CP : {ks}')

        time.sleep(1)
    except Exception as cu_p:
        print(cu_p)
    print("--- %s seconds ---" % round((time.time() - start_time), 3))
# -*- coding:utf-8 -*-

from UBiC_Search_def import one_sell2
from UBiC_Rotate_data import gb, cp4, upbit1, upbit2, upbit3
import time
import keyboard
import pickle
# from UBiC_Rotate_data import gb, cp3, upbit1
# 수동 매수(시장가) 실행
# 1845 = 60
# e = "KRW-ENJ"   #   "KRW-BTT"   (1)
e = "KRW-REP" # "KRW-IOTA" # "KRW-STX"   #   "KRW-BTT"   (1)

upbit = upbit3      # (2)

u = 1
# u = 2


if u == 1:      #  매수
    
    upbit.buy_market_order(e, 8000)   # (매수종목, 매수금액) 지정
    # bid_v = 18000 / bid_p                                 # 매수 수량 계산(목표가) (매수금액 기준)(v)
    # b_order = upbit1.buy_limit_order(e, price, bid_v)

elif u == 2:    # 매도

    tb1 = gb(upbit)[2]
    tb = tb1[e] 
    print(tb)
    upbit.sell_market_order(e, tb )

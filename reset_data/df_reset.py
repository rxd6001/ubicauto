# -*- coding:utf-8 -*-

import pickle
import time
import pyupbit
import requests
import os

""" df_day data 누락 발생 시 실행 필요 """
start = time.time()
url = "https://api.upbit.com/v1/market/all"

querystring = {"isDetails":"true"}
response = requests.request("GET", url, params=querystring)
contents = response.json()                      # 호출한 전체 마켓종목에을 리스트로 변환

if isinstance(contents, list):                  # contents 가 리스트일 경우 유의종목 제외한 원화마켓 종목만 호출 
    km = [x['market'] for x in contents if x['market_warning'] not in 'CAUTION' and x['market'].startswith('KRW')]
with open('/root/UBiCauto/data/krw_markets.pickle', 'wb') as fw:        # 원화마켓 종목의 데이터를 파일로 저장
    pickle.dump(km, fw)    


# def km2():
#     with open('/root/UBiCauto/data/krw_markets.pickle', 'rb') as fr2:       # df_day 파일로 불러 옴
#         km1 = pickle.load(fr2)
#     return km1


# km = km2() 
print(km)
print(" km --- %s seconds ---" % round((time.time() - start), 3))
print(len(km))


""" 30m 데이터 저장 """
# for ticker in km:
#     try:                                                       # 원화마켓에서 종목을 하나씪 가져옴
#         dfm30 = pyupbit.get_ohlcv(ticker, interval="minute30", count=50)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
#         with open('/root/UBiCauto/data/ohlcvm30/%s_df_min30.pickle' %(ticker), 'wb') as fw3:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
#             pickle.dump(dfm30, fw3)
#             time.sleep(1)
#             print(ticker)
#         while True:
#             fs = os.path.getsize('/root/UBiCauto/data/ohlcvm30/%s_df_min30.pickle' %(ticker))
#             if fs < 1024 :
#                 dfm30 = pyupbit.get_ohlcv(ticker, interval="minute30", count=50)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
#                 print()
#                 with open('/root/UBiCauto/data/ohlcvm30/%s_df_min30.pickle' %(ticker), 'wb') as fw3:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
#                     pickle.dump(dfm30, fw3)
#             else:
#                 break
#     except Exception as gg:
#         print(ticker)


""" 10m 데이터 저장 """
# for ticker in km:                                                       # 원화마켓에서 종목을 하나씪 가져옴
#     dfm10 = pyupbit.get_ohlcv(ticker, interval="minute10", count=55)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
#     with open('/root/UBiCauto/data/ohlcvm10/%s_df_min10.pickle' %(ticker), 'wb') as fw10:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
#         pickle.dump(dfm10, fw10)
#         time.sleep(0.2)
#     while True:
#         fs = os.path.getsize('/root/UBiCauto/data/ohlcvm10/%s_df_min10.pickle' %(ticker))
#         if fs < 1024 :
#             dfm10 = pyupbit.get_ohlcv(ticker, interval="minute10", count=55)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
#             with open('/root/UBiCauto/data/ohlcvm10/%s_df_min10.pickle' %(ticker), 'wb') as fw10:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
#                 pickle.dump(dfm10, fw10)
#         else:
#             break


""" 3m 데이터 저장 """
# for ticker in km:                                                       # 원화마켓에서 종목을 하나씪 가져옴
#     dfm3 = pyupbit.get_ohlcv(ticker, interval="minute3", count=51)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
#     with open('/root/UBiCauto/data/ohlcvm3/%s_df_min3.pickle' %(ticker), 'wb') as fw4:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
#         pickle.dump(dfm3, fw4)
#         time.sleep(0.1)
#     while True:
#         fs = os.path.getsize('/root/UBiCauto/data/ohlcvm3/%s_df_min3.pickle' %(ticker))
#         if fs < 1024 :
#             dfm3 = pyupbit.get_ohlcv(ticker, interval="minute3", count=50)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
#             with open('/root/UBiCauto/data/ohlcvm3/%s_df_min3.pickle' %(ticker), 'wb') as fw4:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
#                 pickle.dump(dfm3, fw4)
#         else:
#             break


""" 1m 데이터 저장 """
# for ticker in km:                                                       # 원화마켓에서 종목을 하나씪 가져옴
#     dfm1 = pyupbit.get_ohlcv(ticker, interval="minute1", count=51)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
#     with open('/root/UBiCauto/data/ohlcvm1/%s_df_min1.pickle' %(ticker), 'wb') as fw5:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
#         pickle.dump(dfm1, fw5)
#         time.sleep(0.1)
#     while True:
#         fs = os.path.getsize('/root/UBiCauto/data/ohlcvm1/%s_df_min1.pickle' %(ticker))
#         if fs < 1024 :
#             dfm1 = pyupbit.get_ohlcv(ticker, interval="minute1", count=50)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
#             with open('/root/UBiCauto/data/ohlcvm1/%s_df_min1.pickle' %(ticker), 'wb') as fw5:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
#                 pickle.dump(dfm1, fw5)
#         else:
#             break

# start = time.time()
""" Day 데이터 저장 """
for ticker in km:                                                       # 원화마켓에서 종목을 하나씪 가져옴
        dfd = pyupbit.get_ohlcv(ticker, interval="day", count=100)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
        with open('/root/UBiCauto/data/ohlcvd/%s_df_day.pickle' %(ticker), 'wb') as fw2:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
            pickle.dump(dfd, fw2)
            time.sleep(0.2)
        while True:
            fs = os.path.getsize('/root/UBiCauto/data/ohlcvd/%s_df_day.pickle' %(ticker))
            if fs < 1024 :
                dfd = pyupbit.get_ohlcv(ticker, interval="day", count=100)           # 가져온 종목에 대한 일봉 데이터를 df로 저장
                with open('/root/UBiCauto/data/ohlcvd/%s_df_day.pickle' %(ticker), 'wb') as fw2:     # 원화마켓 종목의 일봉 데이터를 파일로 저장
                    pickle.dump(dfd, fw2)
            else:
                break
# print("--- %s seconds ---" % round((time.time() - start), 3))

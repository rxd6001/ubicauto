# from IPython.display import display
from pandas import DataFrame as df
import pandas as pd
import numpy as np
import pickle
import datetime

""" 사용자 선택 1,2,3 """
id = 3
counter = 0                     # cal 설정여부 체크 '0'(x), '1'(o)

""" cal 재설정 """
if counter == 0:
    pass

elif counter == 1:

    cal_l = [1]

    if u == 1:

        # with open('/root/UBiCauto/data/cal_l1.pickle', 'rb') as fr1:            # mycal 불러오기
        #     cal_l = pickle.load(fr1)

        print(len(cal_l))
        with open('/root/UBiCauto/data/cal_l1.pickle', 'wb') as fw:             # cal_l 저장
            pickle.dump(cal_l, fw)

    elif u == 2:

        with open('/root/UBiCauto/data/cal_l2.pickle', 'rb') as fr1:            # mycal 불러오기
            cal_l = pickle.load(fr1)

        print(len(cal_l))
        with open('/root/UBiCauto/data/cal_l2.pickle', 'wb') as fw:             # cal_l 저장
            pickle.dump(cal_l, fw)

    elif u == 3:

        with open('/root/UBiCauto/data/cal_l3.pickle', 'rb') as fr1:            # mycal 불러오기
            cal_l = pickle.load(fr1)

        print(len(cal_l))
        with open('/root/UBiCauto/data/cal_l3.pickle', 'wb') as fw:             # cal_l 저장
            pickle.dump(cal_l, fw)

""" mycal 재설정 """
# if u == 1:

with open('/root/UBiCauto/data/mycal%s.pickle' %(id), 'rb') as fr1:            # mycal 불러오기
    mycal = pickle.load(fr1)
# mycal = df(index = range(0), columns = ['T_Asset','Profit','ROE','Ct'])
# mycal = mycal.drop("22년8월2일")                                       # 지정행 삭제  
# mycal = pd.read_excel('mycal_m.xlsx', index_col=0)                    # 엑셀에서 불러오기(인덱스 제거)
# mycal['ROE'] = [0, 0.1, 0.2]
# mycal.loc['2022년6월30일'] = [55922504, 0, 0, 0]           # 행 추가 
# mycal.loc['22년10월20일'] = [9003054.3, 705, 0.00, 6]           # 행 추가 
# mycal.loc['22년8월15일'] = [9135036.9, 854.0, 0.01, 19]           # 행 추가 
# 22년8월15일  11135036.9    854.0  0.01  19.0
# mycal.loc['21년6월'] = [47142750, -10895924, -22.3, 0]           # 행 추가 

# mycal.to_excel('mycal_m.xlsx')                                        # 엑셀로 저장하기
# mycal = mycal.iloc[-1:]                                                   # 마지막 한 행만 표시 
# mycal.iloc[-1,1:4] = 0.0                                                  # 마지막 한 행의 내용을 '0' 으로 수정   

# mycal.loc['2021년 총 계'] = [ tsum, mycal['Profit'].sum(), mycal['ROE'].sum(), mycal['Ct'].sum()]         #  총계

# mycal = mycal.rename(index={'2022년6월 계':'22년6월'})                   # 날짜 변경('변경전날짜':'변경후날짜')
# l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# for li in l:
#     mycal = mycal.rename(index={'2021년%s월' %(li):'21년%s월' %(li)})                   # 날짜 변경('변경전날짜':'변경후날짜')
#     mycal = mycal.rename(index={'2022년%s월' %(li):'22년%s월' %(li)})                   # 날짜 변경('변경전날짜':'변경후날짜')


print(mycal)                                                                  # mycal 출력 확인(저장 전)

# id = 3
# 2022년7월31일  11066062.9      0.0  0.00   0.0
# 2022년8월1일   11087855.2  21792.3  0.20  65.0
# 22년8월2일     11088713.0    857.8  0.01  21.0

# id = 2
# 2022년7월31일  1172375.1     0.0  0.00   0.0
# 2022년8월1일   1173265.5   890.4  0.08   8.0
# 22년8월2일     1174166.7   901.2  0.08  22.0

# id = 1
# 2022년7월31일  56717411.5      0.0  0.00    0.0
# 2022년8월1일   56753300.2  35888.7  0.06  209.0
# 22년8월2일     56777139.5  23839.3  0.04   83.0   

# with open('/root/UBiCauto/data/mycal%s.pickle' %(id), 'wb') as fw:                  # mycal 저장
#     pickle.dump(mycal, fw)

""" --------------------------------------------------------- """
# display(cu_p)
# print(cu_p['KRW-HUNT'])
# if __name__ in '__main__':

    # 매도금액 갱신
    # re_cal(cal_ln)
    # print(cal)
    # 자산현황 갱신
    # re_mycal(mycaln)
    # print(mycal)

""" dataframe 초기화 """
# mclt = df(index = range(0), columns = ['T_Asset','Profit','ROE','Ct'])     # mycal 초기화

# display(mclt)


""" 참고사항 """
# mycal = df(data = np.array([[tsum, calsum, roe, len(cal_l)]]), index = [day], 
#         columns = ['총자산'.center(12), '수익'.center(9), '수익률'.ljust(8), '매도횟수'.ljust(9)])
# set_option('display.max_row', 5)          # 최대 5행을 보여주기
# display(mycal.head())
# ls = mycal['T_Asset'] >= 12000000   # 자산이 1천2백 이상이었던 조건비교 결과를 변수에 저장
# lls = mycal[ls]         # 조건 충족 데이터를 필터링하여 변수에 저장
# print(lls)              # 조건 만족하는 행 출력
""" 
--- 참고 ---
dtod = datetime.strptime(yday, "%Y년%m월%d일")
print('dtod:', dtod)
print('년월변환',day) # 2021년3월3일
print('전일자산:', ysum)
daay = datetime(2021, 3, 3)
mycal["2021년3월3일"] = mycal.pop(datetime(2021, 3, 3))
mycal['2021년3월2일'] = mycal.pop("2021년3월3일")  # 딕셔너리 키값 변경
print(mycal)    # {'2021년3월3일': (0, 8075884.6)}
with open('/root/UBiCauto/data/mycal.pickle', 'wb') as fw:
    pickle.dump(mycal, fw)
---
"""
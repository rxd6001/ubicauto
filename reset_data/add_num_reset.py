import pickle
import os

""" 추매 횟수 변경할 종목명 입력 """

e = "KRW-MANA" ; u = 2

"""---------------------------"""
if u == 1:

    os.system("kpss1")                                              # 매도 종료
    with open('/root/UBiCauto/data/add_num1.pickle', 'rb') as fr:    # add_num 호출
        add_num = pickle.load(fr)

    add_num[e][0:1]=[8]                                             # 변경할 횟수 입력



    with open('/root/UBiCauto/data/add_num1.pickle', 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)

    # os.system("pss1")                                               # 매도 실행
    print(f'{e} : {add_num[e]}')                                                  # 

elif u == 2:

    os.system("kpss2")                                              # 매도 종료
    with open('/root/UBiCauto/data/add_num2.pickle', 'rb') as fr:    # add_num 호출
        add_num = pickle.load(fr)

    # add_num[e][0:1]=[5]                                             # 변경할 횟수 입력
    add_num[e]=[0, 30, 9510]


    with open('/root/UBiCauto/data/add_num2.pickle', 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)

    os.system("pss2")                                               # 매도 실행
    print(f'{e} : {add_num[e]}')  

elif u == 3:

    os.system("kpss3")                                              # 매도 종료
    with open('/root/UBiCauto/data/add_num3.pickle', 'rb') as fr:    # add_num 호출
        add_num = pickle.load(fr)

    add_num[e][0:1]=[0]                                             # 변경할 횟수 입력


    with open('/root/UBiCauto/data/add_num3.pickle', 'wb') as fw:    # 추가매수 횟수 저장(dict 로 저장)
        pickle.dump(add_num, fw)

    os.system("pss3")                                               # 매도 실행
    print(f'{e} : {add_num[e]}')  

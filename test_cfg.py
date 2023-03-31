import pickle
from UBiC_Search_def import perct
# from UBiC_Rotate_data import upbit1
from decimal import Decimal
import os

# , 'adp1': 3, 'adp2': 5, 'adp3': 7, 'adp4': 11, 'adp5': 11, 'adp6': 11, 'adp7': 11, 'adp8': 11, 'adp9': 11, 'adp10': 11


# set_cfg1= {'b_money':20000, 'bp':2.9, 'b_count':50, 'blow_money':20000, 'bg':0.001, 'gt':25,\
#            'code':2, 'y3h3or':60, 'tho_30r':30, 'tho_1r':30, 'tpor':30, 'p5g':30, 'p10g':10,\
#            'p510g':40, 'p550g':10, 'p1050g':120, 'nw':90, 'npct':0.5, 'yg':90, 'ask_p':0.004,\
#            'ask_ug':0.1, 'ask_pp':0.01, 'agt':30, 'sell_cont':1, 'adsp':0.1, 'ap':7, 'u_p':4,\
#            'l_money':450000, 'ag1':0.5, 'ag2':0.3,'ag3':0.4, 'ag4':1, 'ag5':1, 'ag6':1, 'ag7':1,\
#            'ag8':1, 'ag9':1, 'ag10':1, adp1, adp2, adp3 'abptime':5}
# set_cfg1= {'sell_cont': 1, 'b_money': 20000, 'bp': 2.9, 'b_count': 50, 'blow_money': 20000, 'bg': 0.001, 'gt': 25, 'code': 2, 'y3h3or': 60, 'tho_30r': 30, 'tho_1r': 30, 'tpor': 30, 'p5g': 30, 'p10g': 10, 'p510g': 40, 'p550g': 10, 'p1050g': 120, 'nw': 90, 'npct': 0.5, 'yg': 90, 'ask_p': 0.0045, 'ask_ug': 0.1, 'ask_pp': 0.01, 'agt': 30, 'adsp': 0.1, 'ap': 7, 'u_p': 4, 'l_money': 450000, 'ag1': 0.5, 'ag2': 0.3, 'ag3': 0.4, 'ag4': 1, 'ag5': 1, 'ag6': 1, 'ag7': 1, 'ag8': 1, 'ag9': 1, 'ag10': 1, 'adp1': 3, 'adp2': 5, 'adp3': 7, 'adp4': 11, 'adp5': 11, 'adp6': 11, 'adp7': 11, 'adp8': 11, 'adp9': 11, 'adp10': 11, 'abptime': 5}

# #            
# set_cfg2= {'b_money':9500, 'bp':10.5, 'b_count':10, 'blow_money':9500, 'bg':0.001, 'gt':25,\
#            'code':2, 'y3h3or':60, 'tho_30r':30, 'tho_1r':30, 'tpor':30, 'p5g':20, 'p10g':10,\
#            'p510g':30, 'p550g':10, 'p1050g':120, 'nw':90, 'npct':0.5, 'yg':60, 'ask_p':0.005,\
#            'ask_ug':0.1, 'ask_pp':0.01, 'agt':10, 'sell_cont':1, 'adsp':0.1, 'ap':6, 'u_p':4,\
#            'l_money':70000, 'ag1':0.6, 'ag2':0.4,'ag3':0.4, 'ag4':1, 'ag5':1, 'ag6':1, 'ag7':1,\
#            'ag8':1, 'ag9':1, 'ag10':1, 'abptime':5}
# set_cfg2= {'sell_cont': 1, 'b_money': 9500, 'bp': 10.5, 'b_count': 10, 'blow_money': 9500, 'bg': 0.001, 'gt': 25, 'code': 2, 'y3h3or': 60, 'tho_30r': 30, 'tho_1r': 30, 'tpor': 30, 'p5g': 20, 'p10g': 10, 'p510g': 30, 'p550g': 10, 'p1050g': 120, 'nw': 90, 'npct': 0.5, 'yg': 60, 'ask_p': 0.0045, 'ask_ug': 0.1, 'ask_pp': 0.01, 'agt': 10, 'adsp': 0.1, 'ap': 5, 'u_p': 4, 'l_money': 70000, 'ag1': 0.6, 'ag2': 0.4, 'ag3': 0.4, 'ag4': 1, 'ag5': 1, 'ag6': 1, 'ag7': 1, 'ag8': 1, 'ag9': 1, 'ag10': 1, 'adp1': 3, 'adp2': 5, 'adp3': 7, 'adp4': 11, 'adp5': 11, 'adp6': 11, 'adp7': 11, 'adp8': 11, 'adp9': 11, 'adp10': 11, 'abptime': 5}

# set_cfg3= {'b_money':8000, 'bp':3.7, 'b_count':35, 'blow_money':8000, 'bg':0.001, 'gt':25,\
#            'code':2, 'y3h3or':60, 'tho_30r':30, 'tho_1r':30, 'tpor':30, 'p5g':20, 'p10g':10,\
#            'p510g':30, 'p550g':10, 'p1050g':120, 'nw':90, 'npct':0.5, 'yg':60, 'ask_p':0.005,\
#            'ask_ug':0.1, 'ask_pp':0.01, 'agt':10, 'sell_cont':1, 'adsp':0.1, 'ap':7, 'u_p':4,\
#            'l_money':280000, 'ag1':1, 'ag2':0.5,'ag3':0.5, 'ag4':0.3, 'ag5':0.5, 'ag6':1, 'ag7':1,\
#            'ag8':1, 'ag9':1, 'ag10':1, 'abptime':5}
# set_cfg3= {'sell_cont': 1, 'b_money': 8000, 'bp': 3.7, 'b_count': 35, 'blow_money': 8000, 'bg': 0.001, 'gt': 25, 'code': 1, 'y3h3or': 60, 'tho_30r': 30, 'tho_1r': 30, 'tpor': 30, 'p5g': 20, 'p10g': 10, 'p510g': 30, 'p550g': 10, 'p1050g': 120, 'nw': 90, 'npct': 0.5, 'yg': 60, 'ask_p': 0.0045, 'ask_ug': 0.1, 'ask_pp': 0.01, 'agt': 10, 'adsp': 0.1, 'ap': 7, 'u_p': 4, 'l_money': 280000, 'ag1': 1, 'ag2': 0.5, 'ag3': 0.5, 'ag4': 0.3, 'ag5': 0.5, 'ag6': 1, 'ag7': 1, 'ag8': 1, 'ag9': 1, 'ag10': 1, 'adp1': 3, 'adp2': 5, 'adp3': 7, 'adp4': 11, 'adp5': 11, 'adp6': 11, 'adp7': 11, 'adp8': 11, 'adp9': 11, 'adp10': 11, 'abptime': 5}
        
# set_cfg1 = {'sell_count': 1, 'b_money': 20000, 'bp': 2.5, 'b_count': 50, 'blow_money': 20000, 'bg': 0.001, 'gt': 25, 'code': 2, 'y3h3or': 60, 'tho_30r': 30, 'tho_1r': 30, 'tpor': 30, 'p5g': 30, 'p10g': 10, 'p510g': 40, 'p550g': 10, 'p1050g': 120, 'nw': 90, 'npct': 0.5, 'ap': 7, 'agt': 0.5, 'l_money': 450000, 'ask_p': 0.0045, 'ask_ug': 0.1, 'ask_pp': 0.01, 'adsp': 0.1, 'u_p': 4, 'yg': 90, 'ag1': 0.5, 'ag2': 0.3, 'ag3': 0.4, 'ag4': 1, 'ag5': 1, 'ag6': 1, 'ag7': 1, 'ag8': 1, 'ag9': 1, 'ag10': 1, 'adp1': 4, 'adp2': 5, 'adp3': 7, 'adp4': 10, 'adp5': 11, 'adp6': 11, 'adp7': 11, 'adp8': 11, 'adp9': 11, 'adp10': 11, 'abptime': 5}
# with open('/root/UBiCauto/data/set_cfg1.pickle', 'wb') as fset:
#     pickle.dump(set_cfg1, fset)

# with open('/root/UBiCauto/data/set_cfg2.pickle', 'wb') as fset:
#     pickle.dump(set_cfg2, fset)
    
# with open('/root/UBiCauto/data/set_cfg3.pickle', 'wb') as fset:
#     pickle.dump(set_cfg3, fset)

# with open('/root/UBiCauto/data/set_cfg1.pickle', 'rb') as fset:
#     set_cfg1= pickle.load(fset)

with open('/root/UBiCauto/data/set_cfg2.pickle', 'rb') as fset:
    set_cfg2= pickle.load(fset)

# with open('/root/UBiCauto/data/set_cfg3.pickle', 'rb') as fset:
#     set_cfg3= pickle.load(fset)


# with open("test_cfg.pickle", "rb") as f:
#     dic = pickle.load(f)
# a =perct(50)
# b_money=dic["b_money"]
# set_cfg1['code'] = 2
# print(set_cfg1)
print(set_cfg2)
# print(set_cfg3)

# print(set_cfg1['b_money'])

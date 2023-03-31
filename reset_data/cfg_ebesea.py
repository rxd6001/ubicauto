import pickle
import os
import pyupbit
# from UBiC_Rotate_data import gb, upbit1

# members = {'zenka' : 'ktu007zk!', 'butysoo' : '8050soo!', 'liebe' : 'lb6114!'}

# with open("/root/UBiCauto/Acct/members.pickle", "wb") as mb:
#     pickle.dump(members, mb)

# acc_str = {'zenka':'ubic1', 'butysoo':'ubic2', 'liebe':'ubic3'}		# 계정별 string 설정
# acc_name = {'ubic1':upbit1, 'ubic2':upbit2, 'ubic3':upbit3 }			# 웹페이지에서 매도버튼 클릭 시 자동으로 들어갈 계정
# cal_name = {'ubic1':['/root/UBiCauto/data/mycal1.pickle', '/root/UBiCauto/data/mycal_m1.pickle',\
# 	'/root/UBiCauto/data/add_num1.pickle', '/root/UBiCauto/data/cal_l1.pickle', '/root/UBiCauto/data/b_money.pickle',\
# 	'/root/UBiCauto/data/t_tp1.pickle', '/root/UBiCauto/data/set_cfg1.pickle', '/root/UBiCauto/data/ext_item1.pickle'],\
# 	'ubic2':['/root/UBiCauto/data/mycal2.pickle', '/root/UBiCauto/data/mycal_m2.pickle', '/root/UBiCauto/data/add_num2.pickle',\
# 	'/root/UBiCauto/data/cal_l2.pickle', '/root/UBiCauto/data/b_money2.pickle', '/root/UBiCauto/data/t_tp2.pickle',\
# 	'/root/UBiCauto/data/set_cfg2.pickle', '/root/UBiCauto/data/ext_item2.pickle'],\
# 	'ubic3':['/root/UBiCauto/data/mycal3.pickle', '/root/UBiCauto/data/mycal_m3.pickle', '/root/UBiCauto/data/add_num3.pickle',\
# 	'/root/UBiCauto/data/cal_l3.pickle', '/root/UBiCauto/data/b_money3.pickle', '/root/UBiCauto/data/t_tp3.pickle',\
# 	'/root/UBiCauto/data/set_cfg3.pickle', '/root/UBiCauto/data/ext_item3.pickle']}					# 자산정보 파일 가져오기위한 경로


with open('/root/UBiCauto/data/set_cfg1.pickle', 'rb') as fset:
    set_conf = pickle.load(fset)




print(set_conf)           # 환경설정

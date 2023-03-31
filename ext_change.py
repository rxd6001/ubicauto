from datetime import datetime, timedelta
import time
import pickle

# cal_l =[]
# for i in range(21):
#   cal_l.insert(0, i)

# print(len(cal_l))
id = 1


with open("/root/UBiCauto/data/ext_item%s.pickle" %(id), "rb") as fr:
  ext_item = pickle.load(fr)

# 매수 제외
eb = ['KRW-BTT']      # 매수 제외 항목

ext_item['ext_b'] = eb
print(ext_item['ext_b'])      # 설정 후 확인

# 매도 제외
es = ['KRW-CRO']      # 매수 제외 항목

ext_item['ext_s'] = es
print(ext_item['ext_s'])      # 설정 후 확인

# 추매 제외
ea = ['KRW-CRO']      # 매수 제외 항목

ext_item['ext_a'] = ea
print(ext_item['ext_a'])      # 설정 후 확인


print(ext_item)
q = input ("정말 실행하시겠습니까? ([y]es/[n]o) : ")
if q == 'y' or q == 'yes':
  # with open("/root/UBiCauto/data/ext_item%s.pickle" %(id), "wb") as fw:
  #   pickle.dump(ext_item, fw)
  pass
else:
  print("다시 실행 하세요!!")
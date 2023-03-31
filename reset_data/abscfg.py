import pickle
import os
import pyupbit

# 1.추매, 매도, 매수 제외 항목 설정
# ext_item = {'ext_b':[], 'ext_s':[], 'ext_a': []}

user = 1           # 사용자 지정(ubic1, 2, 3)
se = 'b'           # a, b, s(추매, 매수, 매도)제외 선택
save = 0            # 1: 저장, 0: 저장 안 함

''' 3. 매수 프로세스에서 매수제외 항목 수정 시 사용 '''
ext_Buy = 0         # 1: 제외 코인 변경, 0: 변경 안 함 (매수에서 제외할 코인 항목 지정 시)
''' ------------------------------------------------------------------------ '''

with open('/root/UBiCauto/data/ext_item%s.pickle' %(user), 'rb') as fr:
    ext_item = pickle.load(fr)

with open('/root/UBiCauto/data/ext_itemB.pickle', 'rb') as fr:      # 신규매수 제외할 코인파일(ext_itemB.pickle)
    ext_itemB = pickle.load(fr)

''' 3. 매수 제외 항목 출력 '''
ext_B = ext_itemB['ext_b']
print(f'신규매수 제외할 코인: {ext_itemB}, {ext_B}')

# 수정 전 출력
print(f'수정 전: {ext_item}')

# 1. 항목 추가
# ext_item['ext_%s' %(se)].append('KRW-SOL')
#set(ext_item['ext_%s' %(se)])
# ext_item['ext_b'].append('KRW-BTT')
# ext_item['ext_b'].append('KRW-SHIB')

# 1. 항목 제거
# ext_item['ext_%s' %(se)].remove('KRW-SOL')
# ext_item['ext_s'].remove('KRW-BTT')
# ext_item['ext_b'].remove('KRW-BTT')
# ext_item = {'ext_a': ['KRW-CRO', 'KRW-SOL'], 'ext_b': ['KRW-SOL'], 'ext_s': []}
# 수정 후 출력
print(f'수정 후: {ext_item}')

""" 3. 새 코인 매수제외 할 항목 """
###################################################################
if ext_Buy == 1:    # '1'일때만 변경

    ext_itemB = {'ext_b': ['KRW-SHIB', 'KRW-BTT', 'KRW-XEC']}   # 제외할 코인

    with open('/root/UBiCauto/data/ext_itemB.pickle' , 'wb') as fw:
        pickle.dump(ext_itemB, fw)
    
    print(f'신규매수 제외할 코인: {ext_itemB}')
else:
    pass
###################################################################

# 저장
if save == 1:
    with open('/root/UBiCauto/data/ext_item%s.pickle' %(user), 'wb') as fw:
        pickle.dump(ext_item, fw)
        print(f'수정 후: {ext_item}')
else:
    pass

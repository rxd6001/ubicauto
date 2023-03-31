
b_money = 5100
fi_money = b_money * 3                            # 1차 추매 시      
se_money = fi_money * 2                           # 2차 추매 시
th_money = se_money * 2                           # 3차 추매 시
fo_money = th_money * 2                           # 4차 추매 시
fif_money = fo_money * 3                          # 5차 추매 시
six_money = fif_money * 2                         # 6차 추매 시
""" --------------- """
l_money = six_money                               # 추매 5회까지 가능 / 금액 제한 (종목당 보유금액( 보유금액의 2배 까지 증가 가능)
print(f'fi_money:{fi_money}, se_money:{se_money}, th_money:{th_money}, fo_moeny:{fo_money}, fif_money:{fif_money}, six_money:{six_money}')
print(l_money)
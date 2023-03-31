import time, os
from datetime import datetime, timedelta


# now = datetime.now()
# now1 = datetime(now.year, now.month, now.day) + timedelta(0)    # 금일 자정 데이터 취합시작 날짜,시간 설정
bf_mid = datetime(2021, 8, 11, hour=1, minute=59, second=30) + timedelta(0)     # 점검 전 스케쥴 정지시간
af_mid = datetime(2021, 8, 11, hour=6, minute=20, second=0) + timedelta(0)     # 점검 후 스케쥴 실행시간

while True:
    now = datetime.now()
    if bf_mid <= now <= bf_mid + timedelta(seconds=5):                          # 데이터 저장 시간 범위 포함여부 확인
        os.system("systemctl stop crond")
        time.sleep(1)
        os.system("ubicstop")
        time.sleep(5)
        print(f'{now}: stop')
    elif af_mid <= now <= af_mid + timedelta(seconds=5):
        os.system("systemctl start crond")
        time.sleep(5)
        print(f'{now}: crond start')
        break
time.sleep(5)
os.system("ps -ef|grep sc.py")

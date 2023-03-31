# -*- coding:utf-8 -*-

import os

process_read = os.popen("shp | grep -v 'grep'").read()          # ps -ef 명령어를 이용해서 현재 프로세스를 출력한 후, 해당 프로세스를 확인
# grep 명령어 자체도 프로세스에 나타나므로 grep -v를 이용해서 제외한다.

# check_process = str(process_read)                             # 문자열로 변환한다.
 
# f_process = ['myc1', 'myc2', 'myc3', 'prr', 'pss1', 'pss2', 'pss3', 'pbb1', 'pbb2', 'pbb3', 'wrun'] # 
f_process = ['myc', 'prr', 'pbb', 'pss', 'wrun'] # 
for fp in f_process:
    # text_location=check_process.find(fp)                      # 문자열로 변환이 필요할 경우
    text_location=process_read.find(fp)                         # 만약 문자열이 없으면, 즉 프로세스가 존재하지 않을 경우에는 -1을 반환한다.
    if ( text_location == -1 ):                                 # "-1"인 경우 프로세스 재 실행 절차 진행
        os.system(fp)                                           # 해당 프로세스를 다시 실행한다.
        # print("(%s) Process restarted !" %(fp))
        # os.system("shp")

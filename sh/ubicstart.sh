pro="myc prr pbb pss wrun"				# 변수선언
for pro1 in $pro								# 반복문 대입
do
        check=`ps -ef | grep -v grep | grep $pro1 |wc | awk '{print $1}'`	# 프로세스 실행 중인지 체크 : 실행 시 1, 미실행 시 0
        if [ $check == 1 ];then							# 프로세스 실행 중이면 아래 줄 출력
                echo $pro1 "is RUNNING ~"
        else									# 프로세스 미실행 이면 프로세스 실행 후 완료 출력
                $pro1
                echo $pro1 "process complete"
        fi
done
shp										# 업비트 모든 프로세스 출력

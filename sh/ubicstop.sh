# kill $(/usr/sbin/pidof p)
kill `ps -ef|grep -v grep|grep /root/UBiCauto/prr|awk '{print $2}'`
kill `ps -ef|grep -v grep|grep /root/UBiCauto/pbb|awk '{print $2}'`
kill `ps -ef|grep -v grep|grep /root/UBiCauto/pss|awk '{print $2}'`
kill `ps -ef|grep -v grep|grep /root/UBiCauto/wrun|awk '{print $2}'`
kill `ps -ef|grep -v grep|grep /root/UBiCauto/myc|awk '{print $2}'`
echo "프로세스를 종료했습니다 !!"

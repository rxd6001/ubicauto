# kill $(ps -ef |grep myc)
kill `ps -ef|grep -v grep|grep /root/UBiCauto/myc|awk '{print $2}'`

# kill $(ps -ef |grep myc3)
kill `ps -ef|grep -v grep|grep /root/UBiCauto/myc3|awk '{print $2}'`
myc3

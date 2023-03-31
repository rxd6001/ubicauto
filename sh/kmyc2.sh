# kill $(ps -ef |grep myc2)
kill `ps -ef|grep -v grep|grep /root/UBiCauto/myc2|awk '{print $2}'`
myc2

# kill $(ps -ef |grep pss|grep -v 'grep')
kill `ps -ef|grep -v grep|grep /root/UBiCauto/pss|awk '{print $2}'`

# kill $(ps -ef |grep pbb|grep -v 'grep')
kill `ps -ef|grep -v grep|grep /root/UBiCauto/pbb|awk '{print $2}'`

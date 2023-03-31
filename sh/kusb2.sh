# kill $(ps -ef |grep pbb2|grep -v 'grep')
kill `ps -ef|grep -v grep|grep /root/UBiCauto/pbb2|awk '{print $2}'`
pbb2

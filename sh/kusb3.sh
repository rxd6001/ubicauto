# kill $(ps -ef |grep pbb3|grep -v 'grep')
kill `ps -ef|grep -v grep|grep /root/UBiCauto/pbb3|awk '{print $2}'`
pbb3

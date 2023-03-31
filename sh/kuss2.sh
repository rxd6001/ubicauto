# kill $(ps -ef |grep pss2|grep -v 'grep')
kill `ps -ef|grep -v grep|grep /root/UBiCauto/pss2|awk '{print $2}'`
pss2

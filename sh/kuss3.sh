# kill $(ps -ef |grep pss3|grep -v 'grep')
kill `ps -ef|grep -v grep|grep /root/UBiCauto/pss3|awk '{print $2}'`
pss3

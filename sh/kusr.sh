# kill $(ps -ef |grep prr|grep -v 'grep')
kill `ps -ef|grep -v grep|grep /root/UBiCauto/prr|awk '{print $2}'`

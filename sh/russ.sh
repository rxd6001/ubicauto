# kill $(ps -ef |grep pss|grep -v 'grep')
kill `ps -ef|grep -v grep|grep /root/UBiCauto/pss|awk '{print $2}'`
nohup p -u /root/UBiCauto/pss 1>/root/UBiCauto/ubiclog/ns.log 2>&1 &

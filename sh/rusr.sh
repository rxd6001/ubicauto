# kill $(ps -ef |grep prr|grep -v 'grep')
kill `ps -ef|grep -v grep|grep /root/UBiCauto/prr|awk '{print $2}'`
nohup p -u /root/UBiCauto/prr 1>/root/UBiCauto/ubiclog/nr.log 2>&1 &

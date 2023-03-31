# kill $(ps -ef |grep pbb|grep -v 'grep')
kill `ps -ef|grep -v grep|grep /root/UBiCauto/pbb|awk '{print $2}'`
nohup p -u /root/UBiCauto/pbb >/root/UBiCauto/ubiclog/nb.log 2>&1 &

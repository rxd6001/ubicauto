# kill $(ps -ef |grep myc)
kill `ps -ef|grep -v grep|grep /root/UBiCauto/myc|awk '{print $2}'`
nohup p -u /root/UBiCauto/myc >/root/UBiCauto/ubiclog/myl.log 2>&1 &

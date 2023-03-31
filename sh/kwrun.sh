# kill $(ps -ef |grep wrun1|grep -v 'grep')
kill `ps -ef|grep -v grep|grep "/root/UBiCauto/wrun" |awk '{print $2}'`

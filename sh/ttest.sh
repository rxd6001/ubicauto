pro="myc1 myc2 myc3 prr pbb1 pbb2 pbb3 pss1 pss2 pss3"
for pro1 in $pro
do
	check=`ps -ef | grep -v grep | grep $pro1 |wc | awk '{print $1}'`
	if [ $check == 1 ];then
		echo "RUNNING ~"
	else
		$pro1	
		echo $pro1 "process complete"
	fi
done
shp

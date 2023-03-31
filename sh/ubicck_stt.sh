#sed -i 's/echo "UBiC_Check.py Stoping ~"/p \/root\/UBiCauto\/UBiC_Check.py/g' /root/UBiCauto/sh/ubicck.sh
echo "p /root/UBiCauto/UBiC_Check.py" > /root/UBiCauto/sh/ubicck.sh
echo "echo 'p /'" >> /root/UBiCauto/sh/ubicck.sh
cat /root/UBiCauto/sh/ubicck.sh

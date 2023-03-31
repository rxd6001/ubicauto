# "/root/UBiCauto/sh/" 에 파일 설치 후 'ln'으로 alias 생성 후 기동시작, '스크립트 파일'

echo " 프로그램 실행 링크 생성 시작 "
sleep 0.5

ln -s /root/UBiCauto/sh/usb.sh /usr/bin/usb1
ln -s /root/UBiCauto/sh/usb.sh /usr/bin/pbb1        # ubicck 용
ln -s /root/UBiCauto/sh/bb.sh /usr/bin/bbl
ln -s /root/UBiCauto/sh/kusb.sh /usr/bin/kusb1
echo " 매수 usb 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/uss.sh /usr/bin/uss1
ln -s /root/UBiCauto/sh/uss.sh /usr/bin/pss1        # ubicck 용
ln -s /root/UBiCauto/sh/bs.sh /usr/bin/bsl
ln -s /root/UBiCauto/sh/kuss.sh /usr/bin/kuss1
echo " 매도 uss 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/myc.sh /usr/bin/myc1                # 자사정보 계산
ln -s /root/UBiCauto/sh/kmyc.sh /usr/bin/kmyc1
ln -s /root/UBiCauto/sh/my.sh /usr/bin/myl                  # log 확인
echo " myc 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/sfg.sh /usr/bin/psfg                # 설정파일
echo " psfg 생성 완료"
sleep 0.5


""" Start - 공통 """
ln -s /root/UBiCauto/sh/usr.sh /usr/bin/usr
ln -s /root/UBiCauto/sh/usr.sh /usr/bin/prr             #  ubicck 용 Rotate 파일 로그 **
ln -s /root/UBiCauto/sh/br.sh /usr/bin/brl
ln -s /root/UBiCauto/sh/kusr.sh /usr/bin/kusr
ln -s /root/UBiCauto/sh/adn.sh /usr/bin/adn                 # add num **
echo " usr 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/Esell.sh /usr/bin/Esell             # 비상 매도 **
echo " Esell 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/now_sell.sh /usr/bin/nsell             # 한 종목 즉시 매도 검색 **
echo " nsell 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/ubicck.sh /usr/bin/ubicck            # 프로세스 실행 감시
echo " ubicck 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/sc.sh /usr/bin/sc                   # 점검시간 설정 -- 공통
ln -s /root/UBiCauto/sh/ksc.sh /usr/bin/ksc
ln -s /root/UBiCauto/sh/scl.sh /usr/bin/sl
echo " sc 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/wrun.sh /usr/bin/wrun1
ln -s /root/UBiCauto/sh/kwrun.sh /usr/bin/kwrun1
echo " wrun 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/myc_add.sh /usr/bin/mycadd          # 자산정보 월내역 수정
echo " mycadd 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/rmhty.sh /usr/bin/rmhty             # 수정내역 삭제(history)
echo " rmhty 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/showp.sh /usr/bin/shp               # 프로세스 확인
echo " shp 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/ubicstart.sh /usr/bin/ubicstart                # 설정파일
ln -s /root/UBiCauto/sh/ubicstop.sh /usr/bin/ubicstop
echo " ubicstart, stop 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/n_deal.sh /usr/bin/ndeal            # 한 종목 매도 시
echo " ndeal 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/n_s.sh /usr/bin/nnss                # 최우선순위 1개 시장가매도
echo " nnss 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/restart_code_server.sh /usr/bin/rcsv       # code-server 재시작 **
echo " code-server 재시작 생성 완료"
sleep 0.5

""" End - 공통 """

# ============================================= #

# 2번 계정 스크립트 생성
ln -s /root/UBiCauto/sh/sfg2.sh /usr/bin/psfg2                # 2 계정 설정파일
echo " psfg2 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/usb2.sh /usr/bin/usb2
ln -s /root/UBiCauto/sh/usb2.sh /usr/bin/pbb2        # ubicck 용
ln -s /root/UBiCauto/sh/kusb2.sh /usr/bin/kusb2
echo " 매수 usb2 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/uss2.sh /usr/bin/uss2
ln -s /root/UBiCauto/sh/uss2.sh /usr/bin/pss2       # ubicck 용
ln -s /root/UBiCauto/sh/kuss2.sh /usr/bin/kuss2
echo " uss2 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/now_sell2.sh /usr/bin/nsell2             # 한 종목 즉시 매도 검색 **
echo " nsell2 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/myc2.sh /usr/bin/myc2                # 자사정보 계산
ln -s /root/UBiCauto/sh/kmyc2.sh /usr/bin/kmyc2
ln -s /root/UBiCauto/sh/my2.sh /usr/bin/myl2                  # log 확인
echo " myc 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/mcc2.sh /usr/bin/mcc2
echo " mcc2 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/bbl2.sh /usr/bin/bbl2
echo " bbl2 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/bs2 /usr/bin/bsl2
echo " bsl2 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/n_s2.sh /usr/bin/nnss2                # 최우선순위 1개 시장가매도
echo " nnss2 생성 완료"
sleep 0.5
# ============================================= #
# 3번 계정 스크립트 생성
ln -s /root/UBiCauto/sh/sfg3.sh /usr/bin/psfg3                # 3 계정 설정파일
echo " psfg3 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/usb3.sh /usr/bin/usb3
ln -s /root/UBiCauto/sh/usb3.sh /usr/bin/pbb3        # ubicck 용
ln -s /root/UBiCauto/sh/kusb3.sh /usr/bin/kusb3
echo " 매수 usb3 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/uss3.sh /usr/bin/uss3
ln -s /root/UBiCauto/sh/uss3.sh /usr/bin/pss3       # ubicck 용
ln -s /root/UBiCauto/sh/kuss3.sh /usr/bin/kuss3
echo " uss3 생성 완료"
sleep 0.5


ln -s /root/UBiCauto/sh/bbl3.sh /usr/bin/bbl3
echo " bbl3 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/bs3 /usr/bin/bsl3
echo " bsl3 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/myc3.sh /usr/bin/myc3                # 자사정보 계산
ln -s /root/UBiCauto/sh/kmyc3.sh /usr/bin/kmyc3
ln -s /root/UBiCauto/sh/my3.sh /usr/bin/myl3                  # log 확인
echo " myc 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/n_s3.sh /usr/bin/nnss3                # 최우선순위 1개 시장가매도
echo " nnss3 생성 완료"
sleep 0.5

ln -s /root/UBiCauto/sh/now_sell3.sh /usr/bin/nsell3             # 한 종목 즉시 매도 검색 **
echo " nsell3 생성 완료"
sleep 0.5
# ============================================= #

echo " Everything 생성 완료 ~ !! "
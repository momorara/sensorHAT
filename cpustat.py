# cat cpustat.py

# CPUのデータを取得します。
 
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
2020/10/11  CpuRate = int(TckBusy*100/TckAll) 0で割るエラー処理追加

scp -r GPIO tk@192.168.68.111:/home/tk
"""
import time 
import subprocess
import sys
 
def GetCpuFreq():
    Cmd = 'vcgencmd measure_clock arm'
    result = subprocess.Popen(Cmd, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    Rstdout ,Rstderr = result.communicate()
    CpuFreq = Rstdout.split('=')
    # print("CpuFreq",CpuFreq)
    return int(CpuFreq[1])
 
def GetCpuTemp():
    Cmd = 'vcgencmd measure_temp'
    result = subprocess.Popen(Cmd, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    Rstdout ,Rstderr = result.communicate()
    CpuTemp = Rstdout.split()
    return CpuTemp[0]
 
 
def GetCpuStat():
    Cmd = 'cat /proc/stat | grep cpu'
    result = subprocess.Popen(Cmd, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    Rstdout ,Rstderr = result.communicate()
    LineList = Rstdout.splitlines()
    #
    TckList = []
    for Line in LineList:
        ItemList = Line.split()
        TckIdle = int(ItemList[4])
        TckBusy = int(ItemList[1])+int(ItemList[2])+int(ItemList[3])
        TckAll  = TckBusy + TckIdle
        TckList.append( [ TckBusy ,TckAll ] )
    return  TckList
 
 
class CpuUsage:
    def __init__(self):
        self._TckList    = GetCpuStat()
 
    def get(self):
        TckListPre       = self._TckList
        TckListNow       = GetCpuStat()
        self._TckList    = TckListNow
        CpuRateList = []
        for (TckNow, TckPre) in zip(TckListNow, TckListPre):
            TckDiff = [ Now - Pre for (Now , Pre) in zip(TckNow, TckPre) ]
            TckBusy = TckDiff[0]
            TckAll  = TckDiff[1]
            try:
                CpuRate = int(TckBusy*100/TckAll)
            except:
                # 極たまに、0で割りエラーになる
                # 表示としては、0か100%以上の数字となり見ればわかる
                CpuRate = int(TckBusy*100/1)
                print(CpuRate,TckBusy,TckAll)
            CpuRateList.append( CpuRate )
        return CpuRateList
 
#
if __name__=='__main__':
    
    gCpuUsage = CpuUsage()       # 初期化
    max_cpu = 0
    max_tmp = 0
    for ix in range(10000):
        time.sleep(1)
        CpuRateList = gCpuUsage.get()
        CpuRate     = CpuRateList[0]
        if int(CpuRate) > max_cpu:
            max_cpu = int(CpuRate)
        CpuRate_str = " CPU:%3d" % CpuRate
        del CpuRateList[0]
        CpuTemp     = GetCpuTemp()
        CpuTemp_n = float(CpuTemp[5:9])
        if CpuTemp_n > max_tmp:
            max_tmp = CpuTemp_n
        CpuFreq     = int(GetCpuFreq()/1000000)
        CpuFreq_str = "ARM %4dMHz " % CpuFreq
        Info_str = CpuFreq_str + CpuTemp + CpuRate_str + "%"
        print(Info_str ,CpuRateList,' /maxCpu=',max_cpu,'maxTemp=',max_tmp,'℃')
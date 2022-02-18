#main function
#!/usr/bin/python

"""
###########################################################################
ラズパイの情報を収集し、表示
/hpme/pi で動く様にしたバージョン

#Filename      :info.py
#Description   :CPU温度、CPU使用率
                モデルの名前
                iPアドレス

#Update        :2020/04/29

############################################################################
"""
# ライブラリの読み込み
import subprocess
import time 

import socket
import binascii

def myIP():
    import subprocess
    p = subprocess.Popen(
        "ifconfig",
        #stdin=subprocess.PIPE
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, 
        env={'LANG':'C'},
        shell=True
        )
    out, err = p.communicate()
    # print(out)
    str_out = out.decode("ascii", "ignore")
    # print(str_out)
    # 192を見つける
    fd1 = str_out.find('192.')
    # print(fd1)
    str_out1 = str_out[fd1:]
    # print(str_out1)
    # 192の先頭からスペースまでの文字数を調べる
    fd2 = str_out1.find(' ')
    # print(fd2)
    #ip = str_out1[:fd2].decode()　←なぜかエラーになる??
    # 192の頭から必要な文字数だけ取り出す
    ip = str_out1[:fd2]
    return ip

#ラズパイ情報取得
def RaspiInfo():
    p = subprocess.Popen(
        "cat /proc/cpuinfo|grep Model",
        #stdin=subprocess.PIPE
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, 
        env={'LANG':'C'},
        shell=True
        )
    out, err = p.communicate()
    # b'Model\t\t: Raspberry Pi 3 Model B Plus Rev 1.3\n'
    # Piから1.3までを切り出す。
    str_out = out.decode("ascii", "ignore")
    # print(str_out)
    # Piを見つける
    fd1 = str_out.find('Pi')
    # print(fd1)
    str_out1 = str_out[fd1:-1]
    # Revを見つける
    fd2 = str_out1.find('Rev')
    str_out2 = str_out1[:fd2]
    # print(str_out2)
    str_out3 = str_out2.replace(" ", "")
    str_out4 = str_out3.replace("Model", "")
    str_out5 = str_out4.replace("Plus", "+")
    return str_out5

#cpu情報取得
def CpuInfo():
    CpuRateList = gCpuUsage.get()
    CpuRate     = CpuRateList[0]
    CpuRate_str = " CPU:%3d" % CpuRate
    del CpuRateList[0]
    CpuTemp     = GetCpuTemp()
    Info_str =  CpuTemp + CpuRate_str + "% "
    CpuTemp = int(CpuTemp[5:7])
    return CpuTemp,CpuRate_str,Info_str.replace(": ", ":")

def GetCpuTemp():
    Cmd = 'vcgencmd measure_temp'
    result = subprocess.Popen(Cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    Rstdout ,Rstderr = result.communicate()
    CpuTemp = Rstdout.split()
    return CpuTemp[0]

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
            CpuRate = int(TckBusy*100/TckAll)
            CpuRateList.append( CpuRate )
        return CpuRateList

def GetCpuStat():
    Cmd = 'cat /proc/stat | grep cpu'
    result = subprocess.Popen(Cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    Rstdout ,Rstderr = result.communicate()
    LineList = Rstdout.splitlines()

    TckList = []
    for Line in LineList:
        ItemList = Line.split()
        TckIdle = int(ItemList[4])
        TckBusy = int(ItemList[1])+int(ItemList[2])+int(ItemList[3])
        TckAll  = TckBusy + TckIdle
        TckList.append( [ TckBusy ,TckAll ] )
    return  TckList


#ブロードキャストにて発信

def main():
    #イニシャライズ処理
    time.sleep(0.5)

    #ラズパイ情報取得
    Raspi_info = RaspiInfo()
    print(Raspi_info)

    #ip取得
    ip = myIP()
    print(ip)

    #cpu情報取得
    # プログラム起動直後にデータ収集すると、大きな負荷率となってしまう
    # なので、一秒程度時間をおくと良い。
    time.sleep(1)
    cpu_temp,cpu_rate,cpu_info = CpuInfo()
    print(cpu_info)

    #ブロードキャストにて発信
    print(Raspi_info,ip,cpu_info)

def destroy():
    pass
#
# if run this script directly ,do:
if __name__ == '__main__':

    gCpuUsage = CpuUsage()       # 初期化

    try:
        main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        print('キーボード押されました。')
        destroy()
    except ValueError as e:
        print(e)


   

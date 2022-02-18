"""
ip_check.py -> ip_get_MakeFile.py

2022/01/04  start
2022/01/07  ipgetにてipアドレスを取得
            wpsはしない
2022/02/13  ip_get_MakeFile.py
            起動時に自身のipアドレスを取得して、ipアドレス名のファィルを作る
            おまけに、osのナンバーもつけておく


cronで起動時に実行する。
@reboot sleep 20 && python3 ip_get_MakeFile.py

インストール
pip3 install ipget

ipアドレスをipgetにて取得、2秒3回試してダメならあきらめる。
ライブラリと使用する。
返り値は ipアドレス or  in not
zeroの場合ipgetが動作しないので、ifconfigで取得している
第一オクテッドが192固定なので、必要なら変更すること


scp -r 標準で入れたい/*.* pi@192.168.68.117:/home/pi/
"""

import subprocess
import sys
import os
import time
import getpass


# sudo ifconfig wlan0 down
# sudo ifconfig wlan0 up
os.system('sudo ifconfig wlan0 up')
time.sleep(5)

# ipgetを使って、ipアドレスを取得
import ipget


# ipアドレスをipgetにて取得、2秒3回試してダメならあきらめる。
def ip_check():
    count = 0
    ip_adr = 'not'
    while 'not' in ip_adr:
        try:
            a = ipget.ipget()
            ip_adr = a.ipaddr("eth0")
            if 'not' in ip_adr:
                pass
                # print('00',ip_adr)
            else:
                ip_adr = ip_adr.replace('/24','')
                ip_adr = ip_adr.replace('/28','')
                # print('01 ip_adr:',ip_adr)
        except :
            pass
            # print('02',ip_adr)
        count = count +1
        # print('1',count,ip_adr)
        if count >3 or ('not' in ip_adr) == False:
            return ip_adr
        else:
            os.system('sudo ifconfig wlan0 up')
            time.sleep(2)

    # print('2',ip_adr)
    return ip_adr

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

def main():
    ip_adr = ip_check()
    print('ip_adr:',ip_adr)

    if ip_adr == 'not':
        ip_adr = myIP()
        print('ip_adr1:',ip_adr)
    
    # 古いファィルを消す
    os.system('rm ' + 'ip_add_*')
    # OSバージョンを取得
    os.system('cat /etc/debian_version | tee os_no')
    with open('os_no') as f:
        os_no = f.read()
    os_no = os_no.replace('\n','')
    # print('os_no:',os_no,':')

    # ipアドレス表示ファィルを作る
    file_name ='ip_add_' + ip_adr + ' os_' + os_no
    with open(file_name, mode='w') as f:
        f.write('ip_address')

if __name__ == '__main__':
    main()

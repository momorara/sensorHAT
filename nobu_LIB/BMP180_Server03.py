# –– coding: utf-8 –
#!/usr/bin/python
"""
TCP_server03.py
TCP_client01.py

新しい名前
BMP180_Server03.py


シンプルにTCP通信をやりとりします。
python2 で動きます。

クライアントから end を送ると、両方停止します。
無理に止めると ソケットを掴んだままになり しばらく使えなくなります。

サーバーは CTL-cでも止まります。

2019/11/16
1 TCP通信する際に文字列そのままでは送れなかったので、バイナリーに変換し送信。
受信側でもバイナリーから文字に変換して表示している。 
本当に必要なのか不明だけれど、動いたのでよしとする。

time_now を送りたいとき
import binascii
msg = binascii.hexlify(time_now.encode('utf-8')) 
time_now = binascii.unhexlify(b"".join(recieve_messages))

2 ＊＊＊＊＊＊ サーバー立てる時には、IPアドレスを当該機器のものに変更すること。

3 BMP180 を埋め込みます。

2019/12/30
    03  IPアドレスを自動取得 有線でも無線でも可能
2020/1/4
    03  名称変更 importをnobu_LIBからできるように

Adafruit_Python_BMP を BMP_inst.txtを参考にインストールして、
必要なBMP085をnobu_LIBに持ってくる。

2020/02/02
        cronで自動起動させたいが、wifi確立する前なので、IPが取得できない。
        ip取得できるまで待たせるため、
        cronで sh BMPStart.shを起動させる。-->一旦止めている
2020/02/05
    03  デーモンとして起動できるようにした。
        sudo systemctl daemon-reload    ユニットをロード
        sudo systemctl start BMP180d    ユニットを起動
        sudo systemctl stop BMP180d.service ユニットを停止
2020/02/21
        気圧を-10hPa補正した。
2020/09/22  ユーザー名変更に対応不要だが、No module named 'Adafruit_GPIO'
            となるので、python 2 で起動だよ



scp -r sensorBox tk@192.168.68.111:/home/tk
"""
import csv
import socket
import datetime
import binascii

#import Adafruit_BMP.BMP085 as BMP085
import nobu_LIB.BMP085 as BMP085
sensor = BMP085.BMP085()
from time import sleep

from nobu_LIB import Lib_IP
# ＊＊＊＊＊＊＊＊＊＊＊＊ ipアドレスを自動取得 ＊＊＊＊＊＊＊＊＊＊＊＊

ip = Lib_IP.myIP()

f = open('ip.csv', 'a') 
csvWriter = csv.writer(f)
csvWriter.writerow('test 1')
csvWriter.writerow(ip)
f.close()

HOST = ip
# HOST = "172.20.10.2"
print(ip,'***')
PORT = 8001

def main():

    # 待ち受け用のソケットオブジェクト
    server = socket.socket()
    try:
        # 待ち受けポートに割り当て ＊＊＊＊＊＊
        # サーバープログラム再起動時、socket.errorになるので、60秒位待つ必要がある。
        for i in range(1, 41):
            try:
                server.bind((HOST, PORT))
            except Exception as e:
                print("error:{e} retry:{i}/{max}".format(e=e, i=i, max=40))
                sleep(5)
            else:
                break
        if i == 40 :print("error end")
        print("--")

        while True:
            # 待ち受け開始
            server.listen(5)

            # 要求がいたら受け付け
            client, addr = server.accept()

            # 受け取ったメッセージを出力
            recieve_messege = client.recv(4096).decode()
            print('message:{}'.format(recieve_messege))

            # endというメッセージを受け取ったら終わる
            if recieve_messege == "end\r\n":
                break

            # Temp Press
            print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
            print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
            print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
            print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))
            Temp = sensor.read_temperature()
            # 気圧は、小数点第一位で四捨五入して、整数値にします。
            # siriの気圧とちょうど10hPa違うので、補正する。
            Press = (sensor.read_pressure()+ 50)/ 100 - 10

            # 現在時間
            dt_now = datetime.datetime.now()
            minute = dt_now.minute
            if minute <10 :
                time_now =  str(dt_now.hour) + ":0" + str(dt_now.minute) 
            else:
                time_now =  str(dt_now.hour) + ":" + str(dt_now.minute) 
            print(time_now)

            # 返信メッセージ作成
            # タイムスタンプあり
            # msg_s = time_now + " Temp= " + str(Temp) + " C Press= " + str(Press) + " hPa"
            # タイムスタンプなし
            msg_s =            " Temp= " + str(Temp) + " C Press= " + str(Press) + " hPa"
            
            print(msg_s)
            msg = binascii.hexlify(msg_s.encode('utf-8')) 

            client.send(msg)
            client.close()


    except KeyboardInterrupt:
        server.close()
    finally:
        server.close()

if __name__ == '__main__':
    main()
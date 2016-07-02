# 中華電信MOD自動鎖(RouterOS)

## 說明：
1.程式啟動時會先將RouterOS指定介面關閉

2.開始依照設定執行判斷，符合條件後重新開啟RouterOS指定介面

3.可相容其他有SSH功能的路由器，請自行修改_mod_switch(turn_on)內的SSH指令
## 執行條件
Python>=3.5.1

paramiko>=2.0.0
## 安裝方式(Windows)
1.安裝Python 3.5.1，請記得勾選 Add Python 3.5 to PATH

2.執行install_hinet_mod_locker.bat

3.打開hinet_mod_locker.py依照自己的需求修改以下欄位並儲存
```
HOST = 'SSH連線主機'
PORT = SSH連線PORT(預設22)
USERNAME = '登入名稱'
PASSWORD = '登入密碼'
ONLINE_PING_RETRY = 必須連線的裝置在離線後重新嘗試ping次數(防止誤判)
SLEEP_TIME = 每次判斷間隔時間(秒)
ROS_INTERFACES = ['ether1', 'pppoe-out-x', 'sstp-client-x']
OFFLINE_DEVICES = ['IP', '或', '網址']
ONLINE_DEVICES = ['IP', '或', '網址']
```

4.把hinet_mod_locker.py丟到開機執行資料夾內(按 Win+R 之後輸入 shell:startup)

5.重新開機或雙擊hinet_mod_locker.py開始執行
## 疑難排解
執行後一片黑
```
請確認RouterOS設定為允許SSH登入
IP > Services > SSH
```
```
請確認Python有正確安裝
在使用者命令列輸入
python -V
正常狀況會顯示
Python 3.5.1
```
```
請確認paramiko有安裝
在使用者命令列輸入
pip freeze
正常狀況會顯示類似下面的資訊
cffi==1.6.0
cryptography==1.3.2
idna==2.1
paramiko==2.0.0
pyasn1==0.1.9
pycparser==2.14
six=1.10.0
```

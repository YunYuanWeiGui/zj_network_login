import requests
from urllib.parse import urljoin, urlparse, parse_qs
import json
# import time

# 配置信息
WLAN_NAME = "i-Zijin"
YOUR_FULL_LOGIN_URL = "http://172.21.2.10:8080/eportal/index.jsp?wlanuserip=eece5af5893131d7cbdf5414bc7f8e8a&wlanacname=efe20fe36b0d5cc7cdd34d866bad9e76&ssid=&nasip=fbba2526398e9984bd6f73050578e0e2&snmpagentip=&mac=0ab2cc7ec8ac0d0d896b859007b4940c&t=wireless-v2&url=2c0328164651e2b4f13b933ddf36628bea622dedcc302b30&apmac=&nasid=efe20fe36b0d5cc7cdd34d866bad9e76&vid=f401b3584db059a8&port=2fca8ff728f8e127&nasportid=5b9da5b08a53a5407f78812b658307e027b17f87a3f590dc179af19ccfc06535"  # 替换为你复制的完整URL

import shutil
max_width = shutil.get_terminal_size().columns
del shutil

def login(USERNAME: str, PASSWORD: str, PROVIDER: str) -> bool:
    # 1. 从URL中解析出queryString参数
    print(" " * max_width, end='\r')
    print("[0/4] 解析URL参数...", end='\r')
    # time.sleep(0.1)
    parsed_url = urlparse(YOUR_FULL_LOGIN_URL)
    query_params = parse_qs(parsed_url.query)

    # 获取queryString，parse_qs返回的是字典，值是列表
    query_string = query_params.get('queryString', [None])[0]

    # 如果URL中没有明确的queryString参数，我们就自己构造一个
    if not query_string:
        # 自己从URL参数中构造一个queryString
        # 剔除不需要的参数，只保留认证相关的
        important_params = {}
        for key in ['wlanuserip', 'wlanacname', 'ssid', 'nasip', 'snmpagentip', 'mac', 't', 'url', 'apmac', 'nasid', 'vid', 'port', 'nasportid']:
            if key in query_params:
                important_params[key] = query_params[key][0]

        # 将参数拼接成queryString格式
        query_string = '&'.join([f"{k}={v}" for k, v in important_params.items()])

    if not query_string:
        print(" " * max_width, end='\r')
        print("❌ 无法从URL中提取queryString参数")
        return False

    # print(f"提取的queryString: {query_string}")

    # 2. 创建Session并设置Headers
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': YOUR_FULL_LOGIN_URL,
    }
    session.headers.update(headers)

    # 3. 获取登录页面（为了获取Cookie）
    print(" " * max_width, end='\r')
    print("[1/4] 获取登录页面...", end='\r')
    # time.sleep(0.1)
    try:
        response_index = session.get(YOUR_FULL_LOGIN_URL)
        response_index.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(" " * max_width, end='\r')
        print(f"获取登录页面失败: {e}")
        return False

    # 4. 准备POST数据 - 关键是包含queryString
    if PROVIDER[:2] == "中国":
        PROVIDER = PROVIDER[2:]
    post_data = {
        'userId': USERNAME,
        'password': PASSWORD,
        'service': PROVIDER,
        'queryString': query_string,  # 这是修复的关键！
        'operatorPwd': '',
        'operatorUserId': '',
        'validcode': '',
        'passwordEncrypt': 'false',
    }

    # 5. 发送POST请求
    post_url = urljoin("http://172.21.2.10:8080", "/eportal/InterFace.do?method=login")

    print(" " * max_width, end='\r')
    print("[2/4] 正在提交登录信息...", end='\r')
    # time.sleep(0.1)
    try:
        response_login = session.post(post_url, data=post_data)
        response_login.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(" " * max_width, end='\r')
        print(f"提交登录请求失败: {e}")
        return False

    # 6. 解析响应
    print(" " * max_width, end='\r')
    print("[3/4] 解析服务器响应...", end='\r')
    # time.sleep(0.1)
    try:
        result = response_login.json()
        message = result.get('message')
        try:
            message = message.encode('latin-1').decode('utf-8')
        except:
            pass
        if result.get('result') == 'success':
            print(" " * max_width, end='\r')
            print(f"[4/4] ✅ 登录成功! {message}", end='\r')
            # time.sleep(0.1)
            return True
        else:
            print(" " * max_width, end='\r')
            print(f"[4/4] ❌ 登录失败! 原因: {message}")
            print(f"服务器返回: {result}")
            return False
    except json.JSONDecodeError:
        print(" " * max_width, end='\r')
        print(f"[4/4] ❌ 错误：服务器返回了非JSON格式的响应。")
        print(f"响应内容: {response_login.text}")
        return False

import os
import configparser
def user_data() -> tuple:
    if os.path.isfile("zj_account.ini"):
        config = configparser.ConfigParser()
        config.read("zj_account.ini", encoding="utf-8")
        username = config.get('Userdata', 'username')
        password = config.get('Userdata', 'password')
        provider = config.get('Userdata', 'provider')
        return username, password, provider
    else:
        config_content = """[Userdata]
;用户名
username = 此处改为你的用户名
;密码
password = 此处改为你的密码
;运营商 (校园网, 中国移动, 中国电信, 中国联通)
provider = 此处改为你的运营商
"""
        with open("zj_account.ini", "w", encoding="utf-8") as f:
            f.write(config_content)
        print(" " * max_width, end='\r')
        print("请配置 zj_account.ini 后重试！")
        return ()

if __name__ == '__main__':
    import subprocess
    import re


    def get_wifi_name() -> str | 无:
        """获取当前连接的WiFi名称"""
        try:
            # 执行命令获取WiFi信息
            result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'],
                                    capture_output=True, text=True, encoding='utf-8', errors='ignore')
            output = result.stdout

            # 使用正则表达式匹配SSID
            ssid_match = re.search(r'SSID\s*:\s*(.+)', output)

            if ssid_match:
                wifi_name = ssid_match.group(1).strip()
                return wifi_name
            else:
                return 无

        except Exception as e:
            return f"获取失败: {str(e)}"

    print(" " * max_width, end='\r')
    print("正在加载用户配置...", end='\r')
    # time.sleep(0.1)
    if user_data():
        USERNAME, PASSWORD, PROVIDER = user_data()
        print(" " * max_width, end='\r')
        print("正在检查网络状态...", end='\r')
        # time.sleep(0.1)
        if get_wifi_name() != WLAN_NAME:
            print(" " * max_width, end='\r')
            print("正在尝试连接网络...", end='\r')
            os.system(f'netsh wlan connect name="{WLAN_NAME}"')
            # time.sleep(1)
        if get_wifi_name() == WLAN_NAME:
            print(" " * max_width, end='\r')
            print("正在尝试登录中...", end='\r')
            # time.sleep(0.1)
            success = login(USERNAME, PASSWORD, PROVIDER)
            print(" " * max_width, end='\r')
            if success:
                print("✅ 登陆成功\n已成功连接校园网！")
            else:
                print('❌ 登录失败')

    input("press enter to exit...")

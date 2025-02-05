# -*- encoding: utf-8 -*-
"""
@File    : utils.py
@Time    : 2021/11/20 16:56
@Author  : smy
@Email   : smyyan@foxmail.com
@Software: PyCharm
"""

import requests
import pickle
import time
import os


class LoginTool:

    def __init__(self, config):
        self.config = config
        self.try_count = 5
        self.base_url = str(config.get_bot_config("byrbt-url"))
        self.login_url = self.get_url('login.php')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        self.cookie_save_path = './data/ByrbtCookies.pickle'

    def get_url(self, url):
        return self.base_url + url

    def load_cookie(self):
        if os.path.exists(self.cookie_save_path):
            print('find ByrbtCookies.pickle, loading cookies')
            read_path = open(self.cookie_save_path, 'rb')
            byrbt_cookies = pickle.load(read_path)
        else:
            print('not find ByrbtCookies.pickle, get cookies...')
            byrbt_cookies = self.login()

        return byrbt_cookies

    def login(self):
        session = requests.session()
        if self.config.get_bot_config("use_proxy") == 'true':
            proxies = {'http': 'socks5://127.0.0.1:2025',
                       'https': 'socks5://127.0.0.1:2025'}
        else:
            proxies = None
        # response = requests.get("https://icanhazip.com/", proxies=proxies)
        # print(f"当前代理 IP: {response.text}")
        # print(session.get("https://byr.pt/login"))

        # login_res = session.post(self.get_url('takelogin.php'),
        #                          headers=self.headers,
        #                          data=dict(
        #                              logintype="username",
        #                              userinput=str(self.config.get_bot_config("username")),
        #                              password=str(self.config.get_bot_config("passwd")),
        #                              remember="yes"))

        for i in range(5):
            login_res = session.post("https://byr.pt/api/v2/login.php", headers=self.headers, json={
                "type": "username",
                "username": str(self.config.get_bot_config("username")),
                "password": str(self.config.get_bot_config("passwd")),
                "remember": False
            }, proxies=proxies)
            json_res = login_res.json()
            if json_res.get("success", False) is True:
                # 登录成功
                cookies = {}
                for k, v in session.cookies.items():
                    cookies[k] = v
                os.makedirs(os.path.dirname(self.cookie_save_path), mode=0o755, exist_ok=True)
                with open(self.cookie_save_path, 'wb') as f:
                    pickle.dump(cookies, f)
                return cookies

            time.sleep(1)

        print('login fail!')
        return None

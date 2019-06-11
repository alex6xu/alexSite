from datetime import datetime, timedelta
import requests


class WXToken:
    def __init__(self, appid, appkey):
        self.appid = appid
        self.appkey = appkey
        self.token_create_time = None
        self.token = None

    def get_token(self, code):
        if self.token_create_time and self.token_create_time + timedelta(seconds=7100) > datetime.now():
            return self.token
        self.token = self.get_access_token()
        self.token_create_time = datetime.now()
        return self.token

    def get_access_token(self):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        self.appid, self.appkey)
        req = requests.get(url).json()
        access_token = req.get('access_token')
        print(access_token)
        return access_token


class WxAuthToken:
    def __init__(self, appid, appkey):
        self.appid = appid
        self.appkey = appkey
        self.access_token = None
        self.refresh_token = None
        self.openid = None
        self.token_create = None

    def get_access_token(self, code):
        acc_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"%(self.appid, self.appkey, code)
        print(acc_url)
        res = requests.get(acc_url)
        resp = res.json()
        # print(resp.data)
        self.access_token = resp.get('access_token')
        self.refresh_token = resp.get('refresh_token')
        self.openid = resp.get('openid')
        return self.access_token, self.openid

    def refresh_access_token(self):
        refresh_url = "https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=APPID&grant_type=refresh_token&refresh_token=REFRESH_TOKEN"

        resp = requests.get(refresh_url).json()
        self.access_token = resp.get('access_token')
        self.refresh_token = resp.get('refresh_token')
        self.openid = resp.get('openid')
        print(self.openid)
        return self.access_token

    def get_userinfo(self):
        print('access token')
        print(self.access_token)
        print('openid')
        print(self.openid)
        user_url = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (self.access_token, self.openid)
        print(user_url)
        res = requests.get(user_url)
        resp = res.json()
        return resp
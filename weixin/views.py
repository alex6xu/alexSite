from django.views import View
import hashlib
import requests
from django.shortcuts import render
from xml.etree import  ElementTree
from .wxauth import WXToken, WxAuthToken
from .models import WXUser
from django.conf import settings
from django.contrib.auth import login
# from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import logging
from .AI import AI
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

from datetime import datetime

logger = logging.getLogger('app')

appid = settings.WX_APPID
appkey = settings.WX_APPKEY


class Index(View):
    def get(self, request):
        return render('blog/index.html', {})


class Info(View):
    respTemp = """<xml>
  <ToUserName><![CDATA[{toUser}]]></ToUserName>
  <FromUserName><![CDATA[{fromUser}]]></FromUserName>
  <CreateTime>{create_time}</CreateTime>
  <MsgType><![CDATA[{msgType}]]></MsgType>
  <Content><![CDATA[{content}]]></Content>
</xml>"""

    def get(self, request):
        token = settings.WX_TOKEN
        sign = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')
        str1 = ''.join(sorted([timestamp, nonce, token])).encode('utf-8')
        signature = hashlib.sha1(str1).hexdigest()
        logger.info(signature)
        if signature == sign:
            return HttpResponse(echostr)
        return HttpResponse('ok')

    def posta(self, request):
        logger.info(request.body)
        info = ElementTree.fromstring(request.body)
        developId = info.find('ToUserName').text
        userId = info.find('FromUserName').text
        createTime = datetime.now().timestamp()
        logger.info(userId)
        logger.info(info.find("MsgType").text)
        logger.info(info.find('Latitude').text if info.find('Latitude') else '')
        logger.info(info.find('Longitude').text if info.find('Longitude') else '')
        resp = self.respTemp.format(toUser=userId,
                                    fromUser=developId,
                                    create_time=createTime,
                                    msgType="text",
                                    content="您好，欢迎关注"
                                    )
        if resp:
            return HttpResponse(resp)
        return HttpResponse("thanks for !")

    def post(self, request):
        token = settings.WX_TOKEN
        sign = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        # echostr = request.GET.get('echostr', '')
        try:
            check_signature(token, sign, timestamp, nonce)
        except InvalidSignatureException:
            logger.warning("Signature check failed.")
            return

        header = {"content_type": "application/xml;charset=utf-8"}
        body = self.request.body
        logger.info(body)
        msg = parse_message(body)
        if not msg:
            logger.info('Empty message, ignored')
            return

        if msg.type == 'text':
            logger.info('message type text from %s', msg.source)
            # new bot
            bot = AI(msg)
            response = bot.respond(msg.content, msg)
            # response = '您好！'
            reply = create_reply(response, msg, render=True)
            logger.info('Replied to %s with "%s"', msg.source, response)
            return HttpResponse(reply, content_type=header['content_type'])

        elif msg.type == 'location':
            # if options.debug:
            logger.info('message type location from %s', msg.source)

        elif msg.type == 'image':
            # if options.debug:
            logger.info('message type image from %s', msg.source)
            image = msg.image

        else:
            logger.info('message type unknown')


class Notify(View):
    def get(self, req):
        pass

    def post(self, request):
        auth_client = WxAuthToken(appid, appkey)
        acode = request.args.get('code')
        logger.info('acode', acode)
        token, openid = auth_client.get_access_token(acode)
        logger.info('token', token)
        logger.info('openid', openid)
        if token:
            user = WXUser(openid=openid, access_token=token)
            login(request, user)
            if request.args.get('state') == "8":
                userinfo = auth_client.get_userinfo()
                # logger.info(userinfo)
                ctx = {'username': userinfo.get('openid')}
            else:
                ctx = {'username': 'test'}
        else:
            ctx = {'info': 'login failed '}
            return render(
                'user/index.html', **ctx
            )

        return render('user/index.html', **ctx)


class Test(View):
    def get(self,request):
        msg = request.args.get('msg')
        bot = AI()
        response = bot.respond(msg, msg)
        return HttpResponse(response)


class Token(View):
    def get(self, request):
        pass


def get_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        appid, appkey)
    req = requests.get(url).json()
    access_token = req.get('access_token')
    return access_token


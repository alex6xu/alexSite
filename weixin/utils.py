import sys
import imageio as gio
import cv2
from io import StringIO
import requests
# from StringIo import
from django.conf import settings
from wechatpy import WeChatClient

st = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

class MyImage:
    def __init__(self, content):
        self.content = content

    def read(self, size=None):
        if not size:
            return self.content
        result = self.content[:size]
        if len(result) == len(self.content):
            self.content = ''
            return result
        else:
            self.content = self.content[size:]
            return result


def trans_image(f):
    try:
        pics = gio.mimread(f)
    except TypeError as e:
        return '图片格式错误'
    except Exception as e:
        return None
    A = []
    output = StringIO()
    for i in pics:
        u, v, _ = i.shape
        c = i * 0 + 255
        gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
        for j in range(0, u, 6):
            for k in range(0, v, 6):
                pix = gray[j, k]
                b, g, r, _ = i[j, k]
                zifu = st[int(((len(st) - 1) * pix) / 256)]
                cv2.putText(c, zifu, (k, j),
                            cv2.FONT_HERSHEY_COMPLEX, 0.3,
                            (int(b), int(g), int(r)), 1)
        A.append(c)

        gio.mimsave(output, A, 'gif', duration=0.1)
    return output

weChatClient = WeChatClient(settings.WX_APPID, settings.WX_APPKEY)


def image_process(img):
    resp = requests.get(img)
    # myimg = MyImage()
    return trans_image(resp.content)

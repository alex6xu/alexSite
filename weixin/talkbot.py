#coding=utf-8

import os
import sys
import aiml

from django.conf import settings

__name__ = 'talkbot'


class TalkBot(aiml.Kernel):
    def __init__(self):
        super(TalkBot, self).__init__()
        self.verbose(settings.DEBUG)
        if os.path.exists(settings.TALKBOT_BRAIN_PATH):
            self.bootstrap(brainFile=settings.TALKBOT_BRAIN_PATH)
        else:
            self.init_bot()
            self.saveBrain(settings.TALKBOT_BRAIN_PATH)

        for p in settings.TALKBOT_PROPERTIES:
            self.setBotPredicate(p, settings.TALKBOT_PROPERTIES[p])

    def init_bot(self):
        for f in os.listdir(settings.AIML_SET):
            if f.endswith('.aiml'):
                self.learn(os.path.join(settings.AIML_SET, f))


talkbot = TalkBot()


def test(data, msg=None, bot=None):
    return True


def respond(data, session=None):

    resp = talkbot.respond(data, session)
    if ' ' in resp:
        resp = ''.join(resp.split(' '))
    return resp


if __name__ == '__main__':
    print(respond("你好"))

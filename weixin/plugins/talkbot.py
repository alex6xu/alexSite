#coding=utf-8

import os
import sys
from .. import aiml

from django.conf import settings

__name__ = 'talkbot'


class TalkBot(aiml.Kernel):
    def __init__(self):
        super(TalkBot, self).__init__()
        self.verbose(settings.DEBUG)
        if os.path.exists(settings.talkbot_brain_path):
            self.bootstrap(brainFile=settings.talkbot_brain_path)
        else:
            self.init_bot()
            self.saveBrain(settings.talkbot_brain_path)

        for p in settings.talkbot_properties:
            self.setBotPredicate(p, settings.talkbot_properties[p])

    def init_bot(self):
        for f in os.listdir(settings.aiml_set):
            if f.endswith('.aiml'):
                self.learn(os.path.join(settings.aiml_set, f))

talkbot = TalkBot()

def test(data, msg=None, bot=None):
    return True

def respond(data, msg=None, bot=None):
    return talkbot.respond(data).encode('utf-8')

if __name__ == '__main__':
    print(respond("你好"))

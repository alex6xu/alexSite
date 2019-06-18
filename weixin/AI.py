# coding=utf-8

import logging
from . import plugins


class AI(object):

    _plugin_modules = []
    _plugin_loaded = False

    def __init__(self, msg=None):
        if msg:
            self.id = msg.source

    @classmethod
    def load_plugins(cls):
        if cls._plugin_loaded:
            return
        for name in plugins.__all__:
            try:
                plugin = __import__('weixin.plugins.%s' % name, fromlist=(name,))
                cls.add_plugin(plugin)
                logging.info('Plugin %s loaded success.' % name)
            except Exception as e:
                logging.exception(e)
                logging.warning('Fail to load plugin %s' % name)
        cls._plugin_loaded = True

    @classmethod
    def add_plugin(cls, plugin):
        if not hasattr(plugin, 'test'):
            logging.error('Plugin %s has no method named test, ignore it')
            return False
        if not hasattr(plugin, 'respond'):
            logging.error('Plugin %s has no method named respond, ignore it')
            return False
        cls._plugin_modules.append(plugin)
        return True

    def respond(self, data, msg=None):
        response = None
        for plugin in self._plugin_modules:
            try:
                if plugin.test(data, msg, self):
                    response = plugin.respond(data, msg, self)
            except:
                logging.warning('Plugin %s failed to respond', plugin.__name__)
                continue
            if response:
                logging.info('Plugin %s respond successfully', plugin.__name__)
                return response

        return response or '您好'


AI.load_plugins()

if __name__ == '__main__':
    bot = AI()
    print(bot.respond('hello'))

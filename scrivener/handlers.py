from collections import defaultdict

from zope.interface import implements

from twisted.python import log

from scrivener.interfaces import ILogHandler


class TwistedLogHandler(object):
    implements(ILogHandler)

    def log(self, category, message):
        log.msg(message, system=category)


class MultiCategoryHandler(object):
    implements(ILogHandler)

    def __init__(self):
        self._handlers = defaultdict(list)

    def addHandler(self, category, handler):
        self._handlers[category].append(handler)

    def log(self, category, message):
        for handler in self._handlers[category]:
            handler.log(category, message)

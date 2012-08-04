from zope.interface import Interface


class ILogHandler(Interface):
    def log(self, category, message):
        """
        Handle an individual log entry as a category and message.
        """

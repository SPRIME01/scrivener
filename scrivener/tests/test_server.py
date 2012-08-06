import mock

from zope.interface import directlyProvides

from twisted.trial.unittest import TestCase

from twisted.test.proto_helpers import StringTransport
from twisted.internet.interfaces import IStreamServerEndpoint
from twisted.internet.defer import succeed

from scrivener.interfaces import ILogHandler
from scrivener.server import ScribeServerService


class ScribeServerServiceTests(TestCase):
    def setUp(self):
        self.handler = mock.Mock()
        directlyProvides(self.handler, ILogHandler)

        self.endpoint = mock.Mock()
        directlyProvides(self.endpoint, IStreamServerEndpoint)

        self.port = mock.Mock()

        def _listen(*args, **kwargs):
            return succeed(self.port)

        self.endpoint.listen.side_effect = _listen

        self.service = ScribeServerService(self.endpoint, self.handler)

        self.transport = StringTransport()

    def test_startService(self):
        self.service.startService()
        self.assertEqual(self.endpoint.listen.call_count, 1)

    def test_stopService(self):
        self.service.startService()
        self.service.stopService()

        self.assertEqual(self.port.stopListening.call_count, 1)

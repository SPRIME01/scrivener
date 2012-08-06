import mock

from twisted.trial.unittest import TestCase
from twisted.internet.defer import succeed, Deferred
from scrivener._thrift.scribe import ttypes
from scrivener.client import ScribeClient


class ScribeClientTests(TestCase):
    def setUp(self):
        self.endpoint = mock.Mock()
        self.client_proto = mock.Mock()

        def _connect(factory):
            self.client_proto = mock.Mock()
            self.client_proto.client.Log.return_value = ttypes.ResultCode.OK
            return succeed(self.client_proto)

        self.endpoint.connect.side_effect = _connect

    def assertFired(self, d):
        results = []
        d.addCallback(lambda r: results.append(r))
        self.assertEqual(len(results), 1)

        return results[0]

    def test_log(self):
        client = ScribeClient(self.endpoint)

        d = client.log('category', 'message')
        self.assertEqual(self.assertFired(d), ttypes.ResultCode.OK)
        self.assertEqual(self.client_proto.client.Log.call_count, 1)

    def test_log_already_connected(self):
        client = ScribeClient(self.endpoint)

        d = client.log('category', 'message')

        self.assertEqual(self.assertFired(d), ttypes.ResultCode.OK)
        self.assertEqual(self.client_proto.client.Log.call_count, 1)

        d = client.log('category', 'message')
        self.assertEqual(self.assertFired(d), ttypes.ResultCode.OK)
        self.assertEqual(self.client_proto.client.Log.call_count, 2)

    def test_log_while_connecting(self):
        connect_d = Deferred()
        real_connect = self.endpoint.connect.side_effect

        def _delay_connect(factory):
            d = real_connect(factory)
            connect_d.addCallback(lambda _: d)

            return connect_d

        self.endpoint.connect.side_effect = _delay_connect
        client = ScribeClient(self.endpoint)

        d = client.log('category', 'message')
        self.assertEqual(self.client_proto.client.Log.call_count, 0)

        d2 = client.log('category', 'message')
        self.assertEqual(self.client_proto.client.Log.call_count, 0)

        connect_d.callback(None)

        self.assertEqual(self.assertFired(d), ttypes.ResultCode.OK)
        self.assertEqual(self.assertFired(d2), ttypes.ResultCode.OK)

        self.assertEqual(self.client_proto.client.Log.call_count, 2)

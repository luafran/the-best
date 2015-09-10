import datetime
import unittest

from thebest.common.tokens import exceptions
from thebest.common.tokens.token import Token


class DummyToken(Token):
    def __init__(self, **kwargs):
        super(DummyToken, self).__init__(**kwargs)


class TestToken(unittest.TestCase):
    def test_default_values(self):
        token = DummyToken()
        self.assertIsNone(token.token)
        self.assertIsNone(token.payload)
        self.assertEqual(datetime.timedelta(hours=1),
                         token.expiration_timedelta)

    def test_raises_empty_token(self):
        token = DummyToken()
        self.assertRaises(exceptions.EmptyToken, token.verify)

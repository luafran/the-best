import unittest

import Crypto.PublicKey.RSA as RSA

from thebest.common.tokens import exceptions
from thebest.common.tokens.jwt_token import JWTToken


class TestJWTToken(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key = RSA.generate(2048)

    def setUp(self):
        super(TestJWTToken, self).setUp()
        self.expected_payload = {'foo': 'bar'}

    def test_verify_created_token_no_certificate(self):
        token = JWTToken(payload=self.expected_payload)
        (headers, payload) = token.verify()

        self.assertTrue(self.expected_payload, payload)

    def test_verify_created_token_with_certificate(self):
        token = JWTToken(payload=self.expected_payload, certificate=self.key)
        (headers, payload) = token.verify()

        self.assertTrue(self.expected_payload, payload)

    def test_verify_string_token_no_certificate(self):
        token = JWTToken(payload=self.expected_payload, certificate=self.key)
        token_to_verify = JWTToken(token=str(token), certificate=self.key)

        self.assertTrue(self.expected_payload, token_to_verify)

    def test_verify_unicode_token(self):
        token = JWTToken(payload=self.expected_payload, certificate=self.key)
        token_to_verify = JWTToken(token=unicode(token), certificate=self.key)

        self.assertTrue(self.expected_payload, token_to_verify)

    def test_verify_string_token_with_certificate(self):
        token = JWTToken(payload=self.expected_payload, certificate=self.key)
        token_to_verify = JWTToken(token=str(token), certificate=self.key)

        self.assertTrue(self.expected_payload, token_to_verify)

    def test_token_verification_fails_because_certificate_is_wrong(self):
        token = JWTToken(payload=self.expected_payload, certificate=self.key)
        self.assertRaises(exceptions.InvalidToken, JWTToken, token=str(token),
                          certificate=RSA.generate(2048))

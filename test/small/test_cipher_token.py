import unittest

from thebest.common.tokens import exceptions
from thebest.common.tokens import cipher
from thebest.common.tokens import jwt_token


class TestCipherToken(unittest.TestCase):
    def setUp(self):
        super(TestCipherToken, self).setUp()
        self.expected_payload = {'foo': 'bar'}

    def test_token_self_encryption_decryption(self):
        token_enctrypted = cipher.CipherToken(jwt_token.JWTToken,
                                              payload=self.expected_payload)
        (headers_encrypted, payload_encrypted) = token_enctrypted.verify()

        token_dectrypted = cipher.CipherToken(jwt_token.JWTToken,
                                              token=str(token_enctrypted))
        (headers_decrypted, payload_decrypted) = token_dectrypted.verify()

        self.assertTrue(self.expected_payload, payload_encrypted)
        self.assertTrue(self.expected_payload, payload_decrypted)

    def test_decrypt_invalid_padding(self):
        with self.assertRaises(exceptions.InvalidToken):
            cipher.CipherToken(jwt_token.JWTToken, token='123')

    def test_inner_token_validation_fail(self):
        dummy_token = cipher.CipherToken(jwt_token.JWTToken,
                                         payload=self.expected_payload)
        invalid_token = dummy_token._encrypt('12345')
        with self.assertRaises(exceptions.InvalidToken):
            cipher.CipherToken(jwt_token.JWTToken, token=invalid_token)

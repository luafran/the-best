import base64

from Crypto.Cipher import AES

from thebest.common import settings
from thebest.common.tokens import exceptions
from thebest.common.tokens.token import Token


class CipherToken(Token):  # pylint: disable=R0903
    BLOCK_SIZE = 32
    PADDING = '{'

    def __init__(self, inner_token_class, **kwargs):
        self._cipher = AES.new(settings.AES_SECRET)

        token = kwargs.pop('token', None)
        if token:
            kwargs['token'] = self._decrypt(token)

        self._inner_token = inner_token_class(**kwargs)

        kwargs['token'] = token if token else self._encrypt(
            self._inner_token.token)
        kwargs['payload'] = self._inner_token.payload

        super(CipherToken, self).__init__(**kwargs)

    def verify(self):
        super(CipherToken, self).verify()
        return self._inner_token.verify()

    def _pad(self, message):
        return message + (
            self.BLOCK_SIZE - len(message) % self.BLOCK_SIZE) * self.PADDING

    def _encrypt(self, message):
        return base64.b64encode(self._cipher.encrypt(self._pad(message)))

    def _decrypt(self, message):
        try:
            return self._cipher.decrypt(base64.b64decode(message)).rstrip(
                self.PADDING)
        except TypeError:
            raise exceptions.InvalidToken('Invalid Token')

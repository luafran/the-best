import datetime

import jws
import jwt

from thebest.common import settings
from thebest.common.tokens import exceptions
from thebest.common.tokens.token import Token


class JWTToken(Token):  # pylint: disable=R0903
    _jwt_registered_claims = ['iss', 'sub', 'aud', 'exp', 'nbf', 'iat', 'jti']

    def __init__(self, certificate=None, **kwargs):
        super(JWTToken, self).__init__(**kwargs)
        self.certificate = certificate
        if not self.token:
            self.token = jwt.generate_jwt(
                self.payload, self.certificate, 'PS512',
                self.expiration_timedelta,
                not_before=(datetime.datetime.now() -
                            settings.JWT_TOKEN_NOT_BEFORE_TIMEDELTA))
        else:
            (self.headers, self.payload) = self.verify()

    def verify(self):
        super(JWTToken, self).verify()

        try:
            self.headers, payload = jwt.verify_jwt(str(self.token),
                                                   self.certificate,
                                                   allowed_algs=['PS512', 'none'],
                                                   checks_optional=True,
                                                   iat_skew=settings.JWT_TOKEN_NOT_BEFORE_TIMEDELTA)
            self.payload = ({key: value for key, value in payload.items()
                             if key not in self._jwt_registered_claims})
        except jws.exceptions.SignatureError:
            raise exceptions.InvalidToken()
        except (Exception, ValueError):
            raise exceptions.InvalidToken()

        return (self.headers, self.payload)

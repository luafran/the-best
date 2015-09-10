import abc
import datetime

import six

from thebest.common.tokens import exceptions


@six.add_metaclass(abc.ABCMeta)  # pylint: disable=R0903
class Token(object):
    def __init__(self, **kwargs):
        self.token = kwargs.get('token')
        self.payload = kwargs.get('payload')
        self.expiration_timedelta = kwargs.get('expiration_timedelta',
                                               datetime.timedelta(hours=1))

    def __str__(self):
        return self.token

    def verify(self):
        if not self.token:
            raise exceptions.EmptyToken()

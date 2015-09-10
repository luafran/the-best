import unittest
import uuid

from thebest.common import exceptions
from thebest.common.utils import resource_normalizer
from thebest.common.utils.resource_normalizer import Rule


class Test(unittest.TestCase):

    def test_when_call_normalize_resource_with_invalid_rules_then_raise_InvalidArgument(self):
        TRANSFORMATION_RULES = {
            'name': Rule(args=('personalInformation.name', )),
            'lastName': Rule(args=('personalInformation.lastName', )),
            'extras': {
                # Invalid rule: multiple args with no "execute"
                'birthday': Rule(args=('personalInformation.dayOfBirth',
                                       'personalInformation.monthOfBirth',
                                       'personalInformation.yearOfBirth', )),
                'email': Rule(args=('personalInformation.email', ))
            },
        }

        EXTERNAL_RESOURCE = {
            'id': uuid.uuid4(),
            'personalInformation': {
                'name': 'Emiliano',
                'lastName': 'Molina',
                'dayOfBirth': '10',
                'monthOfBirth': 'June',
                'yearOfBirth': '1984',
            }
        }

        try:
            resource_normalizer.normalize_resource(EXTERNAL_RESOURCE,
                                                   TRANSFORMATION_RULES)
        except exceptions.InvalidArgument as ex:
            self.assertEqual(ex.information()[exceptions.CONTEXT_KEY],
                             'too many args for a rule with no "execute"')
        except Exception as ex:
            self.fail(ex)
        else:
            self.fail()

    def test_when_call_normalize_resource_then_returns_normalized_resource(self):
        def _build_birthday(yearOfBirth, monthOfBirth, dayOfBirth):
            return '%s-%s-%s' % (yearOfBirth, monthOfBirth, dayOfBirth)

        TRANSFORMATION_RULES = {
            'name': Rule(args=('personalInformation.name', )),
            'lastName': Rule(args=('personalInformation.lastName', )),
            'extras': {
                'birthday': Rule(execute=_build_birthday,
                                 args=('personalInformation.dayOfBirth',
                                       'personalInformation.monthOfBirth',
                                       'personalInformation.yearOfBirth', )),
                'email': Rule(args=('personalInformation.email', ))
            },
        }

        EXTERNAL_RESOURCE = {
            'id': uuid.uuid4(),
            'personalInformation': {
                'name': 'Emiliano',
                'lastName': 'Molina',
                'dayOfBirth': '10',
                'monthOfBirth': 'June',
                'yearOfBirth': '1984',
            }
        }

        expected_resource = {
            'name': 'Emiliano',
            'lastName': 'Molina',
            'extras': {
                'birthday': '1984-June-10',
                'email': None,
            }
        }

        try:
            normalized_resources = resource_normalizer.normalize_resource(
                EXTERNAL_RESOURCE, TRANSFORMATION_RULES)
        except Exception as ex:
            self.fail(ex)

        self.assertEqual(normalized_resources, expected_resource)

    def test_when_call_normalize_resource_using_default_values_then_returns_normalized_resource(self):
        def _build_birthday(yearOfBirth, monthOfBirth, dayOfBirth):
            raise ValueError('value error')

        TRANSFORMATION_RULES = {
            'name': Rule(args=('personalInformation.name', )),
            'lastName': Rule(args=('personalInformation.lastName', )),
            'extras': {
                'age': Rule(args=('personalInformation.age', ),
                            default=25),
                'birthday': Rule(execute=_build_birthday,
                                 args=('personalInformation.dayOfBirth',
                                       'personalInformation.monthOfBirth',
                                       'personalInformation.yearOfBirth', ),
                                 default='YYYY-Month-DD'),
                'email': Rule(args=('adfasf.personalInformation.email', ),
                              default='unknown'),
            },
        }

        EXTERNAL_RESOURCE = {
            'id': uuid.uuid4(),
            'personalInformation': {
                'name': 'Emiliano',
                'lastName': 'Molina',
                'dayOfBirth': '10',
                'monthOfBirth': 'June',
                'yearOfBirth': '1984',
            }
        }

        expected_resource = {
            'name': 'Emiliano',
            'lastName': 'Molina',
            'extras': {
                'birthday': 'YYYY-Month-DD',
                'email': 'unknown',
                'age': 25,
            }
        }

        try:
            normalized_resources = resource_normalizer.normalize_resource(
                EXTERNAL_RESOURCE, TRANSFORMATION_RULES)
        except Exception as ex:
            self.fail(ex)

        self.assertEqual(normalized_resources, expected_resource)

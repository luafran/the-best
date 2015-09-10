import unittest

from thebest.common import roles


class TestRoles(unittest.TestCase):
    def setUp(self):
        super(TestRoles, self).setUp()
        self._SUPER_ROLE_ACCESS_LEVEL = 0
        self._SUPER_ROLE_NAME = 'super_role'
        self._SUPER_ROLE = (self._SUPER_ROLE_ACCESS_LEVEL,
                            self._SUPER_ROLE_NAME)

        self._NORMAL_ROLE_ACCESS_LEVEL = 1
        self._NORMAL_ROLE_NAME = 'normal_role'
        self._NORMAL_ROLE = (self._NORMAL_ROLE_ACCESS_LEVEL,
                             self._NORMAL_ROLE_NAME)

        self._OLD_ROLES = roles.ROLES
        roles.ROLES = (self._SUPER_ROLE, self._NORMAL_ROLE)

    def tearDown(self):
        super(TestRoles, self).tearDown()
        roles.ROLES = self._OLD_ROLES

    def test_find_role_by_access_level(self):
        role = roles.find_role_by_access_level(self._SUPER_ROLE_ACCESS_LEVEL)
        self.assertEqual(self._SUPER_ROLE, role)

    def test_find_role_by_access_level_invalid(self):
        self.assertRaises(roles.InvalidRole,
                          roles.find_role_by_access_level, -1)

    def test_find_role_by_name(self):
        role = roles.find_role_by_name(self._SUPER_ROLE_NAME)
        self.assertEqual(self._SUPER_ROLE, role)

    def test_find_role_by_name_invalid(self):
        self.assertRaises(roles.InvalidRole,
                          roles.find_role_by_name, "invalid_name")

    def test_find_role_with_name_as_criteria(self):
        role = roles.find_role(self._SUPER_ROLE_NAME)
        self.assertEqual(self._SUPER_ROLE, role)

    def test_find_role_with_access_level_as_criteria(self):
        role = roles.find_role(self._SUPER_ROLE_ACCESS_LEVEL)
        self.assertEqual(self._SUPER_ROLE, role)

    def test_find_role_with_role_as_criteria(self):
        role = roles.find_role(self._SUPER_ROLE)
        self.assertEqual(self._SUPER_ROLE, role)

    def test_find_role_with_role_list_as_criteria(self):
        role = roles.find_role(list(self._SUPER_ROLE))
        self.assertEqual(self._SUPER_ROLE, role)

    def test_find_role_invalid(self):
        self.assertRaises(roles.InvalidRole,
                          roles.find_role, "invalid name")

    def test_find_role_invalid_type(self):
        self.assertRaises(roles.InvalidRole,
                          roles.find_role, 1.0)

    def test_is_more_privileged_than(self):
        self.assertTrue(roles.is_more_privileged_than(self._SUPER_ROLE,
                                                      self._NORMAL_ROLE))

    def test_is_more_privileged_than_left_rigth_equals(self):
        self.assertTrue(roles.is_more_privileged_than(self._SUPER_ROLE,
                                                      self._SUPER_ROLE))

    def test_is_less_privileged_than(self):
        self.assertTrue(roles.is_less_privileged_than(self._NORMAL_ROLE,
                                                      self._SUPER_ROLE))

    def test_is_less_privileged_than_left_rigth_equals(self):
        self.assertFalse(roles.is_less_privileged_than(self._SUPER_ROLE,
                                                       self._SUPER_ROLE))

import unittest

import mock

from thebest.common import exceptions
from thebest.common.utils import settings_loader


class SettingsModuleMock(object):
    __name__ = "foo.bar.settings"

    SETTINGS_ONLY = "SETTINGS_ONLY"
    LOCAL_SETTINGS_OVERRIDE = "OVERRIDE"
    PACKAGE_SETTINGS_OVERRIDE = "OVERRIDE"
    LOCAL_PACKAGE_SETTINGS_OVERRIDE = "OVERRIDE"
    LOCAL_PACKAGE_SETTINGS_NOT_DISPLAYED = "NOT_DISPLAYED"

    def __init__(self):
        self.SETTINGS_ONLY = self.SETTINGS_ONLY
        self.LOCAL_SETTINGS_OVERRIDE = self.LOCAL_SETTINGS_OVERRIDE
        self.PACKAGE_SETTINGS_OVERRIDE = self.PACKAGE_SETTINGS_OVERRIDE
        self.LOCAL_PACKAGE_SETTINGS_OVERRIDE = (
            self.LOCAL_PACKAGE_SETTINGS_OVERRIDE)


class LocalSettingsModuleMock(object):
    __name__ = "foo.bar.local_settings"

    DISPLAY_SETTINGS = ['LOCAL_SETTINGS_OVERRIDE',
                        'PACKAGE_SETTINGS_OVERRIDE',
                        'LOCAL_PACKAGE_SETTINGS_OVERRIDE',
                        'I_AM_A_GHOST']
    LOCAL_SETTINGS_OVERRIDE = "LOCAL_SETTINGS_OVERRIDE"
    PACKAGE_SETTINGS_OVERRIDE = "OVERRIDE"
    LOCAL_PACKAGE_SETTINGS_OVERRIDE = "OVERRIDE"
    LOCAL_PACKAGE_SETTINGS_NOT_DISPLAYED = "NOT_DISPLAYED"

    def __init__(self):
        self.LOCAL_SETTINGS_OVERRIDE = self.LOCAL_SETTINGS_OVERRIDE
        self.PACKAGE_SETTINGS_OVERRIDE = self.PACKAGE_SETTINGS_OVERRIDE
        self.LOCAL_PACKAGE_SETTINGS_OVERRIDE = (
            self.LOCAL_PACKAGE_SETTINGS_OVERRIDE)


class PackageSettingsModuleMock(object):
    __name__ = "foo.bar.package"

    DISPLAY_SETTINGS = ['PACKAGE_SETTINGS_OVERRIDE',
                        'LOCAL_PACKAGE_SETTINGS_OVERRIDE']
    PACKAGE_SETTINGS_OVERRIDE = "PACKAGE_SETTINGS_OVERRIDE"
    LOCAL_PACKAGE_SETTINGS_OVERRIDE = "OVERRIDE"
    LOCAL_PACKAGE_SETTINGS_NOT_DISPLAYED = "NOT_DISPLAYED"

    def __init__(self):
        self.PACKAGE_SETTINGS_OVERRIDE = self.PACKAGE_SETTINGS_OVERRIDE
        self.LOCAL_PACKAGE_SETTINGS_OVERRIDE = (
            self.LOCAL_PACKAGE_SETTINGS_OVERRIDE)


class LocalPackageSettingsModuleMock(object):
    __name__ = "foo.bar.local_package"

    DISPLAY_SETTINGS = ['LOCAL_PACKAGE_SETTINGS_OVERRIDE']
    LOCAL_PACKAGE_SETTINGS_OVERRIDE = "LOCAL_PACKAGE_SETTINGS_OVERRIDE"
    LOCAL_PACKAGE_SETTINGS_NOT_DISPLAYED = "NOT_DISPLAYED"

    def __init__(self):
        self.LOCAL_PACKAGE_SETTINGS_OVERRIDE = (
            self.LOCAL_PACKAGE_SETTINGS_OVERRIDE)


class TestSettingsLoader(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch("importlib.import_module")
        self.addCleanup(patcher.stop)
        self._import_module = patcher.start()
        mocked_modules = [PackageSettingsModuleMock(),
                          SettingsModuleMock()]

        def return_module(*args, **kwargs):
            module = mocked_modules.pop(0)
            if isinstance(module, Exception):
                raise module
            return module

        self._import_module.side_effect = return_module

    def test_raise_exception_environment_variable_missing(self):
        with mock.patch.dict('os.environ', {}):
            with self.assertRaises(exceptions.GeneralInfoException):
                settings_loader.SettingsLoader("foo.bar", "NON_EXISTS")

    def test_settings_lazy_load(self):
        expected_prefix = "foobar"
        with mock.patch.dict('os.environ', {'DUMMY_ENV': expected_prefix}):
            settings_loader.SettingsLoader("foo.bar", "DUMMY_ENV")
            self.assertFalse(self._import_module.called)

    def test_settings_packages_prefix(self):
        expected_prefix = "foobar"
        with mock.patch.dict('os.environ', {'DUMMY_ENV': expected_prefix}):
            settings_loader.SettingsLoader("foo.bar", "DUMMY_ENV",
                                           modules_lazy_load=False)
            expected_calls = [
                mock.call('foo.bar.base_settings'),
                mock.call('thebest.common.base_settings')]
            self.assertEqual(expected_calls,
                             self._import_module.call_args_list)

    def test_get_package_setting(self):
        settings = settings_loader.SettingsLoader("foo.bar")
        self.assertEqual(
            PackageSettingsModuleMock.PACKAGE_SETTINGS_OVERRIDE,
            settings.PACKAGE_SETTINGS_OVERRIDE)

    def test_get_setting(self):
        settings = settings_loader.SettingsLoader("foo.bar")
        self.assertEqual(
            SettingsModuleMock.SETTINGS_ONLY,
            settings.SETTINGS_ONLY)

    def test_get_setting_when_module_import_failed(self):
        mocked_modules = [ImportError(),
                          SettingsModuleMock()]

        def return_module(*args, **kwargs):
            module = mocked_modules.pop(0)
            if isinstance(module, Exception):
                raise module
            return module

        self._import_module.side_effect = return_module

        settings = settings_loader.SettingsLoader("foo.bar")
        self.assertEqual(
            SettingsModuleMock.LOCAL_PACKAGE_SETTINGS_OVERRIDE,
            settings.LOCAL_PACKAGE_SETTINGS_OVERRIDE)

    def test_get_environment_setting(self):
        expected_prefix = "foobar"
        expected_env_name = "DUMMY_LOCAL_PACKAGE_SETTINGS_OVERRIDE"
        expected_env_value = "from_environment"
        with mock.patch.dict(
                'os.environ', {'DUMMY_ENV': expected_prefix,
                               expected_env_name: expected_env_value}):
            settings = settings_loader.SettingsLoader(
                "foo.bar", "DUMMY_ENV", "DUMMY")
            self.assertEqual(
                expected_env_value,
                settings.LOCAL_PACKAGE_SETTINGS_OVERRIDE)

    def test_get_unexisting_setting(self):
        settings = settings_loader.SettingsLoader("foo.bar")
        with self.assertRaises(AttributeError):
            settings.NOT_EXISTS

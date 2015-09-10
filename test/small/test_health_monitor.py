import mock

import stevedore

from tornado import testing, gen

from thebest.common import version
from thebest.common.health.health_monitor import HealthMonitor
from thebest.common.health.plugin import HealthPlugin


class DummyPlugin(HealthPlugin):
    def __init__(self, health, status):
        self.health = health
        self.status = status

    @gen.coroutine
    def get_status(self):
        raise gen.Return((self.health, self.status))


class TestHealthMonitor(testing.AsyncTestCase):
    def _buid_status(self, name, status, exposure):
        return {
            'name': name,
            'status': status[1],
            'exposure': exposure
        }

    @testing.gen_test
    def test_get_status_no_version(self):
        with mock.patch('stevedore.extension.ExtensionManager') as extension_manager:
            extension_manager.return_value = []

            health_monitor = HealthMonitor()
            health, status, version_app = yield health_monitor.get_status()

            self.assertEqual(HealthPlugin.GOOD, health)
            self.assertEqual([], status)

    @testing.gen_test
    def test_get_status_no_plugins_no_details(self):
        with mock.patch('stevedore.extension.ExtensionManager') as extension_manager:
            extension_manager.return_value = []

            health_monitor = HealthMonitor()
            health, status, version_app = yield health_monitor.get_status()

            self.assertEqual(HealthPlugin.GOOD, health)
            self.assertEqual([], status)

    @testing.gen_test
    def test_get_status_no_plugins_with_details(self):
        with mock.patch('stevedore.extension.ExtensionManager') as extension_manager:
            extension_manager.return_value = []
            expected_status = [self._buid_status('systemHealth',
                                                 HealthPlugin.GOOD,
                                                 HealthPlugin.HIGH)]

            health_monitor = HealthMonitor()
            health, status, version_app = yield health_monitor.get_status(True)

            self.assertEqual(HealthPlugin.GOOD, health)
            self.assertEqual(expected_status, status)

    @testing.gen_test
    def test_get_status_plugins_no_details(self):
        dummy_health = HealthPlugin.GOOD
        dummy_status = self._buid_status('dummy', dummy_health,
                                         HealthPlugin.HIGH)
        with mock.patch('stevedore.extension.ExtensionManager') as extension_manager:
            extension_manager.return_value = iter([
                stevedore.extension.Extension('dummy_plugin', 'dummy.one',
                                              DummyPlugin,
                                              DummyPlugin(dummy_health,
                                                          dummy_status))])

            health_monitor = HealthMonitor()
            health, status, version_app = yield health_monitor.get_status()
            self.assertEqual(HealthPlugin.GOOD, health)
            self.assertEqual([], status)

    @testing.gen_test
    def test_get_status_plugins_with_details(self):
        dummy_health = HealthPlugin.GOOD
        dummy_status = self._buid_status('dummy', dummy_health,
                                         HealthPlugin.HIGH)
        expected_status = [self._buid_status('systemHealth',
                                             HealthPlugin.GOOD,
                                             HealthPlugin.HIGH),
                           dummy_status]
        with mock.patch('stevedore.extension.ExtensionManager') as extension_manager:
            extension_manager.return_value = iter([
                stevedore.extension.Extension('dummy_plugin', 'dummy.one',
                                              DummyPlugin,
                                              DummyPlugin(dummy_health,
                                                          dummy_status))])

            health_monitor = HealthMonitor()
            health, status, version_app = yield health_monitor.get_status(True)
            self.assertEqual(HealthPlugin.GOOD, health)
            self.assertEqual(expected_status, status)

    @testing.gen_test
    def test_get_status_plugins_warning_status_no_details(self):
        dummy_health = HealthPlugin.WARNING
        dummy_status = self._buid_status('dummy', dummy_health,
                                         HealthPlugin.HIGH)
        with mock.patch('stevedore.extension.ExtensionManager') as extension_manager:
            extension_manager.return_value = iter([
                stevedore.extension.Extension('dummy_plugin', 'dummy.one',
                                              DummyPlugin,
                                              DummyPlugin(dummy_health,
                                                          dummy_status))])

            health_monitor = HealthMonitor()
            health, status, version_app = yield health_monitor.get_status()
            self.assertEqual(HealthPlugin.WARNING, health)
            self.assertEqual([], status)

    @mock.patch('thebest.common.version.get_version')
    @testing.gen_test
    def test_get_app_version_returns_unknown_version_app(self, get_version_mock):

        get_version_mock.return_value = version.UNKNOWN_VERSION

        with mock.patch('stevedore.extension.ExtensionManager') as extension_manager:
            extension_manager.return_value = []

            health_monitor = HealthMonitor()
            health, status, version_app = yield health_monitor.get_status()

            self.assertEqual(HealthPlugin.GOOD, health)
            self.assertEqual([], status)
            self.assertEqual(version.UNKNOWN_VERSION, version_app)

    @mock.patch('thebest.common.version.get_version')
    @testing.gen_test
    def test_get_app_version_returns_known_version_app(self, get_version_mock):
        get_version_mock.return_value = "1.0.0"

        with mock.patch('stevedore.extension.ExtensionManager') as extension_manager:
            extension_manager.return_value = []

            health_monitor = HealthMonitor()
            health, status, version_app = yield health_monitor.get_status()

            self.assertEqual(HealthPlugin.GOOD, health)
            self.assertEqual([], status)
            self.assertEqual("1.0.0", version_app)

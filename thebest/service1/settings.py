import sys

from thebest.common.utils import settings_loader

sys.modules[__name__] = settings_loader.SettingsLoader("thebest.service1")

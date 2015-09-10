import json
import os
import re

from tornado import escape
from tornado import locale as tornado_locale


# pylint: disable=protected-access
def load_json_translations(directory):
    """Loads translations from JSON files in a directory."""
    tornado_locale._translations = {}
    for path in os.listdir(directory):
        if not path.endswith(".json"):
            continue
        locale, _ = path.split(".")
        locale_parts = locale.replace('-', '_').split('_')
        locale = "_".join(
            locale_parts[:1] + [part.upper() for part in locale_parts[1:]])
        if not re.match("[a-z]+(_[A-Z]+)?$", locale):
            # Unrecognized locale
            continue
        full_path = os.path.join(directory, path)
        try:
            with open(full_path, "r") as tr_file:
                all_translations = json.load(tr_file)
        except TypeError:
            # Invalid translation
            continue
        tornado_locale._translations[locale] = {}
        for key, value in all_translations.iteritems():
            tornado_locale._translations[locale].setdefault("unknown", {})[
                escape.to_unicode(key)] = escape.to_unicode(value)
    tornado_locale._supported_locales = frozenset(
        list(tornado_locale._translations.keys())
        + [tornado_locale._default_locale])

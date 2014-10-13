#!/usr/bin/env python

from os.path import dirname, abspath
import sys

from django.conf import settings


if not settings.configured:
    settings_dict = dict(
        INSTALLED_APPS=["djformtags"],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            },
        },
        SILENCED_SYSTEM_CHECKS=["1_7.W001"],
    )

    settings.configure(**settings_dict)


import django
if django.VERSION > (1,7,0):
    django.setup()


def runtests(test_labels):
    sys.path.insert(0, dirname(abspath(__file__)))

    from django.test.runner import DiscoverRunner
    failures = DiscoverRunner(
        verbosity=1,
    ).run_tests(test_labels)
    sys.exit(failures)


if __name__ == "__main__":
    labels = sys.argv[1:] or [
        "djformtags",
    ]

    runtests(labels)

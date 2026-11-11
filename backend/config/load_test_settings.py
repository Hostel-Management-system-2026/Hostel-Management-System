"""Settings overlay for disposable local load-test accounts only."""

from config.settings import *  # noqa: F403
from django.contrib.auth.hashers import PBKDF2PasswordHasher


class FastLoadTestPasswordHasher(PBKDF2PasswordHasher):
    """Keep PBKDF2 while reducing synthetic account hashing cost."""

    iterations = 1_000


PASSWORD_HASHERS = ["config.load_test_settings.FastLoadTestPasswordHasher"]

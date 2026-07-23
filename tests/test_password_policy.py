import unittest

from webapp.password_policy import validate_password


class PasswordPolicyTests(unittest.TestCase):
    def test_no_mfa_requires_ten_characters(self):
        self.assertTrue(validate_password("short", lambda _: False))
        self.assertFalse(validate_password("abcdefghij", lambda _: False))

    def test_printable_ascii_and_spaces_are_allowed(self):
        self.assertFalse(validate_password("long pass phrase", lambda _: False))
        self.assertTrue(validate_password("validlength\n", lambda _: False))

    def test_common_password_is_rejected(self):
        self.assertTrue(validate_password("password123", lambda _: True))

    def test_arbitrary_complexity_is_not_required(self):
        self.assertFalse(validate_password("onlylowercase", lambda _: False))


if __name__ == "__main__":
    unittest.main()

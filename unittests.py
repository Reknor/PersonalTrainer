import unittest

from user import *


class TestUser(unittest.TestCase):
    def run_tests(self):
        self.test_login()
        self.test()

    def test(self):
        a1 = Account("bartek", "bartekbartek")
        assert passlib.hash.sha512_crypt.verify("bartekbartek", a1.password), "Account bartek password bartekbartek verify failed"
        u1 = Account("konrad", "konradkonrad")
        assert passlib.hash.sha512_crypt.verify("konradkonrad", u1.password), "User konrad password konradkonrad verify failed"
        assert u1.login == "konrad", "Account konrad login verify failed"
        assert User.validate_date("21-05-2020"), "21-05-2020 is not a valid date"

    def test_login(self):
        with self.assertRaises(ValueError):
            Account("kd", "ddd")


if __name__ == "__main__":
    TestUser().run_tests()

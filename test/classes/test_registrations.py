import datetime
import unittest

import teamvolik.classes.registration as registration


class RegistrationsTest(unittest.TestCase):
    def test_to_string(self):
        empty_registration = registration.Registration()
        self.assertTrue(str(empty_registration) == f"Registration(user_id=-1, game_id=-1, is_paid=False, is_reserve=False, time={empty_registration.time})")
        another_registration = registration.Registration(1, 1, True, True, datetime.datetime(2001, 6, 15, 9, 15))
        self.assertTrue(str(another_registration) == f"Registration(user_id=1, game_id=1, is_paid=True, is_reserve=True, time={another_registration.time})")

    def test_to_sqlite_table(self):
        empty_registration = registration.Registration()
        self.assertTrue(empty_registration.to_sqlite_table() == (-1, -1, False, False, empty_registration.time.timestamp()))

    def test_from_sqlite_table(self):
        empty_registration = registration.Registration.from_sqlite_table(None)
        self.assertTrue(str(empty_registration == str(registration.Registration(-1, -1, False, False, empty_registration.time))))
        registration_info = (1, 1, True, True, datetime.datetime(2001, 6, 15, 9, 15).timestamp())
        registration_from_sqlite_table = registration.Registration.from_sqlite_table(registration_info)
        registration_from_constructor = registration.Registration(1, 1, True, True, datetime.datetime(2001, 6, 15, 9, 15).timestamp())
        self.assertTrue(str(registration_from_sqlite_table) == str(registration_from_constructor))


if __name__ == "__main__":
    unittest.main()

import unittest
import sqlite3

import src.db.database as database
import src.classes.registration as registration


class DatabaseRegistrationTest(unittest.TestCase):
    connection: sqlite3.Connection
    db_cursor: sqlite3.Cursor

    def setUp(self) -> None:
        self.connection, self.db_cursor = database.connect(":memory:")
        database.create_tables(self.connection, self.db_cursor)

    def tearDown(self) -> None:
        self.connection.close()

    def test_registration_add(self):
        database.add_registration(self.connection, self.db_cursor, registration.Registration(0, 0))
        self.assertTrue(len(database.get_registrations(self.db_cursor)) == 1)

    def test_get_registrations_by_game_id(self):
        database.add_registration(self.connection, self.db_cursor, registration.Registration(1, 1))
        database.add_registration(self.connection, self.db_cursor, registration.Registration(2, 1))
        database.add_registration(self.connection, self.db_cursor, registration.Registration(3, 1))
        registrations_for_game_1 = database.get_registrations_by_game_id(self.db_cursor, 1)
        self.assertTrue(len(registrations_for_game_1) == 3)
        self.assertTrue(sorted(map(lambda x: x.user_id, registrations_for_game_1)) == [1, 2, 3])
        empty_registration_list = database.get_registrations_by_game_id(self.db_cursor, 999)
        self.assertTrue(len(empty_registration_list) == 0)

    def test_get_registrations_by_player_id(self):
        database.add_registration(self.connection, self.db_cursor, registration.Registration(1, 1))
        database.add_registration(self.connection, self.db_cursor, registration.Registration(1, 2))
        database.add_registration(self.connection, self.db_cursor, registration.Registration(1, 3))
        registrations_by_player_1 = database.get_registrations_by_player_id(self.db_cursor, 1)
        self.assertTrue(len(registrations_by_player_1) == 3)
        self.assertTrue(sorted(map(lambda x: x.game_id, registrations_by_player_1)) == [1, 2, 3])
        empty_registration_list = database.get_registrations_by_player_id(self.db_cursor, 999)
        self.assertTrue(len(empty_registration_list) == 0)

    def test_remove_registration(self):
        database.add_registration(self.connection, self.db_cursor, registration.Registration(1, 1))
        self.assertTrue(len(database.get_registrations(self.db_cursor)) == 1)
        database.remove_registration(self.connection, self.db_cursor, 1, 1)
        self.assertTrue(len(database.get_registrations(self.db_cursor)) == 0)


if __name__ == "__main__":
    unittest.main()

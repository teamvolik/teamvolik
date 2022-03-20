import unittest
import sqlite3

import src.db.database as database
import src.classes.game as game
import src.classes.player as player
import src.classes.registration as registration


class DatabaseTest(unittest.TestCase):
    connection: sqlite3.Connection
    db_cursor: sqlite3.Cursor

    def setUp(self) -> None:
        self.connection, self.db_cursor = database.connect(":memory:")
        database.create_tables(self.db_cursor)

    def tearDown(self) -> None:
        self.connection.close()

    def test_creation(self):
        try:
            self.db_cursor.execute("""SELECT * FROM players""")
        except sqlite3.OperationalError as error:
            self.fail(error)
        try:
            self.db_cursor.execute("""SELECT * FROM games""")
        except sqlite3.OperationalError as error:
            self.fail(error)
        try:
            self.db_cursor.execute("""SELECT * FROM registrations""")
        except sqlite3.OperationalError as error:
            self.fail(error)

    def test_no_creation_if_exists(self):
        database.create_tables(self.db_cursor)

    def test_player_add(self):
        database.add_player(self.connection, self.db_cursor, player.Player(0, "", False))
        self.assertTrue(len(database.get_players(self.db_cursor)) == 1)

    def test_game_add(self):
        database.add_game(self.connection, self.db_cursor, game.Game("15.06.2001 21:00", ""))
        self.assertTrue(len(database.get_games(self.db_cursor)) == 1)

    def test_games_should_have_unique_id(self):
        games = [
            database.add_game(self.connection, self.db_cursor, game.Game("15.06.2001 21:00", "")),
            database.add_game(self.connection, self.db_cursor, game.Game("15.06.2001 21:00", "")),
        ]
        self.assertTrue(len(database.get_games(self.db_cursor)) == 2)
        self.assertTrue(len(games) == 2)
        self.assertTrue(games[0].id != games[1].id)

    def test_registration_add(self):
        database.add_registration(self.connection, self.db_cursor, registration.Registration(0, 0))
        self.assertTrue(len(database.get_registrations(self.db_cursor)) == 1)


if __name__ == "__main__":
    unittest.main()

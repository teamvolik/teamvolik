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
        database.create_tables(self.connection, self.db_cursor)

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
        database.create_tables(self.connection, self.db_cursor)

    def test_get_players_by_game_id(self):
        new_players = [
            database.add_player(self.connection, self.db_cursor, player.Player(1, "vertolet", True)),
            database.add_player(self.connection, self.db_cursor, player.Player(2, "dgreflex", True)),
            database.add_player(self.connection, self.db_cursor, player.Player(3, "johndoe", True)),
        ]

        new_game = database.add_game(self.connection, self.db_cursor, game.Game("15.06.2001 21:00", "Chelyabinsk"))
        database.add_registration(self.connection, self.db_cursor, registration.Registration(new_players[0].id, new_game.id))
        database.add_registration(self.connection, self.db_cursor, registration.Registration(new_players[1].id, new_game.id))
        players = database.get_players_by_game_id(self.db_cursor, new_game.id)
        self.assertTrue(len(players) == 2)
        self.assertTrue(players[0].id == new_players[0].id)
        self.assertTrue(players[1].id == new_players[1].id)

    def test_get_games_by_player_id(self):
        new_player = database.add_player(self.connection, self.db_cursor, player.Player(1, "vertolet", True))
        new_games = [
            database.add_game(self.connection, self.db_cursor, game.Game("15.06.2001 21:00", "Chelyabinsk")),
            database.add_game(self.connection, self.db_cursor, game.Game("15.06.2001 22:00", "Moscow")),
            database.add_game(self.connection, self.db_cursor, game.Game("15.06.2001 23:00", "SPb")),
        ]
        database.add_registration(self.connection, self.db_cursor, registration.Registration(new_player.id, new_games[0].id))
        database.add_registration(self.connection, self.db_cursor, registration.Registration(new_player.id, new_games[1].id))
        games = database.get_games_by_player_id(self.db_cursor, new_player.id)
        self.assertTrue(len(games) == 2)
        self.assertTrue(games[0].id == new_games[0].id)
        self.assertTrue(games[1].id == new_games[1].id)


if __name__ == "__main__":
    unittest.main()

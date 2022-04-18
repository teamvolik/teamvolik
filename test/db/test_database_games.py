import datetime
import unittest
import sqlite3

import teamvolik.db.database as database
import teamvolik.classes.game as game


class DatabaseGamesTest(unittest.TestCase):
    connection: sqlite3.Connection
    db_cursor: sqlite3.Cursor

    def setUp(self) -> None:
        self.connection, self.db_cursor = database.connect(":memory:")
        database.create_tables(self.connection, self.db_cursor)

    def tearDown(self) -> None:
        self.connection.close()

    def test_game_add(self):
        database.add_game(self.connection, self.db_cursor, game.Game("15.06.2001 21:00", ""))
        self.assertTrue(len(database.get_games(self.db_cursor)) == 1)

    def test_games_should_have_unique_id(self):
        games = [
            database.add_game(self.connection, self.db_cursor, game.Game("15.06.2001 09:15", "")),
            database.add_game(self.connection, self.db_cursor, game.Game("15.06.2001 21:00", "")),
        ]
        self.assertTrue(len(database.get_games(self.db_cursor)) == 2)
        self.assertTrue(len(games) == 2)
        self.assertTrue(games[0].id != games[1].id)

    def test_get_game_by_id(self):
        new_game = database.add_game(self.connection, self.db_cursor, game.Game("15.06.2001 09:15", "Chelyabinsk"))
        game_from_db = database.get_game_by_id(self.db_cursor, new_game.id)
        self.assertTrue(game_from_db.place == new_game.place)
        self.assertTrue(game_from_db.date == new_game.date)
        non_existing_game = database.get_game_by_id(self.db_cursor, 999)
        self.assertTrue(non_existing_game.id == game.Game().id)
        self.assertTrue(non_existing_game.place == game.Game().place)
        self.assertTrue(non_existing_game.date == game.Game().date)

    def test_get_future_games(self):
        games = [game.Game(datetime.datetime(2001, 1, 1)), game.Game(datetime.datetime(3001, 1, 1))]
        games = [database.add_game(self.connection, self.db_cursor, new_game) for new_game in games]
        future_games = database.get_future_games(self.db_cursor)
        self.assertTrue(len(future_games) == 1)
        self.assertTrue(future_games[0].id == games[1].id)


if __name__ == "__main__":
    unittest.main()

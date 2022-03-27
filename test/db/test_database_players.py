import unittest
import sqlite3

import src.db.database as database
import src.classes.player as player


class DatabasePlayersTest(unittest.TestCase):
    connection: sqlite3.Connection
    db_cursor: sqlite3.Cursor

    def setUp(self) -> None:
        self.connection, self.db_cursor = database.connect(":memory:")
        database.create_tables(self.db_cursor)
        self.johndoe = player.Player(1, "John Doe", True)
        database.add_player(self.connection, self.db_cursor, self.johndoe)

    def tearDown(self) -> None:
        self.connection.close()

    def test_player_add(self):
        self.assertTrue(len(database.get_players(self.db_cursor)) == 1)

    def test_get_player_by_id(self):
        player_from_db = database.get_player_by_id(self.db_cursor, self.johndoe.id)
        self.assertTrue(player_from_db.name == self.johndoe.name)
        non_existing_player = database.get_player_by_id(self.db_cursor, 999)
        self.assertTrue(non_existing_player.id == player.Player().id)
        self.assertTrue(non_existing_player.name == player.Player().name)
        self.assertTrue(non_existing_player.is_adm == player.Player().is_adm)

    def test_remove_player_by_id(self):
        database.remove_player_by_id(self.connection, self.db_cursor, self.johndoe.id)
        self.assertTrue(len(database.get_players(self.db_cursor)) == 0)
        database.remove_player_by_id(self.connection, self.db_cursor, self.johndoe.id)


if __name__ == "__main__":
    unittest.main()

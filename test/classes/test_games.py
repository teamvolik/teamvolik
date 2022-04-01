import datetime
import unittest

import src.classes.game as game


class GamesTest(unittest.TestCase):
    def test_to_string(self):
        empty_game = game.Game()
        self.assertTrue(str(empty_game) == "Game(id=0, date=1990-01-01 00:00:00, place=UNDEFINED, max_players=8, description=)")
        another_game = game.Game(date=datetime.datetime(2001, 6, 15, 9, 15).replace(microsecond=15).timestamp())
        self.assertTrue(str(another_game) == "Game(id=0, date=2001-06-15 09:15:00, place=UNDEFINED, max_players=8, description=)")
        yet_another_game = game.Game("15.06.2001 09:15", "Chelyabinsk", 1, 4, "game")
        self.assertTrue(str(yet_another_game) == "Game(id=1, date=2001-06-15 09:15:00, place=Chelyabinsk, max_players=4, description=game)")

    def test_to_telegram_reply(self):
        some_game_with_description = game.Game("15.06.2001 09:15", "Chelyabinsk", 1, 4, "game")
        self.assertTrue(some_game_with_description.to_telegram_reply() == "2001-06-15 09:15:00\nChelyabinsk\n4\ngame")
        some_game_without_description = game.Game("15.06.2001 09:15", "Chelyabinsk", 1, 4)
        self.assertTrue(some_game_without_description.to_telegram_reply() == "2001-06-15 09:15:00\nChelyabinsk\n4")

    def test_to_sqlite_table(self):
        some_game_with_description = game.Game("15.06.2001 09:15", "Chelyabinsk", 1, 4, "game")
        self.assertTrue(some_game_with_description.to_sqlite_table() == (datetime.datetime(2001, 6, 15, 9, 15).timestamp(), "Chelyabinsk", 4, "game"))
        empty_game = game.Game()
        self.assertTrue(empty_game.to_sqlite_table() == (datetime.datetime(1990, 1, 1).timestamp(), "UNDEFINED", 8, ""))

    def test_from_sqlite_table(self):
        self.assertTrue(str(game.Game.from_sqlite_table(None)) == str(game.Game()))
        game_info = (0, datetime.datetime(1990, 1, 1, 0, 0).timestamp(), "F", 2, "F")
        self.assertTrue(str(game.Game.from_sqlite_table(game_info)) == str(game.Game("01.01.1990 00:00", "F", 0, 2, "F")))


if __name__ == "__main__":
    unittest.main()

import unittest

import teamvolik.classes.player as player


class PlayersTest(unittest.TestCase):
    def test_to_string(self):
        self.assertTrue(str(player.Player()) == "Player(id=-1, name=UNDEFINED, is_adm=False, games=0, pitch=0.0, hold=0.0, passing=0.0, movement=0.0, attacking=0.0, rating=0.0)")

    def test_to_sqlite_table(self):
        empty_player = player.Player()
        self.assertTrue(empty_player.to_sqlite_table() == (-1, "UNDEFINED", False, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))

    def test_from_sqlite_table(self):
        self.assertTrue(str(player.Player.from_sqlite_table(None)) == str(player.Player()))
        player_info = (1, "AF", True, 3, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0)
        self.assertTrue(str(player.Player.from_sqlite_table(player_info)) == str(player.Player(1, "AF", True, 3, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0)))


if __name__ == "__main__":
    unittest.main()

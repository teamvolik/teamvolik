"""Module that implements Player entity."""


class Player:
    """Class that implements player."""

    id: int
    name: str
    is_adm: bool
    games: int
    pitch: float
    hold: float
    passing: float
    movement: float
    attacking: float
    rating: float

    def __init__(
        self,
        id: int = -1,
        name: str = "UNDEFINED",
        is_adm: bool = False,
        games: int = 0,
        pitch: float = 0.0,
        hold: float = 0.0,
        passing: float = 0.0,
        movement: float = 0.0,
        attacking: float = 0.0,
        rating: float = 0.0,
    ) -> None:
        """
        Initialize Player object.

        :param id: player id
        :param name: player name
        :param is_adm: is player an admin
        :param games: number of games played by player
        :param pitch: player's pitch rating
        :param hold: player's hold rating
        :param passing: player's passing rating
        :param movement: player's movement rating
        :param attacking: player's attacking rating
        :param rating: player's general rating
        """
        self.id = id
        self.name = name
        self.is_adm = is_adm
        self.games = games
        self.pitch = pitch
        self.hold = hold
        self.passing = passing
        self.movement = movement
        self.attacking = attacking
        self.rating = rating

    def __str__(self) -> str:
        """
        Get string representation of Player object for debugging.

        :return: string of Player object
        """
        return (
            f"Player("
            f"id={self.id}, "
            f"name={self.name}, "
            f"is_adm={self.is_adm}, "
            f"games={self.games}, "
            f"pitch={self.pitch}, "
            f"hold={self.hold}, "
            f"passing={self.passing}, "
            f"movement={self.movement}, "
            f"attacking={self.attacking}, "
            f"rating={self.rating}"
            f")"
        )

    @staticmethod
    def from_sqlite_table(player_info: tuple or None) -> "Player":
        """
        Get Player object from database record.

        :param player_info: database record.
        :return: Player object
        """
        if player_info is None:
            return Player()
        else:
            return Player(*player_info)

    def to_sqlite_table(self) -> (int, str, bool, int, float, float, float, float, float, float):  # type: ignore
        """
        Get data from Player object to put it in table.

        :return: data that should be put into database
        """
        return self.id, self.name, self.is_adm, self.games, self.pitch, self.hold, self.passing, self.movement, self.attacking, self.rating

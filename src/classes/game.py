"""Module that implements Game class."""
import datetime


class Game:
    """Class that implements game."""

    id: int
    date: datetime.datetime
    place: str
    max_players: int
    description: str

    def __init__(self, date: int or datetime.datetime, place: str, id: int = 0, max_players: int = 8, description: str = "") -> None:
        """
        Initialize Game object.

        :param date: when game takes place
        :param place: where game takes place
        :param id: game id
        :param max_players: maximum number of players
        :param description: game description
        """
        self.id = id
        if isinstance(date, int):
            self.date = datetime.datetime.fromtimestamp(date)
        else:
            self.date = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M")
        self.place = place
        self.max_players = max_players
        self.description = description

    def to_sqlite_table(self) -> (float, str, int, str):  # type: ignore
        """
        Get data from Game object to put it in table.

        :return: data that should be put into database
        """
        return self.date.timestamp(), self.place, self.max_players, self.description

    def to_telegram_reply(self) -> str:
        """
        Get string for pretty output.

        :return: the string to be output in the telegram response
        """
        if self.description != "":
            return "\n".join([self.date, self.place, self.max_players, self.description])
        else:
            return "\n".join([self.date, self.place, self.max_players])

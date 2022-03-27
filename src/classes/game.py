"""Module that implements Game class."""
import datetime


class Game:
    """Class that implements game."""

    id: int
    date: datetime.datetime
    place: str
    max_players: int
    description: str

    def __init__(
        self,
        date: int or datetime.datetime or str = datetime.datetime(day=1, month=1, year=1900),
        place: str = "UNDEFINED",
        id: int = 0,
        max_players: int = 8,
        description: str = "",
    ) -> None:
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
        elif isinstance(date, str):
            self.date = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M")
        else:
            self.date = date
        self.place = place
        self.max_players = max_players
        self.description = description

    def __str__(self) -> str:
        """
        Get string representation of Game object for debugging.

        :return: string of Game object
        """
        return f"Game(id={self.id}, date={self.date}, place={self.place}, max_players={self.max_players}, description={self.description})"

    def to_sqlite_table(self) -> (float, str, int, str):  # type: ignore
        """
        Get data from Game object to put it in table.

        :return: data that should be put into database
        """
        return self.date.timestamp(), self.place, self.max_players, self.description

    @staticmethod
    def from_sqlite_table(game_info: tuple) -> "Game":
        """
        Get Game object from database record.

        :param game_info: database record.
        :return: Game object
        """
        if game_info is None:
            return Game()
        else:
            return Game(datetime.datetime.fromtimestamp(game_info[1]), game_info[2], game_info[0], game_info[3], game_info[4])

    def to_telegram_reply(self) -> str:
        """
        Get string for pretty output.

        :return: the string to be output in the telegram response
        """
        if self.description != "":
            return "\n".join([str(self.date), self.place, str(self.max_players), self.description])  # TODO Сделать более норм вывод
        else:
            return "\n".join([str(self.date), self.place, str(self.max_players)])

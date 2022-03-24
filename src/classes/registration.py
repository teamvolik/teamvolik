"""Module that implements Registration class."""
import datetime
import pytz


class Registration:
    """Class that implements registration."""

    user_id: int
    game_id: int
    is_paid: bool
    is_reserve: bool
    time: datetime.datetime

    def __init__(self, user_id: int, game_id: int, is_paid: bool = False, is_reserve: bool = False, time: int or None = None) -> None:
        """
        Initialize Registration object.

        :param user_id: id of user who has registered for game
        :param game_id: id of game
        :param is_paid: flag that shows if player has paid for a game
        :param is_reserve: flag that shows if player is in reserve
        :param time: time of registration
        """
        self.user_id = user_id
        self.game_id = game_id
        self.is_paid = is_paid
        self.is_reserve = is_reserve
        if isinstance(time, int):
            self.time = datetime.datetime.fromtimestamp(time)
        else:
            self.time = datetime.datetime.now(tz=pytz.timezone("Europe/Moscow"))

    def to_sqlite_table(self) -> (int, int, bool, bool, float):  # type: ignore
        """
        Get data from Registration object to put it in table.

        :return: data that should be put into database
        """
        return self.user_id, self.game_id, self.is_paid, self.is_reserve, self.time.timestamp()

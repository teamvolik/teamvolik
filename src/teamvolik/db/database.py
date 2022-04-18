"""Module that implements all the interactions with database."""
import sqlite3
import pytz
import datetime

import teamvolik.classes.game as game
import teamvolik.classes.player as player
import teamvolik.classes.registration as registration


DATABASE_NAME: str = "database.sqlite"


def connect(db_name: str = DATABASE_NAME) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Get all necessary sqlite objects.

    :param db_name: name of database file
    :return: a pair of necessary sqlite objects: sqlite3.Connection and sqlite3.Cursor
    """
    connection: sqlite3.Connection = sqlite3.connect(db_name)
    db_cursor: sqlite3.Cursor = connection.cursor()
    return connection, db_cursor


def create_tables(connection: sqlite3.Connection, db_cursor: sqlite3.Cursor) -> None:
    """
    Create all tables that are needed for the project.

    :param connection: database object to save changes
    :param db_cursor: cursor to interact with database
    """
    db_cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY_KEY,
            name TEXT,
            is_adm INTEGER,
            games INTEGER,
            pitch REAL,
            hold REAL,
            passing REAL,
            movement REAL,
            attacking REAL,
            rating REAL
        );
    """
    ).execute(
        """
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            date INTEGER,
            place TEXT,
            max_players INTEGER,
            description TEXT
        );
    """
    ).execute(
        """
        CREATE TABLE IF NOT EXISTS registrations (
            user_id INTEGER,
            game_id INTEGER,
            paid INTEGER,
            is_reserve INTEGER,
            reg_time INTEGER,
            FOREIGN KEY(user_id) REFERENCES players(id),
            FOREIGN KEY(game_id) REFERENCES games(id)
            PRIMARY KEY(user_id, game_id)
        );
    """
    )
    connection.commit()


# =========================================================PLAYERS======================================================
def add_player(connection: sqlite3.Connection, db_cursor: sqlite3.Cursor, new_player: player.Player) -> player.Player:
    """
    Add player to database.

    :param connection: database object to save changes
    :param db_cursor: database object to interact with database
    :param new_player: player to add to database
    """
    db_cursor.execute("""INSERT OR REPLACE INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", new_player.to_sqlite_table())
    connection.commit()
    return new_player


def get_players(db_cursor: sqlite3.Cursor) -> list[player.Player]:
    """
    Get players from database.

    :param db_cursor: database object to interact with database
    :return: All players that are present in database
    """
    players: [player.Player] = []  # type: ignore
    for player_info in db_cursor.execute("""SELECT * FROM players""").fetchall():
        players.append(player.Player.from_sqlite_table(player_info))
    return players


def get_player_by_id(db_cursor: sqlite3.Cursor, id: int) -> player.Player:
    """
    Get player by id.

    :param db_cursor: database object to interact with database
    :param id: player id
    :return: player object
    """
    db_cursor.execute("""SELECT * FROM players WHERE id = ?""", [id])
    player_info = db_cursor.fetchone()
    return player.Player.from_sqlite_table(player_info)


def remove_player_by_id(connection: sqlite3.Connection, db_cursor: sqlite3.Cursor, id: int) -> None:
    """
    Remove player from database.

    :param connection: database object to interact with database
    :param db_cursor: database object to interact with database
    :param id: id of a player that should be deleted
    :return: None
    """
    db_cursor.execute("""DELETE FROM players WHERE id = ?""", [id])
    connection.commit()


# =========================================================GAMES========================================================
def add_game(connection: sqlite3.Connection, db_cursor: sqlite3.Cursor, new_game: game.Game) -> game.Game:
    """
    Add game to database.

    :param connection: database object to save changes
    :param db_cursor: database object to interact with database
    :param new_game: game to add to database
    """
    game_info = new_game.to_sqlite_table()
    db_cursor.execute("""INSERT OR REPLACE INTO games VALUES (NULL, ?, ?, ?, ?)""", game_info)
    db_cursor.execute("""SELECT id FROM games WHERE date = ? AND place = ? AND max_players = ? AND description = ?""", game_info)
    new_game.id = db_cursor.fetchone()[0]
    connection.commit()
    return new_game


def get_games(db_cursor: sqlite3.Cursor) -> list[game.Game]:
    """
    Get games from database.

    :param db_cursor: database object to interact with database
    :return: All games that are present in database
    """
    games: [game.Game] = []  # type: ignore
    for game_info in db_cursor.execute("""SELECT * FROM games""").fetchall():
        games.append(game.Game.from_sqlite_table(game_info))
    return games


def get_future_games(db_cursor: sqlite3.Cursor) -> list[game.Game]:
    """
    Get games that will take place in the future.

    :param db_cursor: database object to interact with database
    :return: list of future games
    """
    db_cursor.execute("""SELECT * FROM games WHERE date >= ?""", [datetime.datetime.now(tz=pytz.timezone("Europe/Moscow")).timestamp()])
    game_infos = db_cursor.fetchall()
    games = []
    for game_info in game_infos:
        games.append(game.Game.from_sqlite_table(game_info))
    return games


def get_game_by_id(db_cursor: sqlite3.Cursor, id: int) -> game.Game:
    """
    Get game by game id from database.

    :param db_cursor: database object to interact with database
    :param id: game id
    :return: a game
    """
    db_cursor.execute("""SELECT * FROM games WHERE id = ?""", [id])
    game_info = db_cursor.fetchone()
    return game.Game.from_sqlite_table(game_info)


#   =======================================================REGISTRATIONS================================================
def add_registration(connection: sqlite3.Connection, db_cursor: sqlite3.Cursor, new_registration: registration.Registration) -> registration.Registration:
    """
    Add registration to database.

    :param connection: database object to save changes
    :param db_cursor: database object to interact with database
    :param new_registration: registration to add to database
    """
    db_cursor.execute("""REPLACE INTO registrations VALUES (?, ?, ?, ?, ?)""", new_registration.to_sqlite_table())
    connection.commit()
    return new_registration


def get_registrations(db_cursor: sqlite3.Cursor) -> list[registration.Registration]:
    """
    Get registrations from database.

    :param db_cursor: database object to interact with database
    :return: All registrations that are present in database
    """
    registrations: [registration.Registration] = []  # type: ignore
    for registration_info in db_cursor.execute("""SELECT * FROM registrations""").fetchall():
        registrations.append(registration.Registration.from_sqlite_table(registration_info))
    return registrations


def get_registrations_by_game_id(db_cursor: sqlite3.Cursor, game_id: int) -> list[registration.Registration]:
    """
    Get a list of registration by game id.

    :param db_cursor: database object to interact with database
    :param game_id: game id
    :return: a list of registrations
    """
    db_cursor.execute("""SELECT * FROM registrations WHERE game_id = ?""", [game_id])
    registration_infos = db_cursor.fetchall()
    registrations = []
    for registration_info in registration_infos:
        registrations.append(registration.Registration.from_sqlite_table(registration_info))
    return registrations


def get_registrations_by_player_id(db_cursor: sqlite3.Cursor, player_id: int) -> list[registration.Registration]:
    """
    Get a list of registrations by player id.

    :param db_cursor: database object to interact with database
    :param player_id: player id
    :return: a list of registrations
    """
    db_cursor.execute("""SELECT * FROM registrations WHERE user_id = ?""", [player_id])
    registration_infos = db_cursor.fetchall()
    registrations = []
    for registration_info in registration_infos:
        registrations.append(registration.Registration.from_sqlite_table(registration_info))
    return registrations


def remove_registration(connection: sqlite3.Connection, db_cursor: sqlite3.Cursor, user_id, game_id) -> None:
    """
    Remove player from the game.

    :param connection: database object to interact with database
    :param db_cursor: database object to interact with database
    :param user_id: user id
    :param game_id: game id
    :return: None
    """
    db_cursor.execute("""DELETE FROM registrations WHERE user_id = ? AND game_id = ?""", (user_id, game_id))
    connection.commit()


# ======================================================================================================================
def get_games_by_player_id(db_cursor: sqlite3.Cursor, player_id: int) -> list[game.Game]:
    """
    Get a list of current games for which the player is registered.

    :param db_cursor: database object to interact with database
    :param player_id: player id
    :return: a list of player's games that haven't finished yet
    """
    db_cursor.execute("""SELECT game_id FROM registrations WHERE user_id = ?""", [player_id])
    game_ids = [str(id[0]) for id in db_cursor.fetchall()]
    positions = f"""({", ".join(["?"] * len(game_ids))})"""
    db_cursor.execute(f"""SELECT * FROM games WHERE id IN {positions}""", game_ids)  # nosec
    game_infos = db_cursor.fetchall()
    games = []
    for game_info in game_infos:
        games.append(game.Game.from_sqlite_table(game_info))
    return games


def get_players_by_game_id(db_cursor: sqlite3.Cursor, game_id: int) -> list[player.Player]:
    """
    Get a list of players that are signed up for a game.

    :param db_cursor: database object to interact with database
    :param game_id: game id
    :return: a list of players that are signed up for a game
    """
    db_cursor.execute("""SELECT user_id FROM registrations WHERE game_id = ?""", [game_id])
    player_ids = [str(id[0]) for id in db_cursor.fetchall()]
    positions = f"""({", ".join(["?"] * len(player_ids))})"""
    db_cursor.execute(f"""SELECT * FROM players WHERE id IN {positions}""", player_ids)  # nosec
    player_infos = db_cursor.fetchall()
    players = []
    for player_info in player_infos:
        players.append(player.Player.from_sqlite_table(player_info))
    return players

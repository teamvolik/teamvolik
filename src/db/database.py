"""Module that implements all the interactions with database."""
import sqlite3

import src.classes.game as game
import src.classes.player as player
import src.classes.registration as registration

DATABASE_NAME: str = "database.sqlite"


def connect(db_name: str = DATABASE_NAME) -> (sqlite3.Connection, sqlite3.Cursor):
    """
    Get all necessary sqlite objects.

    :param db_name: name of database file
    :return: a pair of necessary sqlite objects: sqlite3.Connection and sqlite3.Cursor
    """
    connection: sqlite3.Connection = sqlite3.connect(db_name)
    db_cursor: sqlite3.Cursor = connection.cursor()
    return connection, db_cursor


def create_tables(db_cursor: sqlite3.Cursor) -> None:
    """
    Create all tables that are needed for the project.

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
        );
    """
    )


def add_player(connection: sqlite3.Connection, db_cursor: sqlite3.Cursor, player: player.Player) -> player.Player:
    """
    Add player to database.

    :param connection: database object to save changes
    :param db_cursor: database object to interact with database
    :param player: player to add to database
    """
    db_cursor.execute("""INSERT OR REPLACE INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", player.to_sqlite_table())
    connection.commit()
    return player


def add_game(connection: sqlite3.Connection, db_cursor: sqlite3.Cursor, game: game.Game) -> game.Game:
    """
    Add game to database.

    :param connection: database object to save changes
    :param db_cursor: database object to interact with database
    :param game: game to add to database
    """
    db_cursor.execute("""INSERT OR REPLACE INTO games VALUES (NULL, ?, ?, ?, ?)""", game.to_sqlite_table())
    db_cursor.execute("""SELECT max(id) FROM games""")
    game.id = db_cursor.fetchone()[0]
    connection.commit()
    return game


def add_registration(connection: sqlite3.Connection, db_cursor: sqlite3.Cursor, registration: registration.Registration) -> registration.Registration:
    """
    Add registration to database.

    :param connection: database object to save changes
    :param db_cursor: database object to interact with database
    :param registration: registration to add to database
    """
    db_cursor.execute("""REPLACE INTO registrations VALUES (?, ?, ?, ?, ?)""", registration.to_sqlite_table())
    connection.commit()
    return registration


def get_players(db_cursor: sqlite3.Cursor) -> [player.Player]:
    """
    Get players from database.

    :param db_cursor: database object to interact with database
    :return: All players that are present in database
    """
    players: [player.Player] = []
    for player_info in db_cursor.execute("""SELECT * FROM players""").fetchall():
        players.append(player.Player(*player_info))
    return players


def get_games(db_cursor: sqlite3.Cursor) -> [game.Game]:
    """
    Get games from database.

    :param db_cursor: database object to interact with database
    :return: All games that are present in database
    """
    games: [game.Game] = []
    for game_info in db_cursor.execute("""SELECT * FROM games""").fetchall():
        games.append(game.Game(*game_info))
    return games


def get_registrations(db_cursor: sqlite3.Cursor) -> [registration.Registration]:
    """
    Get registrations from database.

    :param db_cursor: database object to interact with database
    :return: All registrations that are present in database
    """
    registrations: [registration.Registration] = []
    for registration_info in db_cursor.execute("""SELECT * FROM registrations""").fetchall():
        registrations.append(registration.Registration(*registration_info))
    return registrations

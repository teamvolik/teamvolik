"""Module that implements all the interactions with database."""
import sqlite3
import pytz
import datetime

"""ВРЕМЕННАЯ МЕРА ПОКА НЕ ПРОПИШЕМ ПУТИ ЧЕРЕЗ setup.py"""
import os
import sys
sys.path.append(os.getcwd() + "/../../")
""""""

import src.classes.game as game
import src.classes.player as player
import src.classes.registration as registration


DATABASE_NAME: str = "database.sqlite"


def connect(db_name: str = DATABASE_NAME) -> (sqlite3.Connection, sqlite3.Cursor): #type: ignore
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
    game_info = game.to_sqlite_table()
    db_cursor.execute("""INSERT OR REPLACE INTO games VALUES (NULL, ?, ?, ?, ?)""", game_info)
    db_cursor.execute("""SELECT id FROM games WHERE date = ? AND place = ? AND max_players = ? AND description = ?""", game_info)
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


def get_players(db_cursor: sqlite3.Cursor) -> [player.Player]: #type: ignore
    """
    Get players from database.

    :param db_cursor: database object to interact with database
    :return: All players that are present in database
    """
    players: [player.Player] = [] #type: ignore
    for player_info in db_cursor.execute("""SELECT * FROM players""").fetchall():
        players.append(player.Player(*player_info))
    return players


def get_games(db_cursor: sqlite3.Cursor) -> [game.Game]: #type: ignore
    """
    Get games from database.

    :param db_cursor: database object to interact with database
    :return: All games that are present in database
    """
    games: [game.Game] = [] #type: ignore
    for game_info in db_cursor.execute("""SELECT * FROM games""").fetchall():
        games.append(game.Game(*game_info))
    return games


def get_registrations(db_cursor: sqlite3.Cursor) -> [registration.Registration]: #type: ignore
    """
    Get registrations from database.

    :param db_cursor: database object to interact with database
    :return: All registrations that are present in database
    """
    registrations: [registration.Registration] = [] #type: ignore
    for registration_info in db_cursor.execute("""SELECT * FROM registrations""").fetchall():
        registrations.append(registration.Registration(*registration_info))
    return registrations


def is_adm(db_cursor: sqlite3.Cursor, user_id: int) -> bool:
    """
    Return whether the user is an admin.

    :param db_cursor: database object to interact with database
    :param user_id: user id
    :return: True if the user is an admin, False otherwise
    """
    db_cursor.execute('''SELECT is_adm FROM players WHERE id = %d''' % user_id)
    return db_cursor.fetchone()[0] == 1


def player_is_registered(db_cursor: sqlite3.Cursor, user_id: int) -> bool:
    """
    Get True if the user is already registered.

    :param db_cursor: database object to interact with database
    :param user_id: user id
    :return: True if the user is sign up, False otherwise
    """
    db_cursor.execute('''SELECT count(*) FROM players WHERE id = %d''' % user_id)
    return db_cursor.fetchone()[0] >= 1


def games_find_game(db_cursor: sqlite3.Cursor, user_id: int) -> [game.Game]: #type: ignore
    """
    Get a list of current games for which the player is registered.

    :param db_cursor: database object to interact with database
    :param user_id: user id
    :return: a list of games that haven't finished yet
    """
    db_cursor.execute('''SELECT id, date, place, description, max_players FROM games WHERE date >= %d''' % datetime.now(tz=pytz.timezone('Europe/Moscow')).timestamp())
    gs = db_cursor.fetchall()

    games = []
    for g in gs:
        db_cursor.execute('''SELECT count(*) FROM registered WHERE game_id = ? AND user_id = ?''', (g[0], user_id))
        if db_cursor.fetchone()[0] == 0:
            games.append(game.Game(datetime.fromtimestamp(g[1]).strftime('%d.%m.%Y'), g[2], int(g[0]),  int(g[4]), g[3]))
    return games


def games_get_player_ids(db_cursor: sqlite3.Cursor, game_id: int) -> [int]: #type: ignore
    """
    Get a list of player ids registered for a game.

    :param db_cursor: database object to interact with database
    :param game_id: game id
    :return: a list of player ids registered for a game.
    """
    db_cursor.execute('''SELECT user_id, is_reserve FROM registered WHERE game_id = %d''' % game_id)
    ids = db_cursor.fetchall()
    return ids


def reserve_slots(db_cursor: sqlite3.Cursor, game_id: int) -> int:
    """
    Reserve slot for player.

    :param sqlite3.Cursor db_cursor: database object to interact with database
    :param int game_id: game id
    :return int: quantity of already reserved slots
    """
    db_cursor.execute('''SELECT count(*) FROM registered WHERE game_id = %d AND is_reserve = 1''' % game_id)
    return db_cursor.fetchone()[0]


def games_show_list(db_cursor: sqlite3.Cursor) -> [game.Game]: #type: ignore
    """
    Get a list of available games.

    :param db_cursor: database object to interact with database
    :param user_id: user id
    :return: a list of games that haven't finished yet
    """
    db_cursor.execute('''SELECT id, date, place, description, max_players FROM games WHERE date >= %d''' % datetime.now(tz=pytz.timezone('Europe/Moscow')).timestamp())
    gs = db_cursor.fetchall()
    games = []
    for g in gs:
        games.append(game.Game(datetime.fromtimestamp(g[1]).strftime('%d.%m.%Y'), g[2], int(g[0]),  int(g[4]), g[3]))
    return games

def players_from_ids(db_cursor: sqlite3.Cursor, ids: list) -> [str]: #type: ignore
    """
    Get a list of players registered for a game.

    :param db_cursor: database object to interact with database
    :param id: a list of ids
    :return: a list of players
    """
    players = []

    for player_id in ids:
        db_cursor.execute('''SELECT name FROM players WHERE id = %d''' % player_id[0])
        players.append([db_cursor.fetchone()[0], player_id[1]])
    return players

def player_games(db_cursor: sqlite3.Cursor, user_id: int) -> [game.Game]: #type: ignore
    """
    Get a list of games for which a player is registered.

    :param db_cursor: database object to interact with database
    :param user_id: user id
    :return: a list of games
    """
    db_cursor.execute('''SELECT game_id FROM registered where user_id = %d''' % user_id)
    game_ids = db_cursor.fetchall()
    gs = []
    for game_id in game_ids:
        db_cursor.execute('''SELECT id, date, place, description, max_players FROM games WHERE date >= ? AND id = ?''',
                       (datetime.now(tz=pytz.timezone('Europe/Moscow')).timestamp(), game_id[0]))
        gs += db_cursor.fetchall()
    games = []
    for g in gs:
        games.append(game.Game(datetime.fromtimestamp(g[1]).strftime('%d.%m.%Y'), g[2], int(g[0]),  int(g[4]), g[3]))
    return games

def remove_registration(connect, cursor, user_id, game_id) -> None:
    """
    Remove player from the game.

    :param db_cursor: database object to interact with database
    :param user_id: user id
    :param game_id: game id
    :return: None
    """
    cursor.execute('''DELETE FROM registered WHERE user_id = ? AND game_id = ?''', (user_id, game_id))
    connect.commit()
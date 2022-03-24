"""A module that implements the visual part of the bot by using ReplyKeyboardMarkup."""
from platform import platform
import sqlite3
from telegram import ReplyKeyboardMarkup

from teamvolik.teamvolik.src.classes.player import Player

"""ВРЕМЕННАЯ МЕРА ПОКА НЕ ПРОПИШЕМ ПУТИ ЧЕРЕЗ setup.py"""
import os
import sys

sys.path.append(os.getcwd() + "/../../../")
""""""

from src.db import database as db
from src.classes import game
from src.classes import player

yes_no_kb = [["Yes", "No"], ["Cancel"]]
user_menu_kb = [["Sign up for a game", "Leave the game"], ["List of games"]]
adm_menu_kb = [["Create a game"], ["Sign up for a game", "Leave the game"], ["List of games"]]
cancel_kb = [["Cancel"]]

yes_no_markup = ReplyKeyboardMarkup(yes_no_kb, resize_keyboard=True, one_time_keyboard=True)
start_markup = ReplyKeyboardMarkup([["/start"]], resize_keyboard=True, one_time_keyboard=True)
user_menu_markup = ReplyKeyboardMarkup(user_menu_kb, one_time_keyboard=True, resize_keyboard=True)
adm_menu_markup = ReplyKeyboardMarkup(adm_menu_kb, one_time_keyboard=True, resize_keyboard=True)
cancel_markup = ReplyKeyboardMarkup(cancel_kb, resize_keyboard=True, one_time_keyboard=True)


def get_perm_kb(user: player.Player) -> ReplyKeyboardMarkup:
    """
    Get the user's or administrator's keyboard, depending on the user's permissions.

    :param user: user id
    :return: ReplyKeyboardMarkup
    """
    return adm_menu_markup if user.is_adm else user_menu_markup


def get_game_kb(games: [game.Game]) -> list:  # type: ignore
    """
    Get a template for games keyboard.

    :param games: a list that contains all upcoming games
    :return: a list containing other lists that will later become buttons
    """
    games_kb = []
    for one_game in games:
        record = "[" + one_game[0] + "] " + one_game[1] + " - " + one_game[2] + " (" + one_game[3] + ") - " + one_game[4] + " players"
        games_kb.append([record])
    return games_kb


def get_game_markup(games_kb: [game.Game]) -> ReplyKeyboardMarkup:  # type: ignore
    """
    Get a keyboard containing upcoming games.

    :param games_kb: a list containing other lists that will later become buttons
    :return: ReplyKeyboardMapkup
    """
    games_kb.append(["Cancel"])
    return ReplyKeyboardMarkup(games_kb, one_time_keyboard=True, resize_keyboard=True)

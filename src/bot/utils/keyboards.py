"""A module that implements the visual part of the bot by using ReplyKeyboardMarkup."""
from telegram import ReplyKeyboardMarkup

from src.classes import game
from src.classes import player
from src.bot.utils.localization import _

yes_no_kb = [[_("Yes"), _("No")], [_("Cancel")]]
user_menu_kb = [[_("Sign up for a game"), _("Leave the game")], [_("List of games")]]
adm_menu_kb = [[_("Create a game")], [_("Sign up for a game"), _("Leave the game")], [_("List of games")]]
cancel_kb = [[_("Cancel")]]

yes_no_markup = ReplyKeyboardMarkup(yes_no_kb, resize_keyboard=True, one_time_keyboard=True)
start_markup = ReplyKeyboardMarkup([["/start"]], resize_keyboard=True, one_time_keyboard=True)
user_menu_markup = ReplyKeyboardMarkup(user_menu_kb, one_time_keyboard=True, resize_keyboard=True)
adm_menu_markup = ReplyKeyboardMarkup(adm_menu_kb, one_time_keyboard=True, resize_keyboard=True)
cancel_markup = ReplyKeyboardMarkup(cancel_kb, resize_keyboard=True, one_time_keyboard=True)


def get_perm_kb(user: player.Player) -> ReplyKeyboardMarkup:
    """
    Get the user's or administrator's keyboard, depending on the user's permissions.

    :param user: user
    :return: ReplyKeyboardMarkup
    """
    return adm_menu_markup if user.is_adm else user_menu_markup


def get_game_kb(games: list[game.Game]) -> list[list[str]]:
    """
    Get a template for games keyboard.

    :param games: a list that contains all upcoming games
    :return: a list containing other lists that will later become buttons
    """
    games_kb = []
    for one_game in games:
        record = "[" + str(one_game.id) + "] " + str(one_game.date) + " - " + one_game.place + " (" + one_game.description + ") - " + str(one_game.max_players) + " players"
        games_kb.append([record])
    return games_kb


def get_game_markup(games_kb: list[list[str]]) -> ReplyKeyboardMarkup:
    """
    Get a keyboard containing upcoming games.

    :param games_kb: a list containing other lists that will later become buttons
    :return: ReplyKeyboardMapkup
    """
    if games_kb[-1] != _("Cancel"):
        games_kb.append(_("Cancel"))
    return ReplyKeyboardMarkup(games_kb, one_time_keyboard=True, resize_keyboard=True)

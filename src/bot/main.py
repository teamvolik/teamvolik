"""The main module containing the main functionality of the bot."""
import json
import logging
import sqlite3
from datetime import datetime

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, ConversationHandler
from telegram.ext.filters import Filters

"""ВРЕМЕННАЯ МЕРА ПОКА НЕ ПРОПИШЕМ ПУТИ ЧЕРЕЗ setup.py"""
import os  # noqa E402
import sys

sys.path.append(os.getcwd() + "/../../../")
""""""

from src.db import database as db
from src.bot.utils import keyboards as kb
from src.bot.utils.reply_list import reply_list as reply
from src.classes import game
from src.classes import player
from src.classes import registration


adms = []

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get_help(update: Update, context: CallbackContext) -> None:
    """
    Get help.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: None
    """
    update.message.reply_text(reply["help"])


def cancel(update: Update, context: CallbackContext) -> int:
    """
    Cancel current operation.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: ConversationHandler.END
    """
    update.message.reply_text(reply["cancel"], reply_markup=kb.get_perm_kb(connect, cursor, update.message.chat_id))
    return ConversationHandler.END


# ==============================================================================NEW_ACCOUNT=============================
def start(update: Update, context: CallbackContext) -> int:
    """
    Start bot.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: ConversationHandler.END
    """
    if db.player_is_registered(cursor, update.message.chat_id):
        update.message.reply_text(reply["error_already_exists"], reply_markup=kb.get_perm_kb(cursor, update.message.chat_id))
        return ConversationHandler.END
    else:
        update.message.reply_text(reply["start"])
        reply_markup = ReplyKeyboardMarkup([["Ok"]], one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(reply["ask_perm"], reply_markup=reply_markup)
        return ASKED_TO_STORE_VDATA


def vdata_ask_perm(update: Update, context: CallbackContext) -> int:
    """
    Ask permission to use personal data.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    answer = update.message.text
    if answer.upper() == "OK":
        update.message.reply_text(reply["yes_permission"])
        update.message.reply_text(reply["ask_name"])
        return RECORD_NAME
    else:
        update.message.reply_text(reply["ask_perm"])
        return ASKED_TO_STORE_VDATA


def signup_success(update: Update, context: CallbackContext) -> int:
    """
    Continue the work of the bot if the registration was successful.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    name = update.message.text
    if len(name.split()) != len("Full Name".split()):
        update.message.reply_text(reply["error_wrong_name_format"])
        return RECORD_NAME
    newplayer = player.Player(update.message.chat_id, name, update.message.chat_id in adms)
    db.add_player(connect, cursor, newplayer)
    update.message.reply_text(reply["signup_success"], reply_markup=kb.adm_menu_markup if newplayer.is_adm else kb.user_menu_markup)
    return ConversationHandler.END


# ==============================================================================NEW_GAME================================
def cr_game(update: Update, context: CallbackContext) -> int:
    """
    Create a new game.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    if not db.player_is_registered(connect, cursor, update.message.chat_id):
        update.message.reply_text(reply["error_not_registered"], reply_markup=kb.start_markup)
        return ConversationHandler.END
    elif db.is_adm(connect, cursor, update.message.chat_id):
        update.message.reply_text(reply["adm_ask_date"], reply_markup=kb.cancel_markup)
        return ASKED_DATE
    else:
        update.message.reply_text(reply["no_access"], reply_markup=kb.user_menu_markup)
        return ConversationHandler.END


def cr_get_date(update: Update, context: CallbackContext) -> int:
    """
    Enter a date to create a new game.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    date = update.message.text
    try:
        datetime.strptime(date, "%d.%m.%Y")
    except ValueError:
        update.message.reply_text(reply["error_wrong_data_format"], reply_markup=kb.cancel_markup)
        return ASKED_DATE
    context.chat_data["date"] = date
    update.message.reply_text(reply["adm_ask_place"], reply_markup=kb.cancel_markup)
    return ASKED_PLACE


def cr_get_place(update: Update, context: CallbackContext) -> int:
    """
    Enter a place to create a new game.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    place = update.message.text
    context.chat_data["place"] = place
    update.message.reply_text(reply["adm_ask_players_num"], reply_markup=kb.cancel_markup)
    return ASKED_PLAYERS


def cr_get_players_num(update: Update, context: CallbackContext) -> int:
    """
    Enter a quantity of players to create a new game.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    num = update.message.text
    if num.isdigit() and int(num) > 0:
        context.chat_data["players_num"] = num
        update.message.reply_text(reply["adm_ask_description"], reply_markup=kb.cancel_markup)
        return ASKED_DESCRIPTION
    else:
        update.message.reply_text(reply["error_wrong_players_num_format"], reply_markup=kb.cancel_markup)
        return ASKED_PLAYERS


def cr_get_description(update: Update, context: CallbackContext) -> int:
    """
    Enter a description (optional) of players to create a new game.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    description = update.message.text
    context.chat_data["description"] = description
    reply_text = context.chat_data["date"] + "\n" + context.chat_data["place"] + "\n" + context.chat_data["players_num"]
    if description != "":
        reply_text += "\n" + description
    update.message.reply_text(reply_text)
    update.message.reply_text(reply["adm_ask_to_check"], reply_markup=kb.yes_no_markup)
    return ASKED_TO_CHECK


def cr_finish(update: Update, context: CallbackContext) -> int:
    """
    Finish creating the game.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    answer = update.message.text
    if answer.upper() == "YES":
        global connect
        global cursor
        newgame = game.Game(context.chat_data["date"], context.chat_data["place"], 0, context.chat_data["players_num"], context.chat_data["description"])
        db.add_game(connect, cursor, newgame)
        update.message.reply_text(reply["adm_game_created"], reply_markup=kb.adm_menu_markup)
        return ConversationHandler.END
    elif answer.upper() == "NO":
        update.message.reply_text(reply["adm_ask_date"], reply_markup=kb.cancel_markup)
        return ASKED_DATE
    else:
        update.message.reply_text(newgame.to_telegram_reply())
        update.message.reply_text(reply["adm_ask_to_check"], reply_markup=kb.yes_no_markup)
        return ASKED_TO_CHECK


# ==============================================================================REG_FOR_A_GAME==========================
def reg_game(update: Update, context: CallbackContext) -> int:
    """
    User registration for the game.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    if not db.player_is_registered(cursor, update.message.chat_id):
        update.message.reply_text(reply["error_not_registered"], reply_markup=kb.start_markup)
        return ConversationHandler.END
    games = db.games_find_game(cursor, update.message.chat_id)
    if len(games) == 0:
        update.message.reply_text(reply["no_games_yet"], reply_markup=kb.get_perm_kb(cursor, update.message.chat_id))
        return ConversationHandler.END
    games_kb = kb.get_game_kb(games)
    context.chat_data["game_list"] = games_kb
    update.message.reply_text(reply["reg_ask_game"], reply_markup=kb.get_game_markup(games_kb))
    return ASKED_GAME


def reg_accept(update: Update, context: CallbackContext) -> int:  # TODO переделать в более человеческий формат с помощью ооп
    """
    Confirm registration and check number of free slots.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    reply = update.message.text
    games_list = context.chat_data["game_list"]
    if [reply] not in games_list:
        update.message.reply_text(reply["error_wrong_game_chosen"], reply_markup=kb.get_game_markup(games_list))
        return ASKED_GAME
    game_id = int(reply.split("]")[0][1:])  # ???
    player_id = update.message.chat_id  # ???
    max_players = int(reply.split(") - ")[1].split()[0])  # ???
    if len(db.games_get_player_ids(cursor, game_id)) >= max_players:
        context.chat_data["game_id"] = game_id
        update.message.reply_text(reply["reg_ask_reserve"], reply_markup=kb.yes_no_markup)
        return ASKED_ABOUT_RESERVE
    else:
        newreg = registration.Registration(player_id, game_id, False)  # TODO допилить оплачиваемые игры, в т.ч. прикрутить платежку
        db.add_registration(connect, cursor, newreg)
        update.message.reply_text(reply["reg_success"], reply_markup=kb.get_perm_kb(cursor, player_id))
    return ConversationHandler.END


def reg_added_to_reserve(update: Update, context: CallbackContext) -> int:
    """
    Confirm reservation.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    reply = update.message.text
    newreg = registration.Registration(update.message.chat_id, context.chat_data["game_id"], False, True)  # TODO
    if reply.upper() == "YES":
        db.add_registration(connect, cursor, newreg)
        reserved_slots = db.reserve_slots(cursor, newreg.game_id)
        update.message.reply_text(reply["reg_success"] + "\n" + "Your position in the queue:" + str(reserved_slots), reply_markup=kb.get_perm_kb(cursor, update.message.chat_id))
        return ConversationHandler.END
    elif reply.upper() == "NO":
        update.message.reply_text(reply["reg_canceled"], reply_markup=kb.get_perm_kb(cursor, newreg.user_id))
        return ConversationHandler.END
    else:
        update.message.reply_text(reply["error_sayitagain"], reply_markup=kb.yes_no_markup)
        return ASKED_ABOUT_RESERVE


# ==============================================================================SHOW_GAMES==============================
def games_show_available_list(update: Update, context: CallbackContext) -> int:
    """
    Show available games.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    if not db.player_is_registered(cursor, update.message.chat_id):
        update.message.reply_text(reply["error_not_registered"], reply_markup=kb.start_markup)
        return ConversationHandler.END
    games = db.games_show_list(connect, cursor)
    if len(games) == 0:
        update.message.reply_text(reply["no_games_yet"], reply_markup=kb.get_perm_kb(cursor, update.message.chat_id))
        return ConversationHandler.END
    games_kb = kb.get_game_kb(games)
    context.chat_data["game_list"] = games_kb
    update.message.reply_text(reply["games_get_players"], reply_markup=kb.get_game_markup(games_kb))
    return ASKED_PLAYERS_LIST


def games_show_players(update: Update, context: CallbackContext) -> int:
    """
    Show players participating in the game.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    reply = update.message.text
    games_list = context.chat_data["game_list"]
    if [reply] not in games_list:
        update.message.reply_text(reply["error_wrong_game_chosen"], reply_markup=kb.get_game_markup(games_list))
        return ASKED_PLAYERS_LIST
    game_id = int(reply.split("]")[0][1:])  # ???????????
    player_ids = db.games_get_player_ids(cursor, game_id)
    if len(player_ids) == 0:
        if db.is_adm(cursor, update.message.chat_id):
            update.message.reply_text(reply["no_players_yet"], reply_markup=kb.adm_menu_markup)
        else:
            update.message.reply_text(reply["no_players_yet"], reply_markup=kb.user_menu_markup)
        return ConversationHandler.END
    players = db.players_from_ids(cursor, player_ids)
    players_msg = reply["games_player_list"]
    counter = 0
    reserve_counter = 0
    for one_player in players:
        if one_player[1] == 0:
            counter += 1
            players_msg += "\n" + str(counter) + ". " + one_player[0]
        if one_player[1] == 1:
            reserve_counter += 1
            players_msg += "\n" + "Р" + str(reserve_counter) + ". " + one_player[0]
    if db.is_adm(connect, cursor, update.message.chat_id):
        update.message.reply_text(players_msg, reply_markup=kb.adm_menu_markup)
    else:
        update.message.reply_text(players_msg, reply_markup=kb.user_menu_markup)
    return ConversationHandler.END


# ==============================================================================LEAVE_GAME==============================
def leave_game(update: Update, context: CallbackContext) -> int:
    """
    Remove a player from a game.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    if not db.player_is_registered(connect, cursor, update.message.chat_id):
        update.message.reply_text(reply["error_not_registered"], reply_markup=kb.start_markup)
        return ConversationHandler.END
    games = db.player_games(cursor, update.message.chat_id)
    if len(games) == 0:
        update.message.reply_text(reply["no_games_yet"], reply_markup=kb.get_perm_kb(cursor, update.message.chat_id))
        return ConversationHandler.END
    games_kb = kb.get_game_kb(games)
    context.chat_data["game_list"] = games_kb
    update.message.reply_text(reply["choose_game_to_leave"], reply_markup=kb.get_game_markup(games_kb))
    return ASKED_GAME_TO_LEAVE


def leave_success(update: Update, context: CallbackContext) -> int:
    """
    Remove a player from a game end with success.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    reply = update.message.text
    games_list = context.chat_data["game_list"]
    if [reply] not in games_list:
        update.message.reply_text(reply["error_wrong_game_chosen"], reply_markup=kb.get_game_markup(games_list))
        return ASKED_PLAYERS_LIST
    game_id = int(reply.split("]")[0][1:])  # ????
    db.remove_registration(connect, cursor, update.message.chat_id, game_id)
    update.message.reply_text(reply["left_game"], reply_markup=kb.get_perm_kb(cursor, update.message.chat_id))
    #    new_player_id = db.games_get_reserve(connect, cursor, game_id)
    #    context.bot.send_message(db.games_get_reserve(connect, cursor, new_player_id),
    #                             reply['reg_from_reserve_to_active'])
    return ConversationHandler.END


# =============================================================================MAIN=====================================
(
    ASKED_TO_STORE_VDATA,
    RECORD_NAME,
    ASKED_DATE,
    ASKED_PLACE,
    ASKED_PLAYERS,
    ASKED_DESCRIPTION,
    ASKED_TO_CHECK,
    ASKED_GAME,
    ASKED_PLAYERS_LIST,
    ASKED_GAME_TO_LEAVE,
    ASKED_ABOUT_RESERVE,
) = range(11)


def main() -> None:
    """
    Start the bot.

    :return: None
    """
    with open("config.json", "r") as f:
        config = json.loads(f.read())
    updater = Updater(config["token"])
    dispatcher = updater.dispatcher

    global adms
    adms = config["admins"]
    global connect
    connect = sqlite3.connect(config["db_fname"], check_same_thread=False)
    global cursor
    cursor = connect.cursor()
    db.create_dbs(connect, cursor)

    base_filter = Filters.text & ~Filters.regex(r"Cancel")

    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex(r"Create game"), cr_game),
            CommandHandler("start", start),
            MessageHandler(Filters.regex(r"Sign up for a game"), reg_game),
            MessageHandler(Filters.regex(r"List of games"), games_show_available_list),
            MessageHandler(Filters.regex(r"Leave the game"), leave_game),
        ],
        states={
            ASKED_DATE: [MessageHandler(base_filter, cr_get_date)],
            ASKED_PLACE: [MessageHandler(base_filter, cr_get_place)],
            ASKED_PLAYERS: [MessageHandler(base_filter, cr_get_players_num)],
            ASKED_DESCRIPTION: [MessageHandler(base_filter, cr_get_description)],
            ASKED_TO_CHECK: [MessageHandler(base_filter, cr_finish)],
            ASKED_TO_STORE_VDATA: [MessageHandler(base_filter, vdata_ask_perm)],
            RECORD_NAME: [
                MessageHandler(base_filter, signup_success),
            ],
            ASKED_GAME: [
                MessageHandler(base_filter, reg_accept),
            ],
            ASKED_PLAYERS_LIST: [MessageHandler(base_filter, games_show_players)],
            ASKED_GAME_TO_LEAVE: [MessageHandler(base_filter, leave_success)],
            ASKED_ABOUT_RESERVE: [MessageHandler(base_filter, reg_added_to_reserve)],
        },
        fallbacks=[MessageHandler(Filters.regex(r"Cancel"), cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

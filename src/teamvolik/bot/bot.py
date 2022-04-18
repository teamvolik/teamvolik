"""The main module containing the main functionality of the bot."""
import json
import locale
import logging
import os
import sqlite3

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, ConversationHandler
from telegram.ext.filters import Filters

from teamvolik.db import database as db
from teamvolik.bot.utils import keyboards as kb
from teamvolik.bot.utils.reply_list import reply_list as reply
from teamvolik.classes import registration, player, game
from teamvolik.bot.utils.localization import _


adms = []

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)


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
    user: player.Player = db.get_player_by_id(cursor, update.message.chat_id)
    update.message.reply_text(reply["cancel"], reply_markup=kb.get_perm_kb(user))
    return ConversationHandler.END


# ==============================================================================NEW_ACCOUNT=============================
def start(update: Update, context: CallbackContext) -> int:
    """
    Start bot.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: ConversationHandler.END
    """
    user: player.Player = db.get_player_by_id(cursor, update.message.chat_id)
    if user.id >= 0:
        update.message.reply_text(reply["error_already_exists"], reply_markup=kb.get_perm_kb(user))
        return ConversationHandler.END
    else:
        update.message.reply_text(reply["start"])
        update.message.reply_text(reply["ask_perm"], reply_markup=ReplyKeyboardMarkup([[_("Ok")]], one_time_keyboard=True, resize_keyboard=True))
        return ASKED_TO_STORE_VDATA


def vdata_ask_perm(update: Update, context: CallbackContext) -> int:
    """
    Ask permission to use personal data.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    answer: str = update.message.text
    if answer.upper() == (_("Ok")).upper():
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
    name: str = update.message.text
    srv_locale: tuple[str | None, str | None] = locale.getdefaultlocale()
    if srv_locale[0] == "ru" or srv_locale[0] == "ru_RU":
        if len(name.split()) != len("Ф И О".split()):
            update.message.reply_text(reply["error_wrong_name_format"])
            return RECORD_NAME
    else:
        if len(name.split()) != len("Full Name".split()):
            update.message.reply_text(reply["error_wrong_name_format"])
            return RECORD_NAME

    newuser: player.Player = player.Player(update.message.chat_id, name, update.message.chat_id in adms)
    db.add_player(connect, cursor, newuser)
    update.message.reply_text(reply["signup_success"], reply_markup=kb.get_perm_kb(newuser))
    return ConversationHandler.END


# ==============================================================================NEW_GAME================================
def cr_game(update: Update, context: CallbackContext) -> int:
    """
    Create a new game.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    user: player.Player = db.get_player_by_id(cursor, update.message.chat_id)
    if user.id < 0:
        update.message.reply_text(reply["error_not_registered"], reply_markup=kb.start_markup)
        return ConversationHandler.END
    elif user.is_adm:
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
    date: str = update.message.text
    newgame: game.Game = game.Game(date=date)

    # try:
    #     datetime.strptime(date, "%d.%m.%Y")
    # except ValueError:
    #     update.message.reply_text(reply["error_wrong_data_format"], reply_markup=kb.cancel_markup)
    #     return ASKED_DATE

    context.chat_data["newgame"] = newgame
    update.message.reply_text(reply["adm_ask_place"], reply_markup=kb.cancel_markup)
    return ASKED_PLACE


def cr_get_place(update: Update, context: CallbackContext) -> int:
    """
    Enter a place to create a new game.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    place: str = update.message.text

    context.chat_data["newgame"].place = place
    update.message.reply_text(reply["adm_ask_players_num"], reply_markup=kb.cancel_markup)
    return ASKED_PLAYERS


def cr_get_players_num(update: Update, context: CallbackContext) -> int:
    """
    Enter a quantity of players to create a new game.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    num: str = update.message.text

    if num.isdigit() and int(num) > 0:
        context.chat_data["newgame"].max_players = int(num)
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
    description: str = update.message.text

    context.chat_data["newgame"].description = description
    update.message.reply_text(context.chat_data["newgame"].to_telegram_reply())
    update.message.reply_text(reply["adm_ask_to_check"], reply_markup=kb.yes_no_markup)
    return ASKED_TO_CHECK


def cr_finish(update: Update, context: CallbackContext) -> int:
    """
    Finish creating the game.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    answer: str = update.message.text
    newgame: game.Game = context.chat_data["newgame"]
    user: player.Player = db.get_player_by_id(cursor, update.message.chat_id)

    if answer.upper() == (_("Yes")).upper():
        db.add_game(connect, cursor, newgame)
        update.message.reply_text(reply["adm_game_created"], reply_markup=kb.get_perm_kb(user))
        return ConversationHandler.END
    elif answer.upper() == (_("No")).upper():
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
    user: player.Player = db.get_player_by_id(cursor, update.message.chat_id)
    games: list[game.Game] = db.get_future_games(cursor)
    user_games: list[int] = list(map(lambda x: x.game_id, db.get_registrations_by_player_id(cursor, user.id)))

    if user.id < 0:
        update.message.reply_text(reply["error_not_registered"], reply_markup=kb.start_markup)
        return ConversationHandler.END

    games = list(filter(lambda x: x.id not in user_games, games))

    if len(games) == 0:
        update.message.reply_text(reply["no_games_yet"], reply_markup=kb.get_perm_kb(user))
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
    answer: str = update.message.text
    games_list: list[str] = context.chat_data["game_list"]
    user: player.Player = db.get_player_by_id(cursor, update.message.chat_id)
    chosen_game: game.Game

    if [answer] not in games_list:
        update.message.reply_text(reply["error_wrong_game_chosen"], reply_markup=kb.get_game_markup(games_list))
        return ASKED_GAME

    game_id = int(answer.split("]")[0][1:])
    chosen_game = db.get_game_by_id(cursor, game_id)

    if len(db.get_players_by_game_id(cursor, chosen_game.id)) >= chosen_game.max_players:
        context.chat_data["chosen_game"] = chosen_game
        update.message.reply_text(reply["reg_ask_reserve"], reply_markup=kb.yes_no_markup)
        return ASKED_ABOUT_RESERVE
    else:
        newreg = registration.Registration(user.id, chosen_game.id)  # TODO допилить оплачиваемые игры, в т.ч. прикрутить платежку
        db.add_registration(connect, cursor, newreg)
        update.message.reply_text(reply["reg_success"], reply_markup=kb.get_perm_kb(user))
    return ConversationHandler.END


def reg_added_to_reserve(update: Update, context: CallbackContext) -> int:
    """
    Confirm reservation.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    answer: str = update.message.text
    user: player.Player = db.get_player_by_id(cursor, update.message.chat_id)
    chosen_game: game.Game = context.chat_data["chosen_game"]
    newreg: registration.Registration = registration.Registration(user.id, chosen_game.id, is_reserve=True)  # TODO

    if answer.upper() == (_("Yes")).upper():
        db.add_registration(connect, cursor, newreg)
        reserved_slots: int = len(list(filter(lambda x: x.is_reserve, db.get_registrations_by_game_id(cursor, chosen_game.id))))
        update.message.reply_text(reply["reg_success"] + "\n" + "Your position in the queue:" + str(reserved_slots), reply_markup=kb.get_perm_kb(user))
        return ConversationHandler.END
    elif answer.upper() == (_("No")).upper():
        update.message.reply_text(reply["reg_canceled"], reply_markup=kb.get_perm_kb(user))
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
    user: player.Player = db.get_player_by_id(cursor, update.message.chat_id)
    games: list[game.Game] = db.get_future_games(cursor)

    if user.id < 0:
        update.message.reply_text(reply["error_not_registered"], reply_markup=kb.start_markup)
        return ConversationHandler.END

    if len(games) == 0:
        update.message.reply_text(reply["no_games_yet"], reply_markup=kb.get_perm_kb(user))
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
    user: player.Player = db.get_player_by_id(cursor, update.message.chat_id)
    answer: str = update.message.text
    games_kb: list[str] = context.chat_data["game_list"]
    chosen_game: game.Game

    if [answer] not in games_kb:
        update.message.reply_text(reply["error_wrong_game_chosen"], reply_markup=kb.get_game_markup(games_kb))
        return ASKED_PLAYERS_LIST

    game_id = int(answer.split("]")[0][1:])
    chosen_game = db.get_game_by_id(cursor, game_id)
    players_in_chosen_game: list[registration.Registration] = db.get_registrations_by_game_id(cursor, chosen_game.id)

    if len(players_in_chosen_game) == 0:
        update.message.reply_text(reply["no_players_yet"], reply_markup=kb.get_perm_kb(user))
        return ConversationHandler.END

    players_msg: str = ""
    players_msg_reserve: str = ""  # TODO НОРМ ОБРАБОТКУ ОЧЕРЕДЕЙ РЕЗЕРВАЦИИ
    counter = 0
    reserve_counter = 0
    for one_player in players_in_chosen_game:
        if one_player.is_reserve:
            reserve_counter += 1
            players_msg_reserve += "\n" + str(reserve_counter) + ". " + db.get_player_by_id(cursor, one_player.user_id).name
        else:
            counter += 1
            players_msg += "\n" + str(counter) + ". " + db.get_player_by_id(cursor, one_player.user_id).name

    res_reply = reply["games_player_list"] + players_msg
    if players_msg_reserve != "":
        res_reply += "\n\n" + reply["games_reserve_list"] + players_msg_reserve

    update.message.reply_text(res_reply, reply_markup=kb.get_perm_kb(user))
    return ConversationHandler.END


# ==============================================================================LEAVE_GAME==============================
def leave_game(update: Update, context: CallbackContext) -> int:
    """
    Remove a player from a game.

    :param ``update``: This class, which employs the ``telegram.ext.Dispatcher``, provides a frontend to ``telegram.Bot`` to the programmer.
    :param ``context``: This is a context object passed to the callback called by ``telegram.ext.Handler`` or by the ``telegram.ext.Dispatcher``.
    :return: int
    """
    user: player.Player = db.get_player_by_id(cursor, update.message.chat_id)
    user_games: list[game.Game] = db.get_games_by_player_id(cursor, user.id)

    if user.id < 0:
        update.message.reply_text(reply["error_not_registered"], reply_markup=kb.start_markup)
        return ConversationHandler.END

    if len(user_games) == 0:
        update.message.reply_text(reply["no_games_yet"], reply_markup=kb.get_perm_kb(user))
        return ConversationHandler.END
    games_kb: list[str] = kb.get_game_kb(user_games)
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
    user: player.Player = db.get_player_by_id(cursor, update.message.chat_id)
    answer: str = update.message.text
    games_kb: list[str] = context.chat_data["game_list"]
    chosen_games: game.Game

    if [answer] not in games_kb:
        update.message.reply_text(reply["error_wrong_game_chosen"], reply_markup=kb.get_game_markup(games_kb))
        return ASKED_PLAYERS_LIST

    game_id: int = int(answer.split("]")[0][1:])
    chosen_games = db.get_game_by_id(cursor, game_id)

    db.remove_registration(connect, cursor, user.id, chosen_games.id)
    update.message.reply_text(reply["left_game"], reply_markup=kb.get_perm_kb(user))
    # TODO допилить резервацию
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


def start_bot() -> None:
    """
    Start the bot.

    :return: None
    """
    CONFIG_FOLDER = os.path.join("teamvolik", "userdata")
    CONFIG_FNAME = "config.json"
    CONFIG_PATH = os.path.join(CONFIG_FOLDER, CONFIG_FNAME)
    if os.path.exists(CONFIG_PATH):
        logger.debug(f"Found config.json with path: {CONFIG_PATH}")
        with open(CONFIG_PATH, "r") as f:
            config = json.loads(f.read())
    else:
        logger.error(f"No config.json file found. Creating {CONFIG_PATH}. Configure it and run bot again.")
        os.makedirs(CONFIG_FOLDER)
        new_config = open(CONFIG_PATH, "w")
        new_config.writelines(["{\n", '  "token":  "<YOUR-TELEGRAM-TOKEN>",\n', '  "admins": [<ADMIN-ID-1>, ...],\n', '  "db_fname":  "DATABASE-FILENAME"\n', "}\n"])
        new_config.close()
        exit(0)
    updater = Updater(config["token"])
    dispatcher = updater.dispatcher

    global adms
    adms = config["admins"]
    global connect
    connect = sqlite3.connect(config["db_fname"], check_same_thread=False)
    global cursor
    cursor = connect.cursor()
    db.create_tables(connect, cursor)

    base_filter = Filters.text & ~Filters.regex(_("Cancel"))

    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex(_("Create a game")), cr_game),
            CommandHandler("start", start),
            MessageHandler(Filters.regex(_("Sign up for a game")), reg_game),
            MessageHandler(Filters.regex(_("List of games")), games_show_available_list),
            MessageHandler(Filters.regex(_("Leave the game")), leave_game),
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
        fallbacks=[MessageHandler(Filters.regex(_("Cancel")), cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

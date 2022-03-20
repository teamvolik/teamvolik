#!/usr/bin/env python3.10

import logging
import json
from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    Filters,
)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(rf"Hi {user.mention_markdown_v2()}\!", reply_markup=ForceReply(selective=True))


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("This is an echo bot that duplicates all messages sent to it.\nTo start working with the bot, type /start")


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    config_path = "config.json"
    with open(config_path, "r") as config_file:
        config = json.loads(config_file.read())

    # Create the Updater to connect program with tg bot via token
    updater = Updater(config["token"])

    # Get the dispatcher to register handlers on it
    dispatcher = updater.dispatcher

    # Binding commands to the dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Binding echo function to the dispatcher to echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()

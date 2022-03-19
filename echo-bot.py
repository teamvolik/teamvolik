#!/usr/bin/env python3.8

import logging
import json
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True)
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("This is an echo bot that duplicates all messages sent to it.\n\
                               To start working with the bot, type /start")

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    pass

def main() -> None:
    """Start the bot."""
    pass

if __name__ == "__main__":
    pass
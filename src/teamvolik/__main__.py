"""Main teamvolikbot module."""
import logging
import os

from .bot.bot import start_bot


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    TEAMVOLIK_DIR = os.path.join(os.path.expanduser("~"), ".teamvolik")
    if not os.path.exists(os.path.join(TEAMVOLIK_DIR)):
        os.mkdir(TEAMVOLIK_DIR)
    CONFIG_FNAME = "config.json"
    CONFIG_PATH = os.path.join(TEAMVOLIK_DIR, CONFIG_FNAME)
    if os.path.exists(CONFIG_PATH):
        logger.debug(f"Found config.json with path: {CONFIG_PATH}")
        with open(CONFIG_PATH, "r") as f:
            raw_config = f.read()
        if "<YOUR-TELEGRAM-TOKEN>" in raw_config:
            logger.error(f"Please update config.json with path {CONFIG_PATH}")
            exit(-1)
    else:
        logger.error(f"No config.json file found. Creating {CONFIG_PATH}. Configure it and run bot again.")
        new_config = open(CONFIG_PATH, "w")
        new_config.writelines(["{\n", '  "token": "<YOUR-TELEGRAM-TOKEN>",\n', '  "admins": [<ADMIN-ID-1>, ...],\n', '  "db_fname": "DATABASE-FILENAME"\n', "}\n"])
        new_config.close()
        exit(0)
    start_bot(CONFIG_PATH, TEAMVOLIK_DIR)

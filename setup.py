"""Script for deployment."""
from setuptools import setup

import versioneer

setup(
    name="teamvolik",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=["teamvolik", "teamvolik.db", "teamvolik.bot", "teamvolik.bot.utils", "teamvolik.classes"],
    package_dir={"teamvolik": "src/teamvolik"},
    package_data={
        "teamvolik": ["localization/ru/LC_MESSAGES/bot.mo"],
    },
    url="https://github.com/teamvolik/teamvolik",
    license="MIT",
    author="sanyavertolet, dgreflex",
    author_email="sanya-vertolet@yandex.ru",
    description="Telegram bot for signing up for volleyball games.",
    install_requires=[
        "python-telegram-bot==13.11",
        "pytz==2022.1",
    ],
)

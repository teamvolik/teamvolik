"""Script for deployment."""
from setuptools import setup
from babel.messages import frontend as babel

setup(
    name="teamvolik",
    version="0.1.1",
    packages=["teamvolik", "teamvolik.db", "teamvolik.bot", "teamvolik.bot.utils", "teamvolik.classes"],
    package_dir={"teamvolik": "src/teamvolik"},
    package_data={
        "teamvolik": ["localization/ru/LC_MESSAGES/bot.po"],
    },
    cmdclass={
        "compile_catalog": babel.compile_catalog,
    },
    url="https://github.com/teamvolik/teamvolik",
    license="MIT",
    author="sanyavertolet, dgreflex",
    author_email="sanya-vertolet@yandex.ru",
    description="Telegram bot for signing up for volleyball games.",
)

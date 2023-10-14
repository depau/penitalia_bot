from setuptools import setup

setup(
    name='penitaliabot',
    version='0.1',
    packages=['penitaliabot'],
    url='https://github.com/depau/penitalia_bot/',
    license='',
    author='Davide Depau',
    author_email='davide@depau.eu',
    description='A Telegram bot that speaks messages using the Windows TTS API',
    install_requires=["python-telegram-bot", "aiohttp", "quart", "redis", "hypercorn"],
    entry_points={
        'console_scripts': ['penitaliabot=penitaliabot.bot:main'],
    }
)

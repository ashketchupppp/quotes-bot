FROM python:3.8-buster

RUN python -m pip install discord
RUN python -m pip install pymongo 

COPY . /discord-bot

ENTRYPOINT ["/discord-bot/scripts/start_bot.sh"]

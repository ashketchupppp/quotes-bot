FROM python:3.8-buster

RUN python pip install discord
RUN python pip install pymongo 

COPY . /discord-bot

ENTRYPOINT ["/discord-bot/scripts/start_bot.sh"]

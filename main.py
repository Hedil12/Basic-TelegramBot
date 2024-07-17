import telebot
from constant import API_key_tele as token
from Handle_respond import TelegramBot, HandleResponse
from Handle_Quiz_Topic import Quiz, Topic
import json

class Running(HandleResponse, Quiz, Topic):
    def __init__(self, token):
        super().__init__(token)
        
if __name__ == '__main__':
    bot = Running(token)
    bot.register_simple_handlers()
    bot.load_topics()
    bot.load_egs()
    bot.Topic_Menu()
    bot.load_questions()
    bot.Quiz_Menu()
    bot.run()
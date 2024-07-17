from telebot import types
from constant import API_key_tele as token
import random as r, telebot
import json


class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token, parse_mode=None)
        self.menu = None
    
    def load_questions(self):
        # Load and read QnA.json
        with open('QnA.json', 'r', encoding='utf-8') as q:
            self.qna = json.load(q)
            self.question = self.qna[0]['Topics']
    
    def load_topics(self):
        # Load and read topics.json
        with open('topics.json','r') as t:
            self.menu = json.loads(t.read())
            self.topics = self.menu[0]['intro']
    
    def load_egs(self):
        # Load and read T&E.json
        with open('TnE.json','r', encoding='utf-8') as te:
            self.tne = json.load(te)
            self.eg = self.tne[0]['T&E']

    def register_simple_handlers(self,message):
        pass
    
    def Topic_Menu(self,message):
        pass

    def Quiz_Menu(self,message):
        pass

    def run(self):
        self.bot.polling()

class HandleResponse(TelegramBot):
    def __init__(self, token):
        super().__init__(token)

    def register_simple_handlers(self):
        # Command handlers
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            command_help:list = ['Hello, welcome to LearnPy!','Commands:\n','/help for the commands','/topic to select topic of choice:','/quiz for selected topic quiz']
            output = '\n'.join(command_help)
            self.bot.send_message(message.chat.id, output)

        # Text message handlers
        @self.bot.message_handler(func=lambda message: message.text.lower() in ['hello', 'hi', 'hey'])
        def handle_hello(message):
            self.bot.send_message(message.chat.id, 'Hi there!')

        # List to respond to the user when ask for help
        Help_response:list = [
                        'How can I assist?',
                        'Here are the series of commands that you are able to access:\n',
                        '/help for the commands',
                        '/topic: Shows a series of topics to chose from','/quiz for selected topic quiz'
                     ]

        @self.bot.message_handler(commands=['help'])
        def handle_help(message):
            #print out using string format
            output = '\n'.join(Help_response)
            self.bot.send_message(message.chat.id, output)


        # List of possible reply from user
        Ty_user:list = ['thanks', 'thank you', 'tyvm', 'tysm', 'thnks', 'thx']
        #message_handler func will handle the list and will reply using range
        @self.bot.message_handler(func=lambda message: message.text.lower() in Ty_user)
        def handle_thank(message):
            # List of poss
            Ty_response:list = ['No problem! :D', "You're welcome! :]", 'My pleasure! :3']
            random_response = Ty_response[r.randint(0, len(Ty_response) - 1)]
            self.bot.send_message(message.chat.id, random_response)

        # Oi message handler
        @self.bot.message_handler(func=lambda message: message.text.lower() == 'oi')
        def handle_help(message):
            self.bot.send_message(message.chat.id, 'What lah')

        # Sticker message handler
        @self.bot.message_handler(content_types=['sticker'])
        def handle_sticker(message):
            self.bot.send_message(message.chat.id, "Errrr idk what you said")
        
        # Goodbye message handler
        #list of probable commands the user might input
        bye_user:list = ['bye','goodbye','bai','cya','take care','see you']
        #message_handler func will handle the list and will reply using range
        @self.bot.message_handler(func=lambda message: message.text.lower() in bye_user)
        def handle_bye(message):
            self.bot.send_message(message.chat.id, "Bye!")



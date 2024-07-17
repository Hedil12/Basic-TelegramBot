from telebot import types
from constant import API_key_tele as token
from Handle_respond import TelegramBot, HandleResponse
import random as r, telebot
import telebot
import json

class Quiz(TelegramBot):
    def __init__(self, token):
        super().__init__(token)
        super().load_questions()

    def Quiz_Menu(self):
        @self.bot.message_handler(commands=["quiz"])
        def Quizmenu(message):
            print('in_quiz_menu')
            # Send the welcome message
            self.bot.send_message(message.chat.id, "Welcome to the Python Quiz Bot! Please select a topic:")

            # Create the keyboard
            keyboard_qn = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

            
            # Add the topic names to the keyboard
            for topic_qn in self.question:
                    keyboard_qn.add(telebot.types.KeyboardButton(topic_qn["Name"]))
            print('Access List')
            print(message)

            # Add the "End" button to the keyboard
            keyboard_qn.add(telebot.types.KeyboardButton("End"))

            # Send the keyboard
            self.bot.send_message(message.chat.id, "Select a Quiz Topic:", reply_markup=keyboard_qn)

            print(message.id)
            print('\n')
            print(message.chat)
        # Define the handler for the topic buttons
        @self.bot.message_handler(func=lambda message: message.text in self.quiz_names()
                                   and isinstance(self, Quiz)  and message.from_user != self.bot.get_me())
        def handle_quiz(message):
            print('break_quiz: handle_quiz')
            # Find the selected topic
            selected_quiz = next((qna for qna in self.question if qna["Name"] == message.text), None)

            # If the topic was found, send the introduction
            if selected_quiz:
                option_quiz:list = ['Test me', 'Back?']

                # Initialise the keyboard differently to prevent clashing of previous keyboard
                keyboard2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

                # Loop through the list and labelling the options
                for x in option_quiz:
                    keyboard2.add(telebot.types.KeyboardButton(x))

                print('display_quiz')
                # Print the button out
                self.bot.send_message(message.chat.id, "Select a component: ", reply_markup=keyboard2)

                # Register option_handling as the next step
                self.bot.register_next_step_handler(message, option_handling)

                # To read the options from options list
            @self.bot.message_handler(func=lambda message: message.text in option_quiz)
            def option_handling(message):
                if message.text == "Test me":
                    print('Quiz_me')
                    # Select a random question from the topic
                    selected_question = r.choice(selected_quiz["questions"])

                    # Send the question to the user
                    self.bot.send_message(message.chat.id, selected_question["question"])

                    # Create the keyboard for the answer options
                    option_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

                    # List to access the options to be able to display: 'Topics'->'questions'->'answer'->'options'
                    # Need [0] to access the first index of answer
                    selected_options: list = selected_question["answer"][0]

                    # Add the answer options to the keyboard
                    for option in selected_options['options']:
                        for option_key in option.keys():
                            option_keyboard.add(telebot.types.KeyboardButton(option_key))

                    print('option_displayed')
                    # Add the 'End' option to handle it stop the questions halfway through
                    option_keyboard.add(telebot.types.KeyboardButton('End'))

                    # Send the answer options to the user
                    self.bot.send_message(message.chat.id, "Select an answer:", reply_markup=option_keyboard)
                    

                    # Define the handler for the answer buttons
                    @self.bot.message_handler(func=lambda message: message.text in [option_key for option in selected_options['options'] for option_key in option.keys()])
                    def handle_answer(message):
                        print('checking')
                        # Check if the selected option is correct
                        for option in selected_options['options']:
                            if message.text in option:
                                if option[message.text] == 'correct':
                                    reply_text = "Correct!"
                                else:
                                    reply_text = "Wrong answer"
                                    
                                break
                        else:
                            reply_text = 'Answer does not exist'

                        # Send the message to the user
                        self.bot.send_message(message.chat.id, reply_text)

                        # Move on to the next question
                        option_handling(message)

                elif message.text == "End":
                    Quizmenu(message)

        # Define the handler for the "Stop" button
        @self.bot.message_handler(func=lambda message: message.text == "End")
        def handle_stop(message):
            print('\n\nhandle_stop\n\n')
            # Send goodbye message
            self.bot.send_message(message.chat.id, "Thanks for playing the Python Quiz Bot!")
            # Remove custom keyboard (if any)
            self.bot.send_message(message.chat.id, "Keyboard removed.", reply_markup=telebot.types.ReplyKeyboardRemove())

    def quiz_names(self):
        # Create a list of topic names
        quiz_names:list = []
        for question in self.question:
            quiz_names.append(question['Name'])
        return quiz_names

class Topic(TelegramBot):
    def __init__(self, token):
        super().__init__(token)
        # Initialize an empty list for tracking the last topic displayed
        self.last_topic_displayed = []
        super().load_topics()
        super().load_egs()

    def load_egs(self):
        with open('TnE.json','r', encoding='utf-8') as te:
            self.tne = json.load(te)
            self.eg = self.tne[0]['T&E']

    def Topic_Menu(self):
        @self.bot.message_handler(commands=["topic"])
        def TopicMenu(message):
            print('in Topic')
            # Send the welcome message
            self.bot.send_message(message.chat.id, "Welcome to the Python Topics Bot! Please select a topic:")

            # Create keyboard
            keyboard_topic = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

            # Add the topic names to the keyboard as well as an 'End' button
            for topic in self.topics:
                keyboard_topic.add(telebot.types.KeyboardButton(topic["Name"]))
            keyboard_topic.add(telebot.types.KeyboardButton("End"))

            print('looped_keys')
            # Send the keyboard
            self.bot.send_message(message.chat.id, "Select a topic:", reply_markup=keyboard_topic)

        # Define the handler for the topic buttons
        @self.bot.message_handler(func=lambda message: message.text in self.topic_names()
                                  and isinstance(self, Topic) and message.from_user != self.bot.get_me())
        def handle_topic(message):
            # Find the selected topic
            print('\nbreak_topic: handle_topic')
            selected_topic_name = message.text
            selected_topic = next((topic for topic in self.topics if topic["Name"] == selected_topic_name), None)
            self.last_topic_displayed = selected_topic["Name"]

            # If the topic was found, send the introduction
            if selected_topic:
                # Update the last topic displayed
                options:list = ['Introduction','Example','Tips','Back?']

                # Initialize the keyboard differently to prevent clashing of previous keyboard
                keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

                # loop through the list and labelling the options
                for i in options:
                    keyboard1.add(telebot.types.KeyboardButton(i))
                
                print('display_topic')
                # Print buttons out
                self.bot.send_message(message.chat.id, "Select a component: ", reply_markup=keyboard1)

                # To read the options from option list
                @self.bot.message_handler(func=lambda message: message.text in options)
                def option_handler2(message):
                    if message.text == "Introduction":
                        intro_text = "\n".join(selected_topic["Introduction"])
                        self.bot.send_message(message.chat.id, intro_text)
                        print('in_Introduction')

                    elif message.text == "Example":
                        print('\n\nin_example:first_condi\n\n')
                        selected_eg = next((eg for eg in self.eg if eg['Name'] == selected_topic_name),None)
                        if selected_eg:
                            random_example = r.choice(selected_eg['Examples'])
                            self.bot.send_message(message.chat.id, random_example)

                    elif message.text == "Tips":
                        print('\n\nin_tips:first_condi\n\n')
                        selected_tip = next((tip for tip in self.eg if tip['Name'] == selected_topic_name), None)
                        if selected_tip:
                            random_tip = r.choice(selected_tip['Tips'])
                            self.bot.send_message(message.chat.id, random_tip)

                    elif message.text == 'Back?':
                        TopicMenu(message)


        # Define the handler for the "Stop" button
        @self.bot.message_handler(func=lambda message: message.text == "End")
        def handle_stop(message):
            print('\n\nhandle_stop\n\n')
            # Reset last_topic_displayed to an empty list
            self.last_topic_displayed = []
            # Remove the custom keyboard
            reply_markup = telebot.types.ReplyKeyboardRemove()

            # Send a message to confirm the menu has been stopped
            self.bot.send_message(message.chat.id, "Session Ended. Select another topic when ready.", reply_markup=reply_markup)
                    

    def topic_names(self):
        # Create a list of topic names
        topic_names:list = []
        for topic in self.topics:
            topic_names.append(topic['Name'])
        
        return topic_names



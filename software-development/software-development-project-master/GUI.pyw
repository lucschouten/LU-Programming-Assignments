#The following pre-defined modules are being imported
import tkinter as tk 
from tkinter import ttk
import time 
import random 
import math
import pygame
import re
from sys import platform
from PIL import Image, ImageTk

#The following functions are imported from our own defined modules 
from SearchEngine import get_questions
from MessageSlicer import fit_message
from database import Database
from GetPathOfFile import get_path

#the following are pre-defined variables to be used troughout the gui
background_color = "#278791"    
text_color = "white"
number_of_rounds = 10

#Tkinter widgets/fonts tend to have different behavior depending on the
#platform on which they are being used, therefore they are defined for different platforms. 
if platform == "darwin": 
    font = "Calibri "
    big = "35"
    small = "20"
    message_box = "15"
    button_height = 2 
elif platform == "win32":
    font = "Calibri "
    big = "28"
    small = "15"
    message_box = "12"
    button_height = 1 
elif platform == "linux" or platform == "linux2":
    pass 


#play_music and stop_music are functions used to turn on and off the background music in the GUI.
def play_music():
    pygame.mixer.music.load(get_path(" Muziek_SD.mp3")) #get_path is a function which makes it possible to find certain files in the same directory 
    pygame.mixer.music.play(loops=100)

def stop_music():
    pygame.mixer.music.stop()

class GuiHandlerGeneral:

    def __init__(self, bottom_layer: tk.Tk):
        """initializes the gui with the variables needed troughout the gui 
    
        Args:
            bottom_layer: The main window for the gui, all the other windows
            go on top of this window. 
        """

        self.bottom_layer = bottom_layer
        bottom_layer.title("Kwis")
        bottom_layer.configure(bg = background_color)
        bottom_layer.minsize(height = 700, width = 800)
        bottom_layer.columnconfigure(0, weight = 1)
        bottom_layer.rowconfigure(0, weight = 1)

        self.container = tk.Frame(bottom_layer)
        self.container.configure(background = background_color)
        self.container.columnconfigure(0, weight =1)
        self.container.rowconfigure(0, weight = 1)

        self.canvas = tk.Canvas(self.container, height = 700, width = 800)
        self.canvas.configure(background = background_color, highlightthickness=0)
        self.canvas.rowconfigure(0, weight = 1)
        self.canvas.columnconfigure(0, weight = 1)
        self.index = 0 
        self.normal_question_index, self.fillin_question_index, self.photo_question_index = 0, 0, 0 
        self.container.grid()
        self.canvas.grid(row = 0, column = 0,sticky="nswe")

        pygame.mixer.init()
        MenuBar = tk.Menu(bottom_layer)
        Menu = tk.Menu(MenuBar, tearoff = 0)
        MenuBar.add_cascade(label = "Muziek", menu = Menu)
        Menu.add_command(label = "Zet aan", command = play_music)
        Menu.add_command(label = "Zet uit", command = stop_music)
        root.config(menu = MenuBar)

    def message_box(self, message: str):
        """Message box to be invoked when some illegal event occurs

        Args:
            message: some message for the user to inform the user about something.
        """

        self.message = tk.Tk()
        self.message.title("")
        self.message.geometry = ("200x300")
        self.message.configure(bg = background_color)
        self.message.minsize(height = 150, width = 280)
        self.message.maxsize(height = 150, width = 280)
        tk.Label(self.message, text = message, font = font+message_box, bg = background_color, fg = text_color).place(rely = 0.3, relx = 0.5, anchor = "center")
        tk.Button(self.message, text = "OK", width = 10, command = self.message.destroy).place(rely = 0.6, relx = 0.5, anchor = "center")

    def start_frame(self):
        """The window on which the Gui starts 

        """

        start_frame = tk.Frame(self.canvas)
        start_frame.configure(background = background_color)

        self.canvas.create_window((400, 300), window=start_frame)


        def type_of_game(kind: str):
            global type_of_game
            type_of_game = kind
            if type_of_game == "classic":
                self.canvas.destroy()
                self.container.destroy()
                child_object = GuiHandlerClassic(root)   
                child_object.player_names()
            elif type_of_game == "tournament":
                self.canvas.destroy()
                self.container.destroy()
                child_object = GuiHandlerCompetition(root)   
                child_object.player_names()
                
        logo_image_path = get_path("/Kwis_logo.png")
        logo_image = Image.open(logo_image_path)
        logo_image = logo_image.resize((400,400), Image.ANTIALIAS) #actual resizing of the image, antialiasing so picture won't look bad after resizing.
        render_logo_image = ImageTk.PhotoImage(logo_image) #ready the image to be used in tkinter. 
        image_label = tk.Label(start_frame, image = render_logo_image, bd = 0, bg = background_color)
        image_label.image = render_logo_image
        image_label.grid(row = 1, pady = (0, 10))

        classic_game = tk.Button(start_frame, text="Klassiek", width = 20, height = button_height,font = font+small, command = lambda:[type_of_game("classic"), start_frame.destroy()]).grid(row = 2)
        tournament = tk.Button(start_frame, text = "Competitie", width = 20, height = button_height, font = font+small, command = lambda:[type_of_game("tournament"), start_frame.destroy()]).grid(row = 3, pady = 10)

    def common_player_names_and_register(self, frame_name: tk.Frame, player_dictionary: dict, password_dictionary: dict):
        """Method to hold the widgets the player_names and register method share.

        player_names, which is used to login into accounts needs some widgets 
        which are exactly the same to the method that is used to regiser, these 
        widgets are stored in this method and invoked by both the player_names and
        register method to construct their windows. 

        Args:
            frame_name: the name of the frame of the window which invokes common_player_names_and_register
            
            player_dictionary: the variable of the player dictionary in which the textvariable for the
            usernames of the players are be stored. these textvariables must be different for usernames 
            of players who are already registered and for players that are registered already while 
            otherwise the entry's for which the textvariables are made would be the same for bot the player_names
            and the register windows. 

            password dictionary: the variable of the password dictionary in which textvariables for the passwords 
            of the players are stored. this dictionary is different for players that are registering and for
            players that are already registered. 
        """

        for player_number in range(1,3):
            player_dictionary["name_player"+str(player_number)] = tk.StringVar(frame_name) 
            password_dictionary["name_player"+str(player_number)] = tk.StringVar(frame_name) 

        username = tk.Label(frame_name, text = "Gebruikersnaam", fg = text_color, bg = background_color, font = font+big)
        username.grid(row = 1, column = 0)
        password = tk.Label(frame_name, text = "Wachtwoord", fg = text_color, bg = background_color, font = font+big)
        password.grid(row = 1, column = 1)

        player1_entry = tk.Entry(frame_name, width = 20, textvariable = player_dictionary["name_player1"], font = font+small, justify = "center").grid(column = 0, row = 2)
        player2_entry = tk.Entry(frame_name, width = 20, textvariable = player_dictionary["name_player2"], font = font+small, justify = "center").grid(column = 0, row = 3)
        player1_password = tk.Entry(frame_name, show = "*", width = 20, textvariable = password_dictionary["name_player1"], font = font+small, justify = "center").grid(column = 1, row = 2, sticky = "w")
        player2_password = tk.Entry(frame_name, show = "*", width = 20, textvariable = password_dictionary["name_player2"], font = font+small, justify = "center").grid(column = 1, row = 3, sticky = "w")

        self.row_number = 4
        self.player = 3 
        def add_player():
            """Adds another entry for players to fill in their names. 

            aside from adding an entry it checks if the number 
            of players doesn't exceed the max number of players. 
            """
            if self.player <= 6:
                player_dictionary["name_player"+str(self.player)] = tk.StringVar(frame_name) #put variables containing the player names in a dictionary for retrieval all at once. 
                password_dictionary["name_player"+str(self.player)] = tk.StringVar(frame_name) 
                tk.Entry(frame_name, width = 20, textvariable = player_dictionary["name_player"+str(self.player)], font = font+small, justify = "center").grid(column = 0, row = self.row_number)
                tk.Entry(frame_name, show = "*", width = 20, textvariable = password_dictionary["name_player"+str(self.player)], font = font+small, justify = "center").grid(column = 1, row = self.row_number, sticky = "w")  
                self.row_number += 1
                self.player += 1        
            else: 
                self.message_box("Maximum aantal spelers bereikt")

        add_player_button = tk.Button(frame_name, text = "Voeg Speler toe", width = 20, height = button_height, font = font+small, command = add_player).grid(row = 1000, columnspan = 2, pady = (10,0))

    def player_names(self):
        """The second window of the GUI, here players can add there names.

        """
        players = tk.Frame(self.canvas)
        players.configure(bg = background_color)

        self.canvas.create_window((400, 100), window=players, anchor = "n")

        player_title = tk.Label(players, text = "Spelers", fg = text_color, bg = background_color, font = font+big)
        player_title.grid(row = 0, columnspan = 2, pady = (0,20))


        self.existing_player_dictionary = {}
        self.existing_password_dictionary = {}

        self.common_player_names_and_register(players, self.existing_player_dictionary, self.existing_password_dictionary)

        def construct_dictionary_of_players():
            """
            A submethod which construct a dictionary of the players

            This method retrieves all the names of the players that
            are participating and adds them to a dictionary which is
            being used to keep the score of the players. it also adds 
            the names to a list of players. The contents of the list
            are being used as keys for the dictionary. 

            """
            db1 = Database("db4free.net", "lucschouten","trivia1234","triviadatabase") #Construct a object to work with the Database class that is imported from another file.

            self.dictionary_of_players = {}
            self.list_of_players = []
            self.dictionary_of_passwords = {}
            for player in range(1, self.row_number-1):
                player_name = self.existing_player_dictionary["name_player"+str(player)].get() #retrieve all the values of the entry's where players could have filled in their names.
                player_password = self.existing_password_dictionary["name_player"+str(player)].get() #retrieve all the values of the entry's where players could have filled in their passwords
                if player_name != "":
                    if db1.check_password(player_name,player_password) in ("No Acces granted, password didnt match", "Account not found in database"): #compare filled in usernames and passwords with accounts in the database. 
                        self.message_box("Account "+player_name+" niet gevonden of \ngebruikersnaam/wachtwoord incorrect")
                        db1.disconnect()
                        return 
                    self.dictionary_of_players[player_name] = 0
                    self.list_of_players.append(player_name)
                    self.dictionary_of_passwords[player_name] = player_password
            db1.disconnect() #close the connection with the database so no "zombie" connections remain. 
            if len(self.list_of_players) != len(set(self.list_of_players)):
                self.message_box("Elke gebruikersnaam dient uniek te zijn")
            elif len(self.list_of_players) < 2:
                self.message_box("Het aantal spelers is nog onvoldoende")
            else:
                players.destroy()
                self.method_handler("choose_difficulty")

        log_in = tk.Button(players, text = "Log in", width = 20, height = button_height, font = font+small, command = lambda:[construct_dictionary_of_players()]).grid(row = 1001, columnspan = 2, pady = (10,0))
        
        register = tk.Button(players, text = "Registreren", width = 20, height = button_height, font = font+small, command = lambda:[players.destroy(), self.method_handler("register")]).grid(row = 1002, columnspan = 2, pady=(10,0))

    def register(self):
        """Method for new players to register.

        In the register method a display is showed which 
        allows for player(s) that don't have an account yet
        to create one that will be stored in the database. 
        """

        register_frame = tk.Frame(self.canvas)
        register_frame.configure(bg = background_color)

        self.canvas.create_window((400, 75), window=register_frame, anchor = "n")

        self.register_player_dictionary = {}
        self.register_password_dictionary = {}

        register_title = tk.Label(register_frame, text = "Kies een gebruikersnaam en \nwachtwoord om mee te registreren", fg = text_color, bg = background_color, font = font+big).grid(row = 0, columnspan = 2, pady = (0,20))

        self.common_player_names_and_register(register_frame, self.register_player_dictionary, self.register_password_dictionary)

        def register_account():
            """Register the account in the database.

            This function checks whether a account already exists
            in the database. When it is not, the account will be 
            added and the player will be returned to the player_names
            method. Otherwise a message wil promp saying the account
            already exists.
            """

            db1 = Database("db4free.net", "lucschouten","trivia1234","triviadatabase")
            for player in range(1, self.row_number-1):
                player_name = self.register_player_dictionary["name_player"+str(player)].get() #retrieve all the values of the entry's where players could have filled in their names.
                player_password = self.register_password_dictionary["name_player"+str(player)].get() #retrieve all the values of the entry's where players could have filled in their passwords
                if player_name != "":
                    if db1.create_account(player_name,player_password) == "This account already exists in the database, please change the username": #compare filled in usernames and passwords with accounts in the database. 
                        self.message_box("de volgende gebuikersnaam \n bestaat al: " + player_name)
                        db1.disconnect()
                        return 
                    self.register_player_dictionary["name_player"+str(player)], self.register_password_dictionary["name_player"+str(player)] = tk.StringVar(register_frame), tk.StringVar(register_frame)
            db1.disconnect()
            register_frame.destroy()
            self.method_handler("player_names")
            self.message_box("Account(s) succesvol geregistreerd")
        register = tk.Button(register_frame, text = "Registreren", width = "20", height = button_height, font = font+small, command = register_account).grid(row = 1001, columnspan = 2, pady = (10,0))

        back = tk.Button(register_frame, text = "Terug", width = "20", height = button_height, font = font+small, command = lambda:[register_frame.destroy(), self.method_handler("player_names")]).grid(row = 1002, columnspan = 2, pady = (10,0))

    def choose_difficulty(self):
        """The third window of the  GUI

        Here the difficulty for the whole game is determined.
        """

        difficulty_frame = tk.Frame(self.canvas)
        difficulty_frame.configure(bg = background_color)

        self.canvas.create_window((400, 250), window=difficulty_frame)

        category = tk.Label(difficulty_frame, text = "Choose a Category", fg = text_color, bg = background_color, font = font+big)
        category.grid(padx = 265, row = 1)

        def initiate_difficulty(difficulty: str):
            self.difficulty = difficulty
        tk.Button(difficulty_frame, text = "Makkelijk", width = 25, height = button_height, font = font+small, command = lambda:[difficulty_frame.destroy(), initiate_difficulty("Easy"), self.method_handler("asked_questions")]).grid(row = 2, pady = (40,10))
        tk.Button(difficulty_frame, text = "Gemiddeld", width = 25, height = button_height, font = font+small, command = lambda:[difficulty_frame.destroy(), initiate_difficulty("Medium"), self.method_handler("asked_questions")]).grid(row = 3, pady = 10)
        tk.Button(difficulty_frame, text = "Moeilijk", width = 25, height = button_height, font = font+small, command = lambda:[difficulty_frame.destroy(), initiate_difficulty("Hard"), self.method_handler("asked_questions")]).grid(row = 4, pady = 10)
        tk.Button(difficulty_frame, text = "Extreem", width = 25, height = button_height, font = font+small, command = lambda:[difficulty_frame.destroy(), initiate_difficulty("Extreme"), self.method_handler("asked_questions")]).grid(row = 5, pady = 10)
        
    def asked_questions(self, list_of_players: list, categorie: str):
        """A method to retrieve the questions for the game. 

        Args: 
            list_of_players: A list consisting of all the playernames 
            of the players participating in the game 

            Categorie: the difficulty the players choose for the game. 
        """

        self.number_of_questions = 17 #the maximum number of questions there is for every type of question. 
        self.Q_and_A_normal = get_questions(self.number_of_questions, categorie, "Normal") #reguests all the questions and answers of a type for the game in the form of a dictionary.
        self.Q_and_A_fillin = get_questions(self.number_of_questions, categorie,'Fill in')
        self.Q_and_A_photo = get_questions(self.number_of_questions, categorie,'Photo')

        self.normal_question_list = [question for question in self.Q_and_A_normal] #puts all the qustions in a list so they can be used to ask the question to the player and as key for the dictionary to get the answers (values).        
        self.fillin_question_list = [question for question in self.Q_and_A_fillin]
        self.photo_question_list = [question for question in self.Q_and_A_photo]
        
        self.method_handler("turn_determiner")

    def turn_determiner(self):
        """A method to determine which player is on move 

        """

        if self.index >= len(self.list_of_players): 
            self.index = 0
        if self.normal_question_index == self.number_of_questions: #return the index back to 0 when al the questions are answered so the list_of_questions doesn't go out of bounds. 
            self.normal_question_index = 0
        elif self.photo_question_index == self.number_of_questions:
            self.photo_question_index = 0 
        elif self.fillin_question_index == self.number_of_questions:
            self.fillin_question_index = 0
        player_on_move = self.list_of_players[self.index]
        self.method_handler("question_to_answer", player_on_move)

    def question_to_answer(self, player_on_move: str):
        """A Method to show the screen with the question and the possible answers.
        
        Args: 
            player_on_move: the name of the player who is on turn
        """

        def modify_answers_for_gui(raw_answers: list): 
            if type_of_question == "photo":
                global photo_path 
                photo_path = raw_answers.pop() #for the photo question type, the path of the photo to be displayed in the gui is put at last in the answer field. 

            global answers 
            answers = []
            for possible_answer in raw_answers: #request the answers to the question the player has to answer by gving the question as key to the dictionary 
                if possible_answer[-1] == "*":
                    self.right_answer = possible_answer.replace("*", "")
                possible_answer = possible_answer.replace("*", "") #remove the * so it isn't clear upfront which answer is the right answer.
                answers.append(possible_answer)
            random.shuffle(answers) #make sure the answers are in a different order every time. 

        type_of_question = random.choice(["fillin", "photo", "normal"]) #use the random module to randomly choose between the three types of questions. 
        if type_of_question == "normal":
            asked_question = self.normal_question_list[self.normal_question_index]
            raw_answers = self.Q_and_A_normal[asked_question]
            modify_answers_for_gui(raw_answers)
            self.normal_question_index += 1 
            self.time_left = 20
        elif type_of_question == "fillin":
            asked_question = self.fillin_question_list[self.fillin_question_index]
            raw_answers = self.Q_and_A_fillin[asked_question]
            self.number_of_answers_needed = int(raw_answers.pop()) #the number of answers which must be given is added to the question in the file as last argument.
            self.right_answer = set([answer.lower().strip() for answer in raw_answers]) #make all the answers of the fillin type lowercase, stripped and make the list a set for better comparebillity with filled in answers.
            self.fillin_question_index += 1
            self.time_left = 30
        elif type_of_question == "photo": 
            asked_question = self.photo_question_list[self.photo_question_index]
            raw_answers = self.Q_and_A_photo[asked_question]
            modify_answers_for_gui(raw_answers)
            self.photo_question_index += 1
            self.time_left = 20


        question_frame = tk.Frame(self.canvas)       
        question_frame.configure(bg = background_color)
        self.canvas.create_window((400, 250), window=question_frame)

        def timer():
            """timer which counts down to zero 

            When the time left becomes zero, the timer 
            method calls for the next window (score_board) and 
            passes None as played_answer, together with the right answer. 
            When the time isn't up yet, the timer keeps counting down 
            until time_left is zero seconds. 
            """

            if self.time_left == 0:
                question_frame.destroy()
                played_answer = None
                self.score_board(player_on_move, played_answer, self.right_answer, type_of_question, None) #calls the score_board window when the time is up 
            else:
                global time_left_label
                time_left_label = tk.Label(question_frame, text = "Tijd: "+ str(self.time_left), fg = text_color, bg = background_color, font = font+big)
                if type_of_question == "normal" or type_of_question == "fillin":
                    time_left_label.grid(row = 1000, pady = 10, sticky = 's') 
                elif type_of_question == "photo":
                    time_left_label.grid(row = 1000, columnspan = 2, pady = 10, sticky = 's')
                self.time_left -= 1
                question_frame.after(1000, functionCaller) #to execute several functions at once the functionCaller method is invoked
        def functionCaller():
            """Used for timer to execute several functions at once

            """

            time_left_label.destroy()
            timer()
        timer()

        if type_of_question == "normal":
            tk.Label(question_frame, text = player_on_move+":", fg = text_color, bg = background_color, font = font+big).grid(row = 1, pady = (150,0))

            #the question that is asked. here the question that is asked is being requested and it is made sure to fit the window. 
            tk.Label(question_frame, text = fit_message(asked_question, font, big), font = font+big, bg = background_color, fg = text_color).grid(row = 2, sticky="e", pady = (20, 30))
            #the answers the player can choose from. 
            tk.Button(question_frame, text = answers[0], width = 25, height = button_height, font = font+small, command = lambda:[question_frame.destroy(), self.method_handler("score_board", player_on_move, type_of_question, 1, answers[0], self.right_answer)]).grid(row = 3, pady = (0, 10))
            tk.Button(question_frame, text = answers[1], width = 25, height = button_height, font = font+small, command = lambda:[question_frame.destroy(), self.method_handler("score_board", player_on_move, type_of_question, 1, answers[1], self.right_answer)]).grid(row = 4, pady = 10)
            tk.Button(question_frame, text = answers[2], width = 25, height = button_height, font = font+small, command = lambda:[question_frame.destroy(), self.method_handler("score_board", player_on_move, type_of_question, 1, answers[2], self.right_answer)]).grid(row = 5, pady = 10)
            tk.Button(question_frame, text = answers[3], width = 25, height = button_height, font = font+small, command = lambda:[question_frame.destroy(), self.method_handler("score_board", player_on_move, type_of_question, 1, answers[3], self.right_answer)]).grid(row = 6, pady = (10,0))
        
        elif type_of_question == "photo":
            tk.Label(question_frame, text = player_on_move+":", fg = text_color, bg = background_color, font = font+big).grid(row = 1, columnspan = 2, pady = (200,0))

            #the question that is asked. here the question that is asked is being requested and it is made sure to fit the window. 
            tk.Label(question_frame, text = fit_message(asked_question, font, big), font = font+big, bg = background_color, fg = text_color).grid(row = 2, columnspan = 2, pady = (20, 20))

            question_image_path = get_path("SD FOTOS")+"/"+photo_path
            question_image = Image.open(question_image_path)
            initial_size = question_image.size
            if initial_size[1] > 260: #when pictures have a height of >260 pixels they are to high and thus must be resized to ft in the window.
                #note that pictures with a wifth of >800 but a height of <=250 would also cause problems. In the gui, panorama's like this 
                #are not being used. 
                resize_factor = 260/initial_size[1] #keep the ratio of the picture. 
                new_width = resize_factor * initial_size[0] 
                new_height = resize_factor * initial_size[1]
                question_image = question_image.resize((int(new_width), int(new_height)), Image.ANTIALIAS) #actual resizing of the image, antialiasing so picture won't look bad after resizing.
            render_question_image = ImageTk.PhotoImage(question_image) #ready the image to be used in tkinter. 
            image_label = tk.Label(question_frame, image = render_question_image, bd = 0, bg = background_color)
            image_label.image = render_question_image
            image_label.grid(row = 3, columnspan = 2)

            tk.Button(question_frame, text = answers[0], width = 25, height = button_height, font = font+small, command = lambda:[question_frame.destroy(), self.method_handler("score_board", player_on_move, type_of_question, 1, answers[0], self.right_answer)]).grid(row = 4, column = 0, pady = (10, 0))
            tk.Button(question_frame, text = answers[1], width = 25, height = button_height, font = font+small, command = lambda:[question_frame.destroy(), self.method_handler("score_board", player_on_move, type_of_question, 1, answers[1], self.right_answer)]).grid(row = 4, column = 1, pady = (10, 0))
            tk.Button(question_frame, text = answers[2], width = 25, height = button_height, font = font+small, command = lambda:[question_frame.destroy(), self.method_handler("score_board", player_on_move, type_of_question, 1, answers[2], self.right_answer)]).grid(row = 5, column = 0, pady = (10, 0))
            tk.Button(question_frame, text = answers[3], width = 25, height = button_height, font = font+small, command = lambda:[question_frame.destroy(), self.method_handler("score_board", player_on_move, type_of_question, 1, answers[3], self.right_answer)]).grid(row = 5, column = 1, pady = (10, 0))

        elif type_of_question == "fillin":
            tk.Label(question_frame, text = player_on_move+":", fg = text_color, bg = background_color, font = font+big).grid(row = 1, columnspan = 2, pady = (100,0))

            #the question that is asked. here the question that is asked is being requested and it is made sure to fit the window. 
            tk.Label(question_frame, text = fit_message(asked_question, font, big), font = font+big, bg = background_color, fg = text_color).grid(row = 2, pady = (20, 20))

            row = 3 
            fillin_answer_dict = {}
            for answer_no in range(self.number_of_answers_needed):
                fillin_answer_dict["answer"+str(answer_no)] = tk.StringVar(question_frame)
                tk.Entry(question_frame, textvariable = fillin_answer_dict["answer"+str(answer_no)], width = 20, font = font+small).grid(row = row)
                row+=1

            def get_played_answers() -> set:
                """the get_played_answers uniforms the played answer.

                uniforming the played answer makes it easier to 
                play the right answer for the answer matches the 
                right answer more easily.

                Returns: set of played answers in a uniformed way. 
                """

                delete_if_present = ["het", "de"]
                played_answers = []
                for answer_no in range(self.number_of_answers_needed):
                    played_answer = fillin_answer_dict["answer"+str(answer_no)].get()
                    if played_answer != "":
                        played_answer = played_answer.lower() 
                        for delete_string in delete_if_present:
                            played_answer = re.sub(r"\b%s\b" %delete_string, "", played_answer) #delete contents of delete_if_present from 
                            #the played answer iff it is at the beginning of the played answer. 
                        played_answer = played_answer.strip()
                        played_answers.append(played_answer)
                played_answers = set(played_answers)
                return played_answers

            tk.Button(question_frame, text = "Antwoord", width = 25, height = button_height, font = font+small, command = lambda:[question_frame.destroy(), self.method_handler("score_board", player_on_move, type_of_question, self.number_of_answers_needed, get_played_answers(), self.right_answer)]).grid(row = row, column = 0, pady = (50, 0))

    def leaderboard(self, previous_window: tk.Frame):
        """The leaderboard is the window used to show the number of won games per player.

        The contents of the number of won games per player will be retrieved
        from the database. For each difficulty a leaderboard will be set up.

        Args:
            previous_window: the previous window is the window/method
            where the game is coming from. this is different for the 
            competition game and the classic version. The previous window
            must be known so all the widgets of this window can be stored.
            The storing of the widgets make it possible to go back to this 
            window. 
        """

        leaderboard_frame = tk.Frame(self.canvas)
        leaderboard_frame.config(bg = background_color)
        self.canvas.create_window((400, 50), window=leaderboard_frame, anchor = "n")

        tk.Label(leaderboard_frame, text = "Leaderboard:", font = font+big, bg = background_color, fg = text_color).grid(row = 0, column = 0, pady = (0, 20))

        dict_treeview_vars = {}

        leaderboard_tabs = ttk.Notebook(leaderboard_frame) #set up the notebook which is used to place tabs for the leaderboard difficulties.
        leaderboard_tabs.grid(row = 1, column = 0, sticky = "nw")

        easy_frame, medium_frame, hard_frame, extreme_frame = tk.Frame(leaderboard_frame), tk.Frame(leaderboard_frame), tk.Frame(leaderboard_frame), tk.Frame(leaderboard_frame)
        leaderboard_frame_list = [easy_frame, medium_frame, hard_frame, extreme_frame] 

        def insert_rank(player_contents: list) -> list:
            """insert the rank into the player_contents.
            
            The player contents retrieved from the database
            are already in descending order but they don't 
            include a rank yet, the rank is added with this
            function.

            Args:
                player_contents: the player_contents are 
                the retrieved contents from the database. 

            Returns: the player contents, now containing the rank. 
            """

            contents_index = 0
            while contents_index < len(player_contents):
                player_contents[contents_index] = list(player_contents[contents_index])
                player_contents[contents_index].insert(0, contents_index+1)
                contents_index+=1
            return player_contents 

        db1 = Database("db4free.net", "lucschouten", "trivia1234", "triviadatabase")
        leaderboard_index = 0
        leaderboard_style = ttk.Style()
        for i in range(4): #for each of the difficulties, make a table containing the ranking, usernames and scores. 
            leaderboard_tabs.add(leaderboard_frame_list[leaderboard_index], text = ["Makkelijk", "Gemiddeld", "Moeilijk", "Extreem"][leaderboard_index])
            player_contents = db1.getleaderboard(10, ["easy", "medium", "hard", "extreme"][leaderboard_index]) #get the contents of the players from the database for the specified difficulty
            insert_rank(player_contents)

            leaderboard = ttk.Treeview(leaderboard_frame_list[leaderboard_index])
            leaderboard['columns'] = ("rank", "Username", "Score")
            leaderboard.column("#0", width=0, minwidth=0)
            leaderboard.column("rank", anchor = "center", width=100)
            leaderboard.column("Username", anchor = "center", width=250)
            leaderboard.column("Score", anchor = "center", width=250)

            leaderboard.heading("rank", text = "Rank")
            leaderboard.heading("Username", text="Gebruikersnaam")
            leaderboard.heading("Score", text="Score")
            leaderboard_style.configure('Treeview', rowheight=30, font = font+small)
            leaderboard_style.configure("Treeview.Heading", rowheight=1, font = font+small+" bold")
            leaderboard.grid(row = 0, column = 0)
            
            for player in player_contents:
                leaderboard.insert('', 'end', values=player) #insert the values from the database into the leaderboard table. 
            leaderboard_index += 1
        db1.disconnect()

        tk.Button(leaderboard_frame, text = "Terug", font = font+small, bg = background_color, height = button_height, width = 20, command = lambda:[leaderboard_frame.destroy(), previous_window.grid(), self.canvas.create_window((400, 50), window=previous_window, anchor = "n")]).grid(row = 3, pady = (20, 0))


class GuiHandlerClassic(GuiHandlerGeneral):
    def __init__(self, bottom_layer: tk.Tk):
        super().__init__(bottom_layer) 

    def method_handler(self, going_to_method: str, *optional_keywoards: tuple):
        """The method handler determines which method needs to be called

        The method handler has an input (method), this input is the method
        where the call to method_handler comes from. this method determines
        which method needs to be called from here. 

        Args:
            method: The method which called method_handler and defines
            the next method to be called
            optional keywoards: An undefined number of keywoards which 
            are needed to call the next method. 
        """

        list_of_keywoards = [keywoard for keywoard in optional_keywoards]
        if going_to_method == "player_names":
            self.player_names()
        if going_to_method == "register":
            self.register()
        elif going_to_method == "choose_difficulty":
            self.choose_difficulty() #turn to the next window.
        elif going_to_method == "register":
            self.register()
        elif going_to_method == "asked_questions": 
            self.asked_questions(self.list_of_players, self.difficulty)
        elif going_to_method == "turn_determiner":
            self.turn_determiner()
        elif going_to_method == "question_to_answer":
            self.question_to_answer(list_of_keywoards[0])
        elif going_to_method == "score_board":
            self.score_board(list_of_keywoards[0], list_of_keywoards[1], list_of_keywoards[2], list_of_keywoards[3], list_of_keywoards[4])
        elif going_to_method == "leaderboard":
            self.leaderboard(self.score_board_frame)

    def score_board(self, player_on_move: str, type_of_question: str, number_of_answers_needed: int, played_answer, right_answer):
        """The scoreboard to be displayed whenever a question is answered

        Args: 
            player_on_move: The name of the player that was on move and played an answer
            type_of_question: the question can be either a fillin, photo or normal question.
                the different kinds of questions have different handling. 
            number_of_answers_needed: the number of answer(s) the player must give. 
            played_answer (None/set/string):  The answer played by the player, the type of answer differs.
                when the type of question is photo or normal, the answer can be either None, 
                when not answered in time or a string. When the type of question is fillin, 
                the answer can be of the type set or none. When something is answered, the type 
                is set. When nothing is answered, the type is None. 
            right_answer (set/string): The right answer on the question asked. The type of the right 
                answer can be either a string or a set. The right answer is of the type string for 
                photo and normal questions and of the type set for fillin questions. 
        """

        self.score_board_frame = tk.Frame(self.canvas)       
        self.score_board_frame.configure(bg = background_color)
        self.canvas.create_window((400, 50), window=self.score_board_frame, anchor = "n")

        def score_board_header(answer_result: bool):
            """the score_board_header determines the header for the scoreboard.

            depending on whether the answer was right, wrong or not given at all
            and depending on the game being done or not, the score_board_header is 
            determined. 

            Args:
                answer_result: whether the given answer was true or false. 
            """

            if answer_result == True:
                self.dictionary_of_players[player_on_move] += 1 #turn to the next player to be on turn.
                if self.dictionary_of_players[player_on_move] != number_of_rounds:
                    tk.Label(self.score_board_frame, text = player_on_move+", je had gelijk!", fg = text_color, bg = background_color, font = font+big).grid(row = 0, columnspan = 2, pady = (40,20))
                else: 
                    tk.Label(self.score_board_frame, text = player_on_move+", gefeliciteerd, je hebt gewonnen!", fg = text_color, bg = background_color, font = font+big).grid(row = 0, columnspan = 2, pady = (40,20))
            else:
                if played_answer == None: 
                    tk.Label(self.score_board_frame, text = player_on_move+", je was te laat met antwoorden", fg = text_color, bg = background_color, font = font+big).grid(row = 0, columnspan = 2, pady = (40,20))                
                else: 
                    tk.Label(self.score_board_frame, text = player_on_move+", je had ongelijk :(", fg = text_color, bg = background_color, font = font+big).grid(row = 0, columnspan = 2, pady = (40,20))

        if type_of_question == "normal" or type_of_question == "photo":
            if played_answer == right_answer:
                score_board_header(True)
            else:
                score_board_header(False)
        elif type_of_question == "fillin":
            if played_answer == None:
                score_board_header(False)
            elif played_answer.issubset(right_answer) and len(played_answer) == number_of_answers_needed:
                score_board_header(True)
            else:
                score_board_header(False)
        
        tk.Label(self.score_board_frame, text = "speler:", fg = text_color, bg = background_color, font = font+big+" bold").grid(row = 1, column = 0)
        tk.Label(self.score_board_frame, text = "score:", fg = text_color, bg = background_color, font = font+big+" bold").grid(row = 1, column = 1)
        row = 2
        for player in self.list_of_players:
            tk.Label(self.score_board_frame, text = player, fg = text_color, bg = background_color, font = font+big).grid(row = row, column = 0)
            tk.Label(self.score_board_frame, text = str(self.dictionary_of_players[player]), fg = text_color, bg = background_color, font = font+big).grid(row = row, column = 1)
            row += 1

        self.index += 1 
        
        if self.dictionary_of_players[player_on_move] != number_of_rounds: #if the player that was on move didn't win, the game continues 
            tk.Button(self.score_board_frame, text = "Volgende", width = 25, height = button_height, bg = background_color, font = font+small, command = lambda:[self.score_board_frame.destroy(), self.turn_determiner()]).grid(row = row+1, columnspan = 2, pady = 10)
        else: 
            db1 = Database("db4free.net", "lucschouten","trivia1234","triviadatabase") 
            new_score_of_winner = db1.retrieve_score(player_on_move, self.dictionary_of_passwords[player_on_move], self.difficulty)[0][1] + 1
            db1.updatescore(player_on_move, self.dictionary_of_passwords[player_on_move], self.difficulty, new_score_of_winner)
            db1.disconnect
            
            tk.Button(self.score_board_frame, text = "Leaderboard", width = 25, height = button_height, bg = background_color, font = font+small, command = lambda:[self.score_board_frame.grid_remove(),self.canvas.delete("all"), self.method_handler("leaderboard")]).grid(row = row+1, columnspan = 2, pady = 10)
            tk.Button(self.score_board_frame, text = "Opnieuw Beginnen", width = 25, height = button_height, bg = background_color, font = font+small, command = lambda:[self.score_board_frame.destroy(), self.start_frame()]).grid(row = row+2, columnspan = 2, pady = (0,10))
            tk.Button(self.score_board_frame, text = "Stop", width = 25, height = button_height, bg = background_color, font = font+small, command = lambda:[root.destroy()]).grid(row = row + 3, columnspan = 2)


class GuiHandlerCompetition(GuiHandlerGeneral):
    def __init__(self, bottom_layer: tk.Tk):
        super().__init__(bottom_layer)

    def method_handler(self, going_to_method: str, *optional_keywoards: tuple):
        """The method handler determines which method needs to be called

        The method handler has an input (method), this input is the method
        where the call to method_handler comes from. this method determines
        which method needs to be called from here. 

        Args:
            method: The method which called method_handler and defines
            the next method to be called
            optional keywoards: An undefined number of keywoards which 
            are needed to call the next method. 
        """

        list_of_keywoards = [keywoard for keywoard in optional_keywoards]
        if going_to_method == "player_names":
            self.player_names()
        if going_to_method == "register":
            self.register()
        elif going_to_method == "choose_difficulty":
            self.choose_difficulty() #turn to the next window.
        elif going_to_method == "asked_questions": 
            self.asked_questions(self.list_of_players, self.difficulty) 
        elif going_to_method == "turn_determiner":
            self.turn_determiner()
        elif going_to_method == "question_to_answer":
            self.question_to_answer(list_of_keywoards[0])
        elif going_to_method == "score_board":
            self.score_board(list_of_keywoards[0], list_of_keywoards[1], list_of_keywoards[2], list_of_keywoards[3], list_of_keywoards[4])
        elif going_to_method == "players_in_round_or_turn_determiner":
            if self.index == len(self.list_of_players):
                self.players_in_round()
            else: 
                self.turn_determiner()
        elif going_to_method == "leaderboard":
            self.leaderboard(self.players_in_round_frame)

    def score_board(self, player_on_move: str, type_of_question: str, number_of_answers_needed: int, played_answer, right_answer):
        """The scoreboard to be displayed whenever a question is answered

        Args: 
            player_on_move: The name of the player that was on move and played an answer
            type_of_question: the question can be either a fillin, photo or normal question.
                the different kinds of questions have different handling. 
            number_of_answers_needed: the number of answer(s) the player must give. 
            played_answer (None/set/string):  The answer played by the player, the type of answer differs.
                when the type of question is photo or normal, the answer can be either None, 
                when not answered in time or a string. When the type of question is fillin, 
                the answer can be of the type set or none. When something is answered, the type 
                is set. When nothing is answered, the type is None. 
            right_answer (set/string): The right answer on the question asked. The type of the right 
                answer can be either a string or a set. The right answer is of the type string for 
                photo and normal questions and of the type set for fillin questions. 
        """

        self.score_board_frame = tk.Frame(self.canvas)       
        self.score_board_frame.configure(bg = background_color)
        self.canvas.create_window((400, 250), window=self.score_board_frame)

        def score_board_header(answer_result: bool):
            if answer_result == True:
                self.dictionary_of_players[player_on_move] += 1 #turn to the next player to be on turn.
                tk.Label(self.score_board_frame, text = player_on_move+", je had gelijk!", fg = text_color, bg = background_color, font = font+big).grid(row = 0, columnspan = 2, pady = (40,20))
            else:
                if played_answer == None:
                    tk.Label(self.score_board_frame, text = player_on_move+", je was te laat met antwoorden", fg = text_color, bg = background_color, font = font+big).grid(row = 0, columnspan = 2, pady = (40,20))                
                else: 
                    tk.Label(self.score_board_frame, text = player_on_move+", je had ongelijk :(", fg = text_color, bg = background_color, font = font+big).grid(row = 0, columnspan = 2, pady = (40,20))

        if type_of_question == "normal" or type_of_question == "photo":
            if played_answer == right_answer:
                score_board_header(True)
            else:
                score_board_header(False)
        elif type_of_question == "fillin":
            if played_answer == None:
                score_board_header(False)
            elif played_answer.issubset(right_answer) and len(played_answer) == number_of_answers_needed:
                score_board_header(True)
            else:
                score_board_header(False)
    
        tk.Label(self.score_board_frame, text = "Speler:", fg = text_color, bg = background_color, font = font+big+" bold").grid(row = 1, column = 0)
        tk.Label(self.score_board_frame, text = "score:", fg = text_color, bg = background_color, font = font+big+" bold").grid(row = 1, column = 1)
    
        row = 2
        for player in self.list_of_players:
            tk.Label(self.score_board_frame, text = player, fg = text_color, bg = background_color, font = font+big).grid(row = row, column = 0)
            tk.Label(self.score_board_frame, text = str(self.dictionary_of_players[player]), fg = text_color, bg = background_color, font = font+big).grid(row = row, column = 1)
            row += 1
        
        tk.Button(self.score_board_frame, text = "Volgende", width = 25, height = button_height, bg = background_color, font = font+small, command = lambda:[self.score_board_frame.destroy(), self.method_handler("players_in_round_or_turn_determiner")]).grid(row = row+2, columnspan = 2, pady = 10)
    
        self.index += 1 

    def players_in_round(self):
        """The players_in_round determines and shows which players continue to the next one and which don't

        The player in round window determines which players drop out. 
        whether players drop out is based on their score. The player(s)
        with the lowest score drop out. If all the players have the same
        (lowest) score, all the players continue for otherwise there would
        be no winner at all. When only one player is over, this is the winning
        player. In this case the GUI will show the "end" screen. 
        """

        self.players_in_round_frame = tk.Frame(self.canvas)       
        self.players_in_round_frame.configure(bg = background_color)
        self.canvas.create_window((400, 50), window=self.players_in_round_frame, anchor = "n")

        lowest_score = min(self.dictionary_of_players.values())
        losing_players = [player for player in self.dictionary_of_players if self.dictionary_of_players[player] == lowest_score]
        list_of_players_copy, dictionary_of_players_copy = self.list_of_players.copy(), self.dictionary_of_players.copy()
        for player in losing_players:
            del self.dictionary_of_players[player]
            self.list_of_players.remove(player)
        if len(self.list_of_players) == 0:
            self.list_of_players, self.dictionary_of_players = list_of_players_copy, dictionary_of_players_copy
            losing_players = []
        
        if len(self.list_of_players) == 1:
            db1 = Database("db4free.net", "lucschouten","trivia1234","triviadatabase") 
            new_score_of_winner = db1.retrieve_score(self.list_of_players[0], self.dictionary_of_passwords[self.list_of_players[0]], self.difficulty)[0][1] + 1
            db1.updatescore(self.list_of_players[0], self.dictionary_of_passwords[self.list_of_players[0]], self.difficulty, new_score_of_winner)
            db1.disconnect

            tk.Label(self.players_in_round_frame, text = self.list_of_players[0]+" Gefeliciteerd, je hebt gewonnen!", fg = text_color, bg = background_color, font = font+big).grid(row = 0, column = 0, pady = (50, 0))

            tk.Button(self.players_in_round_frame, text = "Leaderboard", width = 25, height = button_height, bg = background_color, font = font+small, command = lambda:[self.players_in_round_frame.grid_remove(), self.method_handler("leaderboard")]).grid(row = 1, column = 0, pady = (100,10))
            tk.Button(self.players_in_round_frame, text = "Opnieuw Beginnen", width = 25, height = button_height, bg = background_color, font = font+small, command = lambda:[self.players_in_round_frame.destroy(), self.start_frame()]).grid(row = 2, column = 0, pady = (0, 10))
            tk.Button(self.players_in_round_frame, text = "Stop", width = 25, height = button_height, bg = background_color, font = font+small, command = lambda:[root.destroy()]).grid(row = 3, column = 0)
        else: 
            row = 1
            tk.Label(self.players_in_round_frame, text = "Door naar de volgende ronde:", fg = text_color, bg = background_color, font = font+big+" bold").grid(row = row, column = 0, pady = (100,20))
            for player in self.list_of_players:
                row += 1
                tk.Label(self.players_in_round_frame, text = player, fg = text_color, bg = background_color, font = font+big).grid(row = row, column = 0)
            row += 1 
            if losing_players:
                tk.Label(self.players_in_round_frame, text = "Afvallers:", fg = text_color, bg = background_color, font = font+big+" bold").grid(row = row, column = 0, pady = (20,0))
                for loser in losing_players:
                    row += 1
                    tk.Label(self.players_in_round_frame, text = loser, fg = text_color, bg = background_color, font = font+big).grid(row = row, column = 0)
            tk.Button(self.players_in_round_frame, text = "Volgende Ronde", width = 15, height = 2, bg = background_color, font = font+small, command = lambda:[self.players_in_round_frame.destroy(), self.method_handler("turn_determiner")]).grid(row = row + 1, column = 0, pady = (30, 0))


root = tk.Tk()
root.geometry("800x700")
trivia_gui = GuiHandlerGeneral(root)
trivia_gui.start_frame()

root.mainloop()


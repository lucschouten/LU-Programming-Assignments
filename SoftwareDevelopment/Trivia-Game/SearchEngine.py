import random
import os
from sys import platform
from GetPathOfFile import get_path

def retrievequestions(category:str, difficulty_level:str, filename:str) -> list:
    """Returns a list with questions and answers.
    This functions first checks the filename and make sure it finds the right path to the questions files for every operating system.
    It returns all questions that correspond to the given category, difficulty level and file name.
    
    Args:
        category: category of the questions.
        difficulty_level: easy/medium/hard/extreme.
        filename: NormalQuestions.txt/PhotoQuestions.txt/FillinQuestions.txt"""

    file_path = get_path(filename)
    file = open(file_path,'r', encoding="utf8")
    data = file.read()
    file.close()
    
    categorydata = data.split('#')
    category_questions = list()
    for line in categorydata:
        categorysplit = line.split('\n')
        if category in categorysplit[0]:
            difficultysplit = line.split('&')
            for chunk in difficultysplit:
                levelquestions = chunk.split('\n')
                if difficulty_level in levelquestions[0]:
                    for level in levelquestions:
                        if difficulty_level in level:
                            continue
                        else:
                            category_questions.append(level)
    return category_questions

def get_questions(total_questions: int, difficulty_level = 'Random',question_type = 'Random') -> dict:
    """Makes a random set of questions that can be asked in the game.

    This function based on the specified questions, difficulty level and amount, returns a specific amount of questions as a dictionary.
    The dictionary consists of the questions as keys, and the answers as values.
    The Fill-in questions total answers that need to be correct to get a point are given in the last index of the values of the specific questions.
    The Photo questions photo files are also given in the last index of the values of the specific questions.

    Args:
        total_questions: the number of questions it has to return.
        difficulty_level: the specific difficulty level the questions that are returned must fall under: easy/medium/hard/extreme.
        question_type: the specific type of question that will be returned: NormalQuestions.txt/PhotoQuestions.txt/FillinQuestions.txt. """
    files =['NormalQuestion.txt','FillinQuestions.txt','PhotoQuestions.txt']
    if question_type == 'Normal':
        filename = files[0]
    elif question_type == 'Fill in':
        filename = files[1]
    elif question_type == 'Photo':
        filename = files[2]
    elif question_type == 'Random':
        rd_int= random.randint(0,1)
        filename = files[rd_int]

    categories = ['Wetenschap','Informatica','Geografie','Sport']
    difficulties = ['Easy','Medium','Hard','Extreme']
    temp_question_dict = dict() #Temporary dictionary
    temporary_cat_q = list() #Stores retrieved questions based on category and difficulty level
    question_set = set() #Random because it is unordered
    final_question_dict = dict()
    while len(final_question_dict) < total_questions: #To get the right amount of questions
        if difficulty_level == 'random':
            rd_int_cat = random.randint(0,len(categories)-1)
            rd_int_dif = random.randint(0,len(difficulties)-1)
            temporary_cat_q = retrievequestions(categories[rd_int_cat],difficulties[rd_int_dif],filename)
        else:
            rd_int_cat = random.randint(0,len(difficulties)-1)
            temporary_cat_q = retrievequestions(categories[rd_int_cat], difficulty_level,filename)
        question_answers = list()
        for line in temporary_cat_q:
            if '^' in line and len(question_answers) != 0:
                question = question_answers[0]
                answers = question_answers[1:]
                question_set.add(question) #Using a set for randomization
                temp_question_dict[question] = answers
                question_answers.clear()
                continue
            else:
                question_answers.append(line)

        if len(question_set) > 0:
            random_question = question_set.pop()
            if random_question in final_question_dict: #prevents double questions
                continue
            else:
                final_question_dict[random_question] = temp_question_dict[random_question]
    return final_question_dict

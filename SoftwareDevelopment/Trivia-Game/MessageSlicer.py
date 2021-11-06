import tkinter as tk
from tkinter import font 
import math

def fit_message(message: str, font_family: str, font_size: int) -> str:
    """Measures the width of a message.

    When the width of a message is to big, the message wil be passed
    to the slice_message function which will add new lines. if the 
    width of the message is not too big, the message is returned. 

    Args: 
        message: the question which the user in the qui has to answer 

    Returns:
        When the message is not to width for the gui, the message is 
        immediately returned, otherwise the message with new lines is 
        returned. 
    """
    used_font = font.Font(family=font_family, size=font_size, weight='normal')
    width = used_font.measure(message) #Measures the width of a message in terms of pixels. 
 
    def check_space(split: int) -> int:
        """This function looks for a whitespance in a line.

        After a whitespace is found, the position of the 
        whitespace is returned back so the message can be 
        splitted on the whitespace instead in the middle
        of a word. 

        Args:
            split: the index of a character in the message 

        Returns: 
            the index of the blank space in the message on
            which can be splitted. 
        """

        if split < len(message) and message[split] != " ": 
            split = split + 1
            return check_space(split)
        else: 
            return split

    def slice_message(message_to_split: str) -> str:
        """Function to split message to fit in the GUI.

        This Function splits messages to fit within
        the 800 pixels of the gui. When a message is
        too long to fit within the 800 pixels, it is 
        splitted onto several lines. 

        Args: 
            message_to_split: the question being asked to the user that 
            is to long to fit on the gui and therefore needs to be split 

        Returns: 
            The message which can be displayed in the gui. That is, the 
            passed message but now with added new lines. 
        """

        begin_slicer = 0
        end_slicer = characters_row
        sliced_message = ""
        while len(sliced_message) < len(message):
            end_slicer = check_space(end_slicer) #find some space in the message to split the message on 
            line = message[begin_slicer:end_slicer]

            if end_slicer >= len(message):
                sliced_message += line
            else:
                sliced_message += line+"\n"
                
            begin_slicer = end_slicer
            end_slicer += characters_row

        return sliced_message
    
    if width > 800: #the width of the gui is 800 pixels, so messages may not be wider than this. 
        times_to_split = math.ceil(width/800) 
        characters_row = math.ceil(len(message)/times_to_split) 
        return(slice_message(message)) #slice the message onto several lines 
    else:
        return message


#####################
# Message Classes
#####################
# Parent class for messages in the Adventure game
# There are three types of messages available:
# - A straight message that is printed, then a pause player out
# - A Random message from a list of possible messages to add a bit of variey
#   to the player interaction.
# - A MultiLine message from a list that plays out with a set delay. This is
#   used for printing out option lists and story elements.
#
# Each message has the message text and the delay for printing that message
# to the screen and pacing the story as it plays out.
#
# This may be overkill, but I was looking for a way of defining story
# elements and playing them out using a method, rather than having print
# functions through out the game engine.


#####################
# IMPORTS
#####################


import time
import random


#####################
# CONSTANTS
#####################


# Default delay for all messages setting a 0.5 second delay between lines
DEFAULT_DELAY = 1
# Option print out should be faster to keep things moving
OPTION_DELAY = 0.125
# The default screen is used to calculate when to issue a new line in
# multi line messages. This is used when constructing option lists.
DEFAULT_SCREEN = 80


#####################
# Message Class
#####################


class Message:
    def __init__(self, message, delay=DEFAULT_DELAY):
        # Set the message and the dealy for that message
        # If no dealy is provided, set the default delay
        self.message = message
        self.delay = delay

    def msg_print(self, message):
        # Print any message then sleep for "delay" seconds
        # Default time is 0.5s
        print(message)
        time.sleep(self.delay)

    # Print the message stored in the instance
    def print_msg(self): self.msg_print(self.message)

    # Return the text of the message
    def get_msg_text(self): return self.message

    # Return the length of the stored message
    def get_msg_len(self): return len(self.message)


#####################
# Random Message Class
#####################
# Class to print out random messages from a list of defined messages
# This class adds:
# - msgChoices list, which is a list of messages to select from
# - functions to handle random selection of messages
# - overrides the Message Class print_msg() function so that a radnom
#   message is selected and printed.


class RandomMsg(Message):
    def __init__(self, msgChoicesList, delay=DEFAULT_DELAY):
        # Initialise an array of possible messages
        self.msgChoices = msgChoicesList
        super().__init__('', delay)

    def set_random_msg(self):
        # Randomly select a message from the list of options and set it
        # to the message variable that will be printed out
        self.message = random.choice(self.msgChoices)

    def get_random_msg(self):
        # Chose a random message from the options and return it
        return random.choice(self.msgChoices)

    def print_msg(self):
        # Prints out a random message from the .message
        self.msg_print(self.get_random_msg())


#####################
# Multi Line Message Class
#####################
# Class to print out a multiline message with a pause between each line
# This class adds:
# - msgLines list, which is a list of lines to play out
# - over-rides the print_msg() function to loop over each lins


class MultiLineMsg(Message):
    def __init__(self, msgLinesList, delay=DEFAULT_DELAY):
        self.msgLines = msgLinesList
        super().__init__('NA', delay)

    def print_msg(self):
        # Prints our each line in the msgLines list using the inherited
        # print() function
        for line in self.msgLines:
            self.msg_print(line)

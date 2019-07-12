##########################################
# Import Supporting Data
##########################################
import advmessages
import story_data

OPTION_DELAY = advmessages.OPTION_DELAY

##########################################
# Class Option
##########################################
# Class to manage options available to a player based on conditions and
# location.
#
# An option maps a selector to a keyName that is used to handle the selected
# option


class Option:
    def __init__(self,
                 selector,
                 keyName,
                 optionDesc,
                 optionResp
                 ):
        #
        self.selector = selector
        self.keyName = keyName
        self.optionDesc = optionDesc
        self.optionResp = optionResp

    def get_selector(self): return self.selector


# The OptionList class has a list of options objects, and a list of valid
# options in the selector list. This is used to add and remove options based
# on the conditions of the game.
#
# The selector list is updated based on the available options for the
# current location and condtions.
#
# The option list presents the list of options to the player and validates
# input responses against the selector list until a valid option is selected.
#
# The keyName returned from a valid option is used to direct the next_action


class OptionList:
    def __init__(self):
        self.optionList = {}
        self.messages = {}
        self.messages['prefix'] = advmessages.Message(
                "\nYou have the following options"
                )
        self.messages['bad_option'] = advmessages.Message(
                "Sorry, that's not an option. Something else?"
                )
        self.messages['nothing_list'] =\
            advmessages.Message('There are no options.')

        self.update_selector_list()

    # is_valid is a check to ensure the items in the option list are
    # actually option objects. This is used for debugging issues
    # and to protect the game from errors.
    def is_valid(self, option): return isinstance(option, Option)

    def add(self, option):
        if self.is_valid(option):
            if option.keyName in self.optionList:
                print(f'WARNING: Overwriting option {option.keyName}.')
            self.optionList[option.keyName] = option
        else:
            print(f"Discarded element {element}. Not an Item object.")

    def update_selector_list(self):
        self.selectorList = []
        for option in self.optionList:
            if self.optionList[option].selector in self.selectorList:
                print(
                    f"WARNING: Duplicate selector {option.selector}. Ignoring"
                )
            else:
                self.selectorList.append(self.optionList[option].selector)

    def is_nothing(self, messageKey):
        # Check if there is nothing in the lsit and update the message
        # entry that is being checked for.
        #
        # If the element_list is empty, the value of the message will be
        # updated with the nothing message
        isNothing = len(self.optionList) == 0
        if isNothing:
            nothingText = self.messages['nothing_list'].get_random_msg()
            self.messages[messageKey].message_lines.append(nothingText)

        return isNothing

    def make_line_from_option(self, option):
        # Function to generate the line for the option that is send
        # in the options_list message to the player
        return f'{option.selector}. {option.optionDesc}'

    def make_per_line_list(self, messageKey, delay=OPTION_DELAY):
        # The option_list is a MultiLine message that is sent to the player
        # when it is time to choose the next action in the story.
        #
        # The list depends on the conditons of the game.
        # This function takes the updated optionList and generates
        # the option list message based on the contents of the optionList
        #
        # The messageKey is used to place the optionList message in the
        # messages dictionary.
        #
        # delay is used to change the pacing of the printing of the
        # optionList message. We want this to be faster to move the action
        # along.
        self.messages[messageKey] = advmessages.MultiLineMsg([], delay)

        # Add a random pre-fix line from the prefix_list
        self.messages[messageKey].msgLines.append(
                f"{self.messages['prefix'].get_msg_text()}:"
                )

        if not self.is_nothing(messageKey):
            for option in self.optionList:
                line = self.make_line_from_option(self.optionList[option])
                self.messages[messageKey].msgLines.append(
                        f"  {line}"
                        )

    def check_option_valid(self, inputOption):
        # Simple T/F check to see if the input string is in the list of options
        self.update_selector_list()
        return inputOption in self.selectorList

    def get_selected_option(self, selectedOption):
        for option in self.optionList:
            if self.optionList[option].selector == selectedOption:
                return self.optionList[option]

        print("WARNING - get_selected_option: No options matched input.")
        return ""

    def add_quit(self):
        # Define the option to quit the game, so that there is an opiton
        # to quit with every input request.
        quit = Option('q', 'quit', 'Quit the game.', 'Quitting...')
        return quit

    def really_quit(self):
        # Check that this is really what we want to do.
        # This feeds back to the choose_option loop which handles the response
        while True:
            rage_quit = input("Really quit (y/n)?")
            if rage_quit == "y":
                return True
            elif rage_quit == "n":
                return False

    def choose_option(self):
        # Funtion to chose an option from the option list
        # These generates the option list message from the current optionList
        # and prints it to the screen.

        self.make_per_line_list('option_list', OPTION_DELAY)
        self.messages['option_list'].print_msg()

        # We need to add the quit option to the end of the list.
        # Quit is not displayed in the options, but is always available.
        quit = self.add_quit()

        # Loop over the user input until we have a vaild reponse
        while True:
            optionSelector = input("\nChoose an option: ")

            # If we get quit, we need to feed that back up through the
            # calling functions to handle separately. This is done by
            # retuning the quit option object to the interact() function
            if optionSelector == "q":
                if self.really_quit():
                    return quit

            # If we don't see a quit request, check the input against the
            # selector list which was updated when the optionList was built.
            # These are the valid options and is a faster way of validating
            # the reponse than looping through every option object and
            # checking against the option.selector attribute.
            #
            # If we do get a valid option, return the option object so that
            # the option respose message can be played out and the option
            # keyName can be handled.
            elif self.check_option_valid(optionSelector):
                return self.get_selected_option(optionSelector)

            # Send the bad option message to prompt the user to try again.
            else:
                self.messages['bad_option'].print_msg()


##########################################
# Class Location
##########################################
# Class to track movement from room to room and run the room function that
# matches the current location. This class is based on a stateMachine
# that uses the currentLocation to manage transitions between states
# (ie: rooms)


class Room:
    def __init__(self):
        self.paths = {}
        self.conditions = {}
        self.messages = {}

    def add_path(self, keyName, nextRoom):
        # Function to add a path link to a next room to the room path
        # lookup. The state maching needs the next location object to change
        # state. The links are pre-defined for each room and accessed using
        # the keyName for the link.
        #
        if keyName in self.paths:
            print(f'WARNING: Replacing path {keyName} with {nextRoom}')
        self.paths[keyName] = nextRoom

    def arrival_message(self, player):
        # Check if the player has been here before and play the first visit
        # message if they haven't.
        if player.been_here():
            self.messages['on_arrival']['intro'].print_msg()
        else:
            self.messages['first_visit'].print_msg()
            player.add_place(self)

    def arrive(self, player):
        # Function that gets played when the player arrives at a new location
        # this updates the player location and plays out the arrival message

        player.location = (self)

        self.arrival_message(player)

    def is_selection_a_path(self, keyName):
        return keyName in self.paths

    def handle_get_sword(self, player):
        player.conditions['has_sword'] = True
        return 'no_path'

    def handle_eat_tim_tam(self, player):
        player.conditions['ate_tim_tam'] = True
        self.messages['eat_tim_tam'].print_msg()
        return 'no_path'

    def do_something(self, player):
        # The do_something() function handles user input.
        #
        # This interaction with the player is managed using the optionList
        # function choose_option which will return the selected option object.
        #
        # The returned object is then used to handle actions within a room
        # to play out story messages and update player conditions.

        # Request input from the player
        selection = self.options.choose_option()

        # If we are quitting, go to quit
        if selection.keyName == 'quit':
            return 'quit'

        # Provide feedback of which option was selected to the player
        selection.optionResp.print_msg()

        # Handle the selection
        if self.is_selection_a_path(selection.keyName):
            return selection.keyName
        elif selection.keyName == 'get_sword':
            return self.handle_get_sword(player)
        elif selection.keyName == 'eat_tim_tam':
            return self.handle_eat_tim_tam(player)
        else:
            return 'unmatched_action'

    def do_something_loop(self, player):
        # The do_something_loop() will loop over interactions with the
        # player within a room. It follows this sequence:
        # - Build the options for the room and populate the optionsList
        # - Request input from the player via the do_somthing() function
        # - Validate the responses from the do_something() function.
        #
        # The loop is controlled by the nextAction variable. The 'no_path'
        # keywork is used to indicate that the action does not involve
        # movement to another room, and we continue to loop.
        #
        # If the nextAction key matches 'quit', the quit message is passed
        # back to the calling functions to handle the quit process.
        #
        # If nextAction is set to a keyword that matches in the self.paths
        # we need to move to another room, and the keyName is returned via
        # the interact() function to the main gaim loop.
        #
        # The 'unmatched_action' message is used to trap the condition where
        # the do_something() function returnes an unexpected keyName.
        nextAction = 'no_path'

        while nextAction == 'no_path':
            # Build the options for the room
            self.build_options(player)

            # Call the do_something() function to request and process input
            # This will return a nextAction keywork that will be used to
            # direct the game.
            nextAction = self.do_something(player)

            # If we are quitting, pass a message up to the state maching
            if nextAction == 'quit':
                return nextAction

            # If we have an unmatched_action message, flag a warning
            # and stay in the current room. This stops the game from crashing
            # but provides a debug message that there is an issue with the
            # game keyNames.
            if nextAction == 'unmatched_action':
                print(f"WARNING: Unmatched action in {nextAction}.")
                nextAction = 'no_path'

            # If we don't get a 'no_path' message, check that we do
            # actually have a nameKey for the next room.
            elif nextAction in self.paths:
                # Path access is based on game conditons. Check that the path
                # is open before moving
                if not self.conditions['paths'][nextAction]['path_open']:
                    self.messages['paths'][nextAction]['path_closed']\
                            .print_msg()
                    nextAction = 'no_path'

        return nextAction

    def interact(self, player):
        # The interact() function is an interface between room movement and
        # and room interaction. It provides a control point to handle game
        # conditions that impact movement between rooms.
        #
        # Conditions are processed before calling the do_somthing_loop()
        # function.
        #
        # The default interact function has no conditions. This just
        # passes meessages between the do_something_loop and the next()
        # function in the main game loop.
        #
        # This can be overridden by rooms that do have conditions impacting
        # game movement.
        return self.do_something_loop(player)

    def next(self, nextRoomKey):
        # This function finds the next room object to pass back to the
        # state Machine functions. There are also controls added to
        # handle quitting the game.
        #
        # Links to the next rooms are defind in the self.paths dictionary
        #
        # The choice of path is returned to the next() function by the
        # interact() function which controls interaction with the player
        #
        # In all cases, we return a room object up to the controling state
        # machine. This will either run the next room, or re-run the current
        # room.

        # Check if the nextRoomKey is in the paths dictionary. We need a
        # valid key to access the associated room object.
        if nextRoomKey in self.paths:
            # If it is, return the next room object to the state machine
            # This will be the calling run() function.
            return self.paths[nextRoomKey]

        # If we don't have a room key, check if we want to quit
        elif nextRoomKey == 'quit':
            return nextRoomKey
        else:
            # If we don't match the nextRoomKey, and it isn't a control
            # the game is still under development. Send a warning and
            # stay in the current location. This will re-run the room.
            print(f"WARNING: Unknown path {nextRoomKey}.")
            return self

    def run(self, player):
        # The run function controls story action and movement between rooms.
        # It plays out the following sequence:
        # - Arrive in a room - send messages to the player based on state
        # - Update and respond to conditions
        # - Call the self.interact() function to handle player interaction.
        #
        # The interact function handles:
        # - Checking available options based on conditions
        # - Presenting options to the player
        # - Processing the selected option and update conditions
        #
        # The interact function will loop over player interactions via the
        # do_somthing functions until an option to move rooms is selected
        # or a quit option is selected.
        #
        # If key returned by the interact() function is passed to the
        # self.next() function to map the key to a room object.
        #
        # The Room object is used to update the currentLocation attribute in
        # Adventure object.
        #
        # If there is no match, a worrning is printed and run returns
        # itself. This restarts the cycle in the same room.
        #
        # If self.run() receives a 'quit' message, it will be returned.
        # A 'quit' messages will break the main loop.

        self.arrive(player)
        self.on_arrival_handle_conditions(player)

        return self.next(self.interact(player))

    def on_arrival_handle_conditions(self, player):
        # When the player arrive in the field, we want to check if the
        # troll is still around, and if they have eaten the tim tam
        self.on_arrival_handle_has_sword(player)
        self.on_arrival_handle_ate_tim_tam(player)
        self.on_arrival_handle_troll_around(player)

    def on_arrival_handle_troll_around(self, player):
        # If the troll is still around, we want to add messages to the field
        # story, because the cottage is nearby.
        if player.conditions['troll_around']:
            self.messages['on_arrival']['random_troll_around'].print_msg()

    def on_arrival_handle_ate_tim_tam(self, player):
        # The tim tam is key to getting access to the tree
        # You need to eat the tim tam before you can get to the tree
        if player.conditions['ate_tim_tam']:
            self.messages['on_arrival']['random_tim_tam'].print_msg()
        else:
            self.messages['on_arrival']['random_no_tim_tam'].print_msg()

    def on_arrival_handle_has_sword(self, player):
        # If you have the sword, your confidence grows
        if player.conditions['has_sword']:
            if player.conditions['troll_around']:
                self.messages['on_arrival']['random_troll_sword'].print_msg()
            else:
                self.messages['on_arrival']['random_no_troll_sword']\
                        .print_msg()
        else:
            self.messages['on_arrival']['random_no_sword'].print_msg()


class Field(Room):
    # The field is the central hub of the story.
    # If the troll is around, you can hear him in the field.
    # If the troll is aroung and you don't have the sword...
    # If you have the sword and the troll is around, it begins to glow.
    # If you have the sword and the troll is not around, it feels warm.
    # If you have eaten the tim tam, you can go to the quiet spot
    #
    # Each of these conditions changes the messages that are sent to the
    # player

    def __init__(self):
        super().__init__()
        self.messages = story_data.field_messages
        self.conditions = story_data.field_conditions

    def build_options(self, player):
        self.options = OptionList()
        self.options.add(
            Option(
                '1',
                'field_quietSpot',
                'Head to the tree to lie down.',
                advmessages.Message('You head over to the tree to lie down.')
            )
        )
        message = 'You make your way into the forest. It is dark.'
        self.options.add(
            Option(
                '2',
                'field_cave',
                'Head north into the forest.',
                advmessages.Message(message)
            )
        )
        self.options_handle_troll_around(player)

    def get_option_msg(self, dictKey, msgKey):
        return self.messages[dictKey][msgKey].get_random_msg()

    def options_handle_troll_around(self, player):
        # Different options are available based on the player conditions.
        # This function changes which messages get played out based on those
        # conditions.
        if player.conditions['troll_around']:
            cottageOptionDesc = self.get_option_msg(
                    'optDesc',
                    'random_troll_around'
                    )

            cottageOptionResp = advmessages.Message(
                    self.get_option_msg(
                        'optResp',
                        'random_troll_around',
                        )
                    )
        else:
            cottageOptionDesc = self.get_option_msg(
                    'optDesc',
                    'random_troll_gone'
                    )

            cottageOptionResp = advmessages.Message(
                    self.get_option_msg(
                        'optResp',
                        'random_troll_gone'
                        )
                    )

        self.options.add(
            Option(
                '3',
                'field_cottage',
                cottageOptionDesc,
                cottageOptionResp
                )
            )

    def handle_has_sword(self, player):
        # If the player has the sword, the path to the cottage is open.
        self.conditions['paths']['field_cottage']['path_open'] = True

    def handle_ate_tim_tam(self, player):
        # If the player has eaten the tim tam, the way to the quite spot
        # is open.
        self.conditions['paths']['field_quietSpot']['path_open'] = True

    def interact(self, player):
        # Override the default function to handle having the sword
        # We use this to open the path to the cottage
        if player.conditions['has_sword']:
            self.handle_has_sword(player)

        if player.conditions['ate_tim_tam']:
            self.handle_ate_tim_tam(player)

        return self.do_something_loop(player)


class Cave(Room):
    # We find the sword in the cave but there isn't much else to do. We need
    # to handle getting the sword in the options.
    #
    # The only available path is back to the field.
    def __init__(self):
        super().__init__()
        self.messages = story_data.cave_messages
        self.conditions = story_data.cave_conditions

    def build_options(self, player):
        self.options = OptionList()
        self.options.add(
            Option(
                '1',
                'cave_field',
                'Make your way back to the field.',
                advmessages.Message('You start the journey back to the field.')
            )
        )
        self.options_handle_sword(player)

    def options_handle_sword(self, player):
        if not player.conditions['has_sword']:
            message = \
                f'The {story_data.cave_weapon} feels warm in your hands.'

            self.options.add(
                    Option(
                        '2',
                        'get_sword',
                        f'Pick up the {story_data.cave_weapon}.',
                        advmessages.Message(message)
                    )
                )


class Cottage(Room):
    # The troll lives in the cottage. We need to defeat the troll before we
    # can get into the kitchen.
    #
    # From the cottage, we can go to the field or the kitchen.

    def __init__(self):
        super().__init__()
        self.messages = story_data.cottage_messages
        self.conditions = story_data.cottage_conditions

    def build_options(self, player):
        self.options = OptionList()
        self.options.add(
                Option(
                    '1',
                    'cottage_field',
                    'Step back into the field.',
                    advmessages.Message(
                        'You miander on back into the field.'
                        )
                    )
                )
        self.options.add(
                Option(
                    '2',
                    'cottage_kitchen',
                    'Burst into the kitchen.',
                    advmessages.Message(
                        'You kick open the the kitchen doors and rush inside.'
                        )
                    )
                )

    def interact_handle_troll(self, player):
        # When the player has the sword, and the Troll is around the troll
        # is defeated and we can finally go to the kitchen.
        #
        # We need to set the 'path_open' condition to True and play out the
        # troll_defeat part of the story. Plus the troll is no more.
        #
        # If the player does not have the sword, they are beaten and sent back
        # to the field and the way back is blocked.
        #
        # Return a path key 'cottage_field' to move the player back to the
        # field.
        #
        # Return 'no_path' to go into the do_something_loop.

        if player.conditions['has_sword']:
            player.conditions['troll_around'] = False
            self.conditions['paths']['cottage_kitchen']['path_open'] = True
            self.messages['defeat_troll'].print_msg()
            return 'no_path'
        else:
            self.messages['defeat_player'].print_msg()
            # We want to block coming back to the cottage until the sword
            # has been collected.
            # We use the path link to the field object in self.paths
            # to set the path condition on the field object.
            self.paths['cottage_field']\
                .conditions['paths']['field_cottage']['path_open'] = False
            return 'cottage_field'

    def interact(self, player):
        # This function overrides the default interact function so that
        # we can add handling of the troll story line.

        # If the troll is around, the story sends you back to the field.
        # you can't progress until you get the sword.
        if player.conditions['troll_around']:
            nextAction = self.interact_handle_troll(player)
            if nextAction != 'no_path':
                return nextAction
        # If we haven't gone somewhere else, do something here.
        return self.do_something_loop(player)


class Kitchen(Room):
    # The kitchen has the tim tam, which is needed to open the path to the
    # quiet spot. The only path is back to the cottage.
    def __init__(self):
        super().__init__()
        self.messages = story_data.kitchen_messages
        self.conditions = story_data.kitchen_conditions

    def build_options(self, player):
        self.options = OptionList()
        self.options.add(
                Option(
                    '1',
                    'kitchen_cottage',
                    'Step out of the kitchen.',
                    advmessages.Message(
                        'You make your way back out of the kitchen.'
                        )
                    )
                )
        self.options_handle_tim_tam(player)

    def options_handle_tim_tam(self, player):
        if not player.conditions['ate_tim_tam']:
            message = \
                'You tremble as you raise the last tim tam to your lips.'

            self.options.add(
                Option(
                    '2',
                    'eat_tim_tam',
                    'Eat the last tim tam.',
                    advmessages.Message(message)
                    )
                )


class Quiet_Spot(Room):
    # Getting to the quiet stop is the win condition. There are no options.
    # This plays out the first visit message and quits the game because we
    # are done.
    def __init__(self):
        super().__init__()
        self.messages = story_data.quietSpot_messages
        self.conditionsi = story_data.quietSpot_conditions

    def interact(self, player):
        # If we make it here, we have completed the game
        return 'quit'


class Player:
    def __init__(self):
        # We use conditions associated with a player object so that each
        # room can get a view of actions that have occured in other rooms
        # as that the story plays out. This is necessary if things need
        # to happen in order.
        #
        # This can also be used to add descriptive elements that may
        # help move the story along.
        self.conditions = {}
        self.conditions['ate_tim_tam'] = False
        self.conditions['has_sword'] = False
        self.conditions['troll_around'] = True

        # We want to change the story so that we only play the intro for each
        # room once. To do that, we dfeine a list to track which rooms the
        # player has been to.
        self.places = []

    def been_here(self):
        # Check the list of rooms a player has been to to see if they have
        # been there before.
        return self.location in self.places

    def add_place(self, location):
        # Adds a room to the list of rooms the player has been to
        self.places.append(location)


class Location:
    # This class tracks the state of the machine (or adventure) and records
    # the current location. This gets updated by the next() function in
    # each room that returns the object of the next location (or state).
    def __init__(self, initLocation):
        # When we start the game we need to set the current location to the
        # initial location
        self.currentLocation = initLocation


# An Adventure is a set of locations. Movement between these locations is
# like changing state. Each room has it's own story, but the story is
# influenced by what has happened so far in the story. Using a state machine
# makes for a neater transition between rooms and also make it easier to
# expand the game to add new locations.
class Adventure(Location):
    def __init__(self, story_data):
        # Read in the story data for the Adventure
        self.messages = story_data.adventure_messages
        self.player = Player()
        self.create_rooms()
        self.create_paths()

        # Set the state machine to an initial location
        # The story begins in the field
        Location.__init__(self, self.field)

    def create_rooms(self):
        # Locations
        self.field = Field()
        self.cave = Cave()
        self.cottage = Cottage()
        self.kitchen = Kitchen()
        self.quietSpot = Quiet_Spot()

    def create_paths(self):
        self.field.add_path('field_cave', self.cave)
        self.field.add_path('field_cottage', self.cottage)
        self.field.add_path('field_quietSpot', self.quietSpot)
        self.cave.add_path('cave_field', self.field)
        self.cottage.add_path('cottage_field', self.field)
        self.cottage.add_path('cottage_kitchen', self.kitchen)
        self.kitchen.add_path('kitchen_cottage', self.cottage)
        self.quietSpot.add_path('quietSpot_field', self.field)

    def start_game(self):
        self.messages['intro'].print_msg()

    def play_again(self):
        while True:
            quit = input('\nAgain (y/n)?')

            if quit == 'y':
                return True
            elif quit == 'n':
                return False

    def quit_game(self):
        print("\nYou depart from this world.")
        return self.play_again()

    def play_game(self):
        # Initiate the game
        self.start_game()

        # Run the game as a loop. This loop is based on a state machine
        # where each room represents a state, and each room runs in that
        # state.
        # Each room has it's own conditions that influence how the story
        # is told.
        while True:
            # Run a room. Once a room run cycle completes it will return
            # a quit message, or the next room to run.
            # We pass the room the player object so that game conditions
            # can be checked and acted on.
            nextLocation = self.currentLocation.run(self.player)
            if nextLocation != "quit":
                self.currentLocation = nextLocation
            else:
                return


##########################################
# Main functions
##########################################


def play_adventure():
    # Loop to initiate and play the game until the player quits
    play_on = True
    while play_on:
        adventure = Adventure(story_data)

        adventure.play_game()

        play_on = adventure.quit_game()


##########################################
# Main
##########################################


if __name__ == '__main__':
    play_adventure()

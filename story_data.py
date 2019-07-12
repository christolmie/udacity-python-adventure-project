##########################################
# Imports
##########################################


import advmessages
import random


##########################################
# Player Story Data
##########################################


player_item = random.choice([
    'rusty fork',
    'spatula',
    'pen',
    'bowling ball',
    'cheese grater'
    ])

cave_weapon = random.choice([
    'Sword of Open Wounds',
    'Hammer of Broken Hearts',
    'Crossbow of Denial'
    ])

##########################################
# Adventure Story Data
##########################################


adventure_messages = {}
adventure_messages['intro'] = advmessages.MultiLineMsg(
    [
        '',
        '',
        '',
        '',
        'Welcome to the game...',
        '',
        '',
        'You can quit at any time by pressing \'q\'.',
        '',
        '',
        '\nAs the dust settles and your eyes adjust to the light,',
        'you find yourself standing in a field.',
        '\nThe memory of everything you have been through weighs upon you.',
        'You feel exhausted and hungry. All you want to do is lie down.',
        f'\nFor some reason, you are holding a {player_item}. You don\'t feel safe.'
    ]
)


##########################################
# Field Story Data
##########################################


field_conditions = {}
field_conditions['paths'] = {}
field_conditions['paths']['field_cave'] = {}
field_conditions['paths']['field_cottage'] = {}
field_conditions['paths']['field_quietSpot'] = {}

field_conditions['paths']['field_cave']['path_open'] = True
field_conditions['paths']['field_cottage']['path_open'] = True
field_conditions['paths']['field_quietSpot']['path_open'] = False

field_messages = {}
field_messages['on_arrival'] = {}
field_messages['optDesc'] = {}
field_messages['optResp'] = {}
field_messages['paths'] = {}
field_messages['paths']['field_quietSpot'] = {}
field_messages['paths']['field_cottage'] = {}

field_messages['paths']['field_quietSpot']['path_closed'] = \
        advmessages.Message(
                'You don\'t have enough energy to get there. You need to eat something first.'
                )
field_messages['paths']['field_cottage']['path_closed'] = \
        advmessages.Message(
                'Going back to the cottage is not an option without a weapon.'
                )

field_messages['first_visit'] = advmessages.MultiLineMsg(
    [
        '',
        '',
         '\nAs you look around the field, you notice there is a cottage a short',
        'distance from where you are standing.',
        '\nThere is also a path leading into a dark forest heading off to the north.',
        '\nA shady tree is swaying nearby that looks like a nice place to lie down.'
    ]
)
field_messages['on_arrival']['intro'] = advmessages.Message(
        '\nYou are in the field.'
        )

field_messages['on_arrival']['random'] = advmessages.RandomMsg(
    [
        'The tree is looking very inviting.',
        'You feel the heat of the sun beating down.',
        'A gentle breese blows.'
        ]
    )

field_messages['on_arrival']['random_troll_around'] = advmessages.RandomMsg(
    [
        '\nYou hear banging and the clatter of utensils coming from the cottage.',
        '\nA muted but ominous growl comes from the cottage.',
        '\nYou can see something large and hairy through the window of the cottage.'
        ]
    )

field_messages['on_arrival']['random_tim_tam'] = advmessages.RandomMsg(
    [
        'You feel slightly energised from the tim tam, but still sleepy.',
        'The tim tam is doing its work. You feel a moments peace.',
        'You feel like you could dance.'
        ]
    )

field_messages['on_arrival']['random_no_tim_tam'] = advmessages.RandomMsg(
    [
        'Your stomach is growling at you.',
        'You really want something to eat.',
        'You feel like you could faint.'
        ]
    )

field_messages['on_arrival']['random_troll_sword'] = advmessages.RandomMsg(
    [
        f'The {cave_weapon} has subtle blue glow.',
        f'The warmth from the {cave_weapon} seems to increase.',
        f'The {cave_weapon} feels like it is humming.'
        ]
    )

field_messages['on_arrival']['random_no_troll_sword'] = advmessages.RandomMsg(
    [
        f'The {cave_weapon} feels dense and heavy in your hand.',
        f'The {cave_weapon} feels cold to touch.',
        f'The {cave_weapon} seems to stare at you blankly.'
        ]
    )

field_messages['on_arrival']['random_troll_no_sword'] = advmessages.RandomMsg(
    [
        f'The {player_item} feels cold to touch.',
        f'The {player_item} seems to stare at you blankly.',
        f'You feel vulnerable with just a {player_item} in your hand.',
        f'You begin to wonder why you have a {player_item} at all.'
        ]
    )

field_messages['on_arrival']['random_no_sword'] = advmessages.RandomMsg(
    [
        f'The {player_item} feels cold to touch.',
        f'The {player_item} seems to stare at you blankly.',
        f'You feel vulnerable with just a {player_item} in your hand.',
        f'You begin to wonder why you have a {player_item} at all.'
        ]
    )



field_messages['optDesc']['random_troll_around'] = advmessages.RandomMsg(
        [
            'Sneak over to the cottage.',
            'Quietly make your way towards the cottage.',
            'Head to the cottage and hope nothing notices.'
        ])

field_messages['optResp']['random_troll_around'] = advmessages.RandomMsg([
        'You do your best to sneak over to the cottage.',
        'You crouch as low as you can and move forward.',
        'You slowly creep towards the cottage.'
        ])

field_messages['optDesc']['random_troll_gone'] = advmessages.RandomMsg([
        'Walk over to the cottage.',
        'Strutt your way towards the cottage.',
        'Head to the cottage with confidence.'
        ])

field_messages['optResp']['random_troll_gone'] = advmessages.RandomMsg([
        'You mosey over to the cottage.',
        'You confidently walk to the cottage.',
        'You make your way over to the cottage.'
        ])

##########################################
# Cave Story Data
##########################################
cave_conditions = {}
cave_conditions['paths'] = {}
cave_conditions['paths']['cave_field'] = {}
cave_conditions['paths']['cave_field']['path_open'] = True


cave_messages = {}
cave_messages['on_arrival'] = {}
cave_messages['optDesc'] = {}
cave_messages['optResp'] = {}

cave_messages['first_visit'] = advmessages.MultiLineMsg(
    [
        '',
        '',
         '\nAfter what feels like forever battling your way through the thick',
        'undergrowth of the forest, you discover a cave entrance just visilble',
        'behind a rocky outcrop.',
        '\nYou feel vulnerable in the forest, so you make your way in,',
        'hoping it will provide a place to lie down.',
        '\nThe walls of the cave are damp and not very inviting.',
        'There isn\'t anywhere to lie down, so you press on a little further.',
        '\nIn the fading light you stumble over something and a clamour of',
        'falling metal assalts your ears.',
        '\nAs the noise subsides and you gather yourself, you realise you have',
        'stumbled over the remains of a legendary figure.',
        f'\nOn the floor of the cave your see the {cave_weapon}.',
        ''
    ]
)

cave_messages['on_arrival']['intro'] = advmessages.Message(
        '\nYou are in the cave.'
        )

cave_messages['on_arrival']['random'] = advmessages.RandomMsg(
    [
        'This is not a nice place. The stench of death starts to reach you.',
        'You start to long for the open field.',
        'There is nothing but darkness ahead of you.'
        ]
    )

cave_messages['on_arrival']['random_troll_around'] = advmessages.RandomMsg(
    [
        '\nThere is a disturbance in the force.',
        '\nYou feel like you have unfinished business at the cottage.',
        '\nYou start to wonder what\'s in the kitchen, but your fear rises.'
        ]
    )

cave_messages['on_arrival']['random_tim_tam'] = advmessages.RandomMsg(
    [
        'The joy of the tim tam leaves you as you assess the darkness.',
        'You have an epiphany. This place is not for you.',
        'The darkness seems to be gathering it\'s forces against you.'
        ]
    )

cave_messages['on_arrival']['random_no_tim_tam'] = advmessages.RandomMsg(
    [
        'Your stomach is growling at you and the sound echoes into darkness.',
        'You feel like you are on the edge of an epiphany. If only you could eat.',
        'Nothing here satisfies you. There is no rest here.'
        ]
    )

cave_messages['on_arrival']['random_troll_sword'] = advmessages.RandomMsg(
    [
        f'The {cave_weapon} has a faint blue glow.',
        f'The warmth of the {cave_weapon} increases when pointed towards the field.',
        f'The {cave_weapon} feels like it is singing a sad and hollow song.'
        ]
    )

cave_messages['on_arrival']['random_no_troll_sword'] = advmessages.RandomMsg(
    [
        f'The {cave_weapon} feels dense and heavy in your hand.',
        f'The {cave_weapon} feels cold to touch.',
        f'The {cave_weapon} seems to stare at you blankly.'
        ]
    )

cave_messages['on_arrival']['random_troll_no_sword'] = advmessages.RandomMsg(
    [
        f'The {player_item} feels useless and our of place.',
        f'The {player_item} seems to stare at you blankly.',
        f'You feel vulnerable with just a {player_item} in your hand.',
        f'You begin to wonder why you have a {player_item}.'
        ]
    )
cave_messages['on_arrival']['random_no_sword'] = advmessages.RandomMsg(
    [
        f'The {player_item} feels useless and our of place.',
        f'The {player_item} seems to stare at you blankly.',
        f'You feel vulnerable with just a {player_item} in your hand.',
        f'You begin to wonder why you have a {player_item}.'
        ]
    )



##########################################
# Cottage Story Data
##########################################
cottage_conditions = {}
cottage_conditions['paths'] = {}
cottage_conditions['paths']['cottage_field'] = {}
cottage_conditions['paths']['cottage_field']['path_open'] = True
cottage_conditions['paths']['cottage_kitchen'] = {}
cottage_conditions['paths']['cottage_kitchen']['path_open'] = False



cottage_messages = {}
cottage_messages['on_arrival'] = {}
cottage_messages['optDesc'] = {}
cottage_messages['optResp'] = {}

cottage_messages['first_visit'] = advmessages.MultiLineMsg(
    [
        '',
        '',
         '\nYour passage to the cottage does not go unnoticed.',
        '\nAs you draw near to the cottage, a massive and grotesque troll',
        'bursts through the kitchen door and starts labouring towards you.',
        '\nThe stench of neglect physically pushes you back as the heaving',
        'mass of ugliness encrouches.',
        ''
    ]
)

cottage_messages['on_arrival']['intro'] = advmessages.Message(
        '\nYou are outside the cottage.'
        )

cottage_messages['on_arrival']['random'] = advmessages.RandomMsg(
    [
        'The posibilities in the kitchen draw you closer.',
        'The sun is high above smiling upon you.',
        'Your limbs feel weak and your skin crawls.'
        ]
    )

cottage_messages['on_arrival']['random_troll_around'] = advmessages.RandomMsg(
    [
        '\nThe air is filled with stench and tension.',
        '\nThe beating of your heart sounds like stampeding horses.',
        '\nYour attempts an invisibility are met with derision.'
        ]
    )

cottage_messages['on_arrival']['random_tim_tam'] = advmessages.RandomMsg(
    [
        'The suffering of the past begins to fade. You feel like having a nap.',
        'You feel blessed and restored.',
        'The pain of regret feels distant as it fads in to forgotten memory.'
        ]
    )

cottage_messages['on_arrival']['random_no_tim_tam'] = advmessages.RandomMsg(
    [
        'Your stomach is growling at you, threating mutiny.',
        'The feelings of loss and regret start to overwhelm you.',
        'The end of your suffering feels so close, but still so far away.'
        ]
    )

cottage_messages['on_arrival']['random_troll_sword'] = advmessages.RandomMsg(
    [
        f'The {cave_weapon} is glowing brightly.',
        f'The heat from the {cave_weapon} is almost too much to bear.',
        f'The {cave_weapon} is vibrating violently.'
        ]
    )

cottage_messages['on_arrival']['random_no_troll_sword'] = advmessages.RandomMsg(
    [
        f'The {cave_weapon} feels dense and heavy in your hand.',
        f'The {cave_weapon} feels cold to touch.',
        f'The {cave_weapon} seems to stare at you blankly.'
        ]
    )

cottage_messages['on_arrival']['random_troll_no_sword'] = advmessages.RandomMsg(
    [
        f'The {player_item} runs off in fright.',
        f'The {player_item} emplores you to turn around.',
        f'You fear for your life with just a {player_item} in your hand.',
        ]
    )

cottage_messages['on_arrival']['random_no_sword'] = advmessages.RandomMsg(
    [
        f'The {player_item} ignores you.',
        f'You feel vulnerable with just a {player_item} in your hand.',
        f'You begin to wonder why you have a {player_item} at all.'
        ]
    )

cottage_messages['defeat_player'] = advmessages.MultiLineMsg([
    f'\nThe might of the {player_item} is not sufficient to protect you from',
    'the overwheling power of the troll\'s advance.',
    '\nAs the fowl stench consumes your nostriles, you reatch violently,',
    'and stumble backwards into the field. You keep going before the',
    'troll can do any damage.',
    f'\nYou vow not to come back without something more than a {player_item}',
    'for protection.'
    ])

cottage_messages['defeat_troll'] = advmessages.MultiLineMsg([
    '\nThe troll continues its advance and it takes all your strength to not',
    'melt into the ground. You plant your feet firmly and raise the ',
    f'{cave_weapon} in preparation for the attack.',
    '\nA moment of confusion appears on the trolls distorted face as',
    'he recognises the weapon you weild. In that moment, a blast of',
    'blinding blue light consumes the area in front of the field and',
    'you are thrown into the air.',
    '\nYou briefly pass to the beyond, but are snapped back into the now',
    'as you splatter onto the ground. You feel a shot of pain through your',
    'body, but you are still alive.',
    '\nSmodlering ashes are spead across the field, and a puddle of vile',
    'gloop pools in front of you.',
    '\nThe cottage is still here, but the troll is gone.'
    ])

##########################################
# Kitchen Story Data
##########################################
kitchen_conditions = {}
kitchen_conditions['paths'] = {}
kitchen_conditions['paths']['kitchen_cottage'] = {}
kitchen_conditions['paths']['kitchen_cottage']['path_open'] = True



kitchen_messages = {}
kitchen_messages['on_arrival'] = {}
kitchen_messages['optDesc'] = {}
kitchen_messages['optResp'] = {}

kitchen_messages['first_visit'] = advmessages.MultiLineMsg(
    [
        '',
        '',
         '\nYou take your guard as you burst into the kitchen, expecting another',
        'onslaught. The creaking of the kitchen door is the only thing',
        'challenging your presence as you begin to survey the scene before you.',
        '\nThe kitchen is cluttered, with pots and pans scattered everywhere.',
        'Steam rises from the kettle that is sitting on the stove. It is',
        'warm. You notice on the table an partly drunk cup of tea, and next',
        'to that something that almost brings tears to your eyes.',
        '\nSitting neatly on the unassuming table is a clear plastic',
        'container of individual compartments, with every compartment devoid',
        'of the joy they once held. All except one. The last on.',
        '\nAll the oppression and tragedy of the months preceeding seem',
        'unimportant to you now as you regard this sultry glory. Sitting',
        'patiently on its own, with no consideration for the eternity before...',
        '',
        '...the last time tam.',
        '',
        '',
    ]
)

kitchen_messages['on_arrival']['intro'] = advmessages.Message(
        '\nYou are in the kitchen.'
        )

kitchen_messages['on_arrival']['random'] = advmessages.RandomMsg(
    [
        'This is not a nice place. The stench of death starts to reach you.',
        'You start to long for the open field.',
        'There is nothing but darkness ahead of you.'
        ]
    )

kitchen_messages['on_arrival']['random_tim_tam'] = advmessages.RandomMsg(
    [
        'The joy will never leave you.',
        'You wonder why your are here. It\'s time to lie down.',
        'There is a sound from the field, is it calling your name?'
        ]
    )

kitchen_messages['on_arrival']['random_no_tim_tam'] = advmessages.RandomMsg(
    [
        'Pools of saliva gather on your chin as you regard the beauty.',
        'You are starting to question your life choices.',
        'You can\'t believe it\'s still here. Your starting to lose your mind.'
        ]
    )

kitchen_messages['on_arrival']['random_no_troll_sword'] = advmessages.RandomMsg(
    [
        f'The {cave_weapon} feels dense and heavy in your hand.',
        f'The {cave_weapon} feels cold to touch.',
        f'The {cave_weapon} seems to stare at you blankly.'
        ]
    )

kitchen_messages['eat_tim_tam'] = advmessages.MultiLineMsg(
    [
        '\nA wave of pleasure and joy flows through your body as you eagerly',
        'consume the final remaining tim tam. Regret and despair depart from',
        'your wilting soul and you sense the sun become warmer, a lasting',
        'peace decending upon your known universe.',
        '\nYou are at peace. Your energy is returning and you feel it is time',
        'to go and lie down.'
        ]
    )

##########################################
# Quiet Place Story Data
##########################################
quietSpot_conditions = {}
quietSpot_conditions['paths'] = {}
quietSpot_conditions['paths']['quietSpot_field'] = {}
quietSpot_conditions['paths']['quietSpot_field']['path_open'] = True



quietSpot_messages = {}
quietSpot_messages['on_arrival'] = {}
quietSpot_messages['optDesc'] = {}
quietSpot_messages['optResp'] = {}

quietSpot_messages['first_visit'] = advmessages.MultiLineMsg(
    [
        '',
        '',
         '\nThe tree casts a cooling shadow over a quiet open area in the field.',
        '\nIt has been too long, and the memories of the past swim around your',
        'troubled mind as you make yourself comfortable.',
        '\nWith the satifcation of knowing that you had the last tim tam,',
        'the sleep of the righteous starts to pull you under. You are not',
        'long for this world, and your caring rapidly decends towards zero.'
        '\nYour eyes close and you slip into the beyond.',
        '',
        'You are done.',
        '',
        '',
        ''
    ]
)

quietSpot_messages['on_arrival']['intro'] = advmessages.Message(
        '\n'
        )

quietSpot_messages['on_arrival']['random'] = advmessages.RandomMsg(
    [
        ''
        ]
    )

quietSpot_messages['on_arrival']['random_troll_around'] = advmessages.RandomMsg(
    [
        ''
        ]
    )

quietSpot_messages['on_arrival']['random_tim_tam'] = advmessages.RandomMsg(
    [
        ''
        ]
    )

quietSpot_messages['on_arrival']['random_no_troll_sword'] = advmessages.RandomMsg(
    [
        f'The {cave_weapon} feels dense and heavy in your hand.',
        f'The {cave_weapon} feels cold to touch.',
        f'The {cave_weapon} seems to stare at you blankly.'
        ]
    )



"""The data.

This module is used as a collection of data required for uploading to databases, also file can also be imported as a
module.
"""

# The names for name randomization:
protagonist_names = [
                     "Snake", "Duke", "Shepard", "Kratos", "Link", "Ellie", "Lara", "Jalen", "Gordon", "Jack", "James",
                     "Cloud", "Kyle", "Booker", "Sheppard", "Sam", "Max", "Frank", "Marcus", "Tracer", "Crash", "Spyro",
                     "Nathan", "Price", "Geralt", "Dante", "Ratchet"
                    ]

# The surnames for name randomization:
protagonist_surnames = [
                        "Smith", "Johnson", "Williams", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
                        "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Rodriguez",
                        "Lewis", "Walker", "Hughes", "Evans"
                       ]

# The basic protagonists for download:
protagonist_data = [
                    """INSERT INTO public."Protagonists" (
                                                            id, type, armor, level, strength, completed_tasks, name, 
                                                            health, passed_npcs, defeated_enemies, inventory
                                                         ) 
                    VALUES (
                            '1'::bigint, 'Human'::text, '2'::bigint, '1'::bigint, '2'::bigint, '{}'::text[], 
                            'Stan'::text, '10'::bigint, '{}'::text[], '{}'::text[], '{}'::text[]
                            )
                    returning id;"""
                    ]

# Tasks for filling the database:
tasks_data = [
                # № 1:
                '''
                INSERT INTO public."Tasks" (
                                            id, name, description, difficult
                                           ) 
                VALUES (
                        '1'::bigint, 'The first real deal...'::text, 'It seems to me that the wizard is friendly, but I 
                        will not call him hostile either. He promised me a good weapon if I could defeat lizard. Well, 
                        Ill need a weapon...'::text, 'EASY'::text
                       )
                returning id;
                ''',
                # № 2:
                '''
                INSERT INTO public."Tasks" (
                                            id, name, description, difficult
                                           ) 
                VALUES (
                        '2'::bigint, 'In Search Of The Strange.'::text, 'Little Tina told me to bring her an artifact 
                        from the lost forest. I hope no one will be there, otherwise I dont want to lose my life 
                        today.'::text, 'MEDIUM'::text
                       )
                returning id;
                '''
             ]

# NPCs for filling the database:
npcs_data = [
                # № 1:
                '''
                INSERT INTO public."NPCs" (
                                            id, name, item, description
                                          ) 
                VALUES (
                        '1'::bigint, 'Wizard with a gray beard'::text, 'Hermits cloaks'::text, 'In twilights hush, where shadows danced upon the walls, the venerable wizard Zorvath
                        stirred within his chambers deep beneath the earth. His eyes, aglow like embers from
                        a long-dead fire, flickered open, casting a warm, golden light across the dusty tomes that lined his shelves.'::text
                       )
                returning id;
                ''',
                # № 2:
                '''
                INSERT INTO public."NPCs" (
                                            id, name, description
                                          ) 
                VALUES (
                        '2'::bigint, 'Tiny Tina'::text, 'Girl 165 
                        centimeters tall. By all outward signs, the person is extremely loud, sharp, laughing non-stop'::text
                       )
                returning id;
                ''',
                # № 3:
                '''
                INSERT INTO public."NPCs" (
                                            id, name, item, description
                                          ) 
                VALUES (
                        '3'::bigint, 'The Tadpole'::text, 'The Old Cigare'::text, 'Man... or a girl... No, rather 
                        a creature of the middle kind. When it speaks, it seems that the voice comes from some long distance, like from a black 
                        hole. A pretty tall creature with two arms and a long tail, which is the third hand. If you 
                        look at his face, you can get lost... A terrible creature!'::text
                       )
                returning id;
                '''
               ]

# Enemies for filling the database:
enemies_data = [
                # № 1:
                '''
                INSERT INTO public."Enemies" (
                                               id, armor, health, agility, intelligence, strength, name
                                             ) 
                VALUES (
                        '1'::bigint, '3'::bigint, '3'::bigint, '1'::bigint, '1'::bigint, '2'::bigint, 'Big Lizard'::text
                       )
                returning id;
                ''',
                # № 2:
                '''
                INSERT INTO public."Enemies" (
                                               id, armor, health, agility, intelligence, strength, name
                                             ) 
                VALUES (
                        '2'::bigint, '2'::bigint, '2'::bigint, '3'::bigint, '2'::bigint, '5'::bigint, 'Goblin'::text
                       )
                returning id;
                ''',
                # № 3:
                '''
                INSERT INTO public."Enemies" (
                                              id, armor, health, agility, intelligence, strength, name
                                             ) 
                VALUES (
                        '3'::bigint, '4'::bigint, '3'::bigint, '3'::bigint, '2'::bigint, '6'::bigint, 'Fallen Angel'::text
                       )
                returning id;
                ''',
                # № 4:
                '''
                INSERT INTO public."Enemies" (
                                              id, armor, health, agility, intelligence, strength, name
                                             ) 
                VALUES (
                        '4'::bigint, '2'::bigint, '1'::bigint, '5'::bigint, '10'::bigint, '7'::bigint, 'Joker'::text
                       )
                returning id;
                '''
               ]

# Dialogs for filling the database:
dialogs_data = [
                # № 1 - Wizard:
                '''
                INSERT INTO public."Dialogs" (
                                              id, phrase, answer, number, location_id
                                             ) 
                VALUES (
                        '1'::bigint, 'Hey, hey. Youre talking?'::text, 'Good afternoon, hello.'::text, '1'::bigint, 
                        '2'::bigint
                       )
                returning id;
                ''',

                '''
                INSERT INTO public."Dialogs" (
                                              id, phrase, answer, number, location_id
                                             ) 
                VALUES (
                        '2'::bigint, 'Oh, thats great. Listen... I do not know what kind of world this is, but I am 
                        not used to it here. Can you tell me where we are?'::text, 'Of course, we are in Calanthor - A land of eternal summer and magical forests.
                        The place of residence of various kinds of creatures, goblins, orcs, sorcerers...
                        '::text, '2'::bigint, '2'::bigint
                       )
                returning id;
                ''',

                '''
                INSERT INTO public."Dialogs" (
                                              id, phrase, answer, number, location_id
                                             ) 
                VALUES (
                        '3'::bigint, 'Tell me, is this world real? Its just that theres nothing like it in my world.
                        '::text, 'Its hard to say. For whom as...'::text, '3'::bigint, '2'::bigint
                       )
                returning id;
                ''',

                '''
                INSERT INTO public."Dialogs" (
                                              id, phrase, answer, number, location_id
                                             ) 
                VALUES (
                        '4'::bigint, 'Can you tell me where I can find out more about this?.. The world?'::text, 'To be 
                        honest, I dont have an answer to your question. But I think that the 1641 square will help you. 
                        Just be careful, a certain lizard has been dominating there lately. By the way, if you decide to 
                        rid us of his despotism, I can give you something as a reward.'::text, '4'::bigint, '2'::bigint
                       )
                returning id;
                ''',

                '''
                INSERT INTO public."Dialogs" (
                                              id, phrase, answer, number, location_id
                                             ) 
                VALUES (
                        '5'::bigint, 'OK, thanks.'::text, '...'::text, '5'::bigint, '2'::bigint
                       )
                returning id;
                ''',
                # № 2 - Tiny Tina:
                '''
                INSERT INTO public."Dialogs" (
                                              id, phrase, answer, number, location_id
                                             ) 
                VALUES (
                        '6'::bigint, 'Hey, what the hell. What are you doing in this hole?'::text, 'AHAHAH a new 
                        guest... You know, its not so bad here (BOOM) somewhere nearby.'::text, '1'::bigint, 
                        '10'::bigint
                       )
                returning id;
                ''',

                '''
                INSERT INTO public."Dialogs" (
                                              id, phrase, answer, number, location_id
                                             ) 
                VALUES (
                        '7'::bigint, 'Okay... Listen, I want to get out of here, but I dont know how, could You help 
                        me?'::text, 'Well I do not know...'::text, '2'::bigint, '10'::bigint
                       )
                returning id;
                ''',

                '''
                INSERT INTO public."Dialogs" (
                                              id, phrase, answer, number, location_id
                                             ) 
                VALUES (
                        '8'::bigint, 'Im serious!'::text, 'Okay, traveler, I can give You something that will help you 
                        get out of here. But no more.'::text, '3'::bigint, '10'::bigint
                       )
                returning id;
                ''',

                '''
                INSERT INTO public."Dialogs" (
                                              id, phrase, answer, number, location_id
                                             ) 
                VALUES (
                        '9'::bigint, 'Fine, so...?'::text, 'Well, youre a weird, of course, thats not for nothing. 
                        You have to bring me a plush artifact that is located in the lost forest.'::text, '4'::bigint, 
                        '10'::bigint
                       )
                returning id;
                ''',

                '''
                INSERT INTO public."Dialogs" (
                                              id, phrase, answer, number, location_id
                                             ) 
                VALUES (
                        '10'::bigint, 'Well... I didnt expect anything else.'::text, 'So what?'::text, '5'::bigint, 
                        '10'::bigint
                       )
                returning id;
                ''',
                # № 3 - The Tadpole:
                '''
                INSERT INTO public."Dialogs" (
                                              id, phrase, answer, number, location_id
                                             ) 
                VALUES (
                        '11'::bigint, '...'::text, 'Greetings wanderer!'::text, '1'::bigint, '16'::bigint
                       )
                returning id;
                ''',

                '''
                INSERT INTO public."Dialogs" (
                                              id, phrase, answer, number, location_id
                                             ) 
                VALUES (
                        '12'::bigint, 'Hello.'::text, '...'::text, '2'::bigint, '16'::bigint
                       )
                returning id;
                ''',

                '''
                INSERT INTO public."Dialogs" (
                                              id, phrase, answer, number, location_id
                                             ) 
                VALUES (
                        '13'::bigint, 'You look a little strange.'::text, 'What do you think someone who knows 
                        everything about the world should look like?'::text, '3'::bigint, '16'::bigint
                       )
                returning id;
                ''',

                '''
                INSERT INTO public."Dialogs" (
                                              id, phrase, answer, number, location_id
                                             ) 
                VALUES (
                        '14'::bigint, 'Is that really all?... Wait, what kind of world are you talking about?'::text, 
                        'And which one are you interested in?'::text, '4'::bigint, '16'::bigint
                       )
                returning id;
                ''',

                '''
                INSERT INTO public."Dialogs" (
                                              id, phrase, answer, number, location_id
                                             ) 
                VALUES (
                        '15'::bigint, 'I really want to get out of this world, but I dont know how.'::text, 'Well, 
                        listen up.'::text, '5'::bigint, '16'::bigint
                       )
                returning id;
                ''',

                '''
                INSERT INTO public."Dialogs" (
                                              id, phrase, answer, number, location_id
                                             ) 
                VALUES (
                        '16'::bigint, 'You will need to turn right and find yourself near the stairs. After that, you 
                        must reach the last platform, where you will meet a undead. You will have two options: 1) kill 
                        him and pass by, 2) try to run with risk. After that, you will find yourself in a dark room, in 
                        which your fate will be determined.'::text, 'And whats next?'::text, '6'::bigint, '16'::bigint
                       )
                returning id;
                ''',

                '''
                INSERT INTO public."Dialogs" (
                                              id, phrase, answer, number, location_id
                                             ) 
                VALUES (
                        '17'::bigint, 'Then everything depends on your virtue.'::text, 'Ok...'::text, '7'::bigint, 
                        '16'::bigint
                        )
                returning id;
                '''

                ]

# Locations for filling the database:
locations_data = [
                    # № 1:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, name, bot_side, type, description, area
                                                   ) 
                    VALUES (
                            '1'::bigint, 'The Beginning Of The Story'::text, '2'::bigint, 'Empty'::text, 'I do not know 
                             what I am doing here, this is the place... Its weird. But I know for sure that I need to 
                            go.'::text, 'Abandoned Slums'::text
                           )
                    returning id;
                    ''',
                    # № 2:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, item, name, npc_id, top_side, bot_side, type, description, area
                                                   ) 
                    VALUES (
                            '2'::bigint, 'An Old Katana'::text, 'Park'::text, '1'::bigint, '1'::bigint, 
                            '3'::bigint, 'NPC'::text, 'I went out to a park, an unusual park, there are the trees stood huge and seemed to be alive. Ahead, I see a wizard. Its worth asking whats 
                            going on here.'::text, 'Abandoned Slums'::text
                           )
                    returning id;
                    ''',
                    # № 3:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, name, top_side, bot_side, enemy_id, type, description, area
                                                   ) 
                    VALUES (
                            '3'::bigint, 'The Area Of 1641'::text, '2'::bigint, '4'::bigint, '1'::bigint, 'Enemy'::text, 
                            'I followed the advice of the wizard. Thats how I ended up on the square in 1641. A crowd
                            of walking creatures resembles a colony of ants. What a world... Out of the corner of my 
                            eye, I notice that a huge armored lizard standing on two legs is staring at me intently. It
                            s not good...'::text, 'Abandoned Slums'::text
                           )
                    returning id;
                    ''',
                    # № 4:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, name, top_side, bot_side, type, left_side, right_side, 
                                                    description, area
                                                   ) 
                    VALUES (
                            '4'::bigint, 'Swampy lands'::text, '3'::bigint, '12'::bigint, 'Empty'::text, 
                            '5'::bigint, '9'::bigint, 'After the last one, we were lucky that I survived. Im in the 
                            middle of hell. On each of the four sides there are amazing, dissimilar worlds. Where should
                             I go?'::text, 'Dark Castle'::text
                           )
                    returning id;
                    ''',
                    # № 5:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, name, type, left_side, right_side, description, area
                                                   ) 
                    VALUES (
                            '5'::bigint, 'The Lull'::text, 'Empty'::text, '6'::bigint, '4'::bigint, 'I found myself in
                            a new world. Its buildings partly resembled villages. Low wooden and stone houses, paths 
                            without stone paving. There was even a rustle of tree leaves, or an imitation of them... 
                            I heard a terrible scream from the front, a scream that hurt my soul. I need to see whats 
                            inside.'::text, 'Danger Lane'::text
                           )
                    returning id;
                    ''',
                    # № 6:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, item, name, bot_side, enemy_id, type, right_side, description, 
                                                    area
                                                   )
                    VALUES (
                            '6'::bigint, 'Titanium Shackles'::text, 'Endless Forests'::text, '7'::bigint, 
                            '2'::bigint, 'Enemy'::text, '5'::bigint, 'I went out to the endless dense forests. It 
                            all looked like a pure evil. I couldnt even think that I would see these forests. It feels like they are empty. 
                            Although wait, there is still some kind of creature at 
                            the pile of corpse meat. Who could it be?'::text, 'Danger Lane'::text
                           )
                    returning id;
                    ''',
                    # № 7:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, name, top_side, type, left_side, description, area
                                                   ) 
                    VALUES (
                            '7'::bigint, 'Last Warning'::text, '6'::bigint, 'Empty'::text, '8'::bigint, 'I survived, 
                            thank God. But for some reason I have a feeling that I can die at any moment and its not 
                            worth relaxing. Well, I hope that these are just stupid thoughts, Ill move on... 
                            probably.'::text, 'Danger Lane'::text
                           )
                    returning id;
                    ''',
                    # № 8:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, name, type, right_side, description, area
                                                   )
                    VALUES (
                            '8'::bigint, 'Confrontation'::text, 'Trap'::text, '7'::bigint, 'I entered some kind of open space.
                             Its dark in here. After a while, the lights lit up around me. And with 
                             every second this space has narrowed, judging by their buzzing, they will saw me in two 
                             counts. This seems to be where my story ends...'::text, 'Plateau'::text
                           )
                    returning id;
                    ''',
                    # № 9:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, name, type, left_side, right_side, description, area
                                                   ) 
                    VALUES (
                            '9'::bigint, 'The Iron Yard'::text, 'Empty'::text, '4'::bigint, '10'::bigint, 'Judging by 
                            the inscriptions around me, I am in an iron courtyard, all the buildings are surprisingly 
                            made of iron, and all of them. Theyre rotting. Its not a pleasant sight, as they just didnt 
                            collapse everything here... Okay, I wont get distracted.'::text, 'Rotting Fields'::text
                           )
                    returning id;
                    ''',
                    # № 10:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, name, npc_id, top_side, type, left_side, description, area
                                                   ) 
                    VALUES (
                            '10'::bigint, 'Ship Graveyard'::text, '2'::bigint, '11'::bigint, 'NPC'::text, '9'::bigint, 
                            'The graveyard of ships, exactly, with such an inscription, the pointer meet me. Well, I 
                            admit that it is so. Huge abandoned ships with the size of houses. Each of them has its own 
                            history, somewhat reminiscent of veterans after the war. But what surprised me was that one 
                            of them didnt look like everyone else. It was on land, like everything else, it was painted
                             pink, and there was a... The girl. I need to ask her whats going on here.'::text, 'Rotting 
                             Fields'::text
                           )
                    returning id;
                    ''',
                    # № 11:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, item, name, bot_side, type, description, area
                                                   ) 
                    VALUES (
                            '11'::bigint, 'Guards Wreath'::text, 'Old Joes Ship'::text, '10'::bigint, 'Empty'::text, 
                            'As I should have been on assignment and came to old Joes ship. If a person could imagine 
                            how big it was, it would not compare to one tenth of the size of this vessel. Most of the 
                            inside was rotten through and through, but there were also surviving items. Its worth 
                            digging around...'::text, 'Rotting Fields'::text
                           )
                    returning id;
                    ''',
                    # № 12:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, name, top_side, bot_side, type, description, area
                                                   ) 
                    VALUES (
                            '12'::bigint, 'High Barriers'::text, '4'::bigint, '13'::bigint, 'Empty'::text, 'I found 
                            myself in a new neighborhood. Everything was white and gold. There was a huge staircase in 
                            front of me, the end of which was not visible, on either side of it stood statues of 
                            ancient heroes, at moments they changed their poses with the help of some internal 
                            mechanisms. Maybe theres a way out at the other end.'::text, 'Heavenly Ascent'::text
                           )
                    returning id;
                    ''',
                    # № 13:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, item, name, top_side, bot_side, type, description, area
                                                   ) 
                    VALUES (
                            '13'::bigint, 'Elf Box'::text, 'Is it a dream?'::text, '12'::bigint, '14'::bigint, 
                            'Empty'::text, 'I thought that this staircase was endless, but on some level to my right 
                            there was a room in the form of a closed square, it could only be entered through one door. 
                            At first I thought how it was in the air, then I noticed that the room was flying with the 
                            help of some magic power, like floating in electrified fields. Its worth going in and 
                            looking around, maybe theres someone there.'::text, 'Heavenly Ascent'::text
                           )
                    returning id;
                    ''',
                    # № 14:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, name, top_side, bot_side, type, left_side, right_side, 
                                                    description, area
                                                   ) 
                    VALUES (
                            '14'::bigint, 'The Next Level'::text, '13'::bigint, '17'::bigint, 'Empty'::text, 
                            '16'::bigint, '15'::bigint, 'I got tired and found myself on the next level, with almost 
                            two identical room boxes to my right and left. I need to decide where to go. My heart tells 
                            me to go left. Is it worth listening to him?'::text, 'Heavenly Ascent'::text
                           )
                    returning id;
                    ''',
                    # № 15:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, name, enemy_id, type, left_side, description, area
                                                   ) 
                    VALUES (
                            '15'::bigint, 'An Unpleasant Meeting'::text, '3'::bigint, 'Enemy'::text, '14'::bigint, 
                            'At first glance, an ordinary room, I even calmed down for a moment. But there is an oddity 
                            here... There are gold chains and spikes everywhere. Why would sacred elves need them? 
                            Footsteps sounded to my left, I turned around and saw an bright shine... An unusual creature'::text, 
                            'Heavenly Ascent'::text
                           )
                    returning id;
                    ''',
                    # № 16:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, item, name, npc_id, type, right_side, description, area
                                                   ) 
                    VALUES (
                            '16'::bigint, 'Golden Scorpion'::text, 'Is It A Surprise?'::text, '3'::bigint, 'NPC'::text,
                            '14'::bigint, 'An empty room, completely, from the outside it seemed several times smaller 
                            as it expanded, or is it a visual deception... Its weird in the middle... fuck knows who, 
                            but he doesnt seem to growl, so its worth trying to talk.'::text, 'Heavenly Ascent'::text
                           )
                    returning id;
                    ''',
                    # № 17:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, name, top_side, bot_side, enemy_id, type, 
                                                    description, area
                                                   ) 
                    VALUES (
                            '17'::bigint, 'The Last Battle'::text, '14'::bigint, '18'::bigint, '4'::bigint, 
                            'Enemy'::text, 'Maybe this is the way out, but... next to her is a funny guy who looks like 
                            a joker. I guess Ill have to have some fun with the jerk.'::text, 'Heavenly Ascent'::text
                           )
                    returning id;
                    ''',
                    # № 18:
                    '''
                    INSERT INTO public."Locations" (
                                                    id, name, top_side, type, description, required_item, area
                                                   ) 
                    VALUES (
                            '18'::bigint, 'That is all?'::text, '17'::bigint, 'Empty'::text, 'When I entered the door, 
                            I found myself in the dark. In the pitch darkness, I cant even hear my own breathing. 
                            However, there is a cell in front of me for an elder scroll, apparently something should 
                            be put here. Well, do I have this something...'::text, 'E-Key'::text, 'Heavenly 
                            Ascent'::text
                           )
                    returning id;
                    '''
                ]
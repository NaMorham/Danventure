import logging
import math
from time import sleep

logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.ERROR)


class Screen:
    class ScrFCol:
        NRM = "\033[0m"
        BOLD = "\033[1m"

        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        WHITE = "\033[37m"

        B_BLACK = "\033[90m"
        B_RED = "\033[91m"
        B_GREEN = "\033[92m"
        B_YELLOW = "\033[93m"
        B_BLUE = "\033[94m"
        B_MAGENTA = "\033[95m"
        B_CYAN = "\033[96m"
        B_WHITE = "\033[97m"

    class ScrBCol:
        BLACK = "\033[40m"
        RED = "\033[41m"
        GREEN = "\033[42m"
        YELLOW = "\033[43m"
        BLUE = "\033[44m"
        MAGENTA = "\033[45m"
        CYAN = "\033[46m"
        WHITE = "\033[47m"

        B_BLACK = "\033[100m"
        B_RED = "\033[101m"
        B_GREEN = "\033[102m"
        B_YELLOW = "\033[103m"
        B_BLUE = "\033[104m"
        B_MAGENTA = "\033[105m"
        B_CYAN = "\033[106m"
        B_WHITE = "\033[107m"

    class ScrFNone:
        NRM = ""
        BOLD = ""

        BLACK = ""
        RED = ""
        GREEN = ""
        YELLOW = ""
        BLUE = ""
        MAGENTA = ""
        CYAN = ""
        WHITE = ""

        B_BLACK = ""
        B_RED = ""
        B_GREEN = ""
        B_YELLOW = ""
        B_BLUE = ""
        B_MAGENTA = ""
        B_CYAN = ""
        B_WHITE = ""

    class ScrBNone:
        BLACK = ""
        RED = ""
        GREEN = ""
        YELLOW = ""
        BLUE = ""
        MAGENTA = ""
        CYAN = ""
        WHITE = ""

        B_BLACK = ""
        B_RED = ""
        B_GREEN = ""
        B_YELLOW = ""
        B_BLUE = ""
        B_MAGENTA = ""
        B_CYAN = ""
        B_WHITE = ""

    use_colour = True
    if use_colour:
        fg = ScrFCol
        bg = ScrBCol
    else:
        fg = ScrFNone
        bg = ScrBNone


class Directions:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    UP = 4
    DOWN = 5

    NUM_DIRS = 6


directions = [
    {"name": "North", "abbrev": "N"},
    {"name": "East", "abbrev": "E"},
    {"name": "South", "abbrev": "S"},
    {"name": "West", "abbrev": "W"},
    {"name": "Up", "abbrev": "U"},
    {"name": "Down", "abbrev": "D"}
]


class RoomTypes:
    DEV = 0
    GRASS = 1
    FOREST = 2
    INSIDE = 3
    ROAD = 4
    CITY = 5
    TRACK = 6
    WATER = 7
    HILLS = 8
    MOUNTAIN = 9

    # must be last - must be the highest number
    MAX = 10


'''
These values represent the data about different room types
'''
room_types = [
    {"id": RoomTypes.DEV, "name": "DEV", "mv_cost": 0},
    {"id": RoomTypes.GRASS, "name": "GRASS", "mv_cost": 3},
    {"id": RoomTypes.FOREST, "name": "FOREST", "mv_cost": 5},
    {"id": RoomTypes.INSIDE, "name": "INSIDE", "mv_cost": 1},
    {"id": RoomTypes.ROAD, "name": "ROAD", "mv_cost": 1},
    {"id": RoomTypes.CITY, "name": "CITY", "mv_cost": 2},
    {"id": RoomTypes.TRACK, "name": "TRACK", "mv_cost": 2},
    {"id": RoomTypes.WATER, "name": "WATER", "mv_cost": 8},
    {"id": RoomTypes.HILLS, "name": "HILLS", "mv_cost": 8},
    {"id": RoomTypes.MOUNTAIN, "name": "MOUNTAIN", "mv_cost": 10}
]


class Commands:
    NONE = 0
    LOOK = 1
    MOVE = 2
    EXITS = 3
    QUIT = 4
    HELP = 5
    SAY = 6

    NUM_CMDS = 7  # Must be last, must be largest number


commands = [
    {"id": Commands.NONE, "long": "NONE", "short": "", "args": {"min": 0, "max": 0}},
    {"id": Commands.LOOK, "long": "look", "short": "l", "args": {"min": 0, "max": 1}},
    {"id": Commands.EXITS, "long": "exits", "short": "x", "args": {"min": 0, "max": 0}},

    {"id": Commands.MOVE, "long": "move", "short": "m", "args": {"min": 1, "max": 1}},
    {"id": Commands.MOVE, "long": "north", "short": "n", "args": {"min": 0, "max": 0},
     "vals": {"direction": Directions.NORTH}},
    {"id": Commands.MOVE, "long": "east", "short": "e", "args": {"min": 0, "max": 0},
     "vals": {"direction": Directions.EAST}},
    {"id": Commands.MOVE, "long": "south", "short": "s", "args": {"min": 0, "max": 0},
     "vals": {"direction": Directions.SOUTH}},
    {"id": Commands.MOVE, "long": "west", "short": "w", "args": {"min": 0, "max": 0},
     "vals": {"direction": Directions.WEST}},
    {"id": Commands.MOVE, "long": "up", "short": "u", "args": {"min": 0, "max": 0},
     "vals": {"direction": Directions.UP}},
    {"id": Commands.MOVE, "long": "down", "short": "d", "args": {"min": 0, "max": 0},
     "vals": {"direction": Directions.DOWN}},

    {"id": Commands.QUIT, "long": "quit", "short": "q", "args": {"min": 0, "max": 0}},
    {"id": Commands.HELP, "long": "help", "short": "?", "args": {"min": 0, "max": 1}},
    {"id": Commands.SAY, "long": "say", "short": "'", "args": {"min": 1, "max": 100}},
]


def get_room_type_name(room_id):
    if (room_id >= RoomTypes.DEV) and (room_id < RoomTypes.MAX):
        name = room_types[room_id]["name"]
    else:
        name = "UNKNOWN"
    return name


NONE = -1
NOWHERE = -1
NOBODY = -1
NOTHING = -1

max_room_id = NONE

default_start_room = 1
dev_start_room = 0


def make_rooms():
    new_rooms = [
        {"id": 0, "name": "Dan's Dev Room", "type": RoomTypes.DEV,
         "desc": "This is a temporary dev room.  This is a plain white space for creating new stuff.",
         "exits": [NOWHERE, NOWHERE, NOWHERE, NOWHERE, NOWHERE, 1],
         "special": NONE, "looks": []},

        {"id": 1, "name": "The South Garden", "type": RoomTypes.GRASS,
         "desc": "This is a beautiful and lush garden.  The grass is green and there are flowers and trees all " +
                 "around the place.",
         "exits": [2, NOWHERE, NOWHERE, NOWHERE, NOWHERE, NOWHERE],
         "special": NONE, "looks": [
            {"name": "grass", "desc": "The grass is very lush and a health green."},
            {"name": "trees", "desc": "Tall, medium and short, the trees are lush and healthy."},
            {"name": "flowers", "desc": "Small white and yellow flowers are in the garden beds."}]},

        {"id": 2, "name": "Outside the House", "type": RoomTypes.TRACK,
         "desc": "A small garden outside the front entrance.  Small garden beds full of flowers line the grass " +
                 "beside the path.",
         "exits": [3, 4, 1, NOWHERE, NOWHERE, NOWHERE],
         "special": NONE, "looks": [
            {"name": "grass", "desc": "The grass is very lush and a health green."},
            {"name": "flowers", "desc": "Small white and yellow flowers are in the garden beds."},
            {"name": "path", "desc": "A neat gravel path."}]},

        {"id": 3, "name": "The north garden", "type": RoomTypes.GRASS,
         "desc": "This is a lush and beautiful garden.  The grass is green and there are flowers and trees all " +
                 "around the place.",
         "exits": [NOWHERE, NOWHERE, 1, NOWHERE, NOWHERE, NOWHERE],
         "special": NONE, "looks": [
            {"name": "grass", "desc": "The grass is very lush and a health green."},
            {"name": "trees", "desc": "Tall, medium and short, the trees are lush and healthy."},
            {"name": "flowers", "desc": "Small white and yellow flowers are in the garden beds."}]},

        {"id": 4, "name": "Inside the Entrance Hall", "type": RoomTypes.INSIDE,
         "desc": "A small square room acts as an entrance to a dark hallway.  There is a small painting on the wall " +
                 "and the floor is covered by a carpet.",
         "exits": [NOWHERE, 5, NOWHERE, 2, NOWHERE, NOWHERE],
         "special": NONE, "looks": [
            {"name": "painting", "desc": "A small painting of a bowl of fruit."},
            {"name": "carpet", "desc": "The carpet is made of soft green wool."}]},

        {"id": 5, "name": "A Dark Hallway", "type": RoomTypes.INSIDE,
         "desc": "This hallway is long and quite dark.  The floor feels soft and deadens the sound a little.  " +
                 "Empty candle holder can just be seen on the walls.",
         "exits": [NOWHERE, 6, NOWHERE, 4, NOWHERE, NOWHERE],
         "special": NONE, "looks": []},

        {"id": 6, "name": "A Nexus in the Hallway", "type": RoomTypes.INSIDE,
         "desc": "The hallway comes to an end and rooms branch off it.  Food smells drift in from the" +
                 "north and there is a small room to the south.  The soft carpet is ragged here.",
         "exits": [7, 9, 8, 5, NOWHERE, NOWHERE],
         "special": NONE, "looks": []},

        {"id": 7, "name": "The Kitchen", "type": RoomTypes.INSIDE,
         "desc": "A large wooden table is in the center of the kitchen.  Small cupboards line the walls.",
         "exits": [NOWHERE, NOWHERE, 6, NOWHERE, NOWHERE, NOWHERE],
         "special": NONE, "looks": []},

        {"id": 8, "name": "A Small Bedroom", "type": RoomTypes.INSIDE,
         "desc": "This room is rather small, but the floor is soft and the walls are brightly coloured.",
         "exits": [6, NOWHERE, NOWHERE, NOWHERE, NOWHERE, NOWHERE],
         "special": NONE, "looks": []},

        {"id": 9, "name": "The Back Room", "type": RoomTypes.INSIDE,
         "desc": "This large room has large windows and a set or stairs going up to the next floor.  There is also " +
                 "a large wooden door that has been wedged open.",
         "exits": [NOWHERE, 11, NOWHERE, 6, 10, NOWHERE],
         "special": NONE, "looks": []},

        {"id": 10, "name": "The Attic", "type": RoomTypes.INSIDE,
         "desc": "This dark and dusty room has a lot of junk scattered around the place.  The is a small window " +
                 "looking out over the city.",
         "exits": [NOWHERE, NOWHERE, NOWHERE, NOWHERE, NOWHERE, 9],
         "special": NONE, "looks": []},

        {"id": 11, "name": "A Small Alleyway", "type": RoomTypes.CITY,
         "desc": "A Small Alleyway",
         "exits": [NOWHERE, NOWHERE, NOWHERE, 9, NOWHERE, NOWHERE],
         "special": "City_Bell", "looks": [
            {"name": "dirt", "desc": "small piles of dirt and rubbish line the alleyway"}]}
    ]

    global max_room_id
    for r in new_rooms:
        if r["id"] > max_room_id:
            max_room_id = r["id"]

    return new_rooms


def find_room(room_id, rooms):
    rm = {}
    global max_room_id
    if (room_id >= 0) or (room_id <= max_room_id):
        for r in rooms:
            if r["id"] == room_id:
                rm = r
    return rm


def print_exit_detail(dr, room, rooms):
    """
    :param dr:
    :param room:
    :param rooms:
    :return:
    """
    global directions
    if (dr < Directions.NORTH) or (dr >= Directions.NUM_DIRS):
        # bad direction
        return
    elif len(room) == 0:
        # bad room
        return
    elif len(room["exits"]) < Directions.NUM_DIRS:
        # room has bad exits
        return

    exits = room["exits"]
    ext = exits[dr]
    if ext != NOWHERE:
        print('\t{yel}{dname:5s}: [{cyan}{exnum:3d}:{exname}{yel}]{norm}'.format(yel=Screen.fg.YELLOW,
              cyan=Screen.fg.CYAN, norm=Screen.fg.NRM, exnum=ext,
              exname=find_room(ext, rooms)["name"], dname=directions[dr]["name"]))
    return


def print_room_details(room_id, rooms):
    global max_room_id
    if (room_id > max_room_id) or (room_id < 0):
        return
    else:
        rm = find_room(room_id, rooms)
        if len(rm) >= 1:
            print('--------------------------------------------------------')
            print('{yel}Num: [{cyan}{rnum:5d}{yel}], Name: [{cyan}{rname}{yel}], '
                  'Type [{cyan}{rtype}:{rtypes}{yel}]{norm}'
                  .format(yel=Screen.fg.YELLOW, cyan=Screen.fg.CYAN, norm=Screen.fg.NRM, rnum=rm["id"],
                          rname=rm["name"], rtype=rm["type"], rtypes=room_types[rm["type"]]["name"]))
            print('{yel}Description:{norm}'.format(yel=Screen.fg.YELLOW, norm=Screen.fg.NRM))
            print('{cyan}{rdesc}{norm}'.format(norm=Screen.fg.NRM, cyan=Screen.fg.CYAN, rdesc=rm["desc"]))
            print('{yel}Exits:{norm}'.format(yel=Screen.fg.YELLOW, norm=Screen.fg.NRM))
            print_exit_detail(Directions.NORTH, rm, rooms)
            print_exit_detail(Directions.EAST, rm, rooms)
            print_exit_detail(Directions.SOUTH, rm, rooms)
            print_exit_detail(Directions.WEST, rm, rooms)
            print_exit_detail(Directions.UP, rm, rooms)
            print_exit_detail(Directions.DOWN, rm, rooms)
            if len(rm["looks"]) >= 1:
                print('{yel}Extras:{norm}'.format(yel=Screen.fg.YELLOW, norm=Screen.fg.NRM))
                for lk in rm["looks"]:
                    print("{yel}Name: [{cyan}{lname}{yel}], Description: [{cyan}{ldesc}{yel}]{norm}".format(
                        yel=Screen.fg.YELLOW, cyan=Screen.fg.CYAN, norm=Screen.fg.NRM,
                        lname=lk["name"], ldesc=lk["desc"]))


def test_all_rooms(rooms):
    """
    print all rooms

    :param rooms:  a list of all rooms as unordered dictionaries
    :return:
    """
    # print("\033[30m*\033[31m*\033[32m*\033[33m*\033[34m*\033[35m*\033[36m*\033[37m*\033[0m")
    # print("\033[97;40m*\033[97;41m*\033[97;42m*\033[97;43m*\033[97;44m*\033[97;45m*\033[97;46m*\033[97;47m*\033[0m")
    # print("\033[90m*\033[91m*\033[92m*\033[93m*\033[94m*\033[95m*\033[96m*\033[97m*\033[0m")
    # print("\033[30;100m*\033[97;101m*\033[97;102m*\033[97;103m*\033[97;104m*\033[97;105m*\033[97;106m*\033[30;107m*\033[0m")
    print("There are [{}] rooms in the world".format(len(rooms)))
    for r in rooms:
        print_room_details(r["id"], rooms)
        print()
    logging.debug("Room test dump finished.")


def room_get_exits(room_id, rooms):
    """
    return a list of valid directions
    :param room_id:  the id of the room to search
    :param rooms:  a list of rooms to search
    :return: a list of valid direction ID's
    """
    exits = []
    rm = find_room(room_id, rooms)
    if len(rm) == 0:
        # couldn't find it :(
        logger.error('Attempt to get exits for invalid room with id [{}]'.format(room_id))
    else:
        rm_exits = rm["exits"]
        if len(rm_exits) == 0:
            # no exists in the room
            logger.error('Player in room with no exits, returning to start')
            print('You are somehow stuck, teleporting you to the start room')
            player["room"] = default_start_room
        else:
            for dr, x in enumerate(rm_exits):
                if x != NOWHERE:
                    dr_info = directions[dr]
                    exits.append(dr_info["abbrev"])

    return exits


def can_go(player, dr, rooms):
    """
    Check if a player is capable of going in a direction
    :param player:  The player that is moving
    :param dr:  The direction they want to move
    :param rooms:  All of the rooms to check
    :return:  True/False if they can pass, the cost to move and the destination ID
    """
    rm = find_room(player["room"], rooms)
    # Is it a valid direction?
    if (dr < Directions.NORTH) or (dr >= Directions.NUM_DIRS):
        logger.error("Invalid direction [{}]".format(dr))
        print('{red}Cannot figure out how to go {dr_num}{norm}'.format(red=Screen.fg.RED, norm=Screen.fg.NRM,
                                                                       dr_num=dr))
        return False, 0, NOWHERE

    # is there an exit
    if len(rm) == 0:
        logger.error("Invalid room [{}]".format(player["room"]))
        print('{red}Cannot determine the players room {r_num}{norm}'.format(red=Screen.fg.RED, norm=Screen.fg.NRM,
                                                                            r_num=player["room"]))
        return False, 0, NOWHERE

    # does the exit exist?
    exit_rm_num = rm["exits"][dr]
    if exit_rm_num == NOWHERE:
        logger.error("Invalid exit [{}] from room [{}]".format(directions[dr]["name"], player["room"]))
        print('{red}The exit {d_name} does not lead anywhere{norm}'.format(red=Screen.fg.RED, norm=Screen.fg.NRM,
                                                                           d_name=directions[dr]["name"]))
        return False, 0, NOWHERE

    # does the exit lead somewhere?
    dest_rm = find_room(exit_rm_num, rooms)
    if len(dest_rm) == 0:
        logger.error("Invalid destination room [{}] from [{}]".format(player["room"], dest_rm))
        print('{red}The exit {d_name} does not lead anywhere{norm}'.format(red=Screen.fg.RED, norm=Screen.fg.NRM,
                                                                           d_name=directions[dr]["name"]))
        return False, 0, NOWHERE

    # does the player have enough moves left
    from_type = room_types[rm["type"]]                      # get the from type
    to_type = room_types[dest_rm["type"]]                   # get the to type
    ave = (from_type["mv_cost"] + to_type["mv_cost"]) / 2   # get the average cost of the 2 rooms
    mv_needed = int(math.ceil(ave))                         # must be an integer
    if mv_needed > player["moves"]:
        print("You're too tired to go that way")
        return False, 0, NOWHERE

    # does the player have permission to go there (only Dan in dev rooms)
    if to_type == RoomTypes.DEV:
        if player.get("admin", False):
            print("You are not a dev.  only dev's are allowed in there")
            return False, 0, NOWHERE

    # TODO: Other things....
    #    Are they sitting r standing
    #    Are they fighting
    #    Is there a door...
    return True, mv_needed, exit_rm_num


def move_player(player, to_id, from_id, rooms, cost):
    logging.debug("Move player {} from room [{}] to room [{}]".format(player["name"], from_id, to_id))
    if player["moves"] < cost:
        pass  # no move
    elif to_id == NOWHERE:
        pass  # bad destination
    elif len(find_room(to_id, rooms)) == 0:
        pass  # missing destination
    else:
        player["moves"]
        player["moves"] -= cost
        player["room"] = to_id
        logging.debug('Player now has {} moves'.format(player["moves"]))
    return


def get_prompt_string(player):
    s = "Health: "
    pct_h = (float(player["health"])/float(player["max_health"])) * 100.0
    if pct_h < 5.0:  # badly hurt
        col_s = Screen.fg.B_RED
    elif pct_h < 20.0:
        col_s = Screen.fg.RED
    elif pct_h < 70.0:
        col_s = Screen.fg.YELLOW
    elif pct_h < 70.0:
        col_s = Screen.fg.BLUE
    else:
        col_s = Screen.fg.B_CYAN
    s += "{col}{hp}/{max_hp}{norm}".format(col=col_s, norm=Screen.fg.NRM,
                                           hp=player["health"], max_hp=player["max_health"])
    s += " Moves: "
    pct_m = (float(player["moves"])/float(player["max_moves"])) * 100.0
    if pct_m < 5.0:  # badly hurt
        col_s = Screen.fg.B_RED
    elif pct_m < 20.0:
        col_s = Screen.fg.RED
    elif pct_m < 70.0:
        col_s = Screen.fg.YELLOW
    elif pct_m < 70.0:
        col_s = Screen.fg.BLUE
    else:
        col_s = Screen.fg.B_CYAN
    s += "{col}{mv}/{max_mv}{norm}".format(col=col_s, norm=Screen.fg.NRM,
                                           mv=player["moves"], max_mv=player["max_moves"])
    s += ":"
    return s


def look_at_room(player, rooms):
    if player["room"] == NOWHERE:
        print('Floating in the VOID, just look at all the stars!')
    elif player["room"] < 0 or player["room"] > max_room_id:
        print('Falling !!!!  Somehow you are outside the world, returning you to the start')
        player["room"] = default_start_room
        look_at_room(player, rooms)
    else:
        rm = find_room(player["room"], rooms)
        if len(rm) != 0:
            # Remember that this appears white in pycharm :(
            print('{wht}{rname}{norm}'.format(wht=Screen.fg.BLACK, norm=Screen.fg.NRM, rname=rm["name"]))
            print('{mag}{rdesc}{norm}'.format(mag=Screen.fg.MAGENTA, norm=Screen.fg.NRM, rdesc=rm["desc"]))
            ex = rm["exits"]
            if len(ex) == 0:
                print("{yel}Exits: [{cyn} None {yel}]{norm}".format(yel=Screen.fg.YELLOW, cyn=Screen.fg.CYAN,
                      norm=Screen.fg.NRM))
            else:
                exits = room_get_exits(player["room"], rooms)
                print("{yel}Exits: [{cyn} {e_str} {yel}]{norm}".format(yel=Screen.fg.YELLOW, cyn=Screen.fg.CYAN,
                      norm=Screen.fg.NRM, e_str=' '.join(exits)))
    return


def get_command(player, command_txt):
    global commands
    command_txt = str(command_txt).lstrip().rstrip().lower()
    args = command_txt.split(' ')
    logging.debug('Got command test [{}] - {} args'.format(command_txt, len(args)))
    if len(command_txt) == 0:
        print('You need to type a command')
    else:
        for cmd in commands:
            if cmd["id"] == Commands.NONE:
                continue  # skip the "NONE" command
            elif (cmd["long"] == args[0]) or (cmd["short"] == args[0]):
                # we found it!!!!
                logging.debug('Found command [{}:{}]'.format(cmd["id"], cmd["long"]))
                # check the args
                vals = {}
                if "vals" in cmd:
                    vals.update(cmd["vals"])
                return cmd["id"], cmd, vals

    return Commands.NONE, commands[Commands.NONE], {}


def main():
    player = {"name": "Bob", "room": default_start_room, "moves": 20, "max_moves": 20, "health": 10, "max_health": 10,
              "stuff": [], "admin": False}

    running = True
    counter = 0

    logging.info('Load all rooms')
    all_rooms = make_rooms()
    test_all_rooms(all_rooms)
    print('\n\n\n\n')
    while True:
        new_name = input("What is your name: ").lstrip().rstrip()
        if new_name == '':
            print('You must have a name, try again')
        elif new_name.lower() == 'dan':
            player["name"] = "Dangerous Daniel"
            player["room"] = dev_start_room
            player["admin"] = True
            player["moves"] = 100
            player["max_moves"] = 100
            player["health"] = 100
            player["max_health"] = 100
            break
        else:
            player["name"] = new_name
            player["room"] = default_start_room
            break
        # end while True
    print('Hello {}, welcome to the world'.format(player["name"]))
    look_at_room(player, all_rooms)

    logging.info('Start main loop')
    while running:
        counter += 1
        logging.debug('Counter is at {}'.format(counter))

        if counter == 20:
            logging.info('Game is now quitting')
            running = False

        cmd_txt = input("{} Command: ".format(get_prompt_string(player)))
        cid, cmd, vals = get_command(player, cmd_txt)

        if cid == Commands.NONE:
            print("I don't understand the command [{}], try again".format(cmd_txt))

        elif cid == Commands.LOOK:
            if len(vals) == 0:
                look_at_room(player, all_rooms)
            else:
                print('Cannot look at things yet')

        elif cid == Commands.QUIT:
            print('Goodbye')
            running = False
            continue

        elif cid == Commands.MOVE:
            if len(vals) == 0:
                print("Move where?")
            else:
                m_dir = vals["direction"]
                # check if the abbreviation for this direction is in the exit list
                if directions[m_dir]["abbrev"] not in room_get_exits(player["room"], all_rooms):
                    print('You cannot go {} from here'.format(directions[m_dir]["name"]))
                else:
                    can_pass, cost, dest_id = can_go(player, m_dir, all_rooms)
                    if can_pass and (cost > 0) and (dest_id != NOWHERE):
                        move_player(player, dest_id, player["room"], all_rooms, cost)
                        look_at_room(player, all_rooms)
        else:
            print("Unknown command [{}], try again".format(cmd_txt))

        print()
        # end while running

        print()
        sleep(1)  # wait 1 second


if __name__ == "__main__":
    main()

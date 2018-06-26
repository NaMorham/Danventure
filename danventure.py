import logging
import math
import sys
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


g_directions = [
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
g_room_types = [
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
    TELEPORT = 7

    NUM_CMDS = 8  # Must be last, must be largest number


g_commands = [
    # Place holder for NO COMMAND
    {"id": Commands.NONE, "long": "NONE", "short": "", "args": {"min": 0, "max": 0}},
    # Look can be run with 0 or one arguments.   With 0 it means at the current room, with
    # 1 argument it means look at the thing/person mentioned.
    {"id": Commands.LOOK, "long": "look", "short": "l", "args": {"min": 0, "max": 1}},
    # Exists just lists the exits for the current room, 0 arguments
    {"id": Commands.EXITS, "long": "exits", "short": "x", "args": {"min": 0, "max": 0}},

    # The player can type move <drection>, must have a direction.
    {"id": Commands.MOVE, "long": "move", "short": "m", "args": {"min": 1, "max": 1}},
    # Handle the actual directions, pre fill the movement direction values.
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

    # Teleport moves the player.  If given 1 argument to the room with that ID, if given 2
    # arguments teleport should move the specified object or mob to the room ID
    {"id": Commands.TELEPORT, "long": "teleport", "short": "tp", "args": {"min": 1, "max": 2}, "admin": True},

    # quit the game, no arguments
    {"id": Commands.QUIT, "long": "quit", "short": "q", "args": {"min": 0, "max": 0}},
    # Show the help.  If given 0 arguments, list the commands accessible to the player, if given 1
    # command, list the help for that command.
    {"id": Commands.HELP, "long": "help", "short": "?", "args": {"min": 0, "max": 1}},

    # Allows the player to say things (max 100 words, min 1)
    {"id": Commands.SAY, "long": "say", "short": "'", "args": {"min": 1, "max": 100}},
]


def get_room_type_name(room_id):
    if (room_id >= RoomTypes.DEV) and (room_id < RoomTypes.MAX):
        name = g_room_types[room_id]["name"]
    else:
        name = "UNKNOWN"
    return name


NONE = -1
NOWHERE = -1
NOBODY = -1
NOTHING = -1

g_max_room_id = NONE
g_min_room_id = sys.maxsize
g_default_start_room = 1
g_dev_start_room = 0

g_the_world = []

g_the_player = {"name": "Unknown"}


def is_admin(player=g_the_player):
    """
    Check if a player is an admin.
    :param player: The player to check
    :return:
    """
    if len(player) < 1:
        # not a valid player
        return False
    elif "admin" not in player:
        # not a valid player
        return False
    else:
        return player["admin"]


def make_rooms():
    global g_the_world
    g_the_world = [
        # Zone 0 - up to 100 rooms, use for system and common rooms
        {"id": 0, "name": "The void", "type": RoomTypes.CITY,
         "desc": "There is nothing here.  You are floating in an inky blackness, but look at all the stars!",
         "exits": [NOWHERE, NOWHERE, NOWHERE, NOWHERE, NOWHERE, NOWHERE],
         "special": NONE, "looks": [
            {"name": "stars", "desc": "The stars appear at the same time to be right next to you and somehow far away"}
            ]},

        {"id": 1000, "name": "Dan's Dev Room", "type": RoomTypes.DEV,
         "desc": "This is a temporary dev room.  This is a plain white space for creating new stuff.",
         "exits": [NOWHERE, NOWHERE, NOWHERE, NOWHERE, NOWHERE, 1001],
         "special": NONE, "looks": []},

        # Zone 10 - up to 100 rooms
        {"id": 1000, "name": "Dan's Dev Room", "type": RoomTypes.DEV,
         "desc": "This is a temporary dev room.  This is a plain white space for creating new stuff.",
         "exits": [NOWHERE, NOWHERE, NOWHERE, NOWHERE, NOWHERE, 1001],
         "special": NONE, "looks": []},

        {"id": 1001, "name": "The South Garden", "type": RoomTypes.GRASS,
         "desc": "This is a beautiful and lush garden.  The grass is green and there are flowers and trees all " +
                 "around the place.",
         "exits": [1002, NOWHERE, NOWHERE, NOWHERE, NOWHERE, NOWHERE],
         "special": NONE, "looks": [
            {"name": "grass", "desc": "The grass is very lush and a health green."},
            {"name": "trees", "desc": "Tall, medium and short, the trees are lush and healthy."},
            {"name": "flowers", "desc": "Small white and yellow flowers are in the garden beds."}]},

        {"id": 1002, "name": "Outside the House", "type": RoomTypes.TRACK,
         "desc": "A small garden outside the front entrance.  Small garden beds full of flowers line the grass " +
                 "beside the path.",
         "exits": [1003, 1004, 1001, NOWHERE, NOWHERE, NOWHERE],
         "special": NONE, "looks": [
            {"name": "grass", "desc": "The grass is very lush and a health green."},
            {"name": "flowers", "desc": "Small white and yellow flowers are in the garden beds."},
            {"name": "path", "desc": "A neat gravel path."}]},

        {"id": 1003, "name": "The north garden", "type": RoomTypes.GRASS,
         "desc": "This is a lush and beautiful garden.  The grass is green and there are flowers and trees all " +
                 "around the place.",
         "exits": [NOWHERE, NOWHERE, 1001, NOWHERE, NOWHERE, NOWHERE],
         "special": NONE, "looks": [
            {"name": "grass", "desc": "The grass is very lush and a health green."},
            {"name": "trees", "desc": "Tall, medium and short, the trees are lush and healthy."},
            {"name": "flowers", "desc": "Small white and yellow flowers are in the garden beds."}]},

        {"id": 1004, "name": "Inside the Entrance Hall", "type": RoomTypes.INSIDE,
         "desc": "A small square room acts as an entrance to a dark hallway.  There is a small painting on the wall " +
                 "and the floor is covered by a carpet.",
         "exits": [NOWHERE, 1005, NOWHERE, 1002, NOWHERE, NOWHERE],
         "special": NONE, "looks": [
            {"name": "painting", "desc": "A small painting of a bowl of fruit."},
            {"name": "carpet", "desc": "The carpet is made of soft green wool."}]},

        {"id": 1005, "name": "A Dark Hallway", "type": RoomTypes.INSIDE,
         "desc": "This hallway is long and quite dark.  The floor feels soft and deadens the sound a little.  " +
                 "Empty candle holder can just be seen on the walls.",
         "exits": [NOWHERE, 1006, NOWHERE, 1004, NOWHERE, NOWHERE],
         "special": NONE, "looks": []},

        {"id": 1006, "name": "A Nexus in the Hallway", "type": RoomTypes.INSIDE,
         "desc": "The hallway comes to an end and rooms branch off it.  Food smells drift in from the" +
                 "north and there is a small room to the south.  The soft carpet is ragged here.",
         "exits": [1007, 1009, 1008, 1005, NOWHERE, NOWHERE],
         "special": NONE, "looks": []},

        {"id": 1007, "name": "The Kitchen", "type": RoomTypes.INSIDE,
         "desc": "A large wooden table is in the center of the kitchen.  Small cupboards line the walls.",
         "exits": [NOWHERE, NOWHERE, 1006, NOWHERE, NOWHERE, NOWHERE],
         "special": NONE, "looks": []},

        {"id": 1008, "name": "A Small Bedroom", "type": RoomTypes.INSIDE,
         "desc": "This room is rather small, but the floor is soft and the walls are brightly coloured.",
         "exits": [1006, NOWHERE, NOWHERE, NOWHERE, NOWHERE, NOWHERE],
         "special": NONE, "looks": []},

        {"id": 1009, "name": "The Back Room", "type": RoomTypes.INSIDE,
         "desc": "This large room has large windows and a set or stairs going up to the next floor.  There is also " +
                 "a large wooden door that has been wedged open.",
         "exits": [NOWHERE, 1011, NOWHERE, 1006, 1010, NOWHERE],
         "special": NONE, "looks": []},

        {"id": 1010, "name": "The Attic", "type": RoomTypes.INSIDE,
         "desc": "This dark and dusty room has a lot of junk scattered around the place.  The is a small window " +
                 "looking out over the city.",
         "exits": [NOWHERE, NOWHERE, NOWHERE, NOWHERE, NOWHERE, 1009],
         "special": NONE, "looks": []},

        {"id": 1011, "name": "A Small Alleyway", "type": RoomTypes.CITY,
         "desc": "A Small Alleyway",
         "exits": [NOWHERE, NOWHERE, NOWHERE, 1009, NOWHERE, NOWHERE],
         "special": "City_Bell", "looks": [
            {"name": "dirt", "desc": "small piles of dirt and rubbish line the alleyway"}]}
    ]

    global g_max_room_id
    global g_min_room_id
    for r in g_the_world:
        if r["id"] > g_max_room_id:
            g_max_room_id = r["id"]
        if r["id"] < g_min_room_id:
            g_min_room_id = r["id"]
        # TODO: Check exits

    return g_the_world


def find_room(room_id, rooms=g_the_world):
    """
    Find a given room by ID
    :param room_id: The ID of the room we are looking for
    :param rooms: A list of rooms to search (defaults to the global world list)
    :return: A room object and an index
    """
    rm = {}
    f_idx = NOWHERE
    if (room_id >= 0) or (room_id <= g_max_room_id):
        for idx, r in enumerate(rooms):
            if r["id"] == room_id:
                logging.debug("Found room id [{}] at index [{}]".format(room_id, idx))
                rm = r
                f_idx = idx
    else:
        logging.error('Search ID outside world bounds.  The ID must be in the range [0 <= ID <= {}]'
                      .format(g_max_room_id))
    return rm, f_idx


def print_exit_detail(dr, room, player=g_the_player, rooms=g_the_world):
    """
    :param dr:  The identifier for the direction to display.
    :param room:  A room to display the exits for.
    :param player:  The player to show details to
    :param rooms:  A list of rooms to search.
    :return: True if the call succeeds
    """
    if not is_admin(player):
        # not allowed
        logging.warning("Attempt to show exit details to player [{}]".format(player["name"]))
        return False

    if (dr < Directions.NORTH) or (dr >= Directions.NUM_DIRS):
        # bad direction
        logging.error("Attempt to get detail for invalid exit direction [{}]".format(dr))
        return False

    if len(room) == 0:
        # bad room
        logging.error("Attempt to get exit detail for invalid room")  # it's a empty ref, nothing we can identify
        return False

    if len(room["exits"]) < Directions.NUM_DIRS:
        # room has bad exits
        logging.error("Room [{}] does not have enough exit fields".format(rm["id"]))
        return False

    exits = room["exits"]
    ex_dest_id = exits[dr]
    to_room = find_room(ex_dest_id, rooms)

    if len(to_room) == 0:
        # Exit room is bad
        logging.error("The specified exit [{dir_name}] from room [{rm_id}] leads to a non-existent room [{to_id}]"
                      .format(dir_name=g_directions[dr]["name"], rm_id=rm["id"], to_id=ex_dest_id))
        return False

    # If the exit leads somewhere we can write some details
    if ex_dest_id != NOWHERE:
        print('\t{yel}{dname:5s}: [{cyan}{exnum:3d}:{exname}{yel}]{norm}'.format(yel=Screen.fg.YELLOW,
              cyan=Screen.fg.CYAN, norm=Screen.fg.NRM, exnum=ex_dest_id,
              exname=to_room["name"], dname=g_directions[dr]["name"]))
    return True


def print_room_details(room_id, player=g_the_player, rooms=g_the_world):
    """
    Print dev/design details about a room
    :param room_id:  The id of the room to get details for.
    :param player:  The player to show details to.
    :param rooms:  The list of rooms to search.
    :return True if the details were printed:
    """
    if not is_admin(player):
        logging.error("Attempt to print details for room [{}] from non admin player [{}]"
                      .format(room_id, player["name"]))
        return False

    elif (room_id > g_max_room_id) or (room_id < g_min_room_id):
        logging.error("Attempt to print details for room [{}] outside world".format(room_id))
        return False

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
    return True


def test_all_rooms(player=g_the_player, rooms=g_the_world):
    """
    test method: print all rooms
    :param player:
    :param rooms:  a list of all rooms as unordered dictionaries
    :return:
    """
    # print("\033[30m*\033[31m*\033[32m*\033[33m*\033[34m*\033[35m*\033[36m*\033[37m*\033[0m")
    # print("\033[97;40m*\033[97;41m*\033[97;42m*\033[97;43m*\033[97;44m*\033[97;45m*\033[97;46m*\033[97;47m*\033[0m")
    # print("\033[90m*\033[91m*\033[92m*\033[93m*\033[94m*\033[95m*\033[96m*\033[97m*\033[0m")
    # print("\033[30;100m*\033[97;101m*\033[97;102m*\033[97;103m*\033[97;104m*\033[97;105m*\033[97;106m*\033[30;107m*\033[0m")
    print("There are [{}] rooms in the world".format(len(rooms)))
    for r in rooms:
        print_room_details(r["id"], player=player, rooms=rooms)
        print()

    logging.debug("Room test dump finished.")


def room_get_exit_abbrevs(room_id, player=g_the_player, rooms=g_the_world):
    """
    return a list of valid direction abbreviations
    :param room_id:  the id of the room to search
    :param player:  The player object to check
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
            if is_admin(player):
                # not a problem, admins can teleport
                return exits
            else:
                logger.error('Player in room with no exits, returning to start')
                print('You are somehow stuck, teleporting you to the start room')
                player.update({"room", default_start_room})
        else:
            for dr, x in enumerate(rm_exits):
                if x != NOWHERE:
                    dr_info = g_directions[dr]
                    exits.append(dr_info["abbrev"])

    return exits


def can_go(dr, player=g_the_player, rooms=g_the_world):
    """
    Check if a player is capable of going in a direction
    :param dr:  The direction they want to move
    :param player:  The player that is moving
    :param rooms:  The rooms to check
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


def move_player(to_id, from_id, cost, player=g_the_player, rooms=g_the_world):
    """
    Move a player/char from one room to another
    :param to_id:
    :param from_id:
    :param cost:
    :param player:
    :param rooms:
    :return:
    """
    logging.debug("Move player {} from room [{}] to room [{}]".format(player["name"], from_id, to_id))
    player_mv = player["moves"]
    if player_mv < cost:
        pass  # no move
    elif to_id == NOWHERE:
        pass  # bad destination
    elif len(find_room(to_id, rooms)) == 0:
        pass  # missing destination
    else:
        # Move is OK, update the players movement points and position
        player.update({"moves": (player_mv-cost), "room": to_id})
        logging.debug('Player now has {} moves'.format(player["moves"]))
        # TODO: update the world to move the player too, so we can easily see which players/mobs are in a room
    return


def get_prompt_string(player=g_the_player):
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


def look_at_room(player=g_the_player, rooms=g_the_world):
    player_rm_id = player["room"]
    if player_rm_id == NOWHERE:
        print('Floating in the VOID, just look at all the stars!')
    elif player_rm_id < g_min_room_id or player_rm_id > g_max_room_id:
        print('Falling !!!!  Somehow you are outside the world, returning you to the start')
        player.update({"room": default_start_room})
        look_at_room(player, rooms)
    else:
        rm = find_room(player_rm_id, rooms)
        if len(rm) != 0:
            # Remember that this appears white in pycharm :(
            print('{wht}{rname}{norm}'.format(wht=Screen.fg.BLACK, norm=Screen.fg.NRM, rname=rm["name"]))
            print('{mag}{rdesc}{norm}'.format(mag=Screen.fg.MAGENTA, norm=Screen.fg.NRM, rdesc=rm["desc"]))
            ex = rm["exits"]  # get the list of exits
            if len(ex) == 0:
                # no exits
                print("{yel}Exits: [{cyn} None {yel}]{norm}".format(yel=Screen.fg.YELLOW, cyn=Screen.fg.CYAN,
                      norm=Screen.fg.NRM))
            else:
                exits = room_get_exit_abbrevs(player_rm_id, player, rooms)
                print("{yel}Exits: [{cyn} {e_str} {yel}]{norm}".format(yel=Screen.fg.YELLOW, cyn=Screen.fg.CYAN,
                      norm=Screen.fg.NRM, e_str=' '.join(exits)))
    return


def get_command(command_txt, player=g_the_player, rooms=g_the_world):
    """
    Find a command based on a string.
    :param command_txt: The string to find
    :param player: The player issuing the command
    :param rooms: The list of rooms
    :return The command ID, the command OBJECT and any extra values to use, or the NONE command if not found.
    """
    command_txt = str(command_txt).lstrip().rstrip().lower()
    args = command_txt.split(' ')
    logging.debug('Got command test [{}] - {} args'.format(command_txt, len(args)))
    if len(command_txt) == 0:
        print('You need to type a command')
    else:
        for cmd in commands:
            if cmd["id"] == Commands.NONE:
                continue  # skip matching for the "NONE" command
            if cmd["id"] in find_room(player["room"], rooms).get("cmd_blacklist", []):
                print("This command cannot work here")
            elif (cmd["long"] == args[0]) or (cmd["short"] == args[0]):
                # we found it!!!!
                logging.debug('Found command [{}:{}]'.format(cmd["id"], cmd["long"]))
                if cmd.gets("admin", False) and not is_admin(player):
                    # it's an admin command, and the player is not an admin
                    logging.warning("Attempt to use admin command [{}] by non admin player [{}]"
                                    .format(cmd["long"], player["name"]))
                else:
                    # check the args
                    extra_values = {}
                    if "vals" in cmd:
                        extra_values.update(cmd["vals"])
                    return cmd["id"], cmd, extra_values

    return Commands.NONE, commands[Commands.NONE], {}


def main():
    global g_the_world
    global g_the_player
    g_the_player = {"name": "Bob", "room": g_default_start_room, "moves": 20, "max_moves": 20,
                    "health": 10, "max_health": 10, "stuff": [], "admin": True}

    running = True
    counter = 0

    logging.info('Load all rooms')
    make_rooms()
    plr = g_the_player
    plr["admin"] = True
    test_all_rooms(player=plr)
    print('\n\n\n\n')
    while True:
        new_name = input("What is your name: ").lstrip().rstrip()
        if new_name == '':
            print('You must have a name, try again')
        elif new_name.lower() == 'dan':
            g_the_player["name"] = "Dangerous Daniel"
            g_the_player["room"] = g_dev_start_room
            g_the_player["admin"] = True
            g_the_player["moves"] = 100
            g_the_player["max_moves"] = 100
            g_the_player["health"] = 100
            g_the_player["max_health"] = 100
            break
        else:
            g_the_player["name"] = new_name
            g_the_player["room"] = g_default_start_room
            break
            # end while True
    print('Hello {}, welcome to the world'.format(g_the_player["name"]))
    look_at_room()

    logging.info('Start main loop')
    while running:
        counter += 1
        logging.debug('Counter is at {}'.format(counter))

        if counter == 20:
            logging.info('Game is now quitting')
            running = False

        cmd_txt = input("{} Command: ".format(get_prompt_string()))
        cid, cmd, vals = get_command(cmd_txt)

        if cid == Commands.NONE:
            print("I don't understand the command [{}], try again".format(cmd_txt))

        elif cid == Commands.LOOK:
            if len(vals) == 0:
                look_at_room()
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
                if g_directions[m_dir]["abbrev"] not in room_get_exits(g_the_player["room"]):
                    print('You cannot go {} from here'.format(g_directions[m_dir]["name"]))
                else:
                    can_pass, cost, dest_id = can_go(m_dir, g_the_player, all_rooms)
                    if can_pass and (cost > 0) and (dest_id != NOWHERE):
                        move_player(dest_id, player["room"], cost)
                        look_at_room()
        else:
            print("Unknown command [{}], try again".format(cmd_txt))

        print()
        # end while running

        print()
        sleep(1)  # wait 1 second


if __name__ == "__main__":
    main()

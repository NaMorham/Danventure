#! /bin/python

import logging
import math
import sys
import pathlib
import json
import random
from enum import Enum
# from time import sleep

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


# This should not be an enum since we need to operate like an array and compare directions
class Directions:
    NONE = -1,

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    UP = 4
    DOWN = 5

    NUM_DIRS = 6


g_directions = [
    {"name": "North", "abbrev": "N", "reverse": Directions.SOUTH},
    {"name": "East", "abbrev": "E", "reverse": Directions.WEST},
    {"name": "South", "abbrev": "S", "reverse": Directions.NORTH},
    {"name": "West", "abbrev": "W", "reverse": Directions.EAST},
    {"name": "Up", "abbrev": "U", "reverse": Directions.DOWN},
    {"name": "Down", "abbrev": "D", "reverse": Directions.UP}
]


class RoomTypes(Enum):
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


"""
These values represent the data about different room types
"""
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


class Commands(Enum):
    NONE = 0
    LOOK = 1
    MOVE = 2
    EXITS = 3
    QUIT = 4
    HELP = 5
    SAY = 6
    TELEPORT = 7
    STAT = 8
    WHERE = 9

    NUM_CMDS = 10  # Must be last, must be largest number


g_all_commands = [
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

    # quit the game, no arguments
    {"id": Commands.QUIT, "long": "quit", "short": "q", "args": {"min": 0, "max": 0}},
    # Show the help.  If given 0 arguments, list the commands accessible to the player, if given 1
    # command, list the help for that command.
    {"id": Commands.HELP, "long": "help", "short": "?", "args": {"min": 0, "max": 1}},

    # Allows the player to say things (max 100 words, min 1)
    {"id": Commands.SAY, "long": "say", "short": "'", "args": {"min": 1, "max": 100}},

    # Teleport moves the player.  If given 1 argument to the room with that ID, if given 2
    # arguments teleport should move the specified object or mob to the room ID
    {"id": Commands.TELEPORT, "long": "teleport", "short": "tp", "args": {"min": 1, "max": 2}, "admin": True},

    # Print the statistics of a room, mob, obj or player
    {"id": Commands.STAT, "long": "stat", "short": "", "args": {"min": 0, "max": 1}, "admin": True},

    # Show the location of the player(s)
    {"id": Commands.WHERE, "long": "where", "short": "wh", "args": {"min": 0, "max": 1}, "admin": True},
]


class Stats(Enum):
    STR = 0
    DEX = 1
    CON = 2
    INT = 3
    WIS = 4
    CHA = 5
    
    HIT_POINTS = 6
    MOVES = 7
    MANA = 8
    
    EXP = 9
    
    NUM_STATS = 10   # Must be last


g_stats = {
    Stats.STR: {"long": "Strength", "short": "STR"},
    Stats.DEX: {"long": "Dexterity", "short": "DEX"},
    Stats.CON: {"long": "Constitution", "short": "CON"},
    Stats.INT: {"long": "Intelligence", "short": "INT"},
    Stats.WIS: {"long": "Wisdom", "short": "WIS"},
    Stats.CHA: {"long": "Charisma", "short": "CHA"},
    Stats.HIT_POINTS: {"long": "Hit Points", "short": "HP"},
    Stats.MOVES: {"long": "Moves", "short": "MV"},
    Stats.MANA: {"long": "Mana Points", "short": "MANA"},
    Stats.EXP: {"long": "Experience", "short": "EXP"}
}


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
g_default_start_room = 1001  # Zone 10, room 1
g_dev_start_room = 1000  # zone 10, room 0

g_the_world = {}
g_zones = {}
g_the_player = {"name": "Unknown"}


def capitalise(s):
    """
    Capitalise the first letter of the string s
    :param s: The string to capitalise
    :return:
    """
    # always the first letter
    cp = ""
    s_len = len(s)
    if s_len >= 2:
        cp = s[0].upper() + s[1:]
    elif s_len == 1:
        cp = s.upper()
    return cp


def wrap_text(text, wrap_col = 80):
    s = []
    rem = str(text)
    while len(rem) >= wrap_col:
        k = rem[:wrap_col].rfind(' ')
        s.append(rem[:k])
        rem = rem[k+1:]
    s.append(rem)
    return '\n'.join(s)


def get_min(a, b):
    return a if a < b else b


def get_max(a, b):
    return a if a > b else b


def limit_val(min_v, max_v, v):
    mn = get_min(min_v, max_v)
    mx = get_max(min_v, max_v)
    return get_min(mx, get_max(v, mn))


def dice(sides, num=1, add=0, rolls=[]):
    total = 0
    if (sides >= 1) and (num > 0):
        for c in range(0, num):
            v = random.randint(1, sides)
            rolls.append(v)
            # logging.debug("roll {:2d}/{:2d}: dice({:2d}) --> {:3d}".format(c+1, num, sides, v))
            total += v
    return total + add


def pass_fail_str(val, extra=""):
    return str("{cgrn}PASS{nrm}".format(cgrn=Screen.fg.GREEN, nrm=Screen.fg.NRM) if val else\
               "{cred}FAIL{nrm}".format(cred=Screen.fg.RED, nrm=Screen.fg.NRM)) +\
               str(": " + extra) if len(extra) > 0 else ""


def test_get_min(a, b, ex):
    got = get_min(a, b)
    result = (got == ex)
    print(pass_fail_str(result, "get_min({:3d}, {:3d}); got {:3d}, expected {}".format(a, b, got, ex)))
    return


def test_get_max(a, b, ex):
    got = get_max(a, b)
    result = (got == ex)
    print(pass_fail_str(result, "get_max({:3d}, {:3d}); got {:3d}, expected {}".format(a, b, got, ex)))
    return


def test_get_limit(mn, mx, v, ex):
    got = limit_val(mn, mx, v)
    result = (got == ex)
    print(pass_fail_str(result, "limit_vsl({:3d}, {:3d}, {:3d}); got {:3d}, expected {}".format(mn, mx, v, got, ex)))
    return


def test_min_max():
    test_get_min(0, 0, 0)
    test_get_min(1, 0, 0)
    test_get_min(0, 1, 0)

    test_get_min(-2, -2, -2)
    test_get_min(-2, 0, -2)
    test_get_min(0, -2, -2)

    test_get_min(2, 2, 2)
    test_get_min(2, 0, 0)
    test_get_min(0, 2, 0)

    test_get_min(-5, 5, -5)
    test_get_min(5, -5, -5)

    test_get_min(100, 99, 99)
    print("-----")
    test_get_max(0, 0, 0)
    test_get_max(1, 0, 1)
    test_get_max(0, 1, 1)

    test_get_max(-2, -2, -2)
    test_get_max(-2, 0, 0)
    test_get_max(0, -2, 0)

    test_get_max(2, 2, 2)
    test_get_max(2, 0, 2)
    test_get_max(0, 2, 2)

    test_get_max(-5, 5, 5)
    test_get_max(5, -5, 5)

    test_get_max(100, 99, 100)
    print("-----")
    # limit_val(min, max, val)
    test_get_limit(0, 0, 0, 0)
    test_get_limit(0, 1, 0, 0)
    test_get_limit(1, 0, 0, 0)

    test_get_limit(2, 5, 3, 3)  # is in range
    test_get_limit(2, 5, 1, 2)  # below min
    test_get_limit(2, 5, 7, 5)  # above max

    # test reversed min/max
    test_get_limit(5, 2, 3, 3)  # is in range
    test_get_limit(5, 2, 1, 2)  # below min
    test_get_limit(5, 2, 7, 5)  # above max

    test_get_limit(-5, 5, 0, 0)
    test_get_limit(-5, 5, -3, -3)
    test_get_limit(-5, 5, 3, 3)
    test_get_limit(-5, 5, -12, -5)
    test_get_limit(-5, 5, 12, 5)
    print("-----")

    return


def test_dice_fn(sides, num=1, add=0, repeat=1):
    repeat = get_max(repeat, 1)
    calc_min = (num + add)
    calc_max = (sides * num) + add
    for r in range(repeat):
        rolls = []
        got = dice(sides=sides, num=num, add=add, histo=rolls)
        result = ((got <= calc_max) and (got >= calc_min))
        print(pass_fail_str(result, "Roll {:3d}/{:3d}: [{} <= dice({}, {}, {}) <= {}]; got {} --> {}".format(r+1,
              repeat, calc_min, sides, num, add, calc_max, got, rolls)))
    return


def test_dice():
    test_dice_fn(sides=0)  # 0d0 + 0  --> MUST equal 0
    test_dice_fn(sides=0, add=1)  # 1d0 + 1  --> MUST equal 1
    test_dice_fn(sides=2, num=1, add=1)  # 1d2 + 1 once
    print("------")
    test_dice_fn(sides=2, num=1, add=1, repeat=20)  # 1d2 + 1
    print("------")
    test_dice_fn(sides=6, num=1, add=0, repeat=20)  # 1d6 + 0
    print("------")
    test_dice_fn(sides=6, num=2, add=0, repeat=30)  # 2d6 + 0
    print("------")
    test_dice_fn(sides=4, num=1, add=10, repeat=50)  # 1d4 + 10
    print("------")
    test_dice_fn(sides=4, num=10, add=5, repeat=50)  # 10d4 + 5
    print("------")
    test_dice_fn(sides=4, num=100, add=5, repeat=50)  # 100d4 + 5
    print("------")
    test_dice_fn(sides=20, num=100, add=0, repeat=50)  # 100d20 + 0

    print("------")
    test_dice_fn(sides=0, num=100, add=0, repeat=10)  # 100d0 + 0
    print("------")
    test_dice_fn(sides=1, num=100, add=0, repeat=10)  # 100d1 + 0
    print("------")
    test_dice_fn(sides=2, num=100, add=0, repeat=10)  # 100d1 + 0
    print("------")
    test_dice_fn(sides=4, num=100, add=0, repeat=10)  # 100d1 + 0
    print("------\nTest stat roll")
    test_dice_fn(sides=6, num=2, add=6, repeat=10)  # 100d1 + 0

    return


def test_slice():
    t1 = ""
    print("    t1 = \"{}\"".format(t1))
    print("t1[1:] = \"{}\"".format(t1[1:]))
    print("t1[2:] = \"{}\"".format(t1[2:]))
    t1 = "a"
    print("    t1 = \"{}\"".format(t1))
    print("t1[1:] = \"{}\"".format(t1[1:]))
    print("t1[2:] = \"{}\"".format(t1[2:]))
    t1 = "ab"
    print("    t1 = \"{}\"".format(t1))
    print("t1[1:] = \"{}\"".format(t1[1:]))
    print("t1[2:] = \"{}\"".format(t1[2:]))
    t1 = "abc"
    print("    t1 = \"{}\"".format(t1))
    print("t1[1:] = \"{}\"".format(t1[1:]))
    print("t1[2:] = \"{}\"".format(t1[2:]))


def test_capitalise():
    tmp = {"bob", "Mike", "MacDonald", "McDougal", "macdonald", "mcdougal", "O'Rielly", "o'brian"}
    for t in tmp:
        print("capitalise({}) -> \"{}\"".format(t, capitalise(t)))


def test_gen_stats():
    num_tests = 10
    for idx in range(num_tests):
        print("{:2d}/{:2d}: gen_stats() == {}".format(idx+1, num_tests, gen_stats()))
    return


def test_roll_stat_fn():  # hp_min=10, hp_max=20, mv_min=20, mv_max=40, mg_min=0, mg_max=8):
    return roll_stat()


def test_roll_stat():
    for i in range(20):
        vals = []
        for c in range(6):
            vals.append(test_roll_stat_fn())
        v2 = ["{:2d}".format(v) for v in vals]
        print("[{}]".format(", ".join(v2)))
    return


def is_admin(player):
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


def roll_stat():
    """
    Roll 3d6, keep top 2 and add 6
    :return: top 2d6 + 6
    """
    # TODO: add race(s) and stat adjustments
    rolls = []
    _ = dice(6, add=0, num=3, rolls=rolls)
    rolls.sort(reverse=True)
    return sum(rolls[:2]) + 6


def gen_stats(hp_min=10, hp_max=20, mv_min=20, mv_max=40, mg_min=0, mg_max=8):
    sts = {}
    sts.update({Stats.STR: roll_stat()})
    sts.update({Stats.DEX: roll_stat()})
    sts.update({Stats.CON: roll_stat()})
    sts.update({Stats.INT: roll_stat()})
    sts.update({Stats.WIS: roll_stat()})
    sts.update({Stats.CHA: roll_stat()})

    sts.update({Stats.HIT_POINTS: dice((hp_max-hp_min+1), add=(hp_min-1))})
    sts.update({Stats.MOVES: dice((mv_max-mv_min+1), add=(mv_min-1))})

    tmp = random.randint(mg_min, mg_max)
    if tmp > 0:
        sts.update({Stats.MANA: (tmp*5)})
    else:
        sts.update({Stats.MANA: 0})
    return sts


def new_player(player, name):
    player.update("name", name)
    player.update({"stats": gen_stats().update({Stats.EXP: 0})})
    print(player)
    return


def calc_max_min_world():
    global g_max_room_id
    global g_min_room_id
    for r in g_the_world:  # for each key num in the world
        if r > g_max_room_id:
            g_max_room_id = r
        if r < g_min_room_id:
            g_min_room_id = r


def find_room(room_id, world):
    """
    Find a given room by ID
    :param room_id: The ID of the room we are looking for
    :param world: A list of rooms to search (defaults to the global world list)
    :return: A room object and an index
    """
    if room_id in world:
        return world[room_id]
    else:
        logging.error('Search ID outside world bounds.  The ID must be in the range [0 <= ID <= {}]'
                      .format(g_max_room_id))
        return {}


def print_exit_detail(dr, room, player, world):
    """
    :param dr:  The identifier for the direction to display.
    :param room:  A room to display the exits for.
    :param player:  The player to show details to
    :param world:  A list of rooms to search.
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
        logging.error("Room [{}] does not have enough exit fields".format(room["id"]))
        return False

    exits = room["exits"]
    ex_dest_id = exits[dr]
    if ex_dest_id == NOWHERE:
        return False

    to_room = find_room(ex_dest_id, world)

    if len(to_room) == 0:
        # Exit room is bad
        logging.error("The specified exit [{dir_name}] from room [{rm_id}] leads to a non-existent room [{to_id}]"
                      .format(dir_name=(g_directions[dr])["name"], rm_id=room["id"], to_id=ex_dest_id))
        return False

    # If the exit leads somewhere we can write some details
    if ex_dest_id != NOWHERE:
        print('\t{yel}{dname:5s}: [{cyan}{exnum:3d}:{exname}{yel}]{norm}'.format(yel=Screen.fg.YELLOW,
              cyan=Screen.fg.CYAN, norm=Screen.fg.NRM, exnum=ex_dest_id,
              exname=to_room["name"], dname=g_directions[dr]["name"]))
    return True


def print_room_details(room_id, player, world):
    """
    Print dev/design details about a room
    :param room_id:  The id of the room to get details for.
    :param player:  The player to show details to.
    :param world:  The list of rooms to search.
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
        rm = find_room(room_id, world)
        if len(rm) >= 1:
            print('--------------------------------------------------------')
            print('{yel}Num: [{cyan}{rnum:5d}{yel}], Name: [{cyan}{rname}{yel}], '
                  'Type [{cyan}{rtype}:{rtypes}{yel}]{norm}'
                  .format(yel=Screen.fg.YELLOW, cyan=Screen.fg.CYAN, norm=Screen.fg.NRM, rnum=rm["id"],
                          rname=rm["name"], rtype=rm["type"], rtypes=g_room_types[rm["type"]]["name"]))
            print('{yel}Description:{norm}'.format(yel=Screen.fg.YELLOW, norm=Screen.fg.NRM))
            print('{cyan}{rdesc}{norm}'.format(norm=Screen.fg.NRM, cyan=Screen.fg.CYAN, rdesc=wrap_text(rm["desc"])))
            print('{yel}Exits:{norm}'.format(yel=Screen.fg.YELLOW, norm=Screen.fg.NRM))
            print_exit_detail(Directions.NORTH, rm, player, world)
            print_exit_detail(Directions.EAST, rm, player, world)
            print_exit_detail(Directions.SOUTH, rm, player, world)
            print_exit_detail(Directions.WEST, rm, player, world)
            print_exit_detail(Directions.UP, rm, player, world)
            print_exit_detail(Directions.DOWN, rm, player, world)
            if len(rm["looks"]) >= 1:
                print('{yel}Extras:{norm}'.format(yel=Screen.fg.YELLOW, norm=Screen.fg.NRM))
                for lk in rm["looks"]:
                    print("{yel}Name: [{cyan}{lname}{yel}], Description: [{cyan}{ldesc}{yel}]{norm}".format(
                        yel=Screen.fg.YELLOW, cyan=Screen.fg.CYAN, norm=Screen.fg.NRM,
                        lname=lk["name"], ldesc=lk["desc"]))
    return True


def print_all_room_details(player, world):
    """
    test method: print all rooms
    :param player:  the player for whom to print
    :param world:  a list of all rooms as unordered dictionaries
    :return:  True if something was printed
    """
    # print("\033[30m*\033[31m*\033[32m*\033[33m*\033[34m*\033[35m*\033[36m*\033[37m*\033[0m")
    # print("\033[97;40m*\033[97;41m*\033[97;42m*\033[97;43m*\033[97;44m*\033[97;45m*\033[97;46m*\033[97;47m*\033[0m")
    # print("\033[90m*\033[91m*\033[92m*\033[93m*\033[94m*\033[95m*\033[96m*\033[97m*\033[0m")
    # print("\033[30;100m*\033[97;101m*\033[97;102m*\033[97;103m*\033[97;104m*\033[97;105m*\033[97;106m*\033[30;107m*\033[0m")

    if player.get("admin", False):
        print("There are [{}] rooms in the world".format(len(world)))
        for r in world:
            if print_room_details(r, player, world):
                print()
        logging.debug("Room test dump finished.")
        return True
    else:
        return False


def room_get_exit_abbrevs(room_id, player, world):
    """
    return a list of valid direction abbreviations
    :param room_id:  the id of the room to search
    :param player:  The player object to check
    :param world:  a list of rooms to search
    :return: a list of valid direction ID's
    """
    exits = []
    rm = find_room(room_id, world)
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
                player.update({"room", g_default_start_room})
        else:
            for dir_num, x in enumerate(rm_exits):
                if x != NOWHERE:
                    dr_info = g_directions[dir_num]
                    exits.append(dr_info["abbrev"])

    return exits


def can_go(dr, player, world):
    """
    Check if a player is capable of going in a direction
    :param dr:  The direction they want to move
    :param player:  The player that is moving
    :param world:  The rooms to check
    :return:  True/False if they can pass, the cost to move and the destination ID
    """
    player_rm = player["room"]
    rm = find_room(player_rm, world)

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
                                                                            r_num=player_rm))
        return False, 0, NOWHERE

    # does the exit exist?
    exit_rm_num = rm["exits"][dr]
    if exit_rm_num == NOWHERE:
        logger.error("Invalid exit [{}] from room [{}]".format(g_directions[dr]["name"], player_rm))
        print('{red}The exit {d_name} does not lead anywhere{norm}'.format(red=Screen.fg.RED, norm=Screen.fg.NRM,
                                                                           d_name=g_directions[dr]["name"]))
        return False, 0, NOWHERE

    # does the exit lead somewhere?
    dest_rm = find_room(exit_rm_num, world)
    if len(dest_rm) == 0:
        logger.error("Invalid destination room [{}] from [{}]".format(player_rm, dest_rm))
        print('{red}The exit {d_name} does not lead anywhere{norm}'.format(red=Screen.fg.RED, norm=Screen.fg.NRM,
                                                                           d_name=g_directions[dr]["name"]))
        return False, 0, NOWHERE

    # does the player have enough moves left
    from_type = g_room_types[rm["type"]]                    # get the from type
    to_type = g_room_types[dest_rm["type"]]                 # get the to type
    ave = (from_type["mv_cost"] + to_type["mv_cost"]) // 2  # get the average cost of the 2 rooms
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
    logging.debug("Player [{}] can move [{}] to [{}:{}] at a cost of [{}] moves".format(player["name"],
                  g_directions[dr]["name"], exit_rm_num, dest_rm["name"], mv_needed))
    return True, mv_needed, exit_rm_num


def move_player(to_id, from_id, cost, player, rooms):
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
    player_mv = player.get("moves", 0)
    if player_mv < cost:
        return  # no move
    elif to_id == NOWHERE:
        return  # bad destination

    to_rm = find_room(to_id, rooms)
    if len(to_rm) == 0:
        pass  # missing destination
    else:
        # Move is OK, update the players movement points and position
        player.update({"moves": (player_mv-cost), "room": to_id})
        logging.debug('Player now has {} moves'.format(player["moves"]))
        # TODO: update the world to move the player too, so we can easily see which players/mobs are in a room
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
    player_rm_id = player.get("room", NOWHERE)

    if player_rm_id == NOWHERE:
        print('Floating in the VOID, just look at all the stars!')

    elif player_rm_id < g_min_room_id or player_rm_id > g_max_room_id:
        print('Falling !!!!  Somehow you are outside the world, returning you to the start')
        player.update({"room": g_default_start_room})
        look_at_room(player, rooms)

    else:
        rm = find_room(player_rm_id, rooms)
        if len(rm) != 0:
            # Remember that this appears white in pycharm :(
            print('{name}{rname}{norm}'.format(name=Screen.fg.BLUE, norm=Screen.fg.NRM, rname=rm["name"]))
            print('{body}{rdesc}{norm}'.format(body=Screen.fg.GREEN, norm=Screen.fg.NRM, rdesc=wrap_text(rm["desc"])))
            ex = rm["exits"]  # get the list of exits
            if len(ex) == 0:
                # no exits
                print("{yel}Exits: [{cyn} None {yel}]{norm}".format(yel=Screen.fg.YELLOW, cyn=Screen.fg.CYAN,
                      norm=Screen.fg.NRM))
            else:
                exits = room_get_exit_abbrevs(player_rm_id, player, rooms)
                print("{yel}Exits: [{cyn} {e_str} {yel}]{norm}".format(yel=Screen.fg.YELLOW, cyn=Screen.fg.CYAN,
                      norm=Screen.fg.NRM, e_str=' '.join(exits)))
        else:
            logging.error("could not find room with id [{}]".format(player_rm_id))
    return


def get_command(command_txt, player, rooms):
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
        for cmd in g_all_commands:
            if cmd["id"] == Commands.NONE:
                continue  # skip matching for the "NONE" command
            plr_rm = find_room(player["room"], rooms)
            if cmd["id"] in plr_rm.get("cmd_blacklist", []):
                print("This command cannot work here")
            elif (cmd["long"] == args[0]) or ((len(cmd["short"]) > 0) and (cmd["short"] == args[0])):
                # we found it!!!!
                logging.debug('Found command [{}:{}]'.format(cmd["id"], cmd["long"]))
                if cmd.get("admin", False) and not is_admin(player):
                    # it's an admin command, and the player is not an admin
                    logging.warning("Attempt to use admin command [{}] by non admin player [{}]"
                                    .format(cmd["long"], player["name"]))
                    continue
                else:
                    # check the args
                    extra_values = {}
                    if "vals" in cmd:
                        extra_values.update(cmd["vals"])
                    # TODO: expand command args
                    return cmd["id"], cmd, extra_values

    return Commands.NONE, g_all_commands[Commands.NONE], {}


def regen_player(player):
    """
    Regenerate a player's movement and health
    :param player:
    :return:
    """
    max_hp = player["max_health"]
    max_mv = player["max_moves"]

    if is_admin(player):
        # admins fully regenerate
        player.update({"health": max_hp})
        player.update({"moves": max_mv})
        return

    hp = player["health"]
    mv = player["moves"]
    regen_pct = 0.1  # 10 pct of total

    player_rm_id = player["room"]
    rm = find_room(player_rm_id, g_the_world)

    if len(rm) == 0:
        pass
    else:
        rm_type = rm.get("type", RoomTypes.INSIDE)
        if rm_type == RoomTypes.INSIDE:
            regen_pct += 0.05
            # TODO: handle equipment and potions

    if hp < max_hp:
        regen_hp = math.ceil(regen_pct * float(max_hp))
        hp += regen_hp
        if hp > max_hp:
            hp = max_hp
        player.update({"health": hp})

    if mv < max_mv:
        regen_mv = math.ceil(regen_pct * float(max_mv))
        mv += regen_mv
        if mv > max_mv:
            mv = max_mv
        player.update({"moves": mv})
    return


def show_help(player):
    print("{title}Commands:{norm}".format(title=Screen.fg.MAGENTA, norm=Screen.fg.NRM))
    # hard coded for now, should be generated
    cmds = [
        {"name": "Quit", "desc": "Quit the game"},
        {"name": "Look", "desc": "Look at the room"},
        {"id": Commands.NONE},
        {"name": "North", "desc": "Move north"},
        {"name": "East", "desc": "Move east"},
        {"name": "South", "desc": "Move south"},
        {"name": "West", "desc": "Move west"},
        {"name": "Up", "desc": "Move up"},
        {"name": "Down", "desc": "Move down"},
    ]
    for c in cmds:
        if "name" in c:
            cmd = c["name"]
        elif "id" not in c:
            continue
        elif c["id"] == Commands.NONE:
            print()
            continue
        else:
            cmd = g_all_commands[int(c["id"])]["long"]
        desc = c.get("desc", "TODO")

        print("{ccmd}{cmd:>20s}{norm} : {desc}".format(ccmd=Screen.fg.CYAN, cmd=cmd, norm=Screen.fg.NRM, desc=desc))

    return


def load_generic_rooms():
    global g_the_world
    g_the_world = {
        # Zone 0 - up to 100 rooms, use for system and common rooms
        0: {"id": 0, "name": "The void", "type": RoomTypes.CITY,
            "desc": "There is nothing here.  You are floating in an inky blackness, but look at all the stars!",
            "exits": [NOWHERE, NOWHERE, NOWHERE, NOWHERE, NOWHERE, NOWHERE],
            "special": NONE, "looks": [
                {"name": "stars",
                 "desc": "The stars appear at the same time to be right next to you and somehow far away"}
            ]
            },
        1: {"id": 1, "name": "Dead!", "type": RoomTypes.DEV,
            "desc": "You are dead, Dead, DEAD.  Maybe you should try and respawn.",
            "exits": [NOWHERE, NOWHERE, NOWHERE, NOWHERE, NOWHERE, 1001],
            "special": "Respawn", "looks": []
            }
    }
    return


def load_generic_mobs():
    return


def load_generic_objs():
    return


def load_generic_zone():
    return


def test_load_json_wld(wld_path, allow_overwrite=False):
    global g_the_world
    load_generic_rooms()

    print("There are [{}] rooms in the world".format(len(g_the_world)))
    try:
        with open(wld_path) as fp:
            tmp = json.load(fp)
            for rm in tmp:
                rm_id = rm.get("id", NOWHERE)
                if rm_id == NOWHERE:
                    continue  # ignore it, we do not care

                if not allow_overwrite and rm_id in g_the_world:
                    continue  # already there and not overwriting

                g_the_world[int(rm_id)] = rm
            # end for each room in file
    except FileNotFoundError as fnfe:
        print("Could not open file: {}".format(fnfe))

    calc_max_min_world()
    print("There are [{}] rooms in the world".format(len(g_the_world)))
    return


def test_load_json_mobiles(mob_file_path, allow_overwrite=False):
    print("todo, read [{}]".format(mob_file_path))
    global g_the_world
    return True


def test_load_json_objects(obj_file_path, allow_overwrite=False):
    print("todo, read [{}]".format(obj_file_path))
    global g_the_world
    return True


def test_load_json_zones(zon_file_path, allow_overwrite=False):
    print("todo, read [{}]".format(zon_file_path))
    global g_the_world
    return True


def load_rooms_json(wld_file_path, allow_overwrite=False):
    print("todo, read [{}]".format(wld_file_path))
    global g_the_world

    print("There are [{}] rooms in the world".format(len(g_the_world)))
    try:
        with open(wld_file_path) as fp:
            tmp = json.load(fp)
            for rm in tmp:
                rm_id = rm.get("id", NOWHERE)
                if rm_id == NOWHERE:
                    continue  # ignore it, we do not care

                if not allow_overwrite and rm_id in g_the_world:
                    continue  # already there and not overwriting

                logging.debug("Add room [{}:{}] to the world".format(rm_id, rm.get("name","")))
                g_the_world[int(rm_id)] = rm
            # end for each room in file
    except FileNotFoundError as fnfe:
        print("Could not open file: {}".format(fnfe))

    calc_max_min_world()
    print("There are [{}] rooms in the world".format(len(g_the_world)))
    return True


def load_json_zone_data(zone_file_data_obj, wld_path, obj_path, mob_path, zon_path):
    zone_file_data_obj = dict(zone_file_data_obj)
    global g_zones
    zone_id = zone_file_data_obj.get("id", NOWHERE)
    if zone_id == NOWHERE:
        logging.error("Invalid zone id")
        return False
    if zone_id in g_zones:
        logging.error("Zone id [{}] has already been loaded".format(zone_id))
        return False

    # load the rooms that make up the zone
    wld_file = zone_file_data_obj.get("wld_file", "")
    loaded = False
    if wld_file == '':
        logging.error("No world file path for zone [{}]".format(zone_id))
    else:
        wld_file_path = pathlib.Path(wld_path, wld_file)
        if not wld_file_path.exists():
            logging.error("World file [{}] for zone [{}] does not exist".format(wld_file_path.as_posix(), zone_id))
        else:
            loaded |= load_rooms_json(wld_file_path.as_posix())

    # load data about mobiles native to the zone
    mob_file = zone_file_data_obj.get("mob_file", "")
    loaded = False
    if mob_file == '':
        logging.error("No mobile file path for zone [{}]".format(zone_id))
    else:
        mob_file_path = pathlib.Path(mob_path, mob_file)
        if not mob_file_path.exists():
            logging.error("Mobile file [{}] for zone [{}] does not exist".format(mob_file_path.as_posix(), zone_id))
        else:
            loaded |= test_load_json_mobiles(mob_file_path.as_posix())

    # load data about objects belonging to the zone
    obj_file = zone_file_data_obj.get("obj_file", "")
    loaded = False
    if mob_file == '':
        logging.error("No objects file path for zone [{}]".format(zone_id))
    else:
        obj_file_path = pathlib.Path(obj_path, obj_file)
        if not obj_file_path.exists():
            logging.error("Objects file [{}] for zone [{}] does not exist".format(obj_file_path.as_posix(), zone_id))
        else:
            loaded |= test_load_json_objects(obj_file_path.as_posix())

    # load data about the zone for resets
    zon_file = zone_file_data_obj.get("zon_file", "")
    loaded = False
    if zon_file == '':
        logging.error("No zone loading file path for zone [{}]".format(zone_id))
    else:
        zon_file_path = pathlib.Path(zon_path, zon_file)
        if not zon_file_path.exists():
            logging.error("Zone loading file [{}] for zone [{}] does not exist".format(zon_file_path.as_posix(), zone_id))
        else:
            loaded |= test_load_json_zones(zon_file_path.as_posix())

    logging.debug("Loaded zone [{}]".format(zone_id))
    return loaded


def load_json_data(data_path):
    global g_the_world
    load_generic_rooms()

    data_file_path = pathlib.Path(data_path, "world.json")
    logging.debug("Read world data from world files path [{}]".format(data_file_path.as_posix()))

    try:
        with open(data_file_path.as_posix(), mode="r") as data_fl:
            data_obj = json.load(data_fl)
            # get path data first
            paths_obj = data_obj.get("paths", {})
            if "world_files" not in paths_obj:
                logging.error("Could not load world path info from file [{}]".format(data_file_path.as_posix()))
                return False
            if "object_files" not in paths_obj:
                logging.error("Could not load object path info from file [{}]".format(data_file_path.as_posix()))
                return False
            if "mob_files" not in paths_obj:
                logging.error("Could not load mobile path info from file [{}]".format(data_file_path.as_posix()))
                return False
            if "zon_files" not in paths_obj:
                logging.error("Could not load zone path info from file [{}]".format(data_file_path.as_posix()))
                return False

            wld_path_str = str(paths_obj.get("world_files", "")).lstrip().rstrip()
            if wld_path_str == "":
                logging.error("Empty world path")
                return False
            wld_path = pathlib.Path(data_path, wld_path_str)
            if not wld_path.exists():
                logging.error("World files path [{}] does not exist".format(wld_path.as_posix()))
                return False
            logging.debug("Got world files path [{}]".format(wld_path.as_posix()))

            obj_path_str = str(paths_obj.get("object_files", "")).lstrip().rstrip()
            if obj_path_str == "":
                logging.error("Empty object path")
                return False
            obj_path = pathlib.Path(data_path, obj_path_str)
            if not obj_path.exists():
                logging.error("Object files path [{}] does not exist".format(obj_path.as_posix()))
                return False
            logging.debug("Got object files path [{}]".format(obj_path.as_posix()))

            mob_path_str = str(paths_obj.get("mob_files", "")).lstrip().rstrip()
            if mob_path_str == "":
                logging.error("Empty mobile path")
                return False
            mob_path = pathlib.Path(data_path, mob_path_str)
            if not mob_path.exists():
                logging.error("Mobile files path [{}] does not exist".format(mob_path.as_posix()))
                return False
            logging.debug("Got mobile files path [{}]".format(mob_path.as_posix()))

            zon_path_str = str(paths_obj.get("zon_files", "")).lstrip().rstrip()
            if zon_path_str == "":
                logging.error("Empty zone path")
                return False
            zon_path = pathlib.Path(data_path, zon_path_str)
            if not zon_path.exists():
                logging.error("Zone files path [{}] does not exist".format(zon_path.as_posix()))
                return False
            logging.debug("Got zone files path [{}]".format(zon_path.as_posix()))

            logging.debug("Read zone info from [{}]".format(data_file_path.as_posix()))
            for zone_file_data in data_obj.get("zones", []):
                if not load_json_zone_data(zone_file_data, wld_path.as_posix(), obj_path.as_posix(),
                                           mob_path.as_posix(), zon_path.as_posix()):
                    logging.error("Failed to load zone data [{}]".format(zone_file_data))

    except FileNotFoundError as fnfe:
        logging.error("Could not read world file [{}] -> got [{}]".format(data_file_path.as_posix(), fnfe))
        return False
    except IOError as ioe:
        logging.error("Got an IO error reading [{}] -> got [{}]".format(data_file_path.as_posix(), ioe))
        return False

    return True


def main():
    global g_the_world
    global g_the_player
    g_the_player = {"name": "Bob", "room": g_default_start_room, "moves": 20, "max_moves": 20,
                    "health": 10, "max_health": 10, "stuff": [], "admin": True}

    running = True
    counter = 0

    logging.info('Load all rooms')
    load_json_data("data")
    logging.info("[{}] rooms loaded".format(len(g_the_world)))
    # plr = g_the_player.copy()
    # plr["admin"] = True
    # if print_all_room_details(plr, g_the_world):
    #     print('\n\n\n\n')

    if len(g_the_world) == 0:
        print("No world data found, Exiting...")
        logging.error("Empty world data")
        exit(1)

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
            g_the_player["name"] = capitalise(new_name)
            g_the_player["room"] = g_default_start_room
            g_the_player["admin"] = False
            break
        # end while True

    print('Hello {}, welcome to the world'.format(g_the_player["name"]))
    look_at_room(g_the_player, g_the_world)

    logging.info('Start main loop')
    while running:
        player_rm_num = g_the_player["room"]

        counter += 1
        logging.debug('Counter is at {}'.format(counter))

        if counter == 200:  # no more than 200 turns for testing
            logging.info('Game is now quitting')
            running = False

        cmd_txt = input("{} Command: ".format(get_prompt_string(g_the_player))).lstrip().rstrip()

        if len(cmd_txt) > 0:
            cid, cmd, vals = get_command(cmd_txt, g_the_player, g_the_world)

            if cid == Commands.NONE:
                print("I don't understand the command [{}], try again".format(cmd_txt))

            elif cid == Commands.LOOK:
                if len(vals) == 0:
                    look_at_room(g_the_player, g_the_world)
                else:
                    print('Cannot look at things yet')

            elif cid == Commands.QUIT:
                print('Goodbye')
                running = False
                continue

            elif cid == Commands.MOVE:
                m_dir = vals.get("direction", NONE)
                if m_dir == NONE:
                    print("Move where?")
                else:
                    # check if the abbreviation for this direction is in the exit list
                    rm_exits = room_get_exit_abbrevs(player_rm_num, g_the_player, g_the_world)
                    if g_directions[m_dir]["abbrev"] not in rm_exits:
                        print('You cannot go {} from here'.format(g_directions[m_dir]["name"]))
                    else:
                        can_pass, cost, dest_id = can_go(m_dir, g_the_player, g_the_world)
                        if can_pass and (cost >= 0) and (dest_id != NOWHERE):
                            move_player(dest_id, player_rm_num, cost, g_the_player, g_the_world)
                            look_at_room(g_the_player, g_the_world)
                        else:
                            logging.debug("Player [{}] cannot move [{}] to [{}:{}]".format(g_the_player["name"],
                                          g_directions[m_dir]["name"], dest_id,
                                          find_room(dest_id, g_the_world).get("name", "UNK")))

            elif cid == Commands.STAT:
                if is_admin(g_the_player):
                    print_room_details(player_rm_num, g_the_player, g_the_world)

            elif cid == Commands.WHERE:
                if is_admin(g_the_player):
                    print("{cgrn}{player} [{room_num}:{room_name}]{nrm}".format(cgrn=Screen.fg.GREEN,
                          nrm=Screen.fg.NRM, player=g_the_player["name"], room_num=player_rm_num,
                          room_name=(g_the_world[player_rm_num]["name"] if player_rm_num != NOWHERE else "NOWHERE")))

            elif cid == Commands.HELP:
                        show_help(g_the_player)

            else:
                print("Unknown command [{}], try again".format(cmd_txt))

        if (counter % 3) == 0:
            regen_player(g_the_player)
        # print()
        # sleep(1)  # wait 1 second
    # end while running

    logging.debug("End of main method")
    return


if __name__ == "__main__":
    do_tests = False
    if do_tests:
        logger.setLevel(logging.DEBUG)
        # test_slice()
        # test_capitalise()
        # load_json_data("data")
        # test_min_max()
        # test_dice()
        test_roll_stat()
        test_gen_stats()
    else:
        # actually run the game
        main()

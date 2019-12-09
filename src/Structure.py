import sys
from enum import Enum


class Screen:
    def __init__(self):
        pass

    class ScrFCol:
        def __init__(self):
            pass

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
        def __init__(self):
            pass

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
        def __init__(self):
            pass

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
        def __init__(self):
            pass

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
    def __init__(self):
        pass

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
    ZROOMS = 10

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

    {"id": Commands.ZROOMS, "long": "zrooms", "short": "zr", "args": {"min": 1, "max": 1}, "admin": True}
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

    NUM_STATS = 10  # Must be last


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


# Globals
NONE = -1
NOWHERE = -1
NOBODY = -1
NOTHING = -1

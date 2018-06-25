import logging

logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.ERROR)


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


class Screen:
    global use_colour
    if use_colour:
        fg = ScrFCol
        bg = ScrBCol
    else:
        fg = ScrFNone
        bg = ScrBNone


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
         "exitN": NOWHERE, "exitE": NOWHERE, "exitS": NOWHERE, "exitW": NOWHERE, "exitU": NOWHERE, "exitD": 1,
         "special": NONE, "looks": []},

        {"id": 1, "name": "The South Garden", "type": RoomTypes.GRASS,
         "desc": "This is a beautiful and lush garden.  The grass is green and there are flowers and trees all " +
                 "around the place.",
         "exitN": 2, "exitE": NOWHERE, "exitS": NOWHERE, "exitW": NOWHERE, "exitU": NOWHERE, "exitD": NOWHERE,
         "special": NONE, "looks": [
            {"name": "grass", "desc": "The grass is very lush and a health green."},
            {"name": "trees", "desc": "Tall, medium and short, the trees are lush and healthy."},
            {"name": "flowers", "desc": "Small white and yellow flowers are in the garden beds."}]},

        {"id": 2, "name": "Outside the House", "type": RoomTypes.TRACK,
         "desc": "A small garden outside the front entrance.  Small garden beds full of flowers line the grass " +
                 "beside the path.",
         "exitN": 3, "exitE": 4, "exitS": 1, "exitW": NOWHERE, "exitU": NOWHERE, "exitD": NOWHERE,
         "special": NONE, "looks": [
            {"name": "grass", "desc": "The grass is very lush and a health green."},
            {"name": "flowers", "desc": "Small white and yellow flowers are in the garden beds."},
            {"name": "path", "desc": "A neat gravel path."}]},

        {"id": 3, "name": "The north garden", "type": RoomTypes.GRASS,
         "desc": "This is a lush and beautiful garden.  The grass is green and there are flowers and trees all " +
                 "around the place.",
         "exitN": NOWHERE, "exitE": NOWHERE, "exitS": 1, "exitW": NOWHERE, "exitU": NOWHERE, "exitD": NOWHERE,
         "special": NONE, "looks": [
            {"name": "grass", "desc": "The grass is very lush and a health green."},
            {"name": "trees", "desc": "Tall, medium and short, the trees are lush and healthy."},
            {"name": "flowers", "desc": "Small white and yellow flowers are in the garden beds."}]},

        {"id": 4, "name": "Inside the Entrance Hall", "type": RoomTypes.INSIDE,
         "desc": "A small square room acts as an entrance to a dark hallway.  There is a small painting on the wall " +
                 "and the floor is covered by a carpet.",
         "exitN": NOWHERE, "exitE": 5, "exitS": NOWHERE, "exitW": 2, "exitU": NOWHERE, "exitD": NOWHERE,
         "special": NOTHING, "looks": [
            {"name": "painting", "desc": "A small painting of a bowl of fruit."},
            {"name": "carpet", "desc": "The carpet is made of soft green wool."}]},

        {"id": 5, "name": "A Dark Hallway", "type": RoomTypes.INSIDE,
         "desc": "This hallway is long and quite dark.  The floor feels soft and deadens the sound a little.  " +
                 "Empty candle holder can just be seen on the walls.",
         "exitN": NOWHERE, "exitE": 6, "exitS": NOWHERE, "exitW": 4, "exitU": NOWHERE, "exitD": NOWHERE,
         "special": NONE, "looks": []},

        {"id": 6, "name": "A Nexus in the Hallway", "type": RoomTypes.INSIDE,
         "desc": "The hallway comes to an end and rooms branch off it.  Food smells drift in from the" +
                 "north and there is a small room to the south.  The soft carpet is ragged here.",
         "exitN": 7, "exitE": 9, "exitS": 8, "exitW": 5, "exitU": NOWHERE, "exitD": NOWHERE,
         "special": NOTHING, "looks": []},

        {"id": 7, "name": "The Kitchen", "type": RoomTypes.INSIDE,
         "desc": "A large wooden table is in the center of the kitchen.  Small cupboards line the walls.",
         "exitN": NOWHERE, "exitE": NOWHERE, "exitS": 6, "exitW": NOWHERE, "exitU": NOWHERE, "exitD": NOWHERE,
         "special": NOTHING, "looks": []},

        {"id": 8, "name": "A Small Bedroom", "type": RoomTypes.INSIDE,
         "desc": "This room is rather small, but the floor is soft and the walls are brightly coloured.",
         "exitN": 6, "exitE": NOWHERE, "exitS": NOWHERE, "exitW": NOWHERE, "exitU": NOWHERE, "exitD": NOWHERE,
         "special": NOTHING, "looks": []},

        {"id": 9, "name": "The Back Room", "type": RoomTypes.INSIDE,
         "desc": "This large room has large windows and a set or stairs going up to the next floor.  There is also " +
                 "a large wooden door that has been wedged open.",
         "exitN": NOWHERE, "exitE": 11, "exitS": NOWHERE, "exitW": 6, "exitU": 10, "exitD": NOWHERE,
         "special": NOTHING, "looks": []},

        {"id": 10, "name": "The Attic", "type": RoomTypes.INSIDE,
         "desc": "This dark and dusty room has a lot of junk scattered around the place.  The is a small window " +
                 "looking out over the city.",
         "exitN": NOWHERE, "exitE": NOWHERE, "exitS": NOWHERE, "exitW": NOWHERE, "exitU": NOWHERE, "exitD": 9,
         "special": NOTHING, "looks": []},

        {"id": 11, "name": "A Small Alleyway", "type": RoomTypes.CITY,
         "desc": "A Small Alleyway",
         "exitN": NOWHERE, "exitE": NOWHERE, "exitS": NOWHERE, "exitW": 9, "exitU": NOWHERE, "exitD": NOWHERE,
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


def print_room(room_id, rooms):
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
            if rm["exitN"] != NOWHERE:
                print('\t{yel}North: [{cyan}{exnum:3d}:{exname}{yel}]{norm}'.format(yel=Screen.fg.YELLOW,
                      cyan=Screen.fg.CYAN, norm=Screen.fg.NRM, exnum=rm["exitN"],
                      exname=find_room(rm["exitN"], rooms)["name"]))
            if rm["exitE"] != NOWHERE:
                print('\t{yel}East : [{cyan}{exnum:3d}:{exname}{yel}]{norm}'.format(yel=Screen.fg.YELLOW,
                      cyan=Screen.fg.CYAN, norm=Screen.fg.NRM, exnum=rm["exitE"],
                      exname=find_room(rm["exitE"], rooms)["name"]))
            if rm["exitS"] != NOWHERE:
                print('\t{yel}South: [{cyan}{exnum:3d}:{exname}{yel}]{norm}'.format(yel=Screen.fg.YELLOW,
                      cyan=Screen.fg.CYAN, norm=Screen.fg.NRM, exnum=rm["exitS"],
                      exname=find_room(rm["exitS"], rooms)["name"]))
            if rm["exitW"] != NOWHERE:
                print('\t{yel}West : [{cyan}{exnum:3d}:{exname}{yel}]{norm}'.format(yel=Screen.fg.YELLOW,
                      cyan=Screen.fg.CYAN, norm=Screen.fg.NRM, exnum=rm["exitW"],
                      exname=find_room(rm["exitW"], rooms)["name"]))
            if rm["exitU"] != NOWHERE:
                print('\t{yel}Up   : [{cyan}{exnum:3d}:{exname}{yel}]{norm}'.format(yel=Screen.fg.YELLOW,
                      cyan=Screen.fg.CYAN, norm=Screen.fg.NRM, exnum=rm["exitU"],
                      exname=find_room(rm["exitU"], rooms)["name"]))
            if rm["exitD"] != NOWHERE:
                print('\t{yel}Down : [{cyan}{exnum:3d}:{exname}{yel}]{norm}'.format(yel=Screen.fg.YELLOW,
                      cyan=Screen.fg.CYAN, norm=Screen.fg.NRM, exnum=rm["exitD"],
                      exname=find_room(rm["exitD"], rooms)["name"]))
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
        print_room(r["id"], rooms)
        print()
    logging.debug("Room test dump finished.")


def main():
    running = True
    counter = 0

    logging.info('Load all rooms')
    all_rooms = make_rooms()
    test_all_rooms(all_rooms)

    logging.info('Start main loop')
    while running:
        counter += 1
        logging.debug('Counter is at {}'.format(counter))
        if counter == 20:
            logging.info('Game is now quitting')
            running = False

if __name__ == "__main__":
    main()

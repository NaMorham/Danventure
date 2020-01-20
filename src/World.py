"""
TODO
"""
from src.Structure import *
import Utils


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
g_max_room_id = NONE
g_min_room_id = sys.maxsize
g_default_start_room = 1001  # Zone 10, room 1
g_dev_start_room = 1000  # zone 10, room 0

g_the_world = {}
g_zones = {}


def get_room_type_name(room_id):
    """
    Get the display name type for a given room type Id.
    :param room_id: The room Id type
    :return: A string representing the room type display name
    """
    if (room_id >= RoomTypes.DEV) and (room_id < RoomTypes.MAX):
        name = g_room_types[room_id]["name"]
    else:
        name = "UNKNOWN"
    return name


def calc_max_min_world():
    """
    Calculate the minimum and maximum usable room Id's in the world for range checking
    :return:
    """
    global g_max_room_id
    global g_min_room_id
    for r in g_the_world:  # for each key num in the world
        g_max_room_id = Utils.get_max(r, g_max_room_id)
        g_min_room_id = Utils.get_min(r, g_min_room_id)
        # if r > g_max_room_id:
        #    g_max_room_id = r
        # if r < g_min_room_id:
        #    g_min_room_id = r

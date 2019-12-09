#! /usr/bin/env python

import logging
from src import Utils
from src import World
from src.World import NOWHERE


"""
Simple test_files methods

NOT a substitute for some proper unit tests
"""


def test_get_min(a, b, ex):
    got = Utils.get_min(a, b)
    result = (got == ex)
    print(Utils.pass_fail_str(result, "get_min({:3d}, {:3d}); got {:3d}, expected {}".format(a, b, got, ex)))
    return


def test_get_max(a, b, ex):
    got = Utils.get_max(a, b)
    result = (got == ex)
    print(Utils.pass_fail_str(result, "get_max({:3d}, {:3d}); got {:3d}, expected {}".format(a, b, got, ex)))
    return


def test_get_limit(mn, mx, v, ex):
    got = Utils.limit_val(mn, mx, v)
    result = (got == ex)
    print(Utils.pass_fail_str(result, "limit_vsl({:3d}, {:3d}, {:3d}); got {:3d}, expected {}".format(
        mn,mx, v, got, ex)))
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

    # test_files reversed min/max
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
    repeat = Utils.get_max(repeat, 1)
    calc_min = (num + add)
    calc_max = (sides * num) + add
    for r in range(repeat):
        rolls = []
        got = Utils.dice(sides=sides, num=num, add=add, histo=rolls)
        result = ((got <= calc_max) and (got >= calc_min))
        print(Utils.pass_fail_str(result, "Roll {:3d}/{:3d}: [{} <= dice({}, {}, {}) <= {}]; got {} --> {}".format(r+1,
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
        print("capitalise({}) -> \"{}\"".format(t, Utils.capitalise(t)))


def test_gen_stats():
    num_tests = 10
    for idx in range(num_tests):
        print("{:2d}/{:2d}: gen_stats() == {}".format(idx+1, num_tests, Utils.gen_stats()))
    return


def test_roll_stat_fn():  # hp_min=10, hp_max=20, mv_min=20, mv_max=40, mg_min=0, mg_max=8):
    return Utils.roll_stat()


def test_roll_stat():
    for i in range(20):
        stat_vals = []
        for c in range(6):
            stat_vals.append(test_roll_stat_fn())
        v2 = ["{:2d}".format(v) for v in stat_vals]
        print("[{}]".format(", ".join(v2)))
    return


def test_load_json_wld(wld_path, allow_overwrite=False):
    global g_the_world
    World.load_generic_rooms()

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

    Structure.calc_max_min_world()
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

    World.calc_max_min_world()
    print("There are [{}] rooms in the world".format(len(g_the_world)))
    return True


def run_tests():
    logger = logging.getLogger()
    logger.info("Begin test_files run.")
    test_slice()
    test_capitalise()
    test_min_max()
    test_dice()
    test_roll_stat()
    test_gen_stats()


if __name__ == "__main__":
    run_tests()

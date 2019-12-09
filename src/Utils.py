
import logging
import random
from src.Structure import Screen
from src.Structure import Stats


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


def wrap_text(text, wrap_col=80):
    """
    Wrap text to a certain width.
    :param text:
    :param wrap_col:
    :return:
    """
    s = []
    rem = str(text)
    while len(rem) >= wrap_col:
        k = rem[:wrap_col].rfind(' ')
        s.append(rem[:k])
        rem = rem[k + 1:]
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


def dice(sides, num=1, add=0, rolls=[], histo=None):
    total = 0
    if (sides >= 1) and (num > 0):
        for c in range(0, num):
            v = random.randint(1, sides)
            rolls.append(v)
            # logging.debug("roll {:2d}/{:2d}: dice({:2d}) --> {:3d}".format(c+1, num, sides, v))
            total += v
        if histo:
            logging.debug("TODO: histogram")
    return total + add


def pass_fail_str(val, extra=""):
    return str("{cgrn}PASS{nrm}".format(cgrn=Screen.fg.GREEN, nrm=Screen.fg.NRM) if val else
               "{cred}FAIL{nrm}".format(cred=Screen.fg.RED, nrm=Screen.fg.NRM)) + \
           str(": " + extra) if len(extra) > 0 else ""


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

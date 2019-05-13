#! /usr/bin/env python

import threading
import time
import logging

temp = "The hallway comes to an end and rooms branch off it.  Food smells drift in from the north and there" \
       " is a small room to the south.  The soft carpet is ragged here."

temp2 = "The hallway comes to an end and rooms branch off it.  Food smells drift in from the north and there" \
        " is a small room to the south.  The soft carpet is ragged."


def wrap_text(text, wrap_col = 80):
    s = []
    rem = str(text)
    while len(rem) >= wrap_col:
        k = rem[:wrap_col].rfind(' ')
        s.append(rem[:k])
        rem = rem[k+1:]
    s.append(rem)
    return '\n'.join(s)


def test_lsplit(s):
    s = str(s)
    logging.debug("s = '{}'".format(s))
    logging.debug("s.lsplit(' ') = '{}'".format(s.split(' ',1)))
    return


def test_rsplit(s):
    s = str(s)
    logging.debug("s = '{}'".format(s))
    logging.debug("s.rplit(' ') = '{}'".format(s.rsplit(' ', 1)))
    return


def test_wrap():
    logging.debug(wrap_text(temp))
    logging.debug('----\n')
    logging.debug(wrap_text(temp2))
    logging.debug('----\n')

    logging.debug(test_lsplit("look stars you fool"))
    logging.debug('----\n')
    logging.debug(test_rsplit("look stars you fool"))
    logging.debug('----\n')


g_command_stack=[]
g_is_running = False


def game_loop(timeout=0.5):
    class GameLoopThread(threading.Thread):
        timed_out = False
        final = False
        count = 0

        def run(self):
            global g_is_running
            global g_command_stack

            self.timed_out = False
            while self.count < 100:
                # logging.debug("Game loop.  Count [{}]".format(self.count))
                if len(g_command_stack) < 1:
                    # logging.debug("No command, sleeping 1 second")
                    time.sleep(timeout)
                else:
                    # we have something
                    logging.debug("Commands: {}".format(g_command_stack))
                    command = str(g_command_stack.pop()).lower()
                    # logging.debug("Process command [{}]".format(command))
                    if command == "quit":
                        break
                    else:
                        logging.warn("Unknown command [{}]".format(command))
                self.count += 1

            logging.info("Quitting game loop")
            g_is_running = False

    if timeout < 0.01:
        timeout = 0.01
    it = GameLoopThread()
    global g_is_running
    g_is_running = True
    it.start()
    it.join(5)
    it.timed_out = True


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.info("Begin main loop")

    logging.info("Begin game loop")
    game_loop(0.5)

    logging.info("Begin input loop")
    while g_is_running:
        cmd_txt = str(input("{} Command: ".format("TODO"))).lstrip().rstrip()
        if cmd_txt == '':
            logging.debug("Ignore empty input")
        else:
            g_command_stack.append(cmd_txt)
            if cmd_txt.lower() == 'quit':
                break

    # waiting to quit
    logging.info("Cleanup and kill game loop")
    while g_is_running:
        # logging.debug("Waiting to quit...")
        time.sleep(0.01)

    logging.info("Done")
    exit(0)

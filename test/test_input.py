#! /bin/python

import threading, msvcrt
import sys
import logging

temp = "The hallway comes to an end and rooms branch off it.  Food smells drift in from the north and there" \
       " is a small room to the south.  The soft carpet is ragged here."

temp2 = "The hallway comes to an end and rooms branch off it.  Food smells drift in from the north and there" \
        " is a small room to the south.  The soft carpet is ragged."


def wrap_text1(text, wrap_col = 80):
    s = []
    rem = str(text)
    while len(rem) >= wrap_col:
        k = rem[:wrap_col].rfind(' ')
        s.append(rem[:k])
        rem = rem[k+1:]
    if len(rem):
        s.append(rem)

    return '\n'.join(s)


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
    print("s = '{}'".format(s))
    print("s.lsplit(' ') = '{}'".format(s.split(' ',1)))
    return


def test_rsplit(s):
    s = str(s)
    print("s = '{}'".format(s))
    print("s.rplit(' ') = '{}'".format(s.rsplit(' ', 1)))
    return


def test_wrap():
    print(wrap_text(temp))
    print('----\n')
    print(wrap_text(temp2))
    print('----\n')

    print(test_lsplit("look stars you fool"))
    print('----\n')
    print(test_rsplit("look stars you fool"))
    print('----\n')


def user_input_old(text, timeout=5):
    result = None

    class KeyboardThread(threading.Thread):
        timed_out = False
        input = ''
        final = False

        def run(self):
            self.timed_out = False
            self.input = ''
            while True:
                if msvcrt.kbhit():
                    chr = msvcrt.getche()
                    logging.debug("chr == {}".format(chr))
                    if ord(chr) == 13:
                        self.input += '\n'
                        self.final = True
                        break
                    elif ord(chr) >= 32:
                        self.input += str(chr)
                if len(self.input) == 0 and self.timed_out:
                    break

    sys.stdout.write("{:s}:".format(text))
    it = KeyboardThread()
    it.start()
    it.join(timeout)
    it.timed_out = True
    if (len(it.input) > 0) and it.final:
        # wait for rest of input
        it.join()
        result = it.input
    return result


g_commandStack = []
g_partial = ""


def user_input(text, timeout=5, remainder=g_partial):
    class KeyboardThread(threading.Thread):
        timed_out = False
        input = ''
        final = False
        remain = ''

        def pre_text(self, in_text):
            for c in in_text:
                sys.stdout.write("add [{}] to input\n".format(c))
                sys.stdout.flush()
                self.input += c

        def run(self):
            # sys.stdout.write("input val == {}\n".format(self.input))
            # sys.stdout.flush()
            self.timed_out = False
            # self.input = ''
            self.input = g_partial
            while True:
                if msvcrt.kbhit():
                    chr_sel = msvcrt.getche()
                    # logging.debug("chr == {}".format(chr_sel))
                    if ord(chr_sel) == 13:
                        # self.input += '\n'
                        self.remain = ''
                        self.final = True
                        # print("end by enter")
                        sys.stdout.flush()
                        break
                    elif ord(chr_sel) == 27:  # esc pressed
                        self.input = ''
                        self.remain = ''
                        self.final = True
                        sys.stdout.flush()
                        break
                    elif ord(chr_sel) >= 32:
                        c = msvcrt.getch().decode('utf-8')
                        self.input += c  # str(chr_sel)
                        sys.stdout.write(c)  # chr_sel)
                        sys.stdout.flush()
                if self.timed_out:  # externally timed out
                    # print("end timed out")
                    # sys.stdout.flush()
                    self.remain = self.input
                    self.input = ''
                    break
            # print("leave run func")

    result = None
    remain = None
    # sys.stdout.write(">> text [{}], timeout [{}], remainder [{}]\r\n\r\n".format(text, timeout, remainder))
    # sys.stdout.print()
    # sys.stdout.flush()

    it = KeyboardThread()
    has_remainder = (remainder is not None) and (remainder != "")
    if has_remainder:
        it.pre_text(remainder)
    # print("{}\n".format(it.remain))
    sys.stdout.write("{}: {}".format(text, remainder if has_remainder else ""))
    sys.stdout.flush()
    it.start()
    it.join(timeout)
    it.timed_out = True
    if it.final:
        # wait for rest of input
        result = it.input
        remain = it.remain
    return result, remain


def test_input():
    # and some examples of usage
    question = user_input('Enter something here, you have 2 seconds', timeout=2)
    print("q = \"{}\"".format(question))
    if question is not None:
        print('\nYou did it!')
    else:
        print('\nYou failed')


def test_input_loop(timeout=5):
    counter = 0
    part_txt = ""
    print()
    while counter < 10:
        # and some examples of usage
        new_text = "\n{:4d}) Command: {}".format(counter+1, part_txt)
        # print(">> " + new_text)
        if (part_txt is None) or (part_txt.lower() == "none"):
            part_txt = ''
        in_txt, part_txt = user_input(new_text, timeout=timeout, remainder=part_txt)
        if in_txt is not None:
            if in_txt.lstrip().rstrip().lower() == "quit":
                print("\nQUIT")
                break
            elif len(in_txt) > 0:
                print("\ndo command [{}]".format(in_txt))
                counter = 0  # reset the loop
                part_txt = ''
            else:
                # print("skip")
                pass
        else:
            # print("tick")
            # print(part_txt)
            pass
        counter += 1
    if counter >= 10:
        print()


def ret_test(doom):
    print("in func 1: {}".format(doom))
    doom = "Content from Func"
    doom = doom.swapcase().swapcase()
    print("in func 2: {}".format(doom))
    return


g_foo = ""


def ret_test2(doom):
    global g_foo
    print("in func 1: {}".format(g_foo))
    g_foo = doom
    print("in func 2: {}".format(g_foo))
    return


# This function takes last element as pivot, places
# the pivot element at its correct position in sorted
# array, and places all smaller (smaller than pivot)
# to left of pivot and all greater elements to right
# of pivot
def partition(arr, low, high):
    i = (low - 1)  # index of smaller element
    pivot = arr[high]  # pivot
    print('i = {}, pivot = {}'.format(i, pivot))

    for j in range(low, high):
        print('array: {}, arr[i] = arr[{}] = {}, arr[j] = arr[{}] = {}'.format(arr, i, arr[i], j, arr[j]))
        # If current element is smaller than or
        # equal to pivot
        if arr[j] <= pivot:
            # increment index of smaller element
            i = i + 1
            print('Swap arr[{}] = {} and arr[{}] = {}, pivot = {}'.format(i, arr[i], j, arr[j], pivot))
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# The main function that implements QuickSort
# arr[] --> Array to be sorted,
# low  --> Starting index,
# high  --> Ending index
#
# Function to do Quick sort
def quick_sort(arr, low, high):
    if arr:
        print('Begin Q sort of array size [{}], low [{}], high [{}]'.format(len(arr), low, high))
        if low < high:
            # pi is partitioning index, arr[p] is now
            # at right place
            pi = partition(arr, low, high)

            # Separately sort elements before
            # partition and after partition
            quick_sort(arr, low, pi - 1)
            quick_sort(arr, pi + 1, high)


if __name__ == "__main__":
    # foo = ""
    # print("foo = \"{}\"".format(foo))
    # foo = "test test"
    # print("foo = \"{}\"".format(foo))
    #
    # ret_test(foo)
    #
    # print("foo = \"{}\"".format(foo))

    g_foo = "woooot"
    print("g_foo = \"{}\"".format(g_foo))
    ret_test2("doooom")
    print("g_foo = \"{}\"".format(g_foo))

    # test_wrap()
    # print("------")
    # test_input()
    print("------")
    # test_input_loop()
    print("------")

    g_arr = []
    import random
    for idx in range(25):
        num = random.randrange(0, 100)
        g_arr.append(num)
    print(g_arr)

    quick_sort(g_arr, 0, len(g_arr) - 1)

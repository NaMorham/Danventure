import random


def guess_num(max_val, min_val, num_guesses=3, prompt="What is your guess? "):
    if max_val < min_val:
        tmp = max_val
        max_val = min_val
        min_val = tmp

    num = 0
    gen_number = random.randint(min_val, max_val)

    while num < num_guesses:
        number_guess = int(input(prompt))
        num = num + 1
        if number_guess == gen_number:
            return True
        elif number_guess < gen_number:
            print("Higher.  Guess again. ")
        else:
            print("Lower.  Guess again. ")

    return False


def do_hall():
    print("do_hall")


total_coins = 0
game_over = False
while not game_over:
    if total_coins == 3:
        print("\nYou walk out of the front door, blinking in the sunshine.")
        print("You win!\n\n")
        game_over = True
        break

    print("\nYou wake up. Something is wrong. As you get out of bed, you see a sign pinned to your door by a knife.")
    print("You must find 3 coins to put in the key of the front door to leave.")
    print("You have {} coins so far.".format(total_coins))
    print("You hear something scuffling in the closet. You also think about smashing through the window to escape.")
    print()
    print("You could 1: leave your room and try to find a coin, 2: Try to see what is in your"
          " closet, 3: Smash through the window.")
    startChoice = input("Type 1,2 or 3 to continue: ")
    if startChoice == "1":
        print("\nYou move out of your room and into the hall.")
        print("You hear a clanking noise down the hall. There is also a red door or marked with black,"
              " next to an evil, gnarled dresser.")
        # needs a while loop here, because it is nested you would need to figure out a better way of doing this
        print()
        print("You can either: 1. Go down the hall 2. Go into the red room 3. look in the evil wardrobe.")
        hallChoice = input("Type 1,2 or 3 to continue: ")
        if hallChoice == "1":
            print("You find a headless horseman.")
            print("The horseman says, 'For a coin, you must guess correctly a number from 1 to 10."
                  "You will have 3 guesses.")
            number = random.randint(1, 10)
            print()

            if guess_num(10, 1):
                print("The headless horseman gives you a coin and dashes through the wall. You win!")
                total_coins = total_coins + 1
            else:
                print("Your three guesses failed. You are the headless horseman's slave forever")
                lose = 1

        # numberGuess = input("What is your guess? ")
            # guessAmount = 0
            # lose = 0
            # while int(numberGuess) != number and lose != 1:
            #     if guessAmount == 1:
            #         lose = 1
            #         print("Your three guesses failed. You are the headless horseman's slave forever")
            #         guessAmount = guessAmount+1
            #     elif numberGuess != input("Guess again"):
            #         guessAmount = guessAmount+1
            #         numberGuess = input("Guess again")
            #     elif lose != 1:
            #         print("The headless horseman gives you a coin and dashes through the wall. You win!")
            #         total_coins = total_coins + 1

        elif hallChoice == "2":
            print("\nYou enter the red room.")
            print("There are 2 doors in the red room, one with a 1 scratched on it, one with a 2.")
            redChoice = input("Which door do you pick? ")
            if redChoice == "1":
                print("\nYou enter the first door.")
                print("A mountain of creepy green liquid begins to fall from the ceiling.")
                print("You drown, you die.")
                total_coins = total_coins - 1 if total_coins > 0 else total_coins
                continue

            elif redChoice == "2":
                print("You enter the second room. An old man is sitting in the corner")
                print("The old man smiles a toothless smile")
                print("He says, 'What kills kings, destroys mountians, slaghters millions, grows trees,"
                      " destroys lands?")
                answer = input("What is it?")
                if answer == "time" or "Time":
                    print("The old man scowls, and hands you a coin.")
                    print("You leave the rooms, and slot the coin in the door. You leave. You win!")
                    total_coins = total_coins + 1
                    print("\n\n")
                else:
                    print("You answered incorrectly. You are the old mans slave forever. You lose.")
                    total_coins = total_coins - 1 if total_coins > 0 else total_coins
                    continue

        elif hallChoice == "3":
            print("\nYou are sucked into the wardrobe and are never seen again.")
            print("Game over.")
            total_coins = total_coins - 1 if total_coins > 0 else total_coins
            continue
        else:
            print("You didn't put 1, 2 or 3")

    elif startChoice == "2":
        print("\nYou go into the closet.")
        print("There is a sphinx.")
        riddleAnswer = input("It says, 'What gets wet when drying?' ")
        if riddleAnswer in ["towel", "a towel", "Towel", "A towel", "A Towel"]:
            print("It hisses in disappointment, as you guessed correctly. It gives you a coin. You leave the"
                  " closet and go out of the room, into the hall. You win!")
            total_coins = total_coins + 1
        else:
            print("The sphinx smiles evilly. You guessed wrong. She eats you.")
            total_coins = total_coins-1 if total_coins > 0 else total_coins

    elif startChoice == "3":
        print("You fall into a pit of glowing green liquid, which turns out to be acid.")
        print("You die")
        total_coins = total_coins-1 if total_coins > 0 else total_coins
        continue

    else:
        print("You didn't put 1, 2 or 3.")
# end while

totalcoins = 0
if totalcoins == "3":
    print("You walk out of the front door, blinking in the sunshine.")
    print("You win")
print("You wake up. Something is wrong. As you get out of bed, you see a sign pinned to your door by a knife.")
print("You must find a coin to put in the key of the front door to leave.")
print("You hear something scuffiling in the closet. You also think about smashing through the window to escape.")
print("You could 1: leave your room and try to find a coin, 2: Try to see what is in your closet, 3: Smash through the window.")
startChoice = input("Type 1,2 or 3 to continue")
if startChoice == "1":
    print("You move out of your room and into the hall.")
    print("You hear a clanking noise down the hall. There is also a red door or marked with black, next to an evil, gnarled dresser.")
    print("You can either: 1. Go down the hall 2. Go into the red room 3. look in the evil wardrobe.")
    hallChoice = input("Type 1,2 or 3 to contunue.")
    if hallChoice == "1":
        print("You find a headless horseman.")
        print("The horseman says, 'For a coin, you must guess corectly a number from 1 to 10. You will have 3 guesses.")
        import random
        number = random.randint(1,10)
        numberGuess = input("What is your guess?")
        guessAmount = 0
        lose = 0
        while int(numberGuess) != number and lose != 1:
            if guessAmount == 1:
                lose = 1
                print("Your three guesses failed. You are the headless horseman's slave forever")
                guessAmount = guessAmount+1
            elif numberGuess != input("Guess again"):
                guessAmount = guessAmount+1
                numberGuess = input("Guess again")
            elif lose != 1:
                print("The headless horseman gives you a coin and dashes through the wall. You win!")
    elif hallChoice == "2":
        print("You enter the red room.")
        print("there are 2 doors in the red room, one with a 1 scratched on it, one with a 2.")
        redChoice = input("Which door do you pick?")
        if redChoice == "1":
            print("You enter the first door.")
            print("A mountain of creepy green liquid begins to fall from the ceiling.")
            print("You drown, you die.")
        elif redChoice == "2":
            print("You enter the second room. An old man is sitting in the corner")
            print("The old man smiles a toothless smile")
            print("He says, 'What kills kings, destroys mountians, slaghters millions, grows trees, destroyes lands?")
            answer = input("What is it?")
            if answer == "time" or "Time":
                print("The old man scowls, and hands you a coin.")
                print("You leave the rooms, and slot the coin in the door. You leave. You win!")
            else:
                print("You answered incorrectly. You are the horsemans slave forever. You lose.")
    elif hallChoice == "3":
        print("You are sucked into the wardrobe and are never seen again.")
        print("Game over.")
    else:
        print("You didnt put 1, 2 or 3")
elif startChoice == "2":
    print("You go into the closet.")
    print("There is a sphix.")
    riddleAnswer = input("It says, 'What gets wet when drying?'")
    if riddleAnswer == "towel" or "a towel" or "Towel" or "A towel" or "A Towel":
        print("It hisses in disipointment, as you guessed correctly. It gives you a coin. You leave the closet and go out of the room, into the hall. You win!")
        totalcoins = totalcoins+1
    else:
        print("The sphinx smiles evilly. You guessed wrong. She eats you.")
elif startChoice == "3":
    print("You fall into a pit of glowing green liquid, which turns out to be acid.")
    print("You die")
else:
    print("You didn't put 1, 2 or 3.")
    

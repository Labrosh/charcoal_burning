import random
import os

# Let's put dumb variables up here
press_enter = "Press enter to continue... "
bad_reply = "Sorry, I don't know that"
wood_options = [1, 1, 1, 2, 2, 2, 3, 3,
                4]  # Possible wood values - Testers complained about how bad the rates were - maybe revisit.
game_ticks = 0

player_resources = {
    "wood": 0,
    "charcoal": 0,
    "kiln_status": "unbuilt",
    "burn_time": 0
}  # This will be reworked someday


# Let's put all the functions up here.

def display_time():
    current_hour = game_ticks % 24
    current_day = game_ticks // 24
    print(f"Day {current_day + 1}, Hour {current_hour + 1}\n")


def print_centered(text):
    try:
        # Get terminal width, fallback to 80 if not available
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80  # Default width for non-TTY environments

    for line in text.splitlines():
        print(line.center(terminal_width))


def show_intro():
    cabin_art = r"""
                ~   ~  ~   ~   ~  ~   ~
             ~      ~   ~   ~   ~  ~     ~
        ~  ~    ~    ~   ~  ~  ~   ~  ~   ~
                 ^  ^  ^   ^      ___I_
               /|\/|\/|\ /|\    /\-_--\\
              /|\/|\/|\ /|\   /  |  \\_\\
             /|\/|\/|\ /|\  /    \\    ~
        -------------------------------------
            WELCOME TO THE LIFE OF A 
              CHARCOAL BURNER
        -------------------------------------
    """
    print_centered(cabin_art)
    print("\nAlright, kid. If you're going to survive, you need to learn how to make charcoal.")
    print("First, gather some wood. Get at least 10. Type 'chop' to chop wood.\n")


def chop_wood():  # Our bread and butter chopping
    global game_ticks
    game_ticks += 1
    wood_random = random.choice(wood_options)
    player_resources["wood"] += wood_random
    show_art("chop")  # Show chopping art
    print(f"\nYou managed to gather {wood_random} wood.")
    print(f"You have {player_resources['wood']} wood so far.\n")
    print("Do you want to chop more, or quit and do something else?\n")


def build_kiln():  # Have to have a kiln to burn logs
    if player_resources["kiln_status"] in ["built - unlit", "built - lit", "charcoal ready"]:
        print("\nYou already have a kiln. Maybe you need to 'light' it or 'collect' charcoal first?\n")
        input(press_enter)
    else:
        global game_ticks
        game_ticks += 1
        kiln_cost = 10
        if player_resources["wood"] >= kiln_cost:
            player_resources["wood"] -= kiln_cost
            player_resources["kiln_status"] = "built - unlit"
            show_art("build")  # Show kiln-building art
            print(f"\nYou used {kiln_cost} wood to build a kiln.")
            print(f"You have {player_resources['wood']} remaining.\n")
        else:
            print(f"\nYou need more wood. Try to chop some more trees.")


def light_kiln():  # and we have to light a fire to get fire...
    if player_resources["kiln_status"] == "unbuilt":
        print(f"\nYou don't have a kiln to light. Try building one first.\n")
    elif player_resources["kiln_status"] == "built - lit":
        print(f"\nThe kiln is already burning. Just wait for the charcoal to finish.\n")
    elif player_resources["kiln_status"] == "built - unlit":
        global game_ticks
        game_ticks += 1
        show_art("light")  # Show lighting art
        print(f"\nYou light the kiln. Now you just have to wait for it to burn down...\n")
        player_resources["burn_time"] = random.randint(6, 10)
        player_resources["kiln_status"] = "built - lit"


def collect_charcoal():
    if player_resources["kiln_status"] != "charcoal ready":
        print("\nYou either don't have a kiln, or the charcoal is not ready yet.\n")
    else:
        global game_ticks
        game_ticks += 1
        charcoal_random = random.randint(1, 6)
        player_resources["charcoal"] += charcoal_random
        player_resources["kiln_status"] = "unbuilt"  # Kiln breaks after collection
        show_art("collect")  # Show collecting charcoal art
        print(f"\nYou dig out the charcoal, breaking the kiln and collecting {charcoal_random} charcoal.\n")
        print(f"You have a total of {player_resources['charcoal']} charcoal.\n")
        print("Your kiln has been destroyed. You'll need to build a new one.\n")
        input(press_enter)


def check_kiln():
    if player_resources["kiln_status"] == "charcoal ready":
        print("The kiln is silent, and the smoke has vanished. The charcoal is ready. Try collect to collect it.\n")
        return

    if player_resources["kiln_status"] != "built - lit":
        print("You don't have a lit kiln to check.\n")
        return
    global game_ticks
    game_ticks += 1

    # Decrease burn time
    if player_resources["burn_time"] > 0:
        player_resources["burn_time"] -= 1

    # Smoke hints based on burn time
    burn_hints = [
        (10, "Thick white smoke billows from the kiln. The wood is still releasing moisture.\n"),
        (5, "The smoke has thinned and turned a dull gray. The fire is steady.\n"),
        (2, "A thin blue smoke drifts from the kiln. The wood has almost fully charred.\n"),
        (1, "The kiln is nearly finished. Just a bit longer...\n"),
    ]

    for time, hint in burn_hints:
        if player_resources["burn_time"] >= time:
            print(hint)
            break

    # When burn time hits 0
    if player_resources["burn_time"] == 0:
        print("The kiln is silent, and the smoke has vanished. The charcoal is ready. Try to collect it.\n")
        player_resources["kiln_status"] = "charcoal ready"


def dev_mode():  # I was thinking this would be good, we could add more 'cheats' later
    player_resources["wood"] += 100
    print(f"\n(Dev Cheat) You now have {player_resources['wood']} wood.\n")


def quit_game():  # We all have to leave at some breakpoint

    print("\nYou decide to call it a day and leave the forest behind.")
    print("Here's what you accomplished:")
    print(f"  - Total wood gathered: {player_resources['wood']} pieces")
    print(f"  - Total charcoal created: {player_resources['charcoal']} pieces")

    if player_resources["charcoal"] > 10:
        print("You’re on your way to becoming a master charcoal burner!")
    elif player_resources["charcoal"] > 0:
        print("Not bad for a day's work. Keep at it!")
    else:
        print("Well, at least you tried. Maybe next time you'll get some charcoal!")

    input(press_enter)


def show_help():
    print("\nHere are the available commands:\n")
    for command, details in commands.items():
        if not details.get("hidden", False):  # Skip hidden commands
            print(f"  {command}: {details['description']}")
    print()




def show_art(key):
    art = ascii_art.get(key, None)  # Fetch the art based on the key
    if art:
        print(art)
    else:
        print("No art available for this action.")


ascii_art = {
    "chop": r"""
       ___
      /   \
     |  o o|
     |   ^  |   CHOP! CHOP!
     |  --- |
     \_____/
    """,
    "build": r"""
       _______
      /       \
     /         \
    |           |    A simple kiln is built!
     \         /
      \_______/
    """,
    "light": r"""
       (   )
      (   )
     (   )
    (~~~~~)
   (~~~~~~~)    Flames dance as you light the kiln.
    """,
    "collect": r"""
      _______
     /       \
    /  _____  \  
   |  /     \  |  You collect the charcoal!
    \_______/  
    """
}

commands = {
    "chop": {
        "function": chop_wood,
        "description": "Gather wood from nearby trees."
    },
    "build": {
        "function": build_kiln,
        "description": "Use wood to build a charcoal kiln."
    },
    "light": {
        "function": light_kiln,
        "description": "Light the kiln to start the burning process."
    },
    "check": {
        "function": check_kiln,
        "description": "Check on the status of the burning charcoal."
    },
    "collect": {
        "function": collect_charcoal,
        "description": "Gather finished charcoal once the kiln has burned down."
    },
    "quit": {
        "function": quit_game,
        "description": "Stop playing and exit the game."
    },
    "help": {
        "function": show_help,
        "description": "Display this list of available commands."
    },
    "time": {
        "function": display_time,
        "description": "Displays the current time in Days and Hours since the start of the game."
    },
    "cheat": {
        "function": dev_mode,
        "hidden": True,
        "description": "You shouldn't ever see this"
    }
}

# This is the old intro. RIP old intro
# print("Welcome to the life of a Charcoal Burner")
# print("----------------------------------------------------------------------------------")
# print("Alright, kid. If you're going to survive, you need to learn how to make charcoal.")
# print("First, gather some wood. Type 'chop' to chop wood.")
# print("----------------------------------------------------------------------------------")

show_intro()
# Let's chop some wood!
while True:
    player_action = input("What do you want to do? ").strip().lower()

    if player_action in commands:
        commands[player_action]["function"]()  # Call the associated function
    else:
        print(f"{bad_reply}. Did you mean to 'help'?\n")

import random
import os
import sys

# Let's put dumb variables up here
press_enter = "Press enter to continue... "
bad_reply = "Sorry, I don't know that"
wood_options = [1, 1, 1, 2, 2, 2, 3, 3, 4]
better_axe_options = [2, 3, 3, 4, 4, 5, 5, 6, 7] # WE REVISITED!
game_ticks = 0

# This will be reworked someday
player_resources = {
    "wood": 0,
    "charcoal": 0,
    "kiln_status": "unbuilt",
    "last_burn_game_tick": 0,
    "wood_limit": 10,
    "charcoal_limit": 5,
    "seen_trader_message": False,
    "gold": 0,  # Initial gold amount
    "last_trader_day": 0,  # Tracks the last trader visit
    "trader_available": False,  # No trader available initially
    "better_axe": False,
    "gold_goal": 100,  # Gold needed to end the game
    "game_complete": False,  # Tracks if the game is finished
    "declined_retirement": False,
}


chop_flavor = [
    "The forest echoes with the rhythmic sound of your axe.",
    "Sweat drips as you swing your axe steadily.",
    "The crisp smell of freshly cut wood fills the air.",
    "A cool breeze rustles the leaves as you work.",
    "You pause for a moment, catching your breath.",
    "The blade bites deep into the trunk with each swing.",
    "A bird chirps nearby, seemingly unbothered by your work.",
    "The pile of chopped wood grows steadily.",
    "The axe feels heavy, but you press on.",
    "The sun filters through the trees, warming your back.",
    "Your hands ache, but you feel a sense of accomplishment.",
    "A squirrel darts across the forest floor, watching you cautiously.",
    "The satisfying crack of splitting wood keeps you going.",
    "You clear away some underbrush to reach a better tree.",
    "A patch of sunlight highlights the tree you’re chopping.",
    "The forest seems alive with sounds as you work.",
    "The steady rhythm of chopping wood feels oddly calming.",
    "A small chip of bark flies past your face.",
    "The forest air feels fresh, invigorating your effort.",
    "You hear the distant call of a bird as you swing your axe."
]
collect_flavor = [
    "The charcoal smells sharp and smoky as you gather it.",
    "Blackened chunks of charcoal tumble into your hands.",
    "The kiln is still warm as you dig out the charcoal.",
    "You wipe soot from your hands as you work.",
]


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
    print("First, gather some wood. Get at least 10. Type 'chop' to chop wood. if you get stuck, ask for help.\n")


def chop_wood():
    global game_ticks
    game_ticks += 1

    if game_ticks % 24 == 0 and not player_resources.get("trader_available", False):
        trader()

    wood_random = random.choice(better_axe_options if player_resources["better_axe"] else wood_options)

    # Calculate available storage space
    space_left = player_resources["wood_limit"] - player_resources["wood"]

    if space_left <= 0:
        print("\nYour wood storage is full! Consider upgrading your storage.")
    elif wood_random > space_left:
        # Add only the amount that fits
        player_resources["wood"] += space_left
        show_art("chop")
        print(f"\nYou managed to gather {space_left} wood, but {wood_random - space_left} wood was wasted due to storage limits.")
    else:
        # Add all the wood if there's enough space
        player_resources["wood"] += wood_random
        show_art("chop")
        print(f"\nYou managed to gather {wood_random} wood.")

    # Flavor text is always shown after a chop
    print(random.choice(chop_flavor))
    print(f"You have {player_resources['wood']} wood so far (Limit: {player_resources['wood_limit']}).\n")

    display_time()


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
        player_resources["last_burn_game_tick"] = game_ticks + random.randint(6, 10)
        player_resources["kiln_status"] = "built - lit"


def collect_charcoal():
    if player_resources["kiln_status"] != "charcoal ready":
        print("\nYou either don't have a kiln, or the charcoal is not ready yet.\n")
    else:
        global game_ticks
        game_ticks += 1
        charcoal_random = random.randint(1, 6)
        if game_ticks % 24 == 0 and not player_resources.get("trader_available", False):
            trader()

        space_left = player_resources["charcoal_limit"] - player_resources["charcoal"]

        if space_left <= 0:
            print("\nYour charcoal storage is full! Consider upgrading your storage.")
        elif charcoal_random > space_left:
            player_resources["charcoal"] += space_left
            print(f"\nYou collected {space_left} charcoal, but {charcoal_random - space_left} was wasted due to storage limits.")
        else:
            player_resources["charcoal"] += charcoal_random
            print(f"\nYou collected {charcoal_random} charcoal.")
        print(random.choice(collect_flavor))
        player_resources["kiln_status"] = "unbuilt"  # Reset kiln
        print(f"You have {player_resources['charcoal']} charcoal so far (Limit: {player_resources['charcoal_limit']}).\n")
        input(press_enter)



def upgrade_storage():
    global game_ticks
    game_ticks += 1

    upgrade_cost = player_resources["wood_limit"]

    if player_resources["wood"] >= upgrade_cost:
        player_resources["wood"] -= upgrade_cost
        player_resources["wood_limit"] *= 2
        player_resources["charcoal_limit"] *= 2
        show_art("upgrade")
        print("\nYou upgraded your storage!")
        print(
            f"New wood limit: {player_resources['wood_limit']}, New charcoal limit: {player_resources['charcoal_limit']}.\n")
    else:
        print(f"\nYou don't have enough wood to upgrade. You need {upgrade_cost} wood.\n")


def check_kiln():
    # Check if the kiln is in a valid state
    if player_resources["kiln_status"] not in ["built - lit", "charcoal ready"]:
        print("\nYou don't have a lit kiln to check.\n")
        return

    global game_ticks
    burn_time_remaining = player_resources["last_burn_game_tick"] - game_ticks
    if burn_time_remaining > 0:
        game_ticks += 1  # Advance time for meaningful checks
        burn_time_remaining -= 1

    # Only advance time if there is something to check
    if burn_time_remaining > 0:
        burn_hints = [
            (10, "Thick white smoke billows from the kiln. The wood is still releasing moisture."),
            (5, "The smoke has thinned and turned a dull gray. The fire is steady."),
            (2, "A thin blue smoke drifts from the kiln. The wood has almost fully charred."),
            (1, "The kiln is nearly finished. Just a bit longer...")
        ]

        for time, hint in burn_hints:
            if burn_time_remaining >= time:
                print(hint)
                break
    elif burn_time_remaining <= 0 and player_resources["kiln_status"] == "built - lit":
        # When burning is complete
        print("\nThe kiln is silent, and the smoke has vanished. The charcoal is ready.\n")
        player_resources["kiln_status"] = "charcoal ready"
    else:
        # Inform the player there's no need to check
        print("\nThere’s nothing new to see. Be patient and let the kiln do its work.\n")


def trader():
    global game_ticks

    # Check if a trader is already available
    if player_resources.get("trader_available", False):
        return  # Do nothing if a trader is already nearby

    # Initial trader message
    if player_resources["charcoal"] >= 1 and not player_resources["seen_trader_message"]:
        print("Hey, you've collected some charcoal! Keep an eye out for traders who may want to buy it.")
        player_resources["seen_trader_message"] = True
        return

    # Check if enough time has passed for a trader to visit
    days_since_last_trader = game_ticks // 24
    if player_resources.get("last_trader_day", 0) < days_since_last_trader - 3:
        print("\nYou hear rumors of a trader heading your way. He should arrive soon!")
        player_resources["trader_available"] = True
        player_resources["last_trader_day"] = days_since_last_trader


def visit_trader():
    if not player_resources.get("trader_available", False):
        print("\nNo traders are nearby. Keep gathering charcoal and check back later!")
        print("Rumors say traders visit every few days, so be patient.")
        return

    print("\nA trader arrives, looking for charcoal!")

    # Trader personalities
    trader_personality = random.choice([
        ("grumpy", "A grumpy trader mutters under his breath as he approaches."),
        ("cheerful", "A cheerful trader greets you with a wide smile, carrying a large sack."),
        ("mysterious", "A mysterious trader eyes you cautiously, his face hidden under a hood."),
        ("talkative", "A talkative trader rambles about the latest market gossip as he sets up."),
        ("hurried", "A hurried trader rushes in, eager to complete his business quickly.")
    ])
    personality_type, personality_text = trader_personality
    print(personality_text)

    # Offer to sell charcoal
    charcoal_available = player_resources["charcoal"]
    amount_to_buy = random.randint(1, min(charcoal_available, 5))  # Randomize up to 5 or available
    price_per_charcoal = random.randint(2, 5)  # Randomize price between 2 and 5 coins
    total_price = amount_to_buy * price_per_charcoal

    print(f"The trader offers to buy {amount_to_buy} charcoal for {total_price} coins.")
    choice = input("Do you accept the offer? (yes/no): ").strip().lower()

    if choice == "yes":
        if charcoal_available >= amount_to_buy:
            player_resources["charcoal"] -= amount_to_buy
            player_resources["gold"] = player_resources.get("gold", 0) + total_price
            print(f"You sold {amount_to_buy} charcoal and earned {total_price} coins.")
            print(f"Current charcoal: {player_resources['charcoal']}")
            print(f"Current gold: {player_resources['gold']}\n")
        else:
            print("Something went wrong; you don't have enough charcoal to sell.")  # Failsafe
    else:
        print("The trader leaves, disappointed.\n")

    # Offer the better axe, with personality-specific dialog
    if not player_resources["better_axe"]:
        if personality_type == "grumpy":
            print("\n'You look like you could use a better axe,' the trader grumbles.")
        elif personality_type == "cheerful":
            print("\n'I’ve got the perfect tool for you! A better axe to make your life easier!'")
        elif personality_type == "mysterious":
            print("\nThe trader leans in and whispers, 'A tool for the ambitious. Interested?'")
        elif personality_type == "talkative":
            print("\n'Everyone’s been asking for this axe,' the trader chatters. 'Want one?'")
        elif personality_type == "hurried":
            print("\n'Quickly now, I’ve got a sturdy axe for sale. Take it or leave it!'")

        print("The trader offers to sell you the better axe for 50 gold.")
        axe_choice = input("Do you want to buy the better axe for 50 gold? (yes/no): ").strip().lower()
        if axe_choice == "yes":
            if player_resources["gold"] >= 50:
                player_resources["gold"] -= 50
                player_resources["better_axe"] = True
                print("You bought the better axe! Your wood-gathering efficiency has improved.")
            else:
                print(
                    f"You don't have enough gold to buy the better axe. (You have {player_resources['gold']}/50 gold.)")
        else:
            print("The trader shrugs and puts the axe away. 'Suit yourself.'")

    # Reset trader availability
    player_resources["trader_available"] = False


def check_endgame():
    if player_resources["gold"] >= player_resources["gold_goal"] and not player_resources["game_complete"]:
        if player_resources.get("declined_retirement", False):
            return  # Skip the check if the player previously declined retirement
        print("\nCongratulations! You've saved enough gold to leave the charcoal business.")
        print("Do you want to retire and end the game?")

        choice = input("Type 'yes' to retire or 'no' to keep playing: ").strip().lower()
        if choice == "yes":
            end_game()
        elif choice == "no":
            print("You decide to keep working. If you change your mind, type 'retire' to leave the charcoal business anytime.")
            player_resources["declined_retirement"] = True



def retire():
    if player_resources["gold"] >= player_resources["gold_goal"]:
        end_game()
    else:
        print(f"\nYou don’t have enough gold to retire yet. You need {player_resources['gold_goal']} gold to leave the charcoal business.")



def end_game():
    print("\n--- Final Summary ---")
    print(f"Total wood gathered: {player_resources['wood']}")
    print(f"Total charcoal created: {player_resources['charcoal']}")
    print(f"Total gold earned: {player_resources['gold']}")
    print(f"Days spent in the forest: {game_ticks // 24}")

    print("\nYou've worked hard and saved enough gold to leave the charcoal business behind.")
    print("A brighter future awaits you. Congratulations!")
    player_resources["game_complete"] = True
    sys.exit()  # Exit the game


def show_debug():
    print("\nDEBUG INFORMATION:")
    print(f"  - Game Ticks: {game_ticks}")
    print(f"  - Last Trader Day: {player_resources.get('last_trader_day', 0)}")
    print(f"  - Trader Available: {player_resources.get('trader_available', False)}")
    print(f"  - Wood: {player_resources['wood']} / {player_resources['wood_limit']}")
    print(f"  - Charcoal: {player_resources['charcoal']} / {player_resources['charcoal_limit']}")
    print(f"  - Gold: {player_resources['gold']}\n")
    print(f"  - Days Until Next Trader: {max(0, (player_resources['last_trader_day'] + 3) - (game_ticks // 24))}")
    print(f"  - Better Axe Owned: {player_resources['better_axe']}")
    print(f"  - Gold Goal: {player_resources['gold_goal']}")
    print(f"  - Game Complete: {player_resources['game_complete']}")


def dev_mode():
    show_art("cheat")
    print("\n(Dev Mode Activated) Choose an option:")
    print("1. Add 100 wood")
    print("2. Set wood to max")
    print("3. Set charcoal to max")
    print("4. Skip kiln burn time")
    choice = input("Enter the number of your choice: ").strip()

    if choice == "1":
        player_resources["wood"] += 100
        print(f"\nYou now have {player_resources['wood']} wood.\n")
    elif choice == "2":
        player_resources["wood"] = player_resources["wood_limit"]
        print(f"\nWood storage is now full: {player_resources['wood']} / {player_resources['wood_limit']}.\n")
    elif choice == "3":
        player_resources["charcoal"] = player_resources["charcoal_limit"]
        print(
            f"\nCharcoal storage is now full: {player_resources['charcoal']} / {player_resources['charcoal_limit']}.\n")
    elif choice == "4":
        player_resources["last_burn_game_tick"] = 0
        print("\nKiln burn time skipped to 1 hour.\n")
    else:
        print("\nInvalid choice. Please enter a valid number (1-4).\n")


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
    sys.exit()  # Exit the program completely


def show_help():
    print("\nHere are the available commands:\n")
    for command, details in commands.items():
        if details.get("showInHelp", False):  # Only show commands with showInHelp = True
            print(f"  {command}: {details['description']}")
    print()


def show_storage():
    show_art("storage")
    print("\nYour current storage:")
    print(f"  - Wood: {player_resources['wood']} / {player_resources['wood_limit']}")
    print(f"  - Charcoal: {player_resources['charcoal']} / {player_resources['charcoal_limit']}")
    print(f"  - Gold: {player_resources['gold']} / {player_resources['gold_goal']} (Goal to retire)")

    # Add notes if the player is near or at storage limits
    if player_resources["wood"] == player_resources["wood_limit"]:
        print("  Warning: Your wood storage is full! Consider upgrading your storage.")
    if player_resources["charcoal"] == player_resources["charcoal_limit"]:
        print("  Warning: Your charcoal storage is full! Consider upgrading your storage.")
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
    """,
    "storage": r"""
       _______
      | WOOD  |
      | SHED  |
      |       |     STORAGE
      |_______|
    """,
    "upgrade": r"""
         _______
        |  NEW  |      STORAGE UPGRADED!
        |  WOOD |
        |  SHED |
        |_______|
    """,
    "time": r"""
       ___
     _/   \_
    |  12   |     TIME CHECK
    |       |
    |_______|
    """,
    "cheat": r"""
      DEV MODE
       (o_o)
      <)   )>
       || ||
    """
}


commands = {
    "chop": {
        "function": chop_wood,
        "description": "Gather wood from nearby trees.",
        "showInHelp": True
    },
    "build": {
        "function": build_kiln,
        "description": "Use wood to build a charcoal kiln.",
        "showInHelp": True
    },
    "light": {
        "function": light_kiln,
        "description": "Light the kiln to start the burning process.",
        "showInHelp": True
    },
    "check": {
        "function": check_kiln,
        "description": "Check on the status of the burning charcoal.",
        "showInHelp": True
    },
    "collect": {
        "function": collect_charcoal,
        "description": "Gather finished charcoal once the kiln has burned down.",
        "showInHelp": True
    },
    "quit": {
        "function": quit_game,
        "description": "Stop playing and exit the game.",
        "showInHelp": True
    },
    "help": {
        "function": show_help,
        "description": "Display this list of available commands.",
        "showInHelp": True
    },
    "time": {
        "function": display_time,
        "description": "Displays the current time in Days and Hours since the start of the game.",
        "showInHelp": True
    },
    "cheat": {
        "function": dev_mode,
        "description": "(Dev Tool) Add 100 wood to your inventory.",
        "showInHelp": False  # Hidden from the help menu
    },
    "upgrade": {
        "function": upgrade_storage,
        "description": "Upgrade your storage capacity using wood",
        "showInHelp": True
    },
    "storage": {
        "function": show_storage,
        "description": "Check your current resources and storage limits.",
        "showInHelp": True
    },
    "visit": {
        "function": visit_trader,
        "description": "Interact with a trader to sell your charcoal.",
        "showInHelp": True
    },
    "debug": {
        "function": show_debug,
        "description": "(Dev Tool) Show debugging information.",
        "showInHelp": False
    },
    "retire": {
        "function": retire,
        "description": "Retire and end the game if you've saved enough gold.",
        "showInHelp": True
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
        commands[player_action]["function"]()  # Execute the function

        # Centralized endgame check
        check_endgame()

    else:
        print(f"{bad_reply}. Did you mean to 'help'?\n")


# =========================
# SCHOOL MYSTERY
# =========================

running = True
import random
import json
from student import Student
from student import(amy, ethan, zoe, mia)
from player import Player
from observation import Observation
from observation_data import possible_observations
from item import Item
from message import Message
from detective_helper_functions import(reputation_level, accusation_intro, trust_reaction, school_gossip, texts_you_helper, get_students_at_location,
display_students_here, yes_no_function, give_reward)
from toolbox import(pause, get_choice, display_choices)
from daily_events import run_daily_events
from quest import (Quest, display_quest_log)
from gamestate import GameState

game_state = GameState()

# =========================
# GAME DATA
# =========================

amy_quest = Quest(
    "Getting to know Amy",
    "Get to know Amy better.",
    2,
    0
)

ethan_quest = Quest(
    "Ethan's crush shenanigans",
    "Helping Ethan improve his relationship with Mia.",
    10,
    0
)

quests = [
    amy_quest, ethan_quest
]  

students = {
    "Amy": amy,
    "Ethan": ethan,
    "Zoe": zoe,
    "Mia": mia
}

current_location = "Home"

player = Player("Player")

notebook = Item("Emma's notebook.", "A notebook full of strange notes.")
photo = Item("Family photo.", "An old photo connected to Zoe.")
locker_key = Item("Locker key.", "A key to Emma's locker.")
locker_note = Item("Locker note.", "A note from Emma's locker.")
zoe_diary = Item("Zoe's diary.", "A diary of Zoe's, filled with people she dislikes.")
amy_notebook = Item("Amy's notebook.", "One of the notebooks Amy owns. It's full of odd remarks. ")

valid_items = [notebook, photo, locker_key, locker_note, zoe_diary, amy_notebook]

investigation_log = []

mystery_book_read =False

weekly_clues = {
    1: "Amy's journal holds suspicious information.",
    2: "You might wanna check out Zoe's hideout.",
    3: "Go explore the school when it's night. You can find Emma's locker there."
}

def clue_reports():
    current_week = game_state.get_current_week()
    print(f"\nCurrent week: {current_week}")
    for key, value in weekly_clues.items():
        if key <= current_week:
            print("\n=========================")
            print(f"Week: {key}")
            print(value)
            print("=========================")

def add_log_entry(hint=""):

    print("\n📖 Detective's notebook.")
    print(f"Hint: {hint}")

    entry = input("\nYour notes: ")

    investigation_log.append(entry)

def show_investigation_log():
    print("\n📖 INVESTIGATION LOG")

    if len(investigation_log) == 0:
        print("You haven't recorded any important findings yet.")
        return
    
    for number, entry in enumerate(investigation_log, start=1):
        print(f"{number}. {entry}")

def clue_satchel():
    print("\n💼 CLUE SATCHEL")
    clue_satchel_choices = ["Inventory", "Investigation log", "Previous observations", "Quest log"]
    print("DEBUG: MYSTERY BOOK READ:", mystery_book_read)
    print("DEBUG: CLUE SATCHEL CHOICES LIST:", clue_satchel_choices)
    if mystery_book_read == True:
        clue_satchel_choices.append("Clue reports")
        print("DEBUG: CLUE SATCHEL CHOICES LIST AFTER APPEND:", clue_satchel_choices)
    display_choices(clue_satchel_choices)

    choice = get_choice(1, len(clue_satchel_choices))

    if choice == 1:
        check_inventory()
    elif choice == 2:
        show_investigation_log()
    elif choice == 3:
        show_observations()
    elif choice == 4:
        display_quest_log(quests)
    elif choice == 5:
        clue_reports()


# =========================
# SAVE / LOAD
# =========================

def save_game(): 
    global mystery_book_read
    game_state.times_saved += 1

    data = {
        "player": player.to_dict(),

        "students": {
            "Amy": amy.to_dict(),
            "Ethan": ethan.to_dict(),
            "Mia": mia.to_dict(),
            "Zoe": zoe.to_dict()
        },

        "quests": {
            quest.title: quest.to_dict()
            for quest in quests
        },

        "game": game_state.to_dict(),

        "observations": {
    period: [
        current_observation.to_dict()
        for current_observation in observations
    ]
    for period, observations in possible_observations.items()
},

    "perks": {
        "trust_bonus": Student.trust_bonus,
        "reputation_bonus": Player.reputation_bonus,
        "mystery_book_read": mystery_book_read
    },

    "pets": {
        "pet_name": player.pet_name,
        "pet_species": player.pet_species,
        "old_pet_name": player.old_pet_name,
        "old_pet_species": player.old_pet_species
    },

    "investigation_log": investigation_log
        }
    with open("save_file.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Game saved!")


def load_game():
    global mystery_book_read

    with open("save_file.json", "r") as file:
        data = json.load(file)

    player.reputation = data["player"]["reputation"]
    player.contacts = data["player"]["contacts"]
    player.inventory = []

    for item_data in data["player"]["inventory"]:
        item = Item(item_data["name"], item_data["description"])
        item.load_from_dict(item_data)
        player.add_item(item)
    player.visited_locations = data["player"]["visited_locations"]

    for student_name in students:
        student = students[student_name]

        student.messages = []

        for message_data in data["students"][student_name]["messages"]:
            message = Message(
                message_data["sender"],
                message_data["text"],
                message_data["day_sent"],
                message_data["time_sent"]
            )

            student.messages.append(message)

    saved_observations = data.get("observations", {})

    for period, saved_period_data in saved_observations.items():
        current_period_observations = possible_observations.get(period, [])

        for observation, observation_data in zip(
            current_period_observations,
            saved_period_data
        ):
            observation.load_from_dict(observation_data)

    investigation_log.clear()
    investigation_log.extend(data.get("investigation_log", []))

    saved_quests = data.get("quests", {})

    for quest in quests:
        if quest.title in saved_quests:
            quest.load_from_dict(
                saved_quests[quest.title]
        )

    Student.trust_bonus = data["perks"]["trust_bonus"]
    Player.reputation_bonus = data["perks"]["reputation_bonus"]
    mystery_book_read = data["perks"]["mystery_book_read"]

    player.pet_name = data["pets"]["pet_name"]
    player.pet_species = data["pets"]["pet_species"]
    player.old_pet_name = data["pets"]["old_pet_name"]
    player.old_pet_species = data["pets"]["old_pet_species"]

    amy.load_from_dict(data["students"]["Amy"])
    ethan.load_from_dict(data["students"]["Ethan"])
    mia.load_from_dict(data["students"]["Mia"])
    zoe.load_from_dict(data["students"]["Zoe"])

    game_state.load_from_dict(data.get("game", {}))

    print("Game loaded!")
    print("Times saved:", game_state.times_saved)

def developer_menu():
    global interactions_left

    while True:
        print("\n=== DEVELOPER MENU ===")
        developer_menu_choices = ["Jump to day", "Set game time", "Set reputation", "Unlock all contacts", "Set interactions left", 
"Add item to inventory", "Exit"]

        display_choices(developer_menu_choices)

        choice = get_choice(1, 7)

        if choice == 1:
            game_state.current_day = int(input("Enter day: "))
            print(f"Day changed to {game_state.current_day}.")

        elif choice == 2:
            game_state.current_time = int(input("Enter game time: "))
            print(f"Time changed to {game_state.current_time}.")

        elif choice == 3:
            player.reputation = int(input("Enter reputation: "))
            print(f"Reputation changed to {player.reputation}.")

        elif choice == 4:
            ethan.contact_unlocked = True
            mia.contact_unlocked = True
            zoe.contact_unlocked = True
            amy.contact_unlocked = True
            print("Contacts unlocked.")

        elif choice == 5:
            interactions_left = int(input("Enter interactions left: "))
            print(f"Interactions left set to {interactions_left}")

        elif choice == 6:
            display_choices(valid_items)

            choice = get_choice(1, len(valid_items))

            item = valid_items[choice - 1]

            if item in player.inventory:
                print("You already have that item.")
            else:
                player.add_item(item)
                print(f"'{item}' Added to inventory.")

        elif choice == 7:
            break

# =========================
# NOTIFICATIONS
# =========================

notifications = []
phone_open = False

def add_notification(text):
    notifications.append(text)

def show_notifications():
    if len(notifications) == 0:
        if phone_open:
            print("\nNo notifications.")
        return

    print("\n🔔 Notifications:")
    for notification in notifications:
        print("-", notification)
        
    else:
        print("\n🔔 Notifications")

        for notification in notifications:
            print(f"- {notification}")

def clear_notifications():
    notifications.clear()

    print("Notifications cleared!")


# =========================
# DAYS
# =========================

hours = game_state.current_time // 60
minutes = game_state.current_time % 60

def make_time(hour, minute=0, period="AM"):
    if period.upper() == "PM" and hour != 12:
        hour += 12
    elif period.upper() == "AM" and hour == 12:
        hour = 0

    return hour * 60 + minute

def display_time(current_time):
    hour_24 = current_time // 60
    minutes = current_time % 60

    period = "AM" if hour_24 < 12 else "PM"

    hour_12 = hour_24 % 12

    if hour_12 == 0:
        hour_12 = 12

    return f"{hour_12}:{minutes:02d} {period}"

def get_time_period():
    if make_time(5, 0, "AM") <= game_state.current_time < make_time(10, 0, "AM"):
        return "Sunrise"

    elif make_time(10, 0, "AM") <= game_state.current_time < make_time(12, 0, "PM"):
        return "Morning"

    elif make_time(12, 0, "PM") <= game_state.current_time < make_time(2, 0, "PM"):
        return "Noon"

    elif make_time(2, 0, "PM") <= game_state.current_time < make_time(5, 0, "PM"):
        return "Afternoon"

    else:
        return "Night"
    
def display_game_period_time(current_time):
    readable_time = display_time(current_time)
    period = get_time_period()

    emojis = {
        "Sunrise": "🌅",
        "Morning": "☀️",
        "Noon": "🍽️",
        "Afternoon": "🌤️",
        "Night": "🌙"
    }

    emoji = emojis.get(period, "🕒")

    return f"{emoji} {readable_time} — {period}"

def next_day():
    global running
    global interactions_left
    game_state.current_time = make_time(hour=5, minute=00, period="AM")
    print(game_state.current_time)
    print(get_time_period())

    print("\n🛌 You go to bed...💤")
    pause()
    print("\n🌅 You wake up...")
    pause()

    game_state.current_day += 1
    print(f"\n☀️  Day {game_state.current_day}")
    display_game_period_time(game_state.current_time)
    running = True
    interactions_left = 5

    print("\n\n⏰ You wake up and get ready for the day.")

    main_daily_events()

# =========================
# QUESTS, DAILY EVENTS
# =========================

def main_daily_events():
    global player

    if ethan.contact_unlocked:
        run_daily_events(player, ethan, game_state.current_day, game_state.current_time, mia_trust=mia.trust)

# =========================
# MAIN MENU
# =========================

def main_menu():
    global running
    current_location = "Main menu"

    while running:
        print(
            f"=== SCHOOL MYSTERY === DAY: {game_state.current_day}    |⌚TIME: {display_game_period_time(game_state.current_time)}\n")

        period = get_time_period()
        actions = []

        if period == "Sunrise":
            actions = [
                ("Go somewhere", 60),
                ("Skip to 10AM", 0),
                ("Open satchel", 0),
                ("Quit", 0)
            ]

        elif period in ["Morning", "Noon", "Afternoon"]:
            actions = [
                ("Talk to students", 60),
                ("Go somewhere", 30),
                ("Accuse someone", 60),
                ("Observe", 30),
                ("Open satchel", 0),
                ("Text", 30),
                ("Save game", 0),
                ("Load game", 0),
                ("Devs menu", 0),
                ("Quit", 0)
            ]

        elif period == "Night":
            actions = [
                ("Go somewhere", 60),
                ("Sleep", 0),
                ("Open satchel", 0),
                ("Quit", 0)
            ]

        else:
            print("UNKNOWN PERIOD:", repr(period))
            running = False
            continue

        for number, action in enumerate(actions, start=1):
            print(f"{number}. {action[0]}")

        choice = get_choice(1, len(actions))
        action_name, time_cost = actions[choice - 1]

    # SCHOOL DAYTIME
        if action_name == "Talk to students":
            question_students()

        elif action_name == "Accuse someone":
            accuse_someone()

        elif action_name == "Observe":
            observe()

        elif action_name == "Save game":
            save_game()
        
        elif action_name == "Load game":
            load_game()

    # NIGHT TIME
        elif action_name == "Sleep":
            next_day()

    # SUNRISE
        elif action_name == "Skip to 10AM":
            game_state.current_time = make_time(hour=10, minute=00, period="AM")

    # ANY
        elif action_name == "Quit":
            running = False

        elif action_name == "Open satchel":
            clue_satchel()

        elif action_name == "Go somewhere":
            go_somewhere()

        elif action_name == "Text":
            text()

        elif action_name == "Devs menu":
            developer_menu()

        game_state.current_time += time_cost

        pause()

# =========================
# LOCATIONS
# =========================


def go_somewhere():

    period = get_time_period()

    locations = []

    print("\n=== LOCATIONS ===")
    if period == "Sunrise":
        locations = ["Cafe", "Library", "Pet Store"]
        display_choices(locations)

    elif period in ["Morning", "Noon", "Afternoon"]:
        locations = ["Emma's classroom", "Courtyard", "Zoe's hideout", "Hallways", "Cafeteria"]
        display_choices(locations)

    elif period == "Night":
        locations = ["Emma's classroom", "Courtyard", "Zoe's hideout", "Hallways", "Cafeteria"]
        if ethan.secret_told and "ethan_date_event" not in player.completed_events:
            locations.append("Ethan's date")
        display_choices(locations)

    choice = get_choice(1, len(locations))

    chosen_location = locations[choice - 1]

    if chosen_location == "Cafe":
        current_location = "Cafe"
        cafe()
    elif chosen_location == "Library":
        current_location = "Library"
        library()
    elif chosen_location == "Pet Store":
        current_location = "Pet Store"
        pet_store()
    elif chosen_location == "Courtyard":
        current_location = "Courtyard"
        school_courtyard()
    elif chosen_location == "Emma's classroom":
        current_location = "Emma's classroom"
        emma_classroom()
    elif chosen_location == "Hallways":
        current_location = "Hallways"
        hallway()
    elif chosen_location == "Cafeteria":
        current_location = "Cafeteria"
        cafeteria()
    elif chosen_location == "Zoe's hideout":
        current_location = "Zoe's hideout"
        zoe_hideout()

def text():
    global phone_open
    phone_open = True
    show_notifications()

    if len(notifications) >= 1:
        input("Delete notifications")
        clear_notifications()

    print("\nWho do you text?")
    print("\nContacts:")

    contacts = []

    if ethan.contact_unlocked:
        contacts.append("Ethan")

    if mia.contact_unlocked:
        contacts.append("Mia")

    if amy.contact_unlocked:
        contacts.append("Amy")

    if zoe.contact_unlocked:
        contacts.append("Zoe")

    display_choices(contacts)

    choice = get_choice(1, 4)

    if choice == 1 and ethan.contact_unlocked:
        text_ethan()

    phone_open  = False

def text_ethan():

    print("You text Ethan...")

    ethan.show_chat()

    print("\n1. Ask him for clues\n2. Ask him about Mia")
    if ethan.acting_sus == True:
        print("\n3.Ask him who he was texting before")

    choice = get_choice(1, 2)

    print("\n📱 You text Ethan.")
    if choice == 1:
        ethan_texting_choice_1()

    elif choice == 2:
        ethan_texting_choice_2()

    
    elif choice == 3 and ethan.acting_sus == True:
        ethan_texting_choice_3()


def ethan_texting_choice_1():
    ethan.receive_message( "You", "Could you give me any clues?", game_state.current_day, game_state.current_time)

    if ethan.lied_to == True:
        texts_you_helper(self=ethan)
        ethan.receive_message( "Ethan", "No, you lied to me.", game_state.current_day, game_state.current_time)
    else:
        pause()
        texts_you_helper(self=ethan)
        ethan.receive_message( "Ethan", "Amy is smart, I think you could trust her", game_state.current_day, game_state.current_time)
        pause()
        ethan.receive_message( "You", "You could come question her with me..", game_state.current_day, game_state.current_time)
        pause()
        texts_you_helper(self=ethan)
        ethan.receive_message( "Ethan", "Aye aye captain!", game_state.current_day, game_state.current_time)
        ethan.remember("ethan_player_question_amy")


def ethan_texting_choice_2():
    print("\n📱 You text Ethan.")
    ethan.receive_message( "You", "Hows it going with you and Mia?.", game_state.current_day, game_state.current_time)

    if ethan.lied_to == True:
        texts_you_helper(self=ethan)
        ethan.receive_message( "Ethan", "Not great because of a certain someone.", game_state.current_day, game_state.current_time)
    elif ethan.lied_to == False:
        texts_you_helper(self=ethan)
        ethan.receive_message( "Ethan", "She says that I'm funny! Great!", game_state.current_day, game_state.current_time)
    else:
        ethan.receive_message( "Ethan", "Just neutral.", game_state.current_day, game_state.current_time)
    pause()
    ethan.receive_message( "You", "Nice.", game_state.current_day, game_state.current_time)


def ethan_texting_choice_3():
    print("\n📱 You text Ethan.")
    ethan.receive_message( "You", "Who were you texting with earlier?", game_state.current_day, game_state.current_time)

    if ethan.lied_to == True:
        texts_you_helper(self=ethan)
        ethan.receive_message( "Ethan", "Mia, but it went completely wrong.", game_state.current_day, game_state.current_time)
    elif ethan.lied_to == False:
        texts_you_helper(self=ethan)
        ethan.receive_message( "Ethan", "Mia, I think it went well!", game_state.current_day, game_state.current_time)
    else:
        texts_you_helper(self=ethan)
        ethan.receive_message( "Ethan", "Amy.", game_state.current_day, game_state.current_time)
        pause()
        ethan.receive_message( "Ethan", "I was trying to copy her work.", game_state.current_day, game_state.current_time)
        pause()
        ethan.receive_message( "You", "You're playing a crucial part in a missing person case...", game_state.current_day, game_state.current_time)
        pause()
        ethan.receive_message( "You", "And you're cheating on a test?", game_state.current_day, game_state.current_time)


def emma_classroom():

    print("\nYou enter Emma's classroom.")

    display_students_here(students, "Emma's classroom", get_time_period())

    if notebook.took == False:

        print("\nYou find Emma's notebook.")
        print("1. Take notebook")
        print("2. Leave it")

        choice = get_choice(1, 2)

        if choice == 1:
            player.add_item(notebook)
            add_notification("Emma's notebook added to inventory!")
            notebook.took = True
            print("Notebook added!")


def school_courtyard():

    print("\nYou enter the courtyard.")

    display_students_here(students, "Courtyard", get_time_period())

    if photo.took == False:

        print("You discover an old family photo.\nDo you take it?")

        print("\n1.Yes\n2. No")

        choice = get_choice(1, 2)

        if choice == 1:
            player.add_item(photo)
            photo.took = True
            print("Photo added!")

            add_log_entry(hint="Hint: Write about where you found this, and how it might be useful.")


def zoe_hideout():

    if zoe.trust < 5:
        print("\n⚠️  Zoe doesn't trust you enough.")
        return

    print("\nYou enter Zoe's hideout.")

    display_students_here(students, "Zoe's hideout", get_time_period())

    zoe.secret_told = True

    if zoe_diary.took == False:
        print("You discover Zoe's diary...")
        print("Do you take it?\n\n1. Yes\n2. No")

        choice = get_choice(1, 2)

        if choice == 1:
            print("Diary added!")
            player.add_item(zoe_diary)
            add_notification("Zoe's diary added to inventory!")
            add_notification("Ethan texted you!")
            zoe_diary.took = True

def cafeteria():
    display_students_here(students, "Cafeteria", get_time_period())

    if get_time_period() == "Night":
        print("You look around the dark cafeteria..")
        print("You find Ethan's half-finished bag of doritos.")

        if locker_key not in player.inventory:
            print("\nThe cafeteria is completely silent.\n\n Most of the kitchen equipment has been cleaned and put away.")
            print("\nSomething shiny catches your eye beneath a storage shelf.")
            print("\n You kneel down and pull it out.\n A small keyring.\n The tag attached to it reads:")
            print("'Emma carter: Locker 18'")
            print("Do you take it?\n\n1. Yes\n2. No")

            choice = get_choice(1, 2)

            if choice == 1:
                player.add_item(locker_key)
    else:
        print("You walk around the cafeteria.")
        if game_state.current_time >= 720 and game_state.current_time <= 780:
            print("\nStudents are eating and chatting.")
        elif game_state.current_time >= 600 and game_state.current_time < 720:
            print("Only a few students are here, they're skipping class.")
            print("Staff seem to be preparing food.")

def hallway():
    display_students_here(students, "Hallways", get_time_period())

    print("You go to the hallways.")

    if get_time_period() == "Night":
        print("You walk around the hallway, flashlight in hand.")
        print("You hear the wooden floorboards creek every step you take..")

        print("\n1. Look at Emma's locker")
        print("2. Look at Amy's locker")

        choice = get_choice(1, 2)

        if choice == 1:
            emma_locker_branch()

        elif choice == 2:
            amy_locker_branch()

    else:
        print("\nYou walk around the hallway.")
        school_gossip()
        print("You find Emma's locker.")
        if locker_key in player.inventory and locker_note not in player.inventory:
            print("You can't open the locker right now.")
            print("Too many people are watching.")
        elif locker_key not in player.inventory:
            print("You don't have the key.")
            print("You could try looking around at night...")

def emma_locker_branch():
    if locker_note.took:
        print("You've already checked Emma's locker.")

    if locker_key in player.inventory:
        print("Do you open the locker?\n\n1. Yes\n2. No")
        choice = get_choice(1, 2)

        if choice == 1:
            print("You open Emma's locker...")
            print("You find a copy of the family photo. On the back is a handwritten message.")
            print("'Don't let Zoe find this.'")
            player.add_item(locker_note)
            locker_note.took = True

    else:
        print("You stop infront of it...")
        print("If only you had a key...")

def amy_locker_branch():
    if amy_quest.status == "accepted":
        print("You find Amy's locker.")
        print("\nIt's unlocked.")
        print("\n1.Open locker")
        print("2. Don't")

        choice = get_choice(1, 2)

        if choice == 1:
            print("You open the locker.")
            print("\nA book that was being supported by the door tumbles to the ground.")
            print("The book stops at your feet.")

            print("\nPick the book up?")
            yes_no_function()
            choice = get_choice(1, 2)

            if choice == 1:
                player.inventory.append(amy_notebook)
                print("You pick the book up.")
                print("Actually, upon inspection, it's actually a notebook.")
                print("The front is signed by Amy.")

                add_notification("Meet Amy at the library before school to give this to her!")

    else:
        print("Nothing interesting here. It's locked.")

def cafe():
    print("You enter the cafe.")
    print("The bell chimes behind you as you close the door.")

    display_students_here(students, "Cafe", get_time_period())

    print("\nYou take a seat near the window.")
    print("A waiter hands you a menu.")

    print("\n1.☕ Get a coffee\n(5$)\n(10 minutes)")
    print("2.🥞 Get the breakfast special.\n(16.50$)\n(30 minutes)")

    choice = get_choice(1, 2)

    if choice == 1:
        print("You order a black coffee.")
        pause()
        print("Your mind feels clearer after drinking it.")
        game_state.current_time += 10
        pause()
        print("You gained an extra interaction for the day!")
        interactions_left += 1

    elif choice == 2:
        print("You order the breakfast special.")
        pause()
        print("Pancakes served with maple syrup, eggs, and bacon.")
        pause()
        print("As you eat, you overhear the town gossip from a few locals.")
        pause()

        print("\nLocal 1:\n'Did you hear about Maryl's daughter? Poor girl.'")
        pause()
        print("\nLocal 2:\n'Yea, Emma. She was kidnapped.'")
        pause()
        print("\nLocal 1:\n'Honestly, the teachers seem suspicious.'")
        pause()
        print("Local 3:\n'Personally, I think a student and teacher worked together.'")

        add_log_entry(hint="Hint: Write about what you learned from the gossip.")

    pause()

def library():
    print(player.pet_name, player.pet_species)
    global mystery_book_read
    amy.override_location = "Cafe"
# DOES NOT NEED DISPLAY_STUDENTS_HERE
    students_here = get_students_at_location(students, "Library", get_time_period())

    if amy in students_here:

        print("\nYou enter the local library.")
        print("Amy is there, she's reading a book.")

        print("\n1. Talk to her")
        print("2. Quietly watch her")

        choice = get_choice(1, 2)

        if choice == 1:
            library_amy_choice_1()

        elif choice == 2:
            print("\nYou watch Amy from afar.")
            pause()
            print("\nYou catch a glimpse of her book cover.\nIt's about phsycology and self improvement.")
            pause()
            print("\nShe jots down notes about the book in her journal whilst reading.\nIt's quite impressive, actually.")
            pause()
            print("\nShe notices you watching.")

    else:
        print("\n1. Go pick out a book")
        print("2. Leave")
        choice = get_choice(1, 2)

        if choice == 1:
            print("\nYou walk to the bookshelf. What do you pick?")
            print("\n1. Phsycology book")
            # You gain more trust
            print("2. Mystery")
            # Unlock more detective related things
            print("3. History")
            # More dialogue

            choice = get_choice(1, 3)

            if choice == 1:
                print("\nYou read a book about human phsycology.")
                pause()
                Student.trust_bonus = 1
                print("\n You learn how to gain more trust through your interactions.")

            elif choice == 2:
                print("\nYou read a book about mysterys.")
                pause()
                print("\nYou learn more about how to find more clues.")
                mystery_book_read = True

            elif choice == 3:
                print("\nYou read a book about history.")
                pause()
                Player.reputation_bonus = 1
                print("\nYou learn how to gain more reputation through your interactions.")

    if player.pet_species == "Cat":
        if player.cat_found_clue == False:
            print(f"\n{player.pet_name} suddenly jumps onto one of the shelves.")
            pause()
            print(f"{player.pet_name} makes a book knock onto the floor.")
            pause()
            print("\nSomething falls out from between the pages...")
            player.cat_found_clue = True
            add_log_entry("Write about what you discovered from this:")

    raven_fly()

    sniff_result = dog_sniff()

    if sniff_result == "clue_found":
        print(f"{player.pet_name} finds a book with a piece of paper tucked into it!")
    elif sniff_result == "no_clue_found":
        print(f"{player.pet_name} sniffed out an old cup of coffee somebody left on the table!")



def library_amy_choice_1():
    print("You take a seat across from her.")

    if amy_notebook in player.inventory and amy_quest.status == "accepted":
        print("Do you want to give Amy her notebook?")
        yes_no_function()
        choice = get_choice(1, 2)

        print("You give Amy her notebook.")
        player.remove_item(amy_notebook)
        print("\nAmy:\n'Thanks. I appreciate this.'")
        amy_quest.status = "complete"
        give_reward(player, student=amy, trust=amy_quest.reward)
        add_notification("Go check your quest log to claim the reward!")
        amy.remember("player_found_notebooks")

    if amy.secret_exposed:
        print("Amy's expression slightly sours.")
        pause()
        print("\nAmy:\n'What do you want?'")
    else:
        print("Amy looks up from her book.")
        pause()
        print("\nAmy:\n'Didn't expect you to be here.'")
    
        print("\n1. Ask her what she's reading")
        print("2. Let her ask you something")

        choice = get_choice(1, 2)

        if choice == 1:
            if amy.secret_exposed:
                print("\nAmy:\n'It's a self improvement book. I think you should read it too.'")
            else:
                print("\nAmy:\n'It's a book about self improvement.'")

        elif choice == 2:
            if amy.secret_exposed:
                print("\nAmy:\n'Why are you here? You don't seem much of a reader.'")
            else:
                if amy_quest.status != "complete":
                    print("\nAmy:\n'This is unlikely of me but...'")
                    pause()
                    print("\nAmy:\n'I lost one of my notebooks the other day.'")
                    pause()
                    print("\nAmy:\n'Could you find it for me? It's a lined hardcover black colored book. It should have my name signed on it.'")
                    yes_no_function()
                    print("Saying yes will trigger a quest!")
                    choice = get_choice(1, 2)

                    if choice == 1:
                        amy_quest.accept()
                    else:
                        amy_quest.decline()
                else:
                    print("Didn't expect you to be here.")

def check_adoption_cooldown():
    if player.day_returned is not None:
        available_day = player.day_returned + 14
        return available_day

def pet_store():
    print("day reutrn", player.day_returned)
    print("current pet", player.pet_name)
    print("current old pet", player.old_pet_name)

    # You currently own a pet
    if player.pet_species is not None:
        already_have_pet()
        return

    # You have an old pet waiting
    if player.old_pet_species is not None:
        have_old_pet_ver()
        return

    # You've never returned a pet
    if player.day_returned is None:
        default_pet_menu()
        return
    else:
    # You returned a pet before, so check the cooldown
        print("CURRENT: DAY", game_state.current_day)
        print("return day", player.day_returned)
        print("avaialbe day", available_adopt_day)

        available_adopt_day = check_adoption_cooldown()

        if game_state.current_day >= available_adopt_day:
            default_pet_menu()
        else:
            print("\nYou can't adopt any new pets yet!")
            print(f"Come back on day {available_adopt_day}.")

def default_pet_menu():

    if player.pet_species != None:
        already_have_pet()

    else:
        print("\nYou walk into a pet store.")
        print("The sound of claws, meows, and chattering fill your ears.")
        pause()
        print("You walk towards a few cages.")
        pause()
        print("\nYou see a raven, a Border Collie, and a cat.")
        print("Do you adopt one?")

        yes_no_function()

        choice = get_choice(1, 2)

        if choice == 1:
            print("Which one do you pick?")
            print("\n1. Raven")
            print("2. Border Collie")
            print("3. Cat")

            choice = get_choice(1, 3)

            if choice == 1:
                player.pet_species = "Raven"
            elif choice == 2:
                player.pet_species = "Dog"
            elif choice == 3:
                player.pet_species = "Cat"

            print(f"\nYou sign the papers required to adopt the {player.pet_species}.")
            player.pet_name = input(f"\nName your new {player.pet_species}: ")
            print(f"{player.pet_name} curiously tilts it's head at you.")

            print(player.old_pet_species)

def have_old_pet_ver():

    print(f"\nRe-adopt {player.old_pet_name}?")

    yes_no_function()
    choice = get_choice(1, 2)

    if choice == 1:
        if random.randint(1, 10) <= 5:
            player.old_pet_available = False
            print(f"Oops, somebody has adopted your old pet, {player.old_pet_name}...")
            pause()
            print(f"\nShelter staff:\n'We are sorry to inform that {player.old_pet_name} has been taken in by somebody else.'")
            pause()
            print("\nShelter staff:\n'Please come again.'")
            player.remove_old_pet()

        else:
            player.old_pet_available = True
            print(f"{player.old_pet_name} eagerly nudges the cage after seeing you.")
            pause()
            print(f"You sign the papers required to adopt {player.old_pet_name}")
            player.change_old_pet_to_new()
            player.remove_old_pet()

    elif choice == 2:
        available_adoption_day = check_adoption_cooldown()

        if available_adoption_day is None:
            default_pet_menu()

        elif game_state.current_day < available_adoption_day:
            print("\nYou can't adopt a new pet yet!")
            print(f"Come back on day {available_adoption_day}.")

        else:
            default_pet_menu()

def already_have_pet():
    print("You already have a pet!")
    pause()

    print(f"Pet name: {player.pet_name}")
    print(f"Pet species {player.pet_species}")

    pause()
    print(f"Do you want to return {player.pet_name}?")

    yes_no_function()
    choice = get_choice(1, 2)

    if choice == 1:
        if player.old_pet_species is not None:
            have_old_and_new_pet()
            return
        player.day_returned = game_state.current_day
        print("DEBUG RETURN DAY", player.day_returned)
        player.change_new_pet_to_old()
        player.remove_pet()

def have_old_and_new_pet():
    print(f"\nAs you return your {player.pet_species}...")
    pause()
    print(f"You notice a happy couple standing besides {player.old_pet_name}, your old pet.")
    pause()
    print(f"They give {player.old_pet_name} a new name.")
    pause()
    print("They sign the adoption papers.")
    pause()
    print(f"{player.old_pet_name} leaves with them.")
    pause()
    print(f"You return {player.pet_name} as they leave.")

    player.remove_old_pet()
    player.change_new_pet_to_old()
    player.remove_pet()

def dog_sniff():
    if player.pet_species == "Dog":
        pause()
        print(f"\n{player.pet_name} starts sniffing the air and dragging you towards somewhere...")
        pause()
        if random.randint(1, 10) <= 5:
            print(f"{player.pet_name} finds a clue!")
            print("\nClue found!")
            return "clue_found"
        else:
            print(f"{player.pet_name} turns out, it was a false alarm!")
            print("\nNo clue found...")
            return "no_clue_found"

def raven_fly():
    if player.pet_species == "Raven":
        if player.raven_found_clue == False:
            print(f"{player.pet_name} notices something and flies off.")
            pause()
            print(f"\nFollow {player.pet_name}?")
            yes_no_function()
            choice = get_choice(1, 2)
            pause()
            if choice == 1:
                print(f"{player.pet_name} leads you to the school courtyard!")
                pause()
                school_courtyard()
                player.raven_found_clue = True
            else:
                print(f"You watch as {player.pet_name} gets further and further away from you...")
                pause()
                print("It'll come back after it's had it's fun.")

def ethans_date():
    print("You arrive at a cozy diner.")
    print("You take a seat by the quiet booth in the corner.")
    if ethan.contact_unlocked:
        print("📱 Ethan calls you.\n\n1. Pick up\n2. Decline")
        choice = get_choice(1, 2)
    
        if choice == 1:
            print("You answer the phone.\n\nEthan asks you to coach him and tell him what to say.")
            print("\nMia talks about how she misses Emma.")

            print("\n1. Tell Ethan to comfort her\n2. Tell her to live in the moment")

            choice = get_choice(1, 2)

            if choice == 1:
                print("You tell Ethan to comfort Mia.\nMia is touched.")

            elif choice == 2:
                print("Ethan pushes Mia's feelings aside.\nMia gets angry.")

        print("\nMia talks about how she finds Ethan funny.")

        print("\n1. Compliment her\n2. Tell a joke")
        choice = get_choice(1, 2)

        if choice == 1:
            print("\nEthan tells Mia that she's beautiful.\n\nMia thanks him.")
        elif choice == 2:
            print("\nEthan asks why the chicken crossed the road.\n\nMia gets visibly annoyed.")

    pause()
    print("Ethan hangs up.")


# =========================
# QUESTIONING
# =========================

def question_students():

    print("\n=== QUESTION STUDENTS ===")
    print("1. Mia")
    print("2. Zoe")
    print("3. Amy")
    print("4. Ethan")

    choice = get_choice(1, 4)

    if choice == 1:
        if game_state.current_time < 720:
            print("You pull Mia out of class to question her.")
        mia_questioned()
        mia.times_questioned += 1

    elif choice == 2:
        if game_state.current_time < 720:
            print("You pull Zoe out of class to question her.")
        zoe_questioned()
        zoe.times_questioned += 1

    elif choice == 3:
        if game_state.current_time < 720:
            print("You pull Amy out of class to question her.")

            if ethan.remembers("ethan_player_question_amy") and not ethan.remembers("question_amy_with_ethan"):
                print("Ethan glances at you.")
                print("\nAre we doing this together?")

                choices = ["Question Amy with Ethan", "Question Amy alone"]

                display_choices(choices)
                choice = get_choice(1, len(choices))

                if choice == 1:
                    dual_question_amy()
                    return

        amy_questioned()
        amy.times_questioned += 1

    elif choice == 4:
        if game_state.current_time < 720:
            print("You pull Ethan out of class to question him.")
        ethan_questioned()
        ethan.times_questioned += 1


def dual_question_amy():
    print("You and Ethan approach Amy together.")
    print("\nEthan:\n'WE have a few questions.'")
    print("\nAmy shows a trace of surprise.")

    ethan.remember("question_amy_with_ethan")
            

def mia_questioned():

    print("\nYou question Mia.")

    if mia.times_questioned >= 4:
        print("\nMia🤨:\n'You're questioning me.. Again?'")
    elif mia.times_questioned >= 6:
        print("\nMia💢:\n'How many more times are you gonna question me!'")

    print("Mia explains her alibi.")
    print("\nMia:\n'I was in PE. The gym teacher can verify this.'")

    print("\n1. Question her more\n2. Leave")
    choice = get_choice(1, 2)

    if choice == 1:

        print("\nMia gets nervous.")

        print("\n1. Push harder\n2. Be understanding")
        choice = get_choice(1, 2)

        if choice == 1:

            mia.lose_trust(1)
            player.lose_reputation(1)

            print("\nMia gets defensive and flustered.💢")

        elif choice == 2:

            mia.gain_trust(1)
            player.gain_reputation(1)
            print("DEBUG TRUST BONUS:", Student.trust_bonus)
            print("DEBUG REPUTATION BONUS:", Player.reputation_bonus)

            print("\nMia trusts you a little more.. 😊")

            if mia.trust >= 3:

                mia.secret_told = True

                print("Mia reveals she fought with Emma, the missing student.")
                print("\nMia:\n'Me and Emma may have... Fought.'")
                pause()
                print("Mia pauses to watch your reaction.")
                pause()
                print("Mia:\n'We last argued on the rooftop. 2 days before she disappeared.'")
                pause()
                print("Mia:\n'I thought I would make it up to her later... I would have bought her icecream like we used to.'")
                pause()
                print("Mia gets emotional and she gets up to leave.")

                add_log_entry(hint="Hint: Write about what you learned from this interaction. Mia and Emma appear to be friends.")


def zoe_questioned():

    print("\nYou question Zoe.")

    if zoe.times_questioned >= 3:
        print("\nZoe😒:\n'You're wasting my time.'")
    elif zoe.times_questioned >= 5:
        print("\nZoe😒:\n'Leave me alone.'")

    print("Zoe explains that she wasn't on school grounds when Emma went missing.")

    if photo in player.inventory:

        print("\nZoe notices the family photo.")

        print("\n1. Show her the photo\n2. Don't")

        choice = get_choice(1, 2)

        if choice == 1:

            player.remove_item(photo)

            zoe.gain_trust(10)
            player.gain_reputation(1)

            print("\nZoe stares at the photo silently.")

    if "Locker note" in player.inventory:

        print("Zoe notices you're holding something.")

        print("\n1. Show the locker note\n2. Don't")

        choice = get_choice(1, 2)

        if choice == 1:
            print("You show Zoe the locker note you found.")
            print("Zoe admits that she doesn't like Mia, nor Emma.")

    add_log_entry(hint="Write what you learned about from questioning Zoe.")


def amy_questioned():

    print("\nYou question Amy.")

    if amy.times_questioned == 4:
        print("\nAmy🤨:\n'You've questioned me 4 times.'")
    elif amy.times_questioned > 4:
        print("\nAmy🤨:\n'...'")

    print("Amy acts suspicious.")

    print("\n1. Confront her\n2. Leave")

    choice = get_choice(1, 2)

    if choice == 1:

        amy.secret_told = True

        print("\nAmy admits she spies on students..👀")

    add_log_entry(hint="Write about what you learned from questioning Amys.")


def ethan_questioned():

    print("\nYou question Ethan.")

    if ethan.times_questioned > 3:
        print("\nEthan😁:\n'Dude, this could've been 3 hours of fortnite, not 3 hours of questions.'")
    elif ethan.times_questioned > 5:
        print("\nEthan🤨:\n'-10 aura points for this.'")

    print("Ethan admits he likes Mia..")
    print("\nEthan:\n'Please help get Mia to like me too!'")
    ethan.secret_told = True

    print("\n1. Accept\n2. Don't")
    choice = get_choice(1, 2)
    if choice == 1:
        print("\nEthan proceeds to then give you his phone number.")
        ethan.contact_unlocked = True
        player.contacts.append("Ethan")

    print("Gaining Ethan's trust will allow you to get more information out of him.")
    add_log_entry(hint="Write about what you learned from questioning Ethan.")


# =========================
# ACCUSATIONS
# =========================

def accuse_someone():

    print("\n=== ACCUSE SOMEONE ===")
    print("1. Mia")
    print("2. Zoe")
    print("3. Amy")
    print("4. Ethan")

    choice = get_choice(1, 4)

    if choice == 1:
        mia_accuse()

    elif choice == 2:
        zoe_accuse()

    elif choice == 3:
        amy_accuse()

    elif choice == 4:
        ethan_accuse()

    ending_check()


def mia_accuse():

    accusation_intro("Mia", player.reputation)

    print("\n1. She fought with Emma")
    print("2. She's defensive")

    choice = get_choice(1, 2)

    if choice == 1:

        if mia.secret_told:

            mia.secret_exposed = True

            mia.lose_trust(20)

            print("\nMia feels betrayed..💔")

        else:
            print("\nYou don't have enough evidence.")
            print("Mia smirks at you triumphantly!😏")

    elif choice == 2:
        print("Mia looks offended.😒")
        print("Students aren't fully convinced..👀")
        player.lose_reputation(1)


def zoe_accuse():

    accusation_intro("Zoe", player.reputation)

    print("\n1. Show Zoe's diary")

    choice = get_choice(1, 2)

    if choice == 1:

        if zoe_diary in player.inventory:

            zoe.secret_exposed = True

            print("\nThe students are shocked!🫣")

        else:
            print("\nYou haven't found enough evidence..")


def amy_accuse():

    accusation_intro("Amy", player.reputation)

    print("\n1. Amy spies on everyone")
    print("2. Amy is creepy.")

    choice = get_choice(1, 2)

    if choice == 1:

        if amy.secret_told:

            amy.secret_exposed = True

            print("You explain that Amy often spies on everybody.")
            print("\nStudents fully believe you!😏")
            print("Amy says that it's her hobby.👀")
            player.gain_reputation(1)

        else:
            print("\nNobody believes you.💀")
            player.lose_reputation(1)
    
    elif choice == 2:
        print("Students aren't fully convinced..👀")


def ethan_accuse():

    accusation_intro("Ethan", player.reputation)

    print("\n1. Ethan could've helped Mia")
    print("2. Ethan is too chill")

    choice = get_choice(1, 2)

    if choice == 1:

        if (
            ethan.secret_told
            and
            mia.secret_told
        ):

            ethan.secret_exposed = True
            mia.secret_exposed = True

            print("You explain that Mia and Emma had argued lately, and how Ethan likes Mia.")
            print("Ethan could've teamed up with Mia to get rid of Emma to gain her favor.")
            print("Students seem convinced..👀")
            
        else:
            print("\nNobody believes you💀")
            player.lose_reputation(1)

    elif choice == 2:
        print("Students don't agree!💀")
        player.lose_reputation(1)


# ========================
# OBSERVING
# ========================

from observation_data import possible_observations

def show_observations():
    print("\nPREVIOUS OBSERVATIONS")

    found_any = False

    for time_period in possible_observations:
        for observation in possible_observations[time_period]:
            if observation.seen:
                print(f"\n{observation.title}")

                print(observation.description)
                found_any = True

    if found_any == False:
        print("You haven't made any observations yet.")

def observe():
    time_period = get_time_period()

    observations_for_this_time = possible_observations[time_period]

    available_observations = []

    for observation in observations_for_this_time:

        if observation.can_appear():
            available_observations.append(observation)


    if len(available_observations) == 0:
        print("You don't notice anything interesting right now.")
        input("\nPress Enter to leave...")
        return

    chosen_observation = random.choice(available_observations)
    chosen_observation.show(students)

    input("\nPress Enter to leave...")



# =========================
# ENDINGS
# =========================

def ending_check():
    global running

    if (
        zoe.secret_exposed
        and
        player.reputation > 2
    ):

        print("\n=== GOOD ENDING ===")
        print("Zoe gets arrested.")
        print("The school praises you!✨😏")
        running = False


# =========================
# INVENTORY
# =========================

def check_inventory():

    print("\n=== INVENTORY ===")

    if len(player.inventory) == 0:
        print("Your inventory is empty.")

    else:
        for item in player.inventory:
            print("-", item.name)

# =========================
# START GAME
# =========================

main_menu()
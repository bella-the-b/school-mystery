import random
from student import Student

def accusation_intro(student_name, reputation):

    print("\nYou gather all the students in the gym...")
    print("The lights flicker off.")
    print(f"\nYou accuse {student_name}!")

    trust_reaction(reputation)

def reputation_level(reputation):
    if reputation >= 3:
        return "trusted"
    elif reputation <= -2:
        return "wary"
    else:
        return "neutral"

def trust_reaction(reputation):
    level = reputation_level(reputation)

    if level == "trusted":
        print("Students seem happy to see you!😁")
    elif level == "wary":
        print("Students whisper suspiciously about you...🤨")

def school_gossip(student, reputation):
    trust_reaction(reputation)

    if (
        student.secret_exposed
        and reputation > 2
        and random.randint(1, 10) <= 5
    ):
        print(
            f"Two students gossip about {student.name}.\n"
            "They quiet down as you pass by."
        )
        input("\nPress Enter to leave...")

def texts_you_helper(self):
        input(f"📱 {self.name} texts you...")

def get_students_at_location(students, location, period):
    students_here = []

    for student in students.values():
        print(
            "DEBUG:",
            student.name,
            "| location:", repr(student.get_location(period)),
            "| checking:", repr(location)
        )

        if student.get_location(period) == location:
            students_here.append(student)

    return students_here

def display_students_here(students, location, period):
    students_here = get_students_at_location(
        students,
        location, 
        period
    )

    for student in students_here:
        print(f"{student.name} is here.")


def yes_no_function():
    print("\n1. Yes")
    print("2. No")

def give_reward(player, student=None, trust=0, money=0, item=None):

    print("\n===========================")
    print("\nQUEST COMPLETED")

    if student is not None and trust != 0:
        student.gain_trust(trust)
        print(f"\n+{trust} {student.name} trust")

    if money != 0:
        player.money += money
        print(f"\n+💸{money}")

    if item is not None:
        player.inventory.append(item)
        print(f"\nReceived: {item}")

    print("\n===========================")


def pause():
    input("\nPress enter to continue...")

def get_choice(min_choice, max_choice):
    while True:
        user_input = input("Choose: ")

        try:
            choice = int(user_input)
        except ValueError:
            print("Please enter a number.")
            continue

        if min_choice <= choice <= max_choice:
            return choice

        print(f"Please choose a number from {min_choice} to {max_choice}.")

def display_choices(choices):
    for number, choice in enumerate(choices, start=1):
        print(f"{number}. {choice}")
from toolbox import get_choice
from detective_helper_functions import texts_you_helper

def ethan_update_event(
    player,
    ethan,
    current_day,
    current_time,
    mia_trust
):
    ethan.receive_message(
        "Ethan",
        "Can you give me any updates on Mia??👀",
        current_day,
        current_time
    )

    print("\n1. Give him information")
    print("2. Don't")

    choice = get_choice(1, 2)

    if choice == 2:
        print("You decline Ethan's request.")
        return
    
    if mia_trust >= 3:
        ethan.receive_message(
            "You",
            "Mia really cares about Emma.",
            current_day,
            current_time
        )

        ethan.lied_to = False
        ethan.remember("player_gave_honest_update")

        player.complete_event("ethan_update_event")
        
    else:
        print("You don't actually know much about Mia.")
        print("\n1. Make something up")
        print("2. Back out")

        choice = get_choice(1, 2)

        if choice == 2:
            print("You decide not to answer.")
            return

        ethan.receive_message(
            "You",
            "She likes gossiping.",
            current_day,
            current_time
        )

        ethan.lied_to = True
        ethan.remember("player_lied_about_mia")

        player.complete_event("ethan_update_event")


def ethan_date_event(
    player,
    ethan,
    current_day,
    current_time,
    mia_trust
):
    ethan.receive_message(
        "Ethan",
        "Mia agreed to go out with me. Can you come help?",
        current_day,
        current_time
    )

    print("\n1. Help Ethan")
    print("2. Don't go")

    choice = get_choice(1, 2)
    if ethan.remembers("player_lied_about_mia"):
        if choice == 2:
            ethan.remember("date_failed_without_player")
            ethan.trust -= 2

            ethan.receive_message(
                "Ethan",
                "That went horribly. You could've warned me.",
                current_day,
                current_time
            )
            
        elif choice == 1 and mia_trust >= 3:
            ethan.remember("date_recovered")
            ethan.lied_to = False
            ethan.trust += 2

            ethan.receive_message(
                "Ethan",
                "You saved that entire date. I think we're good now.",
                current_day,
                current_time
            )

        elif choice == 1 and mia_trust < 3:
            ethan.remember("date_failed_with_bad_help")
            ethan.trust -= 3

            ethan.receive_message(
                "Ethan",
                "You somehow made it worse.",
                current_day,
                current_time
            )

    elif ethan.remembers("player_gave_honest_update"):
        ethan.remember("date_succeeded")
        ethan.trust += 1

        ethan.receive_message(
            "Ethan",
            "The date went really well! Your information actually helped.",
            current_day,
            current_time
        )

    player.complete_event("ethan_date_event")


def run_daily_events(
    player,
    ethan,
    current_day,
    current_time,
    mia_trust
):
    if (
        current_day >= 3
        and not player.completed("ethan_update_event")
    ):
        ethan_update_event(
            player,
            ethan,
            current_day,
            current_time,
            mia_trust
        )
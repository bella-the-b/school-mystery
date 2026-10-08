class Quest:
    def __init__(self, title, description, reward, penalty):
        self.title = title
        self.description = description
        self.reward = reward
        self.penalty = penalty
        self.status = "available"


    def to_dict(self):
        return {
            "title": self.title,
            "status": self.status,
            "reward": self.reward,
            "penalty": self.penalty
        }

    def load_from_dict(self, data):
        self.title = data["title"]
        self.status = data["status"]
        self.reward = data["reward"]
        self.penalty = data["penalty"]

    def accept(self):
        self.status = "accepted"

    def decline(self):
        self.status = "declined"

def display_quest_log(quests):
    print("\n══════ QUEST LOG ══════")

    visible_quests = [
        quest for quest in quests
        if quest.status != "available"
    ]

    if not visible_quests:
        print("\nYou haven't discovered any quests yet.")

    else:
        for quest in visible_quests:
            print(f"\n{quest.title}")
            print(f"Description: {quest.description}")
            print(f"Status: {quest.status.title()}")
            print(f"Reward: {quest.reward}")

    print("\n═══════════════════════")
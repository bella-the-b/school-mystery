from message import Message

class Student:
    trust_bonus = 0
    def __init__(self, name, trust, schedule):

        self.name = name
        self.trust = 0
        self.schedule = schedule or {}
        self.override_location = None

        self.contact_unlocked = False
        self.messages = []
        self.status = "offline"

        self.secret_told = False
        self.secret_exposed = False
        self.lied_to = None

        self.times_questioned = 0
        self.acting_sus = None
        self.times_observed = 0
        self.suspicion = 0
        self.memories = []


    def get_location(self, current_time):
        if self.override_location is not None:
            return self.override_location
        return self.schedule.get(current_time, "Unknown")

    def to_dict(self):
        return {
            "name": self.name,

            "trust": self.trust,

            "suspicion": self.suspicion,

            "contact_unlocked": self.contact_unlocked,

            "secret_told": self.secret_told,

            "secret_exposed": self.secret_exposed,

            "lied_to": self.lied_to,

            "times_questioned": self.times_questioned,

            "times_observed": self.times_observed,

            "acting_sus": self.acting_sus,

            "messages": [message.to_dict() for message in self.messages]


        }
    
    def load_from_dict(self, data):
        self.name = data["name"]
        self.trust = data["trust"]
        self.suspicion = data["suspicion"]
        self.contact_unlocked = data["contact_unlocked"]
        self.secret_exposed = data["secret_exposed"]
        self.secret_told = data["secret_told"]
        self.lied_to = data["lied_to"]
        self.times_questioned = data["times_questioned"]
        self.acting_sus = data["acting_sus"]
        self.times_observed = data["times_observed"]

    
    def gain_trust(self, amount):
        max_trust = 100
        min_trust = 0

        amount += self.trust_bonus

        self.trust += amount

        if self.trust > max_trust:
            self.trust = max_trust
        elif self.trust < min_trust:
            self.trust = min_trust

    def lose_trust(self, amount):
        max_trust = 100
        min_trust = 0

        self.trust -= amount

        if self.trust > max_trust:
            self.trust = max_trust
        elif self.trust < min_trust:
            self.trust = min_trust

    def receive_message(self, sender, text, day_sent, time_sent, print_message=True):
        message = Message(sender, text, day_sent, time_sent)
        self.messages.append(message)

        if print_message:
            print(f"{sender}: {text}")

    def show_chat(self):
        print(f"\n📱 Chat with {self.name}")
        print("=" * 30)

        if len(self.messages) == 0:
            print("No messages yet.")
            return
        
        for message in self.messages:
            print(f"\nDay {message.day_sent} | Time {message.time_sent}")
            print(f"{message.sender}:\n {message.text}")
        
        print("\n" + "=" * 30)

    def remember(self, memory):
        if memory not in self.memories:
            self.memories.append(memory)

    def remembers(self, memory):
        return memory in self.memories



ethan = Student(
    name="Ethan",
    trust=0,
    schedule={
        "Sunrise": "Home",
        "Morning": "Classroom",
        "Noon": "Cafeteria",
        "Afternoon": "Classroom",
        "After School": "Home"
    }
)
amy = Student(
    name="Amy",
    trust=0,
    schedule={
        "Sunrise": "Library",
        "Morning": "Classroom",
        "Noon": "Cafeteria",
        "Afternoon": "Classroom",
        "After School": "Library"
    }
)
zoe = Student(
    name="Zoe",
    trust=0,
    schedule={
        "Sunrise": "Zoe's hideout",
        "Morning": "Classroom",
        "Noon": "Courtyard",
        "Afternoon": "Classroom",
        "After School": "Zoe's Hideout"
    }
)
mia = Student(
    name="Mia",
    trust=0,
    schedule={
        "Sunrise": "Park",
        "Morning": "Classroom",
        "Noon": "Cafeteria",
        "Afternoon": "Classroom",
        "After school": "Home"
    }
)
    
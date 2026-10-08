from item import Item

class Player:
    reputation_bonus = 0
    def __init__(self, name):
        self.name = name
        self.reputation = 0
        self.contacts = []
        self.inventory = []
        self.visited_locations = []
        self.completed_events = []

        self.pet_species = None
        self.pet_name = None
        self.cat_found_clue = False
        self.raven_found_clue = False
        
        self.old_pet_name = None
        self.old_pet_species = None
        self.old_pet_available = None
        self.day_returned = None


    def to_dict(self):
        return {
            "reputation": self.reputation,

            "contacts": self.contacts,

            "inventory": [item.to_dict() for item in self.inventory],

            "visited_locations": self.visited_locations,

        }
    

    def gain_reputation(self, amount):
        max_reputation = 100
        min_reputation = 0

        amount += self.reputation_bonus

        self.reputation += amount

        if self.reputation > max_reputation:
            self.reputation = max_reputation
        elif self.reputation < min_reputation:
            self.reputation = min_reputation

    def lose_reputation(self, amount):
        max_reputation = 100
        min_reputation = 0

        self.reputation -= amount

        if self.reputation > max_reputation:
            self.reputation = max_reputation
        elif self.reputation < min_reputation:
            self.reputation = min_reputation

    def remove_old_pet(self):
        self.old_pet_name = None
        self.old_pet_species = None

    def remove_pet(self):
        self.pet_name = None
        self.pet_species = None

    def change_old_pet_to_new(self):
        self.pet_species = self.old_pet_species
        self.pet_name = self.old_pet_name

    def change_new_pet_to_old(self):
        self.old_pet_species = self.pet_species
        self.old_pet_name = self.pet_name

    def complete_event(self, event_name):
        if event_name not in self.completed_events:
            self.completed_events.append(event_name)

    def completed(self, event_name):
        return event_name in self.completed_events

    def add_item(self, item):
        if item in self.inventory:
            print(f"Could not add {item} as you already have it.")
            return False
        
        self.inventory.append(item)
        print(f"Succesfully added {item} to inventory.")
        return True

    def remove_item(self, item):
        if item not in self.inventory:
            print(f"Could not remove {item} as you do not have it.")
            return False

        self.inventory.append(item)
        print(f"Succesfully removed {item} from inventory.")
        return True
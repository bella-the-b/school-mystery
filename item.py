class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.took = False

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "took": self.took
        }
    
    def load_from_dict(self, data):
        self.name = data["name"]
        self.description = data["description"]
        self.took = data["took"]
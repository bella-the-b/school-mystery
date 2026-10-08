from student import Student

class Observation:
    def __init__(
        self,
        title,
        character,
        location,
        description,
        reveals_student=None,
        observation_id=None
    ):
        self.title = title
        self.character = character
        self.location = location
        self.description = description
        self.seen = False
        self.reveals_student = reveals_student
        self.observation_id = observation_id


    def to_dict(self):
        return {
            "title": self.title,
            "seen": self.seen
        }

    def load_from_dict(self, data):
        self.title = data["title"]
        self.seen = data.get("seen", False)

    def show(self, students):
        if self.seen == False:
            print(self.title)
            print(self.description)
            self.seen = True

            print("SHOW OBJECT:",
                  self.title,
                  self.seen,
                  id(self))

            if self.reveals_student is not None:
                students[self.reveals_student].secret_told = True

        return False

    def can_appear(self):
        if self.seen:
            return False
        
        return True
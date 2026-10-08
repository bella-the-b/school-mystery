class GameState:
    def __init__(self):
        self.current_day = 1
        self.current_time = 300
        self.times_saved = 0

    def to_dict(self):
        return {
            "current_day": self.current_day,
            "current_time": self.current_time,
            "times_saved": self.times_saved
        }

    def load_from_dict(self, data):
        self.current_day = data.get("current_day", 1)
        self.current_time = data.get("current_time", 300)
        self.times_saved = data.get("times_saved", 0)

    def advance_time(self, minutes):
        self.current_time += minutes

    def next_day(self):
        self.current_day += 1
        self.current_time = 300

    def get_current_week(self):
        return ((self.current_day - 1) // 7) + 1
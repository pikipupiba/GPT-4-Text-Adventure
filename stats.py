class Stats:
    def __init__(self, items):
        self.day = "Monday"
        self.time = 60
        self.items = items
        self.relationships = {
            "Acquaintances": {
                "count": 0,
                "info": "",
            },
            "Friends": {
                "count": 0,
                "info": "",
            },
            "Best Friend": {
                "count": 0,
                "info": "",
            },
            "Enemies": {
                "count": 0,
                "info": "",
            },
            "Arch Nemesis": {
                "count": 0,
                "info": "",
            }
        }

    def set_day(self, day):
        self.day = day
    
    def set_time(self, time):
        self.time = time
    
    def subtract_time(self, time):
        self.time -= time

    def format_day_time(self):
        return f"{self.day} --- {self.time} minutes remaining"
    
    def format_items(self):
        return "\r".join(self.items)

    def format_relationships(self):
        return "\r".join([f"{data['count']} {rank}{' --- ' + data['info'] if data['info'] else ''}" for rank, data in self.relationships.items()])

    def format_stats(self):
        return [self.format_day_time(), self.format_items(), self.format_relationships()]
    
    def to_string(self):
        formatted_stats = self.format_stats()
        return f"Day:{formatted_stats[0]}\n\nItems:\n{formatted_stats[1]}\n\nFriends:\n{formatted_stats[2]}"
    
    def update(self, arguments_json):
        self.subtract_time(int(arguments_json['Time']))
        self.items = arguments_json['Items']
        self.relationships = arguments_json['Relationships']

stats = Stats([])
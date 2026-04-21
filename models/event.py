#--------------------------
# EVENT MODEL
#--------------------------
class Event:
    def __init__(self, title, start, end, description=""):
        self.title = title
        self.start = start
        self.end = end
        self.description = description
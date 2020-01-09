class ip:
    def __init__(self):
        self.address = None
        self.country = None
        self.lat = None
        self.lon = None
        self.visit_rec = 1

        
class loggy:
    def __init__(self):
        self.default_str = None
        self.ip = None
        self.identity = None
        self.userID = None
        self.datetime = None #datetime.datetime
        self.timezone = None
        self.req = None
        self.status_code = None
        self.return_size = None
        self.referer = None
        self.user_agent = None
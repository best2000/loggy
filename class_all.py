class ip:
    def __init__(self):
        self.address = None
        self.country = None
        self.city = None
        self.lat = None
        self.lon = None
        self.isp = None

class time:
    def __init__(self):
        self.day = None
        self.month = None
        self.year = None
        self.hour = None
        self.minute = None
        self.second = None
        self.zone = None

class http_req:
    def __init__(self):
        self.method = None
        self.path = None
        self.protocol = None
        
class loggy:
    def __init__(self):
        self.default_str = None
        self.ip = ip()
        self.identity = None
        self.userID = None
        self.time = time()
        self.http_req = http_req()
        self.status_code = None
        self.return_size = None
        self.referer = None
        self.user_agent = None
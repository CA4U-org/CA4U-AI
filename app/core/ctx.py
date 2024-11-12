
CTX = None

class Container:
    def __init__(self, env, db, scheduler):
        self._environment = env
        self._db = db
        self._scheduler = scheduler

    @property
    def environment(self):
        return self._environment

    @property
    def DB(self):
        return self._db
    
    @property
    def scheduler(self):
        return self._scheduler
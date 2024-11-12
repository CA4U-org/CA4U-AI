
CTX = None

class Container:
    def __init__(self, env, db):
        self._environment = env
        self._db = db

    @property
    def environment(self):
        """읽기 전용 속성으로 설정"""
        return self._environment

    @property
    def DB(self):
        """읽기 전용 속성으로 설정"""
        return self._db
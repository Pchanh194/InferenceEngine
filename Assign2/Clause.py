class Clause:
    def __init__(self, conclusion, premise=None):
        self._conclusion = conclusion
        self._premise = premise if premise is not None else []

    @property
    def premise(self):
        return self._premise

    @property
    def conclusion(self):
        return self._conclusion

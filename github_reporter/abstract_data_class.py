from abc import ABC, abstractmethod, abstractproperty

class AbstractDataClass(ABC):

    @abstractmethod
    def __init__(self):
        self.__asdict = None

    def __getitem__(self, key):
        return self._asdict[key]

    @property
    def _asdict(self):
        if self.__asdict is None:
            self.__asdict = dict(zip(self.keys(), self._vals))
        return self.__asdict

    @abstractproperty
    def _vals(self):
        return

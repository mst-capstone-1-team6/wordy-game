import abc


class Screen(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def next_screen(self) -> 'Screen':
        pass

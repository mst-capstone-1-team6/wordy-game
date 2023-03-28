import abc


class Screen(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def update(self, game_display):
        pass

    @abc.abstractmethod
    def next_screen(self) -> 'Screen':
        pass

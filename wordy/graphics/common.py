import sys

from pygame.event import Event
from pygame.locals import *


def common_handle_event(event: Event):
    """
    This function should be called whenever pygame.event.get() is called.
    """
    if event.type == QUIT or (
        event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)
    ):
        sys.exit(0)


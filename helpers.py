from settings import *


def print_debug(DEBUG, *args, **kwargs) -> None:
    if DEBUG:
        print("[DEBUG]", *args, **kwargs)

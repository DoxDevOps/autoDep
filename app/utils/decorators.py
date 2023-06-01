from functools import wraps
from .net import host_is_reachable
import random


def check_if_host_is_reachable(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if host_is_reachable(args[0]):
            return func(*args, **kwargs)
        else:
            print("host is not reachable")
    return decorated


def print_tap_window_box(strings, heading):

    # Generate random color codes
    color_codes = [random.choice(["\033[1;32m", "\033[1;33m", "\033[1;34m", "\033[1;35m", "\033[1;36m"]) for _ in strings]


    for color_code in color_codes:
        
        if find_error(heading):
            color_code = "\033[1;31m"

        print("#########################################################################################################")
        print(f"         {heading}")
        print("#########################################################################################################")
        for line in strings:
            print(f" {color_code}{line}\033[0m ")
        break

def find_error(string):
    lowercase_string = string.lower()
    if "error" in lowercase_string:
        return True
    else:
        return False


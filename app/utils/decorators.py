from functools import wraps
from .net import host_is_reachable
import random
from utils import imp_exp_func
import os
from dotenv import load_dotenv

headers = {'Content-type': 'application/json',
    'Accept': 'text/plain', 'Authorization': os.getenv('EXPORTER_KEY')}


def check_if_host_is_reachable(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if host_is_reachable(args[0]):
            return func(*args, **kwargs)
        else:
            print("host is not reachable")

            ip_address = args[0]

            payload = {
                "ip_address": "10.40.30.3",
                "message": "failed to auto deploy"
            }
        
            try:
                imp_exp_func.send_data(
                    os.getenv('NOTIFICATION_ENDPOINT'), payload, headers)
            except Exception as e:
                print("eeror: ", e)

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


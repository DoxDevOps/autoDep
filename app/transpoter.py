from utils import imp_exp_func, host, decorators, net
from utils.app_version import apps, check_versions
import os
from dotenv import load_dotenv
import asyncio
load_dotenv()
import colorama
from colorama import Fore, Style

@decorators.check_if_host_is_reachable
def update_host(ip_address: str, user_name: str, headers: dict) -> bool:

    details = asyncio.run(host.update_remote_host(user_name, ip_address))

    decorators.print_tap_window_box(details["error_output"], net.get_host_name(ip_address) +" ERROR LOG")

    decorators.print_tap_window_box(details["output"], net.get_host_name(ip_address) +" GENERAL LOG")

    # if check_versions(details["result"]):

    #     data = {
    #         "ip_address": "10.40.30.3",
    #         "apps": apps
    #         }

        # try:
        #     imp_exp_func.send_data(
        #         os.getenv('NOTIFICATION_ENDPOINT'), data, headers)
        # except Exception as e:
        #     print("eeror: ", e)
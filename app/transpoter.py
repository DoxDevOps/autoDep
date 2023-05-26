from utils import imp_exp_func, host, decorators, net
from utils.app_version import apps, check_versions
import os
from dotenv import load_dotenv
import asyncio
load_dotenv()

@decorators.check_if_host_is_reachable
def update_host(ip_address: str, user_name: str, headers: dict) -> bool:

    details = asyncio.run(host.update_remote_host(user_name, ip_address))

    print(details)

    if check_versions(details):

        data = {
            "ip_address": "10.40.30.3",
            "apps": apps
            }

        try:
            imp_exp_func.send_data(
                os.getenv('NOTIFICATION_ENDPOINT'), data, headers)
        except Exception as e:
            print("eeror: ", e)
from curses import echo
import re
import paramiko
import os
import asyncio
from .net import AsyncParamikoSSHClient, RedisCls
from .app_version import getTag, instruction_set, generate_git_url
from dotenv import load_dotenv
load_dotenv()

_PASSWORDS_ = os.getenv('PASSWORDS')
passwords = _PASSWORDS_.split(',')

# Step 1: Remove unwanted characters (square brackets and single quotes) from the passwords
password_list = [password.strip("['").strip("']") for password in passwords]
password_list = [password.replace("'", "").strip("")
                 for password in password_list]

async def update_remote_host(user_name: str, ip_address: str) -> str:
    try:
        client = await check_if_password_works(ip_address, user_name)
        app_dirs = os.getenv('APP_DIRS').split(',')
        collection = []
        if isinstance(client,AsyncParamikoSSHClient):
            try:
                await client.clsConnect()
                apps = []


                for app_dir in app_dirs:
                    git_pull_cmd = f"cd {app_dir} && git pull --tags http://{os.getenv('GIT_HOST')}:{generate_git_url(app_dir)}"
                    print(f"Git Pull Command: {git_pull_cmd}")
                    git_pull_stdout = await client.send_command(git_pull_cmd)
                    git_pull_decoded_stdout = git_pull_stdout.decode("utf-8")
                    print(f"Git Pull Output:\n{git_pull_decoded_stdout}")

                    result = git_pull_stdout.splitlines()

                    tag = getTag(app_dir=app_dir)
                    if tag:
                        git_checkout_cmd = f"cd {app_dir} && git checkout {tag} -f"
                        print(git_checkout_cmd)
                        checkout_stdout = await client.send_command(git_checkout_cmd)
                        checkout_decoded_stdout = checkout_stdout.decode("utf-8")
                        print(f"Git Checkout Output:\n{checkout_decoded_stdout}")

                        if "BHT-EMR-API" in app_dir:
                            for instruction in instruction_set:
                                _cmd_ = f"cd {app_dir} && {instruction}"
                                stdout = await client.send_command(_cmd_)
                                decoded_stdout = stdout.decode("utf-8")
                                print(f"{instruction} Output:\n{decoded_stdout}")

                    collection.append(result)

                client.close()
                return collection
            
            except Exception as e:
                print("An error occured fn(update_remote_host): ", e)

    except Exception as e:
        print(
            f"--- Failed to initiate update task on {ip_address} with exception: {e} ---")
        return "failed_to_update_remote_host"


# retuns AsyncParamikoSSHClient instance
async def check_if_password_works(remote_host, ssh_username):
    redisInstance = RedisCls()
    await redisInstance.connect()
    redisPassword = await redisInstance.getPswrd(remote_host)

    # Use Redis password if available, otherwise iterate through password list
    passwords_to_try = [redisPassword] if redisPassword else password_list

    for password in passwords_to_try:
        try:
            client = AsyncParamikoSSHClient(host=remote_host, username=ssh_username,
                    password=str(password).strip())
            
            await client.clsConnect()
            await redisInstance.updatePswrdDict(remote_host, str(password).strip())
            return client
        except paramiko.SSHException as e:
            print("Unable to establish SSH connection:", str(e))
        except Exception as e:
            print(e)
        finally:
            client.close()
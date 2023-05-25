from curses import echo
import re
import paramiko
import os
import asyncio
from .net import AsyncParamikoSSHClient, RedisCls
from .app_version import getTag, generate_git_url
from .remote_exec_app import find_bundle_dir, find_ruby
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

                for app_dir in app_dirs:
                    git_pull_cmd = f"cd {app_dir} && git pull --tags http://{os.getenv('GIT_HOST')}:{generate_git_url(app_dir)}"
                    print(f"Git Pull Command: {git_pull_cmd}")
                    stdout = await client.send_command(git_pull_cmd)
                    decoded_stdout = stdout.decode("utf-8")  # Decode the stdout bytes into a string
                    print(f"Git Pull Output:\n{decoded_stdout}")


                for app_dir in app_dirs:
                    tag = getTag(app_dir=app_dir)
                    if tag:

                        # Perform Git operations
                        git_checkout_cmd = f"cd {app_dir} && git checkout {tag} -f"
                        print(f"Git Checkout Command: {git_checkout_cmd}")
                        stdout = await client.send_command(git_checkout_cmd)
                        decoded_stdout = stdout.decode("utf-8")  # Decode the stdout bytes into a string
                        print(f"Git Checkout Output:\n{decoded_stdout}")
                        

                        git_describe_cmd = f"cd {app_dir} && git describe > HEAD"
                        print(f"Git Describe Command: {git_describe_cmd}")
                        stdout = await client.send_command(git_describe_cmd)
                        decoded_stdout = stdout.decode("utf-8")  # Decode the stdout bytes into a string
                        print(f"Git Describe write to head Output:\n{decoded_stdout}")

                        git_describe_cmd = f"cd {app_dir} && git describe"
                        print(f"Git Describe Command: {git_describe_cmd}")
                        stdout = await client.send_command(git_describe_cmd)
                        git_describe_decoded_stdout = stdout.decode("utf-8")  # Decode the stdout bytes into a string
                        print(f"Git Describe Output:\n{git_describe_decoded_stdout}")

                        if git_describe_decoded_stdout:
                            collection.append(tag)

                        if "BHT-EMR-API" in app_dir:
                            bundle_dirs = await find_bundle_dir(client=client)
                            for bundle_path in bundle_dirs:
                                    bundle_install_cmd = f"cd {app_dir} && {bundle_path} install --local"
                                    print(f"Trying bundle path {bundle_path}...")

                                    stdout = await client.send_command(bundle_install_cmd)
                                    for line in stdout.decode('utf-8').splitlines():
                                        print(line)
                                    
                            ruby_dirs = await find_ruby(client=client)
                            for ruby_path in ruby_dirs:
                                migration_cmd = f"cd {app_dir} && {ruby_path} bin/rails db:migrate"
                                print(f"Trying ruby path {ruby_path}...")


                                stdout = await client.send_command(migration_cmd)
                                for line in stdout.decode('utf-8').splitlines():
                                    print(line)
                        

                # Reload Nginx
                reload_nginx_cmd = "systemctl reload nginx"
                reload_nginx_output = await client.send_sudo_command(reload_nginx_cmd)
                decoded_reload_nginx_output = reload_nginx_output.decode("utf-8")
                print(f"Nginx Reload Output:\n{decoded_reload_nginx_output}")

                # Nginx Status
                status_nginx_cmd = "systemctl status nginx"
                status_nginx_output = await client.send_sudo_command(status_nginx_cmd)
                decoded_status_nginx_output = status_nginx_output.decode("utf-8")
                print(f"Nginx Status Output:\n{decoded_status_nginx_output}")
                
                # Stop Puma service
                stop_puma_cmd = "systemctl stop puma"
                stop_puma_output = await client.send_sudo_command(stop_puma_cmd)
                decoded_stop_puma_output = stop_puma_output.decode("utf-8")
                print(f"Puma Stop Output:\n{decoded_stop_puma_output}")
                
                # Start Puma service
                start_puma_cmd = "systemctl start puma"
                start_puma_output = await client.send_sudo_command(start_puma_cmd)
                decoded_start_puma_output = start_puma_output.decode("utf-8")
                print(f"Puma Start Output:\n{decoded_start_puma_output}")

                # Status Puma service
                status_puma_cmd = "systemctl status puma"
                status_puma_output = await client.send_sudo_command(status_puma_cmd)
                decoded_status_puma_output = status_puma_output.decode("utf-8")
                print(f"Puma Status Output:\n{decoded_status_puma_output}")
                            

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
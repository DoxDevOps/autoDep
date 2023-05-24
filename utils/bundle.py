from .net import AsyncParamikoSSHClient
import os

async def find_bundle_dir(client: AsyncParamikoSSHClient):


    home_dir = await client.send_command("echo $HOME")
    home_dir = home_dir.decode("utf-8")

    command      = "find "+home_dir+" -name bundle"
    print(command)
    stdout     = await client.send_command(command)
    results    = stdout.decode("utf-8")
    return command
    # results    = [result.strip() for result in results]
    
    # matching_dirs = []
    # for bundle_dir in results:
    #     command = f"grep -liE 'rvm|rbenv' {bundle_dir}/*"
    #     stdout  = await client.send_command(command)
    #     rvm_rbenv_found = any(['rvm' in line.lower() or 'rbenv' in line.lower() for line in stdout.readlines()])
    #     if not rvm_rbenv_found:
    #         matching_dirs.append(bundle_dir)
    
    # return matching_dirs
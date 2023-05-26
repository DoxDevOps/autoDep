from .net import AsyncParamikoSSHClient
import asyncio

async def find_bundle_dir(client: AsyncParamikoSSHClient):
    try:
        home_dir = await client.send_command("echo $HOME")
        home_dir = home_dir.decode("utf-8").strip()

        command = f"find {home_dir} -name bundle"

        stdout = await client.send_command(command)
        results = stdout.decode("utf-8").strip().split('\n')

        matching_dirs = []
        rvm_rbenv_dirs = []
        for bundle_dir in results:
            command = f"grep -liE 'rvm|rbenv' {bundle_dir}/*"
            stdout = await client.send_command(command)
            lines = stdout.decode("utf-8").strip().split('\n')
            rvm_rbenv_found = any(['rvm' in line.lower() or 'rbenv' in line.lower() for line in lines])
            if rvm_rbenv_found:
                rvm_rbenv_dirs.append(bundle_dir)
            else:
                matching_dirs.append(bundle_dir)

        if rvm_rbenv_dirs:
            return rvm_rbenv_dirs
        else:
            return matching_dirs

    except Exception as e:
        print(f"An error occurred in fn(find_bundle_dir): {str(e)}")

async def find_ruby(client: AsyncParamikoSSHClient):
    try:
        home_dir = await client.send_command("echo $HOME")
        home_dir = home_dir.decode("utf-8").strip()

        command = f"find {home_dir} -name ruby"

        stdout = await client.send_command(command)
        results = stdout.decode("utf-8").strip().split('\n')
        return results
    
    except Exception as e:
        print(f"An error occurred in fn(find_ruby): {str(e)}")
        

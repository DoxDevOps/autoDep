import platform
import subprocess
import asyncio
import paramiko
import redis
import aioredis


def host_is_reachable(ip_address: str) -> bool:
    """checks if remote host is reachable

        Args:
            ip_address (str): ip address of remote server

        Returns:
            bool: True if remote host is reachable, False otherwise
        """

    param = '-n' if platform.system().lower() == 'windows' else '-c'

    if subprocess.call(['ping', param, '1', ip_address]) != 0:
        return False

    return True


class AsyncParamikoSSHClient(paramiko.SSHClient):
    
    def __init__(self, host, username, password):
        super().__init__()
        self.host = host
        self.username = username
        self.password = password

    async def clsConnect(self):
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(None, self._connect, self.host, self.username, self.password)
        await future

    def _connect(self, host, username, password):
        # self.connect(host, username, password)
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connect(hostname=host, username=username, password=password, port=22)

    async def send_command(self, command):
        channel = self.exec_command(command)
        stdin, stdout, stderr = channel
        decoded_stderr = stderr.read().decode("utf-8")  # Decode the stdout bytes into a string
        if decoded_stderr:
            print(f"ERRor:\n{decoded_stderr}")
        output = stdout.read()
        # self.close()
        return output
    
    async def send_sudo_command(self, command):
        sudo_command = f"echo \"{self.password}\" | sudo -S "+command
        print(sudo_command)
        channel = self.exec_command(sudo_command)
        stdin, stdout, stderr = channel
        decoded_stderr = stderr.read().decode("utf-8")  # Decode the stdout bytes into a string
        if decoded_stderr:
            print(f"ERRor:\n{decoded_stderr}")
        output = stdout.read()
        # self.close()
        return output

    async def receive_command(self, command):
        channel = await self.open_channel('session')
        await channel.exec_command(command)
        output = await channel.read_until_eof()
        channel.close()
        return output

class RedisCls():
    def __init__(self):
        self.host = 'localhost'
        self.port = 6379
        self.db = 0
        self.redis = None

    async def connect(self):
        # connect to Redis asynchronously
        self.redis = await aioredis.Redis(host=self.host, port=self.port, db=self.db)

    async def updatePswrdDict(self, key, value):
        # update or insert a key-value pair asynchronously
        await self.redis.set(key, value)

    async def getPswrd(self, ip_address):
        # get the value for the given key asynchronously, or return False if the key is not in Redis
        try:
            value = await self.redis.get(ip_address)

            if value is None:
                return False
            else:
                return value.decode('utf-8')
        except Exception as e:
            return False


import os
import platform
import aiofiles
import aiohttp
import tqdm.asyncio
import globals
import subprocess
import re

async def download_lavalink():
    async with aiohttp.ClientSession() as session:
        async with session.get(globals.LAVALINK_DOWNLOAD_URL) as r:
            total_size = int(r.headers.get('Content-Length', 0))
            with tqdm.asyncio.tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading Lavalink") as pbar:
                async with aiofiles.open("./Lavalink/Lavalink.jar", 'wb') as file:
                    chunk_size = 1024
                    while True:
                        chunk = await r.content.read(chunk_size)
                        if not chunk:
                            break
                        await file.write(chunk)
                        pbar.update(len(chunk))


def get_java_version():
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True, check=True)
        version_info = result.stderr
        match = re.search(r'java version "(\d+)\.(\d+)\.(\d+)', version_info)
        if match:
            major_version = int(match.group(1))
            minor_version = int(match.group(2))
            patch_version = int(match.group(3))
            return major_version, minor_version, patch_version
        if not match:
            match = re.search(r'openjdk version "(\d+)\.(\d+)\.(\d+)', version_info)
            major_version = int(match.group(1))
            minor_version = int(match.group(2))
            patch_version = int(match.group(3))
            return major_version, minor_version, patch_version
        return None
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        return None

def has_major_java_version(Version):
    version = get_java_version()
    if version:
        major_version, minor_version, patch_version = version
        if major_version >= Version:
            return True
        else:
            return False
    else:
        return None


def start_lavalink():
    
    if platform.system() == 'Windows':
        command = ['java', '-jar', "./Lavalink/Lavalink.jar"]
        creationflags = subprocess.CREATE_NEW_CONSOLE
    else:
        command = ['java', '-jar', "./Lavalink/Lavalink.jar"]
        creationflags = 0
    try:
        process = subprocess.Popen(command, creationflags=creationflags)
        return process.pid
    except Exception as e:
        return e
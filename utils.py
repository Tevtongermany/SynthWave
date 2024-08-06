
import aiofiles
import aiohttp
import tqdm.asyncio
import globals

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
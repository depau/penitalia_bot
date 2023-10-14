import asyncio

import aiohttp

from penitaliabot.config import Config


async def sapi_get_opus(config: Config, text: str) -> bytes:
    session = aiohttp.ClientSession()

    # Add a slight pause at the end
    if not text.endswith("."):
        text += "."

    print(f"Requesting '{text}'")

    endpoint = config.sapi_endpoint
    if endpoint.endswith("/"):
        endpoint = endpoint[:-1]

    async with session.post(
        f"{endpoint}/api/speech/speak",
        params={
            "vendor": config.voice_vendor,
            "name": config.voice_name,
        },
        headers={
            "Content-Type": "text/plain",
            "Accept": "audio/wav",
        },
        data=text.encode("utf-8"),
    ) as r:
        if r.status != 200:
            raise RuntimeError(f"Error from SAPI endpoint: {r.status} {await r.text()}")

        p = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-i",
            "pipe:",
            "-c:a",
            "libopus",
            "-f",
            "ogg",
            "pipe:",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )

        async def forward_data(a, b):
            try:
                chunk = await a.read(1024)
                while chunk != b"":
                    b.write(chunk)
                    chunk = await a.read(1024)
                    await b.drain()
            finally:
                # a.close()
                b.close()

        output = b""

        async def read_output():
            nonlocal output
            while True:
                chunk = await p.stdout.read(1024)
                if chunk == b"":
                    break
                output += chunk

        await asyncio.gather(forward_data(r.content, p.stdin), read_output())

        print(p.stdout, type(p.stdout))

        return output

from typing import AsyncGenerator
import httpx
from penitaliabot.config import Config


def _get_tts_request_params(config: Config, text: str):
    # Add a slight pause at the end if not present
    if not text.endswith((".", "!", "?")):
        text += "."

    url = config.tts_url
    if url.endswith("/"):
        url = url[:-1]

    endpoint = f"{url}/audio/speech"

    headers = {}
    if config.tts_api_key:
        headers["Authorization"] = f"Bearer {config.tts_api_key}"

    payload = {
        "model": config.tts_model,
        "input": text,
        "voice": config.tts_voice,
        "response_format": "opus",
        "speed": float(config.tts_speed),
    }

    if config.tts_instructions:
        payload["instructions"] = config.tts_instructions

    return endpoint, headers, payload


async def get_tts_opus(config: Config, text: str) -> bytes:
    """
    Generates audio from text using an OpenAI-compatible TTS server.
    """
    buffer = b""
    async for chunk in stream_tts_opus(config, text):
        buffer += chunk
    return buffer


async def stream_tts_opus(config: Config, text: str) -> AsyncGenerator[bytes, None]:
    """
    Streams audio from text using an OpenAI-compatible TTS server.
    """
    print(f"Streaming TTS for: '{text}'")
    endpoint, headers, payload = _get_tts_request_params(config, text)

    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            endpoint,
            json=payload,
            headers=headers,
            timeout=60.0,
        ) as response:
            if response.status_code != 200:
                # Read the response body for error message before raising
                error_text = await response.aread()
                raise RuntimeError(
                    f"Error from TTS server: {response.status_code} {error_text.decode()}"
                )

            async for chunk in response.aiter_bytes():
                yield chunk

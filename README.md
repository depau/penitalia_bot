# PenitaliaBot

A Telegram bot that uses an OpenAI-compatible text-to-speech API to read out loud
the messages sent to it. It is designed to work with
[loquendo-tts-server](https://github.com/depau/loquendo-tts-server), which
provides high-quality Italian voices like the iconic Roberto (Trenitalia station
voice).

The name has to do with the default voice in the official bot instance, which
*might* remind something to people who have traveled around Italy.

The bot is currently running on Telegram as
[@PenitaliaBot](https://t.me/PenitaliaBot).

## Installation

This project uses `uv` for dependency management.

```bash
uv sync
```

## Running

You can run the bot using `uv run`:

```bash
uv run penitaliabot
```

## Configuration

The bot is configured via environment variables:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `PENITALIA_TOKEN` | Telegram Bot Token | **Required** |
| `PENITALIA_TTS_URL` | Base URL of the OpenAI-compatible TTS server | `http://localhost:8080/v1` |
| `PENITALIA_TTS_MODEL` | TTS model/voice ID (e.g. `tts-loquendo-roberto`) | `tts-loquendo-roberto` |
| `PENITALIA_TTS_VOICE` | Voice name | `roberto` |
| `PENITALIA_TTS_INSTRUCTIONS` | Optional Loquendo parameters (Key=Value pairs) | |
| `PENITALIA_TTS_SPEED` | Speech speed (0.25 to 4.0) | `1.0` |
| `PENITALIA_TTS_API_KEY` | Optional API key for the TTS server | |
| `PENITALIA_ALLOWED_IDS` | Comma-separated list of allowed Telegram user IDs | |
| `REDIS_URL` | Redis URL for caching inline query results | |
| `PENITALIA_HTTP_URL` | Base URL for serving audio files (inline queries) | |
| `PENITALIA_HTTP_TOKEN` | Secret token for securing audio file access | |

## License

Copyright (C) 2023-2026 Davide Depau

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

See `LICENSE` for the full license text.
import os
from typing import Optional

import redis
from quart import Quart, request

from penitaliabot import sapi
from penitaliabot.config import Config

app = Quart(__name__)

config = Config()
r = redis.StrictRedis.from_url(config.redis_url)


@app.route(f"{config.root_path}/<sha>.ogg", methods=["GET"])
async def penitalia_ogg(sha):
    # Check token in GET parameters
    if "token" not in request.args or request.args["token"] != config.http_token:
        return "Invalid token", 403

    text: Optional[bytes] = r.get(sha)
    if not text:
        return "Not found", 404

    text_u = text.decode("utf-8")

    opus = await sapi.sapi_get_opus(config, text_u)
    return opus, 200, {"Content-Type": "audio/ogg"}


if __name__ == "__main__":
    app.run()

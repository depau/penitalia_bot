import asyncio
import hashlib
import traceback
from typing import Optional, cast

import redis
import telegram
from telegram import Bot, Update, InputFile
from telegram.ext import Updater

from penitaliabot import sapi
from penitaliabot.config import Config


class PenitaliaBot:
    bot: Optional[Bot]

    def __init__(self, config: Config, loop: asyncio.AbstractEventLoop):
        self.config = config
        self.bot = None
        self.token = config.telegram_token
        redis_url = config.redis_url
        if redis_url:
            self.redis = redis.from_url(redis_url)
        else:
            self.redis = None
        self.sapi_endpoint = config.sapi_endpoint
        self.voice_vendor = config.voice_vendor
        self.voice_name = config.voice_name
        self.http_token = config.http_token
        self.root_path = config.root_path
        self.http_url = config.http_url
        self.allowed_ids = list(
            map(
                lambda x: int(x),
                filter(lambda x: x != "", config.allowed_ids.split(",")),
            )
        )
        self._offset = 0
        self.loop = loop
        self.me = None

    def user_allowed(self, user: telegram.User):
        if len(self.allowed_ids) == 0:
            return True
        if user.id in self.allowed_ids:
            return True
        print("Not allowed: {}".format(user))
        return False

    async def parse_message(self, msg: telegram.Message):
        print(f"Message from {msg.from_user}: {msg.text}")

        if not self.user_allowed(msg.from_user):
            return

        text = msg.text
        tagme = "@{}".format(self.me.username).lower()

        # If it's a group message, only reply to messages where the bot is tagged
        if msg.chat.type == "group" and not text.lower().startswith(tagme):
            return

        if msg.reply_to_message and msg.reply_to_message.text:
            text = msg.reply_to_message.text.strip()
        elif text and text.lower().startswith(tagme):
            text = text[len(tagme) :].strip()

        if not text:
            return

        asyncio.ensure_future(self.bot.send_chat_action(msg.chat.id, "upload_audio"))

        opus = await sapi.sapi_get_opus(self.config, text)
        await self.bot.send_voice(
            msg.chat.id, InputFile(opus, "vm.ogg"), reply_to_message_id=msg.message_id
        )

    async def parse_inline_query(self, iq: telegram.InlineQuery):
        text = iq.query
        allowed = self.user_allowed(iq.from_user)
        if not allowed or not text:
            reply = (
                "Send some text to get a voice message"
                if allowed
                else "Not authorized to use this bot"
            )
            await self.bot.answer_inline_query(
                iq.id,
                [
                    telegram.InlineQueryResultVideo(
                        id="never_gonna_give_you_up",
                        video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                        thumbnail_url="https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
                        mime_type="text/html",
                        title=reply,
                        input_message_content=telegram.InputTextMessageContent(
                            f"[{reply}](https://www.youtube.com/watch?v=dQw4w9WgXcQ)",
                            parse_mode="Markdown",
                        ),
                    )
                ],
            )
            return

        if not text:
            return

        text_id = hashlib.sha1(text.encode("utf-8")).hexdigest()

        if self.redis:
            self.redis.set(text_id, text, ex=60 * 60 * 24)

        url = f"{self.http_url}{self.root_path}/{text_id}.ogg?token={self.http_token}"
        print(f"Inline query: {text} -> {url}")

        await self.bot.answer_inline_query(
            iq.id,
            [
                telegram.InlineQueryResultVoice(
                    id=text_id,
                    voice_url=url,
                    title="Speak with Trenitalia's voice",
                )
            ],
        )

    async def parse_update(self, upd: telegram.Update):
        print(upd)

        if upd.message:
            asyncio.ensure_future(self.parse_message(upd.message))

        if upd.inline_query and self.redis:
            asyncio.ensure_future(self.parse_inline_query(upd.inline_query))

    async def run(self):
        self.bot = telegram.Bot(token=self.token)
        async with self.bot:
            self.me = await self.bot.get_me()

            print(f"Bot is running as {self.me.username}")

            updater = Updater(bot=self.bot, update_queue=asyncio.Queue())
            async with updater:
                queue = await updater.start_polling(
                    allowed_updates=[Update.MESSAGE, Update.INLINE_QUERY]
                )

                while True:
                    # noinspection PyBroadException
                    try:
                        upd = cast(Update, await queue.get())
                        await self.parse_update(upd)
                    except Exception:
                        traceback.print_exc()


def main():
    config = Config()

    loop = asyncio.get_event_loop()

    bot = PenitaliaBot(config, loop)
    loop.run_until_complete(bot.run())
    loop.close()


if __name__ == "__main__":
    main()

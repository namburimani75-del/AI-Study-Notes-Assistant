import asyncio
from typing import Optional, Tuple
import streamlit as st
from telegram import Bot
from telegram.error import TelegramError

TELEGRAM_MAX_MESSAGE_LENGTH = 4000


def get_telegram_bot_token() -> Optional[str]:
    """Retrieve Telegram Bot Token safely from Streamlit secrets."""
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN", "")
        if not token or "your_telegram_bot_token" in token.lower():
            return None
        return token.strip()
    except Exception:
        return None


async def send_telegram(chat_id: str, text: str) -> bool:
    """
    Send a message to a Telegram chat via the Telegram Bot API.
    Follows the specification structure: async def send_telegram(chat_id, text).
    """
    token = get_telegram_bot_token()
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not configured in .streamlit/secrets.toml.")

    if not chat_id or not str(chat_id).strip():
        raise ValueError("Invalid Telegram Chat ID.")

    bot = Bot(token=token)

    # Split message if it exceeds Telegram's maximum message length
    chunks = [
        text[i : i + TELEGRAM_MAX_MESSAGE_LENGTH]
        for i in range(0, len(text), TELEGRAM_MAX_MESSAGE_LENGTH)
    ]

    for chunk in chunks:
        await bot.send_message(chat_id=str(chat_id).strip(), text=chunk)

    return True


def send_telegram_sync(chat_id: str, text: str) -> Tuple[bool, Optional[str]]:
    """
    Synchronous wrapper for Streamlit button actions to execute send_telegram safely.
    Returns (success: bool, error_message: Optional[str]).
    """
    try:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            # If the current thread already has a running loop
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                result = pool.submit(lambda: asyncio.run(send_telegram(chat_id, text))).result()
                return (True, None)
        else:
            loop.run_until_complete(send_telegram(chat_id, text))
            return (True, None)
    except TelegramError as te:
        return (False, f"Telegram API error: {str(te)}")
    except Exception as e:
        return (False, str(e))

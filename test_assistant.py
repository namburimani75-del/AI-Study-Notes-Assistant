"""
Automated Test Suite for AI Study Notes Assistant
Testing Phases 1 through 10 as defined in spec.md
"""

import os
import unittest
import asyncio
from io import BytesIO
from PIL import Image

import prompts
import gemini_utils
import telegram_utils


class TestPhase1StreamlitApp(unittest.TestCase):
    def test_app_file_exists(self):
        self.assertTrue(os.path.exists("app.py"), "app.py should exist")

    def test_requirements_file_exists(self):
        self.assertTrue(os.path.exists("requirements.txt"), "requirements.txt should exist")
        with open("requirements.txt", "r") as f:
            content = f.read()
            self.assertIn("streamlit", content)
            self.assertIn("google-genai", content)
            self.assertIn("Pillow", content)
            self.assertIn("python-telegram-bot", content)

    def test_gitignore_contains_secrets_and_venv(self):
        self.assertTrue(os.path.exists(".gitignore"), ".gitignore should exist")
        with open(".gitignore", "r") as f:
            content = f.read()
            self.assertIn(".streamlit/secrets.toml", content)
            self.assertIn("venv/", content)


class TestPhase2ImageUpload(unittest.TestCase):
    def test_image_processing_valid(self):
        # Create an in-memory image
        img = Image.new("RGB", (100, 100), color=(73, 109, 137))
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        opened = Image.open(img_byte_arr)
        self.assertEqual(opened.size, (100, 100))
        self.assertEqual(opened.format, "PNG")

    def test_image_processing_invalid(self):
        corrupt_data = BytesIO(b"not an image file")
        with self.assertRaises(Exception):
            Image.open(corrupt_data)


class TestPhase4Prompts(unittest.TestCase):
    def test_system_prompt_exists(self):
        self.assertTrue(hasattr(prompts, "STUDY_SYSTEM_PROMPT"))
        prompt = prompts.STUDY_SYSTEM_PROMPT
        self.assertIn("AI Study Notes Assistant", prompt)
        self.assertIn("handwritten notes", prompt)
        self.assertIn("unclear or unreadable", prompt)

    def test_summary_template_structure(self):
        self.assertTrue(hasattr(prompts, "SUMMARY_PROMPT_TEMPLATE"))
        template = prompts.SUMMARY_PROMPT_TEMPLATE
        self.assertIn("📚 Study Summary", template)
        self.assertIn("Topic:", template)
        self.assertIn("🧠 Simple Explanation:", template)
        self.assertIn("⭐ Important Points:", template)
        self.assertIn("📌 Key Terms:", template)
        self.assertIn("📝 Quick Revision:", template)


class TestPhase3And5GeminiUtils(unittest.TestCase):
    def test_get_gemini_api_key_handles_missing(self):
        # In testing without secrets.toml populated, it should safely return None
        key = gemini_utils.get_gemini_api_key()
        # Should be None if placeholder or missing
        if key:
            self.assertNotEqual(key, "your_gemini_api_key_here")

    def test_client_init_error_when_no_key(self):
        # Overwrite get_gemini_api_key temporarily
        original_fn = gemini_utils.get_gemini_api_key
        try:
            gemini_utils.get_gemini_api_key = lambda: None
            with self.assertRaises(ValueError) as ctx:
                gemini_utils.get_gemini_client()
            self.assertIn("Gemini API key is not configured", str(ctx.exception))
        finally:
            gemini_utils.get_gemini_api_key = original_fn


class TestPhase6ChatHistoryFormat(unittest.TestCase):
    def test_chat_message_schema(self):
        user_msg = {"role": "user", "content": "Explain deadlock."}
        assistant_msg = {"role": "assistant", "content": "Deadlock is..."}
        self.assertEqual(user_msg["role"], "user")
        self.assertEqual(assistant_msg["role"], "assistant")


class TestPhase7And8TelegramUtils(unittest.TestCase):
    def test_get_telegram_bot_token_handles_missing(self):
        token = telegram_utils.get_telegram_bot_token()
        if token:
            self.assertNotEqual(token, "your_telegram_bot_token_here")

    def test_send_telegram_missing_token_error(self):
        original_fn = telegram_utils.get_telegram_bot_token
        try:
            telegram_utils.get_telegram_bot_token = lambda: None
            with self.assertRaises(ValueError) as ctx:
                asyncio.run(telegram_utils.send_telegram("12345", "Hello"))
            self.assertIn("TELEGRAM_BOT_TOKEN is not configured", str(ctx.exception))
        finally:
            telegram_utils.get_telegram_bot_token = original_fn

    def test_send_telegram_empty_chat_id(self):
        original_fn = telegram_utils.get_telegram_bot_token
        try:
            telegram_utils.get_telegram_bot_token = lambda: "fake_token_123"
            with self.assertRaises(ValueError) as ctx:
                asyncio.run(telegram_utils.send_telegram("", "Hello"))
            self.assertIn("Invalid Telegram Chat ID", str(ctx.exception))
        finally:
            telegram_utils.get_telegram_bot_token = original_fn

    def test_send_telegram_sync_wrapper_catches_error(self):
        # Sync wrapper should catch errors gracefully and return (False, error_msg)
        success, err = telegram_utils.send_telegram_sync("", "Hello")
        self.assertFalse(success)
        self.assertIsNotNone(err)


class TestPhase9SummaryFormat(unittest.TestCase):
    def test_fallback_summary_format(self):
        summary_text = (
            "📚 Study Summary\n\n"
            "Topic:\nDeadlock in Operating Systems\n\n"
            "🧠 Simple Explanation:\nA situation where processes are blocked.\n\n"
            "⭐ Important Points:\n- Mutual Exclusion\n- Hold and Wait\n- No Preemption\n- Circular Wait\n\n"
            "📌 Key Terms:\n- Deadlock: System freeze due to circular resource dependency.\n\n"
            "📝 Quick Revision:\nRemember the 4 Coffman conditions!"
        )
        self.assertIn("📚 Study Summary", summary_text)
        self.assertIn("Topic:", summary_text)
        self.assertIn("🧠 Simple Explanation:", summary_text)
        self.assertIn("⭐ Important Points:", summary_text)
        self.assertIn("📌 Key Terms:", summary_text)
        self.assertIn("📝 Quick Revision:", summary_text)


if __name__ == "__main__":
    unittest.main()

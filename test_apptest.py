"""
End-to-End Streamlit App Testing using AppTest
Verifies that all components, inputs, headers, and UI widgets are rendered as specified.
"""

import unittest
from streamlit.testing.v1 import AppTest
from PIL import Image
from io import BytesIO


class TestAppTestE2E(unittest.TestCase):
    def test_app_initial_render(self):
        at = AppTest.from_file("app.py").run()
        self.assertFalse(at.exception)

        # Verify title & header
        rendered_markdown = " ".join([m.value for m in at.markdown])
        self.assertIn("🎓 AI Study Notes Assistant", rendered_markdown)
        self.assertIn("Turn your study material into an interactive AI tutor", rendered_markdown)

        # Verify Onboarding inputs
        self.assertEqual(len(at.text_input), 2)
        self.assertEqual(at.text_input[0].label, "Student Name")
        self.assertEqual(at.text_input[1].label, "Telegram Chat ID")

        # Verify file uploader
        self.assertEqual(len(at.file_uploader), 1)
        self.assertEqual(at.file_uploader[0].label, "Upload Your Study Material")

        # Verify initial state message
        info_messages = [info.value for info in at.info]
        self.assertTrue(any("Please upload a study image first." in msg for msg in info_messages))

    def test_app_student_onboarding_interaction(self):
        at = AppTest.from_file("app.py").run()
        at.text_input[0].input("N Manikanta").run()
        at.text_input[1].input("987654321").run()
        self.assertFalse(at.exception)

        # Check session state update
        self.assertEqual(at.session_state["student_name"], "N Manikanta")
        self.assertEqual(at.session_state["telegram_chat_id"], "987654321")

        # Verify welcome message
        success_messages = [s.value for s in at.success]
        self.assertTrue(any("Welcome, N Manikanta!" in msg for msg in success_messages))

    def test_app_with_uploaded_image_state(self):
        at = AppTest.from_file("app.py").run()
        # Simulate having an image in session state
        test_img = Image.new("RGB", (50, 50), color=(100, 150, 200))
        at.session_state["uploaded_image"] = test_img
        at.session_state["student_name"] = "N Manikanta"
        at.session_state["telegram_chat_id"] = "12345"
        at.run()
        self.assertFalse(at.exception)

        # The analyze button should now be available
        button_labels = [b.label for b in at.button]
        self.assertTrue(any("Analyze Study Material" in label for label in button_labels))
        self.assertTrue(any("Send Summary to Telegram" in label for label in button_labels))

    def test_telegram_send_without_chat_id(self):
        at = AppTest.from_file("app.py").run()
        test_img = Image.new("RGB", (50, 50), color=(100, 150, 200))
        at.session_state["uploaded_image"] = test_img
        at.session_state["telegram_chat_id"] = ""
        at.run()

        # Click the "Send Summary to Telegram" button
        tg_button = None
        for b in at.button:
            if "Send Summary to Telegram" in b.label:
                tg_button = b
                break
        self.assertIsNotNone(tg_button)
        tg_button.click().run()

        # Should display error asking for Telegram Chat ID
        error_messages = [e.value for e in at.error]
        self.assertTrue(
            any("Please check your Telegram Chat ID" in msg for msg in error_messages),
            f"Expected error message not found in {error_messages}",
        )


if __name__ == "__main__":
    unittest.main()

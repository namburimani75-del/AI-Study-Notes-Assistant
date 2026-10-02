# AI Study Notes Assistant

## 1. Project Overview

Build a web-based AI Study Notes Assistant that allows students to upload images of study materials such as:

* Handwritten notes
* Textbook pages
* Questions
* Diagrams
* Assignment problems
* Lecture notes

The application uses **Google Gemini Vision** to understand the uploaded study material and provides a conversational AI experience where students can ask questions about the uploaded content.

The application must also provide a **Send to Telegram** action that sends the generated study summary or explanation to the student's Telegram chat.

The project should be built with:

* Python
* Streamlit
* Google Gemini API
* Gemini Vision
* Telegram Bot API
* `python-telegram-bot`

---

# 2. Main Goal

The goal is to create an AI-powered study assistant that can:

1. Accept study material as an image.
2. Analyze the image using Gemini Vision.
3. Explain the material in simple language.
4. Extract important concepts and key points.
5. Allow the student to chat with the AI about the uploaded material.
6. Generate a useful study summary.
7. Send the summary to Telegram.

The application should be simple enough for students to use without technical knowledge.

---

# 3. Workshop Architecture

Follow this architecture:

```text
Student
   |
   v
Upload Study Material
   |
   v
Gemini Vision
   |
   v
Study Material Analysis
   |
   v
AI Study Chat
   |
   v
Generate Summary
   |
   v
Send to Telegram
```

The application should preserve the workshop pattern:

```text
Onboarding
    ↓
Image / Text Input
    ↓
Gemini Vision + Chat
    ↓
Generate Summary
    ↓
Telegram Action
```

Do not replace the core architecture with an unrelated workflow.

---

# 4. Core Features

## 4.1 Onboarding

When the application starts, provide a simple onboarding section.

Collect:

* Student name
* Telegram Chat ID

The Telegram Chat ID should be stored in Streamlit session state after onboarding.

Do not ask the user for their Telegram Bot Token.

The bot token must remain in Streamlit Secrets.

---

# 5. Study Material Upload

Provide a Streamlit file uploader.

Supported formats:

* PNG
* JPG
* JPEG
* WEBP

Example UI:

```text
Upload Your Study Material

[ Browse files ]

Supported formats:
PNG, JPG, JPEG, WEBP
```

After upload:

* Display the image.
* Send the image to Gemini Vision.
* Analyze its contents.

---

# 6. Gemini Vision Analysis

Gemini must analyze the uploaded image.

The analysis should identify:

### Topic

Example:

```text
Topic:
Deadlock in Operating Systems
```

### Simple Explanation

Explain the material in student-friendly language.

### Important Concepts

Extract the major concepts.

Example:

```text
Important Concepts:

1. Mutual Exclusion
2. Hold and Wait
3. No Preemption
4. Circular Wait
```

### Key Points

Generate concise revision points.

### Step-by-Step Explanation

When the image contains a process, algorithm, mathematical problem, diagram, or procedure, explain it step by step.

---

# 7. AI Study Chat

After the image has been analyzed, provide a chat interface.

The student should be able to ask questions about the uploaded material.

Example questions:

```text
Explain this in simple terms.

Give me an example.

What are the important points?

Give me 5 exam questions.

Explain the diagram.

Summarize this topic.

What should I remember for an exam?
```

The assistant must answer using the uploaded study material as the primary context.

Do not invent information that is not supported by the uploaded material.

If information is unclear or unreadable, explicitly tell the user.

---

# 8. System Prompt

Create a separate file:

```text
prompts.py
```

Store the main Gemini system prompt in this file.

Use the following behavior:

```python
STUDY_SYSTEM_PROMPT = """
You are AI Study Notes Assistant, an AI tutor designed to help
students understand their study material.

Your primary task is to analyze uploaded study material such as
handwritten notes, textbook pages, diagrams, questions,
assignments, and lecture notes.

When analyzing an image:

1. Identify the main topic if possible.
2. Explain the content in simple student-friendly language.
3. Extract important concepts.
4. Extract important definitions, formulas, or facts when visible.
5. Provide step-by-step explanations when appropriate.
6. Create concise revision points.
7. Mention unclear or unreadable portions.
8. Do not invent information that cannot be supported by the
   uploaded material.

When the student asks follow-up questions, use the uploaded
study material and previous conversation as context.

Keep explanations clear, structured, and educational.

Prefer headings, bullet points, numbered steps, and examples
when they improve understanding.

If the uploaded image does not contain enough information to
answer a question, clearly say so instead of making up an answer.
"""
```

Keep this prompt in `prompts.py` rather than placing it directly inside `app.py`.

---

# 9. Gemini Integration

Create:

```text
gemini_utils.py
```

This file should contain Gemini-related functionality.

Responsibilities:

* Initialize Gemini client.
* Send image + system prompt to Gemini.
* Generate study analysis.
* Generate chat responses.
* Handle Gemini API errors.

Do not place the Gemini API key directly in source code.

Use:

```python
st.secrets["GEMINI_API_KEY"]
```

---

# 10. Telegram Integration

Create:

```text
telegram_utils.py
```

This file should contain Telegram functionality.

Use the `python-telegram-bot` package.

The main function should follow this structure:

```python
async def send_telegram(chat_id, text):
    ...
```

The application should provide a button:

```text
📲 Send Summary to Telegram
```

When clicked:

1. Generate or retrieve the current study summary.
2. Retrieve the student's Telegram Chat ID.
3. Send the summary through the Telegram bot.
4. Display a success message.

Example:

```text
✅ Study summary sent to Telegram!
```

If sending fails:

```text
❌ Unable to send the summary.
Please check your Telegram Chat ID and try again.
```

---

# 11. Telegram Bot Configuration

The Telegram bot token must be stored in Streamlit Secrets.

Use:

```toml
TELEGRAM_BOT_TOKEN = "your_bot_token"
```

The user should create the bot through Telegram's `@BotFather`.

The student must start the bot and send it at least one message before the bot can send messages to that chat.

The application should not expose the bot token anywhere in the UI.

---

# 12. Streamlit Secrets

Create:

```text
.streamlit/
    secrets.toml
```

Expected configuration:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
```

Do not hard-code secrets in Python files.

Do not commit `secrets.toml` to GitHub.

Add:

```text
.streamlit/secrets.toml
```

to `.gitignore`.

---

# 13. User Interface

Create a clean, modern student-friendly Streamlit interface.

Page title:

```text
🎓 AI Study Notes Assistant
```

Subtitle:

```text
Turn your study material into an interactive AI tutor.
```

Recommended layout:

```text
==================================================
          🎓 AI Study Notes Assistant
      Turn your notes into an AI tutor
==================================================

👤 Student Information
Name: [____________]
Telegram Chat ID: [____________]

--------------------------------------------------

📚 Upload Study Material

[ Browse files ]

--------------------------------------------------

                 Uploaded Image

--------------------------------------------------

🤖 AI Study Analysis

Topic:
...

Simple Explanation:
...

Important Concepts:
...

Key Points:
...

--------------------------------------------------

💬 Ask Your Study Assistant

[ Ask a question......................... ]

[ Send ]

--------------------------------------------------

📲 Telegram

[ Send Summary to Telegram ]

==================================================
```

---

# 14. Session State

Use Streamlit session state to maintain:

```text
student_name
telegram_chat_id
uploaded_image
analysis
chat_history
current_summary
```

Chat history should survive Streamlit reruns during the current session.

---

# 15. Chat History

Store messages in this format:

```python
{
    "role": "user",
    "content": "Explain this in simple terms."
}
```

and:

```python
{
    "role": "assistant",
    "content": "Deadlock occurs when..."
}
```

Display chat messages using Streamlit's chat interface.

Use:

```python
st.chat_message()
```

and:

```python
st.chat_input()
```

---

# 16. Summary Generation

Provide a function that creates a concise study summary.

The summary should contain:

```text
📚 Study Summary

Topic:
...

🧠 Simple Explanation:
...

⭐ Important Points:
- ...
- ...
- ...

📌 Key Terms:
- ...
- ...

📝 Quick Revision:
...
```

This summary is the content sent to Telegram.

---

# 17. Error Handling

The application must gracefully handle:

### No image

Display:

```text
Please upload a study image first.
```

### Invalid image

Display:

```text
The uploaded file could not be processed.
Please upload a valid image.
```

### Gemini API failure

Display:

```text
Unable to analyze the image right now.
Please check your Gemini API configuration and try again.
```

### Telegram failure

Display:

```text
Unable to send the Telegram message.
Please verify that the bot is running and the Chat ID is correct.
```

### Missing secrets

Display a helpful configuration message without revealing secret values.

---

# 18. Security Requirements

Never expose:

* Gemini API key
* Telegram Bot Token

Do not place credentials in:

* `app.py`
* `prompts.py`
* `gemini_utils.py`
* `telegram_utils.py`
* README files
* GitHub commits

Use Streamlit Secrets.

Add a `.gitignore` file containing:

```text
venv/
__pycache__/
.streamlit/secrets.toml
.env
*.pyc
```

---

# 19. Project Structure

The final project should have:

```text
AI-Study-Notes-Assistant/
│
├── app.py
├── prompts.py
├── gemini_utils.py
├── telegram_utils.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    └── secrets.toml
```

---

# 20. Requirements

Create `requirements.txt`:

```text
streamlit
google-genai
Pillow
python-telegram-bot
```

Use current compatible versions unless a specific version is required by the environment.

---

# 21. README

Create a professional README containing:

## Project title

AI Study Notes Assistant

## Description

A Gemini-powered multimodal study assistant that analyzes images of study materials, explains concepts, supports conversational learning, and sends study summaries to Telegram.

## Features

* Gemini Vision image analysis
* AI study explanations
* Interactive study chat
* Key point extraction
* Study summary generation
* Telegram integration
* Streamlit interface
* Secure API key management

## Tech Stack

* Python
* Streamlit
* Google Gemini
* Gemini Vision
* Telegram Bot API
* python-telegram-bot

## Setup

Explain:

1. Clone/download the project.
2. Create a virtual environment.
3. Install requirements.
4. Configure Streamlit Secrets.
5. Start the Streamlit application.

Do not include real API keys or tokens in the README.

---

# 22. Development Order

Build the project in this order.

### Phase 1

Create the Streamlit application.

Verify:

```text
🎓 AI Study Notes Assistant
```

appears correctly.

### Phase 2

Add image upload.

Verify that uploaded images display correctly.

### Phase 3

Connect Gemini Vision.

Verify that the uploaded study image is analyzed.

### Phase 4

Move the system prompt to:

```text
prompts.py
```

### Phase 5

Add structured study analysis:

* Topic
* Explanation
* Important concepts
* Key points
* Revision notes

### Phase 6

Add conversational chat.

### Phase 7

Create the Telegram bot.

### Phase 8

Connect Telegram to the application.

### Phase 9

Add:

```text
📲 Send Summary to Telegram
```

### Phase 10

Test the complete workflow.

---

# 23. Final User Workflow

The finished application should work like this:

```text
1. Student opens the application.

2. Student enters their name and Telegram Chat ID.

3. Student uploads a photo of study material.

4. Gemini Vision analyzes the image.

5. Application displays:
   - Topic
   - Simple explanation
   - Important concepts
   - Key points
   - Revision notes

6. Student asks follow-up questions.

7. Gemini answers using the study material as context.

8. Student clicks:
   "📲 Send Summary to Telegram"

9. Application sends the study summary to Telegram.

10. Application displays:
    "✅ Study summary sent to Telegram!"
```

---

# 24. Important Implementation Rules

* Keep the code modular.
* Do not put everything in `app.py`.
* Keep prompts in `prompts.py`.
* Keep Gemini functionality in `gemini_utils.py`.
* Keep Telegram functionality in `telegram_utils.py`.
* Use Streamlit session state for temporary application state.
* Never expose API keys.
* Never commit secrets.
* Provide clear error messages.
* Do not invent information when the uploaded image is unclear.
* Keep the application focused on study assistance.
* Make the interface simple and suitable for students.

---

# 25. Success Criteria

The project is complete when all of the following work:

* [ ] Streamlit application starts successfully.
* [ ] User can upload a study image.
* [ ] Image is displayed.
* [ ] Gemini Vision analyzes the image.
* [ ] Topic is identified when possible.
* [ ] Simple explanation is generated.
* [ ] Important concepts are extracted.
* [ ] Key points are generated.
* [ ] Student can ask follow-up questions.
* [ ] Chat history is maintained during the session.
* [ ] Study summary can be generated.
* [ ] Telegram bot can send the summary.
* [ ] API credentials are stored securely.
* [ ] No secrets are committed to GitHub.
* [ ] Application handles errors gracefully.

# Final Project

**AI Study Notes Assistant**

Tagline:

> **Turn your study material into an interactive AI tutor.**

Core technologies:

**Streamlit + Gemini Vision + AI Chat + Telegram**

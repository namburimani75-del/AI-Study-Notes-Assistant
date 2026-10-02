# 🎓 AI Study Notes Assistant

> **Turn your study material into an interactive AI tutor.**

A Gemini-powered multimodal study assistant that analyzes images of study materials, explains concepts, supports conversational learning, and sends study summaries to Telegram.

---

## 🚀 Features

* **Gemini Vision Image Analysis**: Upload handwritten notes, textbook pages, diagrams, assignment questions, or lecture slides.
* **AI Study Explanations**: Generates student-friendly conceptual explanations, definitions, formulas, and step-by-step procedures.
* **Interactive Study Chat**: Ask follow-up questions, request exam preparation tips, analogies, or practical examples directly related to the uploaded study material.
* **Key Point & Concept Extraction**: Automatically identifies core topics, revision takeaways, and highlights illegible portions if any.
* **Study Summary Generation**: Prepares concise, structured study summaries ready for quick revision.
* **Telegram Integration**: Send generated study summaries directly to the student's personal Telegram chat with one click.
* **Modern Streamlit Interface**: Clean, accessible, and responsive user experience designed for students.
* **Secure API Key Management**: Uses Streamlit Secrets (`secrets.toml`) to prevent API keys and bot tokens from being exposed or committed.

---

## 🛠 Tech Stack

* **Python**: Core programming language.
* **Streamlit**: Web application framework and interactive user interface.
* **Google Gemini & Gemini Vision** (`google-genai`): Multimodal reasoning, conceptual explanations, and conversational tutoring.
* **Telegram Bot API & `python-telegram-bot`**: Asynchronous messaging and delivery of study summaries to Telegram.
* **Pillow (PIL)**: Image loading, verification, and preprocessing.

---

## 📁 Project Structure

```text
AI-Study-Notes-Assistant/
│
├── app.py                  # Main Streamlit web application & user workflow
├── prompts.py              # System prompts & structured response templates
├── gemini_utils.py         # Google Gemini Vision & chat interaction logic
├── telegram_utils.py       # Telegram Bot messaging functions
├── test_assistant.py       # Unit test suite covering all phases
├── test_apptest.py         # Streamlit AppTest end-to-end testing suite
├── requirements.txt        # Project dependencies
├── README.md               # Documentation & setup guide
├── .gitignore              # Ignored files (secrets, venv, pycache)
│
└── .streamlit/
    └── secrets.toml        # Secret API keys and bot tokens (never commit!)
```

---

## ⚙️ Setup and Installation

### 1. Clone or Download the Project
```bash
git clone <repository-url>
cd "AI Study Notes Assistant"
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows (Command Prompt / PowerShell)**:
  ```powershell
  .\venv\Scripts\activate
  ```
- **macOS / Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Configure Streamlit Secrets
Create or update `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
```

> **Note**:
> - Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/).
> - Create a Telegram bot using Telegram's [@BotFather](https://t.me/BotFather) to get your Bot Token.
> - Before receiving messages, make sure you open your Telegram bot and click **Start** or send it at least one message.
> - You can find your Telegram Chat ID by messaging [@userinfobot](https://t.me/userinfobot) on Telegram.

### 5. Run the Application
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🧪 Running Automated Tests

To run the complete test suite:
```bash
python -m unittest test_assistant.py test_apptest.py -v
```

---

## 🔒 Security Best Practices
- Never commit `.streamlit/secrets.toml` or `.env` files to git.
- Verify `.gitignore` includes `secrets.toml` and `venv/`.

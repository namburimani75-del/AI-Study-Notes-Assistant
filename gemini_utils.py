import streamlit as st
from PIL import Image
from typing import List, Dict, Optional
from google import genai
from google.genai import types
from google.genai.errors import APIError

from prompts import STUDY_SYSTEM_PROMPT, ANALYSIS_INSTRUCTION, SUMMARY_PROMPT_TEMPLATE

PRIMARY_MODEL = "gemini-2.5-flash"
FALLBACK_MODELS = ["gemini-2.0-flash", "gemini-1.5-flash"]


def get_gemini_api_key() -> Optional[str]:
    """Retrieve Gemini API key safely from Streamlit secrets."""
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
        if not api_key or "your_gemini_api_key" in api_key.lower():
            return None
        return api_key.strip()
    except Exception:
        return None


def get_gemini_client() -> genai.Client:
    """Initialize and return the Google GenAI client."""
    api_key = get_gemini_api_key()
    if not api_key:
        raise ValueError(
            "Gemini API key is not configured. Please set GEMINI_API_KEY in .streamlit/secrets.toml."
        )
    return genai.Client(api_key=api_key)


def _generate_with_fallback(client: genai.Client, contents: list, config: types.GenerateContentConfig) -> str:
    """Generate content trying primary model first, then falling back if needed."""
    candidate_models = [PRIMARY_MODEL] + FALLBACK_MODELS
    last_error = None
    for model_name in candidate_models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config,
            )
            if response and response.text:
                return response.text
        except Exception as e:
            last_error = e
            continue
    raise last_error if last_error else RuntimeError("Failed to generate response from Gemini API.")


def analyze_study_material(image: Image.Image) -> str:
    """Send image and system prompt to Gemini Vision to analyze study material."""
    client = get_gemini_client()
    config = types.GenerateContentConfig(
        system_instruction=STUDY_SYSTEM_PROMPT,
        temperature=0.3,
    )
    contents = [image, ANALYSIS_INSTRUCTION]
    return _generate_with_fallback(client, contents, config)


def ask_study_assistant(
    image: Optional[Image.Image],
    chat_history: List[Dict[str, str]],
    user_question: str,
) -> str:
    """Generate a conversational answer using the uploaded image and prior chat context."""
    client = get_gemini_client()
    config = types.GenerateContentConfig(
        system_instruction=STUDY_SYSTEM_PROMPT,
        temperature=0.4,
    )

    contents = []
    # Include the study image if available as primary context
    if image is not None:
        contents.append(image)
        contents.append("Here is the study material context for the conversation.")

    # Include recent chat history
    for msg in chat_history:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "user":
            contents.append(f"Student: {content}")
        else:
            contents.append(f"Assistant: {content}")

    contents.append(f"Student: {user_question}\nAssistant:")

    return _generate_with_fallback(client, contents, config)


def generate_study_summary(
    image: Optional[Image.Image],
    analysis: Optional[str] = None,
    chat_history: Optional[List[Dict[str, str]]] = None,
) -> str:
    """Generate a structured, concise study summary formatted for quick revision and Telegram."""
    client = get_gemini_client()
    config = types.GenerateContentConfig(
        system_instruction=STUDY_SYSTEM_PROMPT,
        temperature=0.2,
    )

    instruction = (
        "Create a concise study summary based on the study material and analysis. "
        "Strictly follow this exact layout with these exact headings:\n\n"
        "📚 Study Summary\n\n"
        "Topic:\n"
        "[Topic Name]\n\n"
        "🧠 Simple Explanation:\n"
        "[2-3 sentence clear explanation]\n\n"
        "⭐ Important Points:\n"
        "- [Point 1]\n"
        "- [Point 2]\n"
        "- [Point 3]\n\n"
        "📌 Key Terms:\n"
        "- [Term 1: Definition]\n"
        "- [Term 2: Definition]\n\n"
        "📝 Quick Revision:\n"
        "[Short revision tip or memory aid]"
    )

    contents = []
    if image is not None:
        contents.append(image)
    if analysis:
        contents.append(f"Analysis of material:\n{analysis}")
    if chat_history:
        recent_chats = "\n".join(
            [f"{m['role'].capitalize()}: {m['content']}" for m in chat_history[-6:]]
        )
        contents.append(f"Recent discussion:\n{recent_chats}")
    contents.append(instruction)

    return _generate_with_fallback(client, contents, config)

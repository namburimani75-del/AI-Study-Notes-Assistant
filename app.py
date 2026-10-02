from pdf_utils import create_study_pdf
import streamlit as st
from PIL import Image
import prompts
from gemini_utils import (
    analyze_study_material,
    ask_study_assistant,
    generate_study_summary,
    get_gemini_api_key,
)
from telegram_utils import (
    send_telegram_sync,
    get_telegram_bot_token,
)

# Page configuration
st.set_page_config(
    page_title="AI Study Notes Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Styling
st.markdown(
    """
    <style>
    .main-header {
        text-align: center;
        padding: 1.8rem 1rem 1.2rem 1rem;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 14px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
    }
    .main-subtitle {
        font-size: 1.15rem;
        color: #94a3b8;
        font-weight: 400;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    .analysis-container {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 1.2rem;
        margin-top: 1rem;
    }
    .summary-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 10px;
        padding: 1.2rem;
        font-family: monospace;
        white-space: pre-wrap;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- SESSION STATE INITIALIZATION -----------------
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "telegram_chat_id" not in st.session_state:
    st.session_state.telegram_chat_id = ""
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None
if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_summary" not in st.session_state:
    st.session_state.current_summary = None

# Header Banner
st.markdown(
    """
    <div class="main-header">
        <div class="main-title">🎓 AI Study Notes Assistant</div>
        <div class="main-subtitle">Turn your study material into an interactive AI tutor.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------- SECTION 1: ONBOARDING -----------------
st.subheader("👤 Student Information")
col_name, col_tg = st.columns(2)
with col_name:
    name_input = st.text_input(
        "Student Name",
        value=st.session_state.student_name,
        placeholder="Enter your name (e.g. Manikanta)",
    )
    if name_input != st.session_state.student_name:
        st.session_state.student_name = name_input

with col_tg:
    tg_input = st.text_input(
        "Telegram Chat ID",
        value=st.session_state.telegram_chat_id,
        placeholder="Enter your Telegram Chat ID (e.g. 123456789)",
        help="To get your Chat ID, start Telegram and message @userinfobot or your bot.",
    )
    if tg_input != st.session_state.telegram_chat_id:
        st.session_state.telegram_chat_id = tg_input

if st.session_state.student_name and st.session_state.telegram_chat_id:
    st.success(f"Welcome, {st.session_state.student_name}! Ready for study sessions.")

st.markdown("---")


# ----------------- SECTION 2: STUDY MATERIAL UPLOAD -----------------
st.subheader("📚 Upload Study Material")
uploaded_file = st.file_uploader(
    "Upload Your Study Material",
    type=["png", "jpg", "jpeg", "webp"],
    help="Supported formats: PNG, JPG, JPEG, WEBP ",
)

if uploaded_file is not None:
    try:
        opened_image = Image.open(uploaded_file)
        # If a new image is uploaded, update state and reset previous analysis and chats
        if st.session_state.uploaded_file_name != uploaded_file.name:
            st.session_state.uploaded_image = opened_image
            st.session_state.uploaded_file_name = uploaded_file.name
            st.session_state.analysis = None
            st.session_state.chat_history = []
            st.session_state.current_summary = None
    except Exception:
        st.error("The uploaded file could not be processed. Please upload a valid image.")
        st.session_state.uploaded_image = None

# Display uploaded image if present
if st.session_state.uploaded_image is not None:
    col_img_left, col_img_center, col_img_right = st.columns([1, 4, 1])
    with col_img_center:
        st.image(
            st.session_state.uploaded_image,
            caption="📸 Uploaded Study Material",
            width="stretch",
        )
else:
    st.info("Please upload a study image first.")

st.markdown("---")

# ----------------- SECTION 3: GEMINI VISION ANALYSIS -----------------
st.subheader("🤖 AI Study Analysis")

if st.session_state.uploaded_image is None:
    st.info("Upload study material above to enable AI Vision analysis.")
else:
    # Button to trigger or re-run analysis
    analyze_btn_label = "🔍 Analyze Study Material" if st.session_state.analysis is None else "🔄 Re-analyze Study Material"
    if st.button(analyze_btn_label, type="primary"):
        gemini_key = get_gemini_api_key()
        if not gemini_key:
            st.error(
                "Unable to analyze the image right now. Please check your Gemini API configuration and try again."
            )
            st.info("Tip: Add GEMINI_API_KEY in `.streamlit/secrets.toml`.")
        else:
            with st.spinner("Analyzing study material with Gemini Vision..."):
                try:
                    result = analyze_study_material(st.session_state.uploaded_image)
                    st.session_state.analysis = result
                    # Generate an initial summary as well
                    st.session_state.current_summary = generate_study_summary(
                        image=st.session_state.uploaded_image,
                        analysis=result,
                        chat_history=[],
                    )
                except Exception as e:
                    st.error(
                        "Unable to analyze the image right now. Please check your Gemini API configuration and try again."
                    )

    if st.session_state.analysis:
        st.markdown(
            f'<div class="analysis-container">{st.session_state.analysis}</div>',
            unsafe_allow_html=True,
        )

st.markdown("---")

# ----------------- SECTION 4: AI STUDY CHAT -----------------
st.subheader("💬 Ask Your Study Assistant")

if st.session_state.uploaded_image is None:
    st.info("Upload your notes or textbook image above to start chatting with your AI Study Assistant.")
else:
    # Display existing chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_query = st.chat_input("Ask a question about the uploaded study material...")
    if user_query:
        if not user_query.strip():
            st.warning("Please enter a question.")
        else:
            # Append student query
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)

            # Generate response from Gemini
            gemini_key = get_gemini_api_key()
            if not gemini_key:
                err_msg = (
                    "Unable to answer right now. Please check your Gemini API configuration and try again."
                )
                with st.chat_message("assistant"):
                    st.error(err_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": err_msg})
            else:
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        try:
                            assistant_reply = ask_study_assistant(
                                image=st.session_state.uploaded_image,
                                chat_history=st.session_state.chat_history[:-1],
                                user_question=user_query,
                            )
                            st.markdown(assistant_reply)
                            st.session_state.chat_history.append(
                                {"role": "assistant", "content": assistant_reply}
                            )
                        except Exception:
                            fallback_err = (
                                "Unable to analyze the question right now. "
                                "Please check your Gemini API configuration and try again."
                            )
                            st.error(fallback_err)
                            st.session_state.chat_history.append(
                                {"role": "assistant", "content": fallback_err}
                            )

st.markdown("---")

# ----------------- SECTION 5: TELEGRAM SUMMARY & ACTION -----------------
st.subheader("📲 Telegram")

if st.session_state.uploaded_image is None:
    st.info("Upload and analyze your study material to generate and send a study summary.")
else:
    col_sum_action, col_sum_view = st.columns([1, 1])

    with col_sum_action:
        st.write(
            "Send a comprehensive revision summary directly to your Telegram chat for quick on-the-go review."
        )

        send_btn = st.button("📲 Send Summary to Telegram", type="primary", width="stretch")
        if send_btn:
            # Validate onboarding credentials
            chat_id = st.session_state.telegram_chat_id.strip()
            if not chat_id:
                st.error("❌ Unable to send the summary. Please check your Telegram Chat ID and try again.")
            else:
                bot_token = get_telegram_bot_token()
                if not bot_token:
                    st.error(
                        "Unable to send the Telegram message. Please verify that the bot is running and the Chat ID is correct."
                    )
                    st.info("Tip: Ensure TELEGRAM_BOT_TOKEN is configured in `.streamlit/secrets.toml`.")
                else:
                    with st.spinner("Preparing summary and sending to Telegram..."):
                        # Ensure current_summary is generated
                        summary_text = st.session_state.current_summary
                        if not summary_text:
                            gemini_key = get_gemini_api_key()
                            if gemini_key:
                                try:
                                    summary_text = generate_study_summary(
                                        image=st.session_state.uploaded_image,
                                        analysis=st.session_state.analysis,
                                        chat_history=st.session_state.chat_history,
                                    )
                                    st.session_state.current_summary = summary_text
                                except Exception:
                                    summary_text = None

                        if not summary_text:
                            # Fallback summary format if Gemini summary call had an issue
                            student_header = f"Student: {st.session_state.student_name}\n" if st.session_state.student_name else ""
                            summary_text = (
                                f"📚 Study Summary\n\n"
                                f"{student_header}"
                                f"Topic:\nUploaded Study Material\n\n"
                                f"🧠 Simple Explanation:\n{st.session_state.analysis or 'Material analyzed by AI Study Notes Assistant.'}\n\n"
                                f"⭐ Important Points:\n- Review uploaded notes\n- Test key definitions\n\n"
                                f"📌 Key Terms:\n- Core concepts from uploaded study notes\n\n"
                                f"📝 Quick Revision:\nRe-read key formulas and diagrams before the exam."
                            )
                            st.session_state.current_summary = summary_text

                        # Personalize with student name if provided
                        message_payload = summary_text
                        if st.session_state.student_name and not summary_text.startswith(f"👤 Student: {st.session_state.student_name}"):
                            message_payload = f"👤 Student: {st.session_state.student_name}\n\n" + summary_text

                        success, err = send_telegram_sync(chat_id, message_payload)
                        if success:
                            st.success("✅ Study summary sent to Telegram!")
                        else:
                            st.error(
                                "❌ Unable to send the summary. Please check your Telegram Chat ID and try again."
                            )
                            st.warning(
                                "Unable to send the Telegram message. Please verify that the bot is running and the Chat ID is correct."
                            )

    with col_sum_view:
        if st.session_state.current_summary:
            st.caption("📋 Current Summary Preview:")
            st.markdown(
                f'<div class="summary-card">{st.session_state.current_summary}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.caption("Summary preview will appear here once study material is analyzed.")

# ----------------- SECTION 6: PDF EXPORT -----------------
st.markdown("---")
st.subheader("📄 Export Study Notes")

st.write(
    "Download your AI-generated study summary "
    "for offline revision."
)

if st.session_state.current_summary:
    try:
        pdf_bytes = create_study_pdf(
            student_name=st.session_state.student_name or "Student",
            summary=st.session_state.current_summary,
        )

        st.download_button(
            label="📄 Download Study Notes as PDF",
            data=pdf_bytes,
            file_name="AI_Study_Notes.pdf",
            mime="application/pdf",
            key="download_study_notes_pdf",
            width="stretch",
        )

    except Exception as e:
        st.error(f"❌ Unable to generate PDF: {e}")

else:
    st.info(
        "Generate your study analysis first to enable PDF download."
    )

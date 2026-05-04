import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import urllib.parse as urlparse
import os
import time
import yt_dlp
import requests
from streamlit_lottie import st_lottie

# --- Page Configuration & Modern Theme ---
st.set_page_config(page_title="AI Summarizer 2026", page_icon="🔮", layout="wide")

# --- Helper: Load Lottie Animations ---
@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except:
        return None

lottie_ai = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_V9t630.json")

# --- Custom CSS for 2026 Ultimate UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Outfit:wght@700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main-title {
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        margin-top: -30px;
        margin-bottom: 0px;
        animation: glow 2s ease-in-out infinite alternate;
        letter-spacing: -1.5px;
    }
    .sub-title {
        text-align: center; color: #A0AEC0; font-size: 1.1rem;
        margin-bottom: 50px; font-weight: 300; letter-spacing: 1px;
    }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%) !important;
        color: white !important; border: none !important;
        border-radius: 50px !important; padding: 0.8rem 2.5rem !important;
        font-weight: 600 !important; letter-spacing: 1px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 10px 20px -10px rgba(118, 75, 162, 0.8) !important;
        width: 100%; text-transform: uppercase; font-size: 0.9rem;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-5px) scale(1.02) !important;
        box-shadow: 0 15px 30px -10px rgba(118, 75, 162, 1) !important;
    }
    .stTextInput input, .stFileUploader {
        border-radius: 16px !important;
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 14px !important; color: white !important;
        transition: all 0.3s ease !important; backdrop-filter: blur(10px);
    }
    .stTextInput input:focus {
        border-color: #00F2FE !important;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.3) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }
    @keyframes glow {
        from { text-shadow: 0 0 10px rgba(0, 242, 254, 0.1); }
        to { text-shadow: 0 0 25px rgba(0, 242, 254, 0.4); }
    }
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px; padding: 15px; margin-bottom: 10px;
        backdrop-filter: blur(10px);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; border-radius: 10px 10px 0 0; padding: 0 20px; }
    </style>
""", unsafe_allow_html=True)

# --- Fetch API Key securely ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("🚨 CRITICAL: Streamlit secrets missing! Please check `.streamlit/secrets.toml`.")
    st.stop()

# --- Main Headers ---
st.markdown('<div class="main-title">NeuroNotes AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">The Next-Gen Audio/Visual Intelligence Engine • Powered by Gemini 2.5 Flash</div>', unsafe_allow_html=True)

# --- Session State Initialization ---
if "source_type" not in st.session_state: st.session_state.source_type = None
if "transcript" not in st.session_state: st.session_state.transcript = None
if "uploaded_gemini_file" not in st.session_state: st.session_state.uploaded_gemini_file = None
if "summary" not in st.session_state: st.session_state.summary = None
if "video_id" not in st.session_state: st.session_state.video_id = None
if "chat_history" not in st.session_state: st.session_state.chat_history = []

# --- Beautiful Sidebar ---
with st.sidebar:
    if lottie_ai: st_lottie(lottie_ai, height=180, key="ai_brain")
    st.markdown("### 🔮 The 2026 Engine")
    st.markdown("""
    Welcome to the ultimate intelligence suite. We process multi-modal data in real-time.

    **Supported Platforms:**
    - 🟥 YouTube (Auto-Fallback enabled)
    - 🌐 Vimeo & X/Twitter
    - 📂 Local MP4/MP3 files

    *Your API key is securely encrypted.* 🔐
    """)
    st.markdown("---")
    st.caption("v2.6.0 Cloud | Developed by Atharva & DeepMind AI")

# --- Helper Functions ---
def extract_video_id(url):
    try:
        if "youtu.be" in url: return url.split("/")[-1].split("?")[0]
        if "shorts/" in url: return url.split("shorts/")[-1].split("?")[0]
        parsed_url = urlparse.urlparse(url)
        return urlparse.parse_qs(parsed_url.query)['v'][0]
    except Exception: return None

def get_transcript_with_timestamps(video_id):
    try:
        ytt_api = YouTubeTranscriptApi()
        try:
            fetched_transcript = ytt_api.fetch(video_id, languages=['en', 'hi', 'en-IN'])
        except Exception:
            transcript_list = ytt_api.list(video_id)
            transcript_obj = next(iter(transcript_list), None)
            if transcript_obj: fetched_transcript = transcript_obj.fetch()
            else: return "ERROR_FETCHING_TRANSCRIPT: No transcript found for this video."

        formatted_transcript = ""
        for snippet in fetched_transcript:
            start_time = int(snippet.start)
            formatted_transcript += f"[{start_time // 60:02d}:{start_time % 60:02d}] {snippet.text}\n"
        return formatted_transcript
    except Exception as e: return f"ERROR_FETCHING_TRANSCRIPT: {str(e)}"

def upload_file_to_gemini(file_path):
    try:
        genai.configure(api_key=API_KEY)
        uploaded_file = genai.upload_file(path=file_path)
        while uploaded_file.state.name == "PROCESSING":
            time.sleep(2)
            uploaded_file = genai.get_file(uploaded_file.name)
        if uploaded_file.state.name == "FAILED": raise Exception("Processing failed on AI servers.")
        return uploaded_file
    except Exception as e: raise Exception(f"File Upload Error: {str(e)}")

def download_audio_from_url(url, output_path="temp/downloaded_audio"):
    os.makedirs("temp", exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '128'}],
        'quiet': True, 'no_warnings': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
        final_path = f"{output_path}.mp3"
        if os.path.exists(final_path): return final_path
        else: raise Exception("Audio extraction failed.")
    except Exception as e: raise Exception(f"Download failed: {str(e)}")

def generate_detailed_summary(input_data, is_file=False):
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = """
        You are NeuroNotes, an ultra-advanced AI. Analyze the media.
        Format EXACTLY like this using neat Markdown:

        ## 🧠 Core Synthesis
        (A brilliant 2-3 sentence overview)

        ## ⏱️ Timeline & Analysis
        (Divide into chapters. Format:
        - **[Start Time - End Time] Topic**
        - In-depth, analytical bullet points.)

        ## 🎯 Strategic Takeaways
        (Actionable, high-impact conclusions)
        """
        if is_file: response = model.generate_content([prompt, input_data])
        else: response = model.generate_content(prompt + "\n\nTranscript:\n" + input_data)
        return response.text
    except Exception as e: raise Exception(f"AI Core Error: {str(e)}")

# --- Layout UI ---
_, col_main, _ = st.columns([1, 8, 1])

with col_main:
    st.markdown("#### 📡 Initialize Neural Uplink")
    input_method = st.radio("Select Source",
                            ["🟥 YouTube Instant", "📁 Local Media Link", "🌐 Universal URL Extraction"],
                            horizontal=True, label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        if input_method == "🟥 YouTube Instant":
            youtube_url = st.text_input("YouTube URL:", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")
            if st.button("Synthesize Knowledge ⚡"):
                if not youtube_url: st.error("⚠️ Provide a URL first.")
                else:
                    video_id = extract_video_id(youtube_url)
                    if video_id:
                        st.session_state.source_type = 'youtube'
                        st.session_state.transcript, st.session_state.summary, st.session_state.chat_history = None, None, []
                        st.session_state.video_id = video_id

                        with st.status("🌌 Establishing Neural Connection...", expanded=True) as status:
                            st.write("📡 Fetching temporal data layers...")
                            transcript = get_transcript_with_timestamps(video_id)

                            if transcript.startswith("ERROR"):
                                st.warning("⚠️ Cloud IP Block Detected. Initiating Deep Audio Fallback...")
                                try:
                                    st.write("📥 Ripping audio signature bypassing blocks...")
                                    audio_path = download_audio_from_url(youtube_url)
                                    st.write("☁️ Streaming secure audio to AI Core...")
                                    gemini_file = upload_file_to_gemini(audio_path)
                                    st.write("🧠 Synthesizing neural patterns...")
                                    final_summary = generate_detailed_summary(gemini_file, is_file=True)

                                    # Update state to act as a 'file' so chat works correctly
                                    st.session_state.uploaded_gemini_file = gemini_file
                                    st.session_state.summary = final_summary
                                    st.session_state.source_type = 'file'

                                    if os.path.exists(audio_path): os.remove(audio_path)
                                    status.update(label="✅ Fallback Knowledge Synthesized.", state="complete", expanded=False)
                                    st.rerun()
                                except Exception as fallback_e:
                                    status.update(label="❌ Total Uplink Failure", state="error")
                                    st.error(f"Fallback extraction also failed: {fallback_e}")
                                    if 'audio_path' in locals() and audio_path and os.path.exists(audio_path): os.remove(audio_path)

                            elif len(transcript.strip()) < 50:
                                status.update(label="❌ Uplink Failed", state="error")
                                st.error("Void detected. No words found.")
                            else:
                                st.write("🧠 Synthesizing neural patterns...")
                                try:
                                    final_summary = generate_detailed_summary(transcript, is_file=False)
                                    st.session_state.transcript, st.session_state.summary = transcript, final_summary
                                    status.update(label="✅ Knowledge Synthesized.", state="complete", expanded=False)
                                    st.rerun()
                                except Exception as e:
                                    status.update(label="❌ Core Failure", state="error")
                                    st.error(e)
                    else: st.error("❌ Invalid Signature URL.")

        elif input_method == "📁 Local Media Link":
            uploaded_file = st.file_uploader("Drop Media", type=["mp3", "wav", "mp4"], label_visibility="collapsed")
            if st.button("Synthesize Knowledge ⚡"):
                if not uploaded_file: st.error("⚠️ Provide media first.")
                else:
                    st.session_state.source_type = 'file'
                    st.session_state.transcript, st.session_state.summary, st.session_state.chat_history = None, None, []
                    st.session_state.video_id = uploaded_file.name

                    os.makedirs("temp", exist_ok=True)
                    temp_file_path = os.path.join("temp", uploaded_file.name)
                    with open(temp_file_path, "wb") as f: f.write(uploaded_file.getbuffer())

                    with st.status("🌌 Processing Local Databank...", expanded=True) as status:
                        try:
                            st.write("☁️ Securely streaming to AI Core...")
                            gemini_file = upload_file_to_gemini(temp_file_path)
                            st.write("🧠 Synthesizing neural patterns...")
                            final_summary = generate_detailed_summary(gemini_file, is_file=True)
                            st.session_state.uploaded_gemini_file, st.session_state.summary = gemini_file, final_summary
                            if os.path.exists(temp_file_path): os.remove(temp_file_path)
                            status.update(label="✅ Knowledge Synthesized.", state="complete", expanded=False)
                            st.rerun()
                        except Exception as e:
                            status.update(label="❌ Core Failure", state="error")
                            st.error(e)
                            if os.path.exists(temp_file_path): os.remove(temp_file_path)

        elif input_method == "🌐 Universal URL Extraction":
            other_url = st.text_input("Universal URL:", placeholder="https://vimeo.com/...", label_visibility="collapsed")
            if st.button("Synthesize Knowledge ⚡"):
                if not other_url: st.error("⚠️ Provide URL first.")
                else:
                    st.session_state.source_type = 'file'
                    st.session_state.transcript, st.session_state.summary, st.session_state.chat_history = None, None, []
                    st.session_state.video_id = "external_media"
                    audio_path = ""

                    with st.status("🌌 Connecting to Universal Grid...", expanded=True) as status:
                        try:
                            st.write("📥 Ripping audio signature...")
                            audio_path = download_audio_from_url(other_url)
                            st.write("☁️ Streaming to AI Core...")
                            gemini_file = upload_file_to_gemini(audio_path)
                            st.write("🧠 Synthesizing neural patterns...")
                            final_summary = generate_detailed_summary(gemini_file, is_file=True)
                            st.session_state.uploaded_gemini_file, st.session_state.summary = gemini_file, final_summary
                            if os.path.exists(audio_path): os.remove(audio_path)
                            status.update(label="✅ Knowledge Synthesized.", state="complete", expanded=False)
                            st.rerun()
                        except Exception as e:
                            status.update(label="❌ Core Failure", state="error")
                            st.error(e)
                            if audio_path and os.path.exists(audio_path): os.remove(audio_path)


    # --- RESULTS SECTION ---
    if st.session_state.summary:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🧬 Synthesized Output")
        tab_notes, tab_chat = st.tabs(["📄 Nexus Notes", "💬 Interactive Terminal"])
        with tab_notes:
            with st.container(border=True): st.markdown(st.session_state.summary)
            st.download_button("📥 Export Protocol (TXT)", data=st.session_state.summary, file_name=f"NeuroNotes_{st.session_state.video_id}.txt", mime="text/plain", use_container_width=True)
        with tab_chat:
            st.caption("Ask NeuroNotes anything about the processed media.")
            chat_container = st.container(border=True, height=500)
            with chat_container:
                for msg in st.session_state.chat_history:
                    with st.chat_message(msg["role"]): st.write(msg["text"])
            user_query = st.chat_input("Enter query...")
            if user_query:
                st.session_state.chat_history.append({"role": "user", "text": user_query})
                st.rerun()

    # Chat logic processor
    if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
        user_query = st.session_state.chat_history[-1]["text"]
        try:
            genai.configure(api_key=API_KEY)
            gemini_history = []
            if st.session_state.source_type == 'youtube':
                sys_instr = f"You are NeuroNotes AI. Answer based ONLY on this context:\n{st.session_state.transcript}"
                model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=sys_instr)
            else:
                model = genai.GenerativeModel("gemini-2.5-flash")
                gemini_history = [
                    {"role": "user", "parts": [st.session_state.uploaded_gemini_file, "This is the core media. Answer all questions strictly based on it."]},
                    {"role": "model", "parts": ["Acknowledged. Awaiting queries."]}
                ]
            for msg in st.session_state.chat_history[:-1]:
                role = "user" if msg["role"] == "user" else "model"
                gemini_history.append({"role": role, "parts": [msg["text"]]})

            chat = model.start_chat(history=gemini_history)
            with st.spinner("Processing query... 💫"):
                response = chat.send_message(user_query)

            st.session_state.chat_history.append({"role": "assistant", "text": response.text})
            st.rerun()
        except Exception as e:
            st.session_state.chat_history.pop()
            st.error(f"❌ Terminal Error: {e}" if "429" not in str(e) else "❌ Grid Overloaded (Quota Exceeded). Wait 60s.")

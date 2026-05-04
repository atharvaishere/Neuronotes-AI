# 🔮 NeuroNotes AI 

**The Next-Gen Audio/Visual Intelligence Engine**  
Extract beautiful, structured notes from YouTube videos, Vimeo links, and local audio/video files instantly, and chat directly with the media context—all powered by **Google Gemini 2.5 Flash**.

![NeuroNotes UI](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![AI Backend](https://img.shields.io/badge/AI-Gemini%202.5-4285F4?style=for-the-badge&logo=google)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)

---

## ✨ Features

- 🟥 **YouTube Instant Sync:** Fetches exact transcripts & timestamps flawlessly, avoiding heavy downloads.
- 🌐 **Universal URL Extraction:** Uses `yt-dlp` to pull audio from Vimeo, Twitter/X, and 1000+ other sites.
- 📁 **Native Local Media Parsing:** Upload MP3/MP4 files directly. Uses Gemini's native multi-modal capabilities (no extra Whisper dependencies needed!).
- 💬 **Interactive Terminal (Chat):** Ask questions directly to the video. The AI remembers the context.
- 🎨 **2026 Modern UI:** Glassmorphism, animations, gradient glowing text, and Lottie integrations.

## 🛠️ Tech Stack
- **Frontend:** Streamlit (Custom CSS injected for Dark/Modern Theme)
- **AI Core:** Google Generative AI (`gemini-2.5-flash`)
- **Extraction:** `youtube-transcript-api`, `yt-dlp`
- **Animations:** `streamlit-lottie`

## 🚀 Quickstart (Local Setup)

1. **Clone the repository**
   ```bash
   git clone https://github.com/atharvaishere/Neuronotes-AI.git
   cd Neuronotes-AI
   ```

2. **Create a virtual environment & install dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   Create a folder `.streamlit` and a file `secrets.toml` inside it:
   ```bash
   mkdir .streamlit
   echo 'GEMINI_API_KEY = "your_google_gemini_api_key_here"' > .streamlit/secrets.toml
   ```

4. **Run the Engine**
   ```bash
   streamlit run app.py
   ```

## ☁️ Deployment (Streamlit Cloud)
This app is ready to be hosted on Streamlit Community Cloud. 
1. Link your GitHub repository.
2. Select `app.py` as the entrypoint.
3. Add your `GEMINI_API_KEY` in the **Advanced Settings > Secrets** section before deploying.

---
*Developed by Atharva Shrivastava.*

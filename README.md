# 📝 AI Resume Critiquer

> **Get instant, SaaS-level AI feedback on your resume** — with ATS scoring, section-by-section review, bullet rewrites, keyword analysis, and actionable improvements.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.13+](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ Features

### 🎯 Three Distinct Analysis Modes

| Mode | What You Get | Best For |
|------|-------------|----------|
| **🎯 Full Analysis** | 13-section deep dive — candidate profile, section reviews, bullet rewrites, action verb audit, keyword analysis, formatting issues, quick wins, and more | Complete resume overhaul |
| **⚡ ATS Optimization** | ATS-focused report with PASS/FAIL parsing results, keyword match rates, parsing blockers, ATS-optimized rewrites, and fix checklist | Before applying online |
| **📋 Quick Review** | 4-section compact report — score, verdict, strengths/weaknesses, and quick wins | Fast feedback in 30 seconds |

### 📊 What Gets Analyzed

- **🏆 Resume Score** — Overall score + ATS score with animated score ring and letter grade
- **👤 Candidate Profile** — Detected career level, experience years, competitive ranking, readability score
- **📑 Section-by-Section Review** — Every section (Contact, Summary, Experience, Education, Skills, Projects) scored individually
- **✏️ Bullet Point Rewrites** — Your weakest bullets rewritten with stronger action verbs and metrics (Before → After)
- **💬 Action Verb Analysis** — Strong verbs found ✓, weak verbs to replace ✗, and suggested power verbs
- **🔑 Keyword Analysis** — Found vs. missing keywords with match rate percentage
- **🎨 Formatting Issues** — Specific formatting problems detected
- **📌 Missing Sections** — Resume sections that should be added
- **⚡ Quick Wins** — Changes that take less than 5 minutes but have big impact
- **🚀 Actionable Improvements** — Specific, detailed steps to improve your resume
- **🤖 ATS Optimization Tips** — How to make your resume ATS-friendly
- **📥 Downloadable Report** — Export your full analysis as a `.txt` file

### 🎨 Design

- **Warm, light, peaceful UI** — Cream/off-white background with coral/peach accents
- **DM Sans typography** — Clean, modern, and highly readable
- **White cards with warm shadows** — Professional and approachable
- **Color-coded everything** — Green (good), yellow (warning), red (needs work)
- **Responsive layout** — Works on desktop and mobile

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/resume-critiquer.git
cd resume-critiquer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.env` file in the project root:

```env
# Option 1: Groq API (Recommended — faster & free)
GROQ_API_KEY=your_groq_api_key_here

# Option 2: OpenRouter API (fallback)
OPENAI_API_KEY=your_openrouter_api_key_here
```

**Get your free API key:**
- 🚀 **Groq** (recommended): [console.groq.com](https://console.groq.com) — Fast, free tier available
- 🌐 **OpenRouter**: [openrouter.ai](https://openrouter.ai) — Multiple model access

### 4. Run the app

```bash
streamlit run main.py
```

The app will open at `http://localhost:8501`

---

## 🌐 Deploy to Streamlit Community Cloud

### Steps:

1. **Push to GitHub** (make sure `.env` is in `.gitignore`!)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set the main file to `main.py`
5. Add your API key in **Settings → Secrets**:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
6. Deploy! 🎉

### Streamlit Secrets Setup

When deploying to Streamlit Community Cloud, add your secrets in the app's settings:

```toml
# .streamlit/secrets.toml (for local development)
# Or add in Streamlit Cloud dashboard under Settings > Secrets

GROQ_API_KEY = "gsk_your_key_here"
```

> **Note:** The app auto-detects `GROQ_API_KEY` first (faster), then falls back to `OPENAI_API_KEY`.

---

## 🛠 Tech Stack

| Technology | Purpose |
|-----------|---------|
| **[Streamlit](https://streamlit.io)** | Web framework & UI |
| **[OpenAI SDK](https://github.com/openai/openai-python)** | API client for LLM calls |
| **[Groq](https://groq.com)** | Fast LLM inference (Llama 3.3 70B) |
| **[PyPDF2](https://pypdf2.readthedocs.io)** | PDF text extraction |
| **[python-dotenv](https://pypi.org/project/python-dotenv/)** | Environment variable management |

---

## 📁 Project Structure

```
resume-critiquer/
├── main.py              # Main Streamlit application
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project metadata
├── .env                 # API keys (not committed)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

---

## 📸 Screenshots

### Upload & Analyze
Upload your resume (PDF or TXT), optionally set a target job role with autocomplete suggestions, and choose your analysis mode.

### Results Dashboard
Get a comprehensive analysis with scores, section reviews, bullet rewrites, keyword analysis, and actionable improvements — all in a warm, beautiful interface.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io) ❤️
- AI powered by [Groq](https://groq.com) & [OpenRouter](https://openrouter.ai)
- Font: [DM Sans](https://fonts.google.com/specimen/DM+Sans) by Google Fonts

---

<div align="center">
  <strong>⭐ Star this repo if you found it useful!</strong>
  <br><br>
  Built with ❤️ using Streamlit & AI
</div>

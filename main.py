import streamlit as st
import PyPDF2
import io
import os
import json
import re
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

from auth import (
    is_logged_in, get_user_info,
    get_user_email, show_login_page, load_history, save_to_history
)

# ─── Page Config ───
st.set_page_config(
    page_title="AI Resume Critiquer",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─── Warm Light Theme CSS ───
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800&display=swap');

:root {
    --bg: #faf8f5;
    --bg-warm: #fdf6ee;
    --bg-card: #ffffff;
    --bg-sidebar: #fef8f1;
    --accent: #e8734a;
    --accent-light: #fdeee8;
    --accent-hover: #d4623c;
    --accent-gradient: linear-gradient(135deg, #e8734a 0%, #d4623c 100%);
    --green: #16a34a;
    --green-light: #f0fdf4;
    --green-border: #bbf7d0;
    --red: #dc2626;
    --red-light: #fef2f2;
    --red-border: #fecaca;
    --yellow: #ca8a04;
    --yellow-light: #fefce8;
    --yellow-border: #fef08a;
    --blue: #2563eb;
    --blue-light: #eff6ff;
    --blue-border: #bfdbfe;
    --purple: #7c3aed;
    --purple-light: #f5f3ff;
    --purple-border: #ddd6fe;
    --text: #1f1f1f;
    --text-secondary: #6b7280;
    --text-muted: #9ca3af;
    --border: #f0ece6;
    --border-dark: #e5e0d8;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.03);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.05), 0 1px 3px rgba(0,0,0,0.04);
    --shadow-lg: 0 8px 30px rgba(0,0,0,0.06);
    --radius: 16px;
    --radius-sm: 12px;
    --radius-xs: 8px;
}

/* ── Global ── */
html, body, .stApp {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}
.stApp {
    background: var(--bg) !important;
}

/* ── Hide Defaults ── */
#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}

/* ── Scrollbar ── */
::-webkit-scrollbar {width: 6px;}
::-webkit-scrollbar-track {background: var(--bg);}
::-webkit-scrollbar-thumb {background: #d4cfc7; border-radius: 3px;}
::-webkit-scrollbar-thumb:hover {background: var(--accent);}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 1rem;
    background: var(--accent-light);
    border-radius: 24px;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--accent);
    margin-bottom: 1rem;
    letter-spacing: 0.3px;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 0.5rem;
    letter-spacing: -0.8px;
    line-height: 1.15;
}
.hero-title span {
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1.05rem;
    color: var(--text-secondary);
    line-height: 1.65;
    max-width: 500px;
    margin: 0 auto;
}

/* ── Card ── */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.3s ease, border-color 0.3s ease;
}
.card:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--border-dark);
}
.card-head {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin-bottom: 0.85rem;
}
.card-dot {
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-xs);
    font-size: 1.05rem;
    flex-shrink: 0;
}
.dot-orange {background: var(--accent-light); color: var(--accent);}
.dot-green {background: var(--green-light); color: var(--green);}
.dot-red {background: var(--red-light); color: var(--red);}
.dot-yellow {background: var(--yellow-light); color: var(--yellow);}
.dot-blue {background: var(--blue-light); color: var(--blue);}
.dot-purple {background: var(--purple-light); color: var(--purple);}
.card-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text);
}
.card-desc {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-top: 1px;
}

/* ── ATS Score ── */
.score-section {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2.5rem;
    padding: 1rem 0;
    flex-wrap: wrap;
}
.score-circle {
    position: relative;
    width: 150px;
    height: 150px;
}
.score-circle svg {
    transform: rotate(-90deg);
}
.ring-bg {
    fill: none;
    stroke: var(--border);
    stroke-width: 10;
}
.ring-fill {
    fill: none;
    stroke-width: 10;
    stroke-linecap: round;
    stroke-dasharray: 408;
    transition: stroke-dashoffset 1.5s cubic-bezier(0.4,0,0.2,1);
}
.ring-green {stroke: var(--green);}
.ring-yellow {stroke: var(--yellow);}
.ring-red {stroke: var(--red);}
.score-num {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
}
.score-big {
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1;
}
.score-big.c-green {color: var(--green);}
.score-big.c-yellow {color: var(--yellow);}
.score-big.c-red {color: var(--red);}
.score-tag {
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-top: 4px;
}
.score-details {
    display: flex;
    flex-direction: column;
    gap: 0.55rem;
}
.score-detail-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.55rem 1rem;
    background: var(--bg);
    border-radius: var(--radius-xs);
    border: 1px solid var(--border);
    min-width: 200px;
}
.score-detail-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}
.bg-green {background: var(--green);}
.bg-yellow {background: var(--yellow);}
.bg-red {background: var(--red);}
.score-detail-label {
    font-size: 0.82rem;
    color: var(--text-secondary);
    flex-grow: 1;
}
.score-detail-val {
    font-size: 0.82rem;
    font-weight: 700;
}

/* ── Progress Bars ── */
.bar-wrap {margin-bottom: 0.85rem;}
.bar-top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.3rem;
}
.bar-name {font-size: 0.85rem; font-weight: 500; color: var(--text-secondary);}
.bar-val {font-size: 0.82rem; font-weight: 700;}
.bar-track {
    width: 100%;
    height: 7px;
    background: var(--border);
    border-radius: 4px;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 1.2s cubic-bezier(0.4,0,0.2,1);
}
.fill-green {background: var(--green);}
.fill-yellow {background: var(--yellow);}
.fill-red {background: var(--red);}

/* ── Item Lists ── */
.items {list-style: none; padding: 0; margin: 0;}
.items li {
    padding: 0.6rem 0.9rem;
    margin-bottom: 0.4rem;
    border-radius: var(--radius-xs);
    font-size: 0.9rem;
    line-height: 1.6;
    color: var(--text);
    display: flex;
    align-items: flex-start;
    gap: 0.55rem;
}
.items li .li-icon {flex-shrink: 0; margin-top: 2px;}
.items.s-green li {background: var(--green-light); border: 1px solid var(--green-border);}
.items.s-red li {background: var(--red-light); border: 1px solid var(--red-border);}
.items.s-blue li {background: var(--blue-light); border: 1px solid var(--blue-border);}
.items.s-yellow li {background: var(--yellow-light); border: 1px solid var(--yellow-border);}

/* ── Tags ── */
.tags {display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.3rem;}
.tag {
    display: inline-block;
    padding: 0.3rem 0.75rem;
    border-radius: 8px;
    font-size: 0.8rem;
    font-weight: 600;
}
.t-found {background: var(--green-light); border: 1px solid var(--green-border); color: var(--green);}
.t-miss {background: var(--yellow-light); border: 1px solid var(--yellow-border); color: var(--yellow);}

/* ── Streamlit Overrides ── */
.stFileUploader > div {
    background: var(--bg-card) !important;
    border: 2px dashed var(--border-dark) !important;
    border-radius: var(--radius) !important;
}
.stFileUploader > div:hover {
    border-color: var(--accent) !important;
}
.stTextInput input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-dark) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.6rem 0.9rem !important;
}
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(232,115,74,0.12) !important;
}
.stTextInput > div > div {
    background: transparent !important;
    border: none !important;
}
.stButton > button {
    background: var(--accent-gradient) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.65rem 2rem !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    font-family: 'DM Sans', sans-serif !important;
    box-shadow: 0 4px 14px rgba(232,115,74,0.25) !important;
    transition: transform 0.2s, box-shadow 0.3s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(232,115,74,0.35) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-dark) !important;
    border-radius: var(--radius-sm) !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMarkdown p {
    color: var(--text-secondary) !important;
}

/* ── Download ── */
.stDownloadButton > button {
    background: var(--bg) !important;
    color: var(--text) !important;
    border: 1px solid var(--border-dark) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    box-shadow: none !important;
}
.stDownloadButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ── Divider ── */
hr {
    border: none;
    height: 1px;
    background: var(--border);
    margin: 1.5rem 0;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 2.5rem 0 1rem;
    color: var(--text-muted);
    font-size: 0.78rem;
}
.footer a {color: var(--accent); text-decoration: none;}
.footer a:hover {text-decoration: underline;}
</style>
""", unsafe_allow_html=True)


# ─── Helpers ───

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text


def extract_text_from_upload(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")


def color_class(score):
    if score >= 70: return "green"
    if score >= 50: return "yellow"
    return "red"


def grade(score):
    if score >= 90: return "A+"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    if score >= 50: return "D"
    return "F"


def build_prompt(text, role, mode):
    ctx = f"targeting the role of **{role}**" if role else "for general job applications"

    if mode == "🎯 Full Analysis":
        return f"""You are an elite resume reviewer, ATS expert, and career coach with 15+ years of HR and recruitment experience at top companies like Google, McKinsey, and Amazon.

Perform a DEEP, thorough, SaaS-level analysis of this resume {ctx}. Be specific, cite exact lines from the resume, and give brutally honest feedback. Return ONLY valid JSON — no markdown, no code fences, no extra text.

{{
  "ats_score": <integer 0-100>,
  "overall_score": <integer 0-100>,
  "summary": "<3-4 sentence executive summary. Be specific about what makes this resume strong or weak. Mention specific sections.>",
  "ats_verdict": "<one detailed sentence ATS verdict>",
  "readability_score": <integer 0-100, how easy it is to scan in 6 seconds>,
  "career_level": "<detected career level: Entry/Junior/Mid/Senior/Lead/Executive>",
  "estimated_experience_years": "<estimated years like '1-2 years' or '5+ years'>",
  "competitive_ranking": "<Top 10%/Top 25%/Top 50%/Bottom 50% compared to similar candidates>",
  "scores": {{
    "Content & Impact": <int 0-100>,
    "Formatting & Structure": <int 0-100>,
    "Skills Presentation": <int 0-100>,
    "Experience Quality": <int 0-100>,
    "ATS Compatibility": <int 0-100>,
    "Keyword Optimization": <int 0-100>,
    "Quantification & Metrics": <int 0-100>,
    "Action Verbs & Language": <int 0-100>
  }},
  "section_review": [
    {{"section": "<section name like Contact Info/Summary/Experience/Education/Skills/Projects/Certifications>", "score": <int 0-100>, "verdict": "<1-2 sentence specific feedback for this section>"}}
  ],
  "strengths": ["<specific strength citing resume content>", "<strength 2>", "<strength 3>", "<strength 4>"],
  "weaknesses": ["<specific weakness with example from resume>", "<weakness 2>", "<weakness 3>", "<weakness 4>"],
  "improvements": ["<very specific actionable improvement with example>", "<improvement 2>", "<improvement 3>", "<improvement 4>", "<improvement 5>", "<improvement 6>"],
  "bullet_rewrites": [
    {{"original": "<exact weak bullet point from resume>", "rewritten": "<improved version with metrics and action verbs>"}},
    {{"original": "<another weak bullet>", "rewritten": "<improved version>"}},
    {{"original": "<another weak bullet>", "rewritten": "<improved version>"}}
  ],
  "action_verb_analysis": {{
    "strong_verbs_found": ["<verb1>", "<verb2>", "<verb3>"],
    "weak_verbs_found": ["<weak verb1>", "<weak verb2>"],
    "suggested_power_verbs": ["<suggested1>", "<suggested2>", "<suggested3>", "<suggested4>", "<suggested5>"]
  }},
  "formatting_issues": ["<specific formatting issue 1>", "<issue 2>", "<issue 3>"],
  "missing_sections": ["<missing section that should be added>"],
  "missing_keywords": ["<kw1>", "<kw2>", "<kw3>", "<kw4>", "<kw5>"],
  "found_keywords": ["<found kw1>", "<found kw2>", "<found kw3>", "<found kw4>"],
  "ats_tips": ["<specific ATS tip 1>", "<tip 2>", "<tip 3>", "<tip 4>"],
  "quick_wins": ["<change that takes <5 min and has big impact 1>", "<quick win 2>", "<quick win 3>"]
}}

Resume:
{text}"""

    elif mode == "⚡ ATS Optimization":
        return f"""You are an ATS (Applicant Tracking System) optimization expert who has worked with Workday, Greenhouse, Lever, and iCIMS systems.

Perform a deep ATS-focused analysis of this resume {ctx}. Be very specific. Return ONLY valid JSON — no markdown, no code fences, no extra text.

{{
  "ats_score": <integer 0-100>,
  "overall_score": <integer 0-100>,
  "summary": "<3-4 sentence ATS-focused summary>",
  "ats_verdict": "<one detailed sentence ATS verdict>",
  "readability_score": <integer 0-100>,
  "career_level": "<detected career level>",
  "estimated_experience_years": "<estimated years>",
  "competitive_ranking": "<Top 10%/Top 25%/Top 50%/Bottom 50%>",
  "scores": {{
    "ATS Parsing": <int 0-100>,
    "Keyword Match": <int 0-100>,
    "Section Headers": <int 0-100>,
    "File Format": <int 0-100>,
    "Contact Info": <int 0-100>,
    "Quantified Results": <int 0-100>,
    "Date Formatting": <int 0-100>,
    "Overall Structure": <int 0-100>
  }},
  "section_review": [
    {{"section": "<section name>", "score": <int 0-100>, "verdict": "<ATS-specific feedback for this section>"}}
  ],
  "strengths": ["<ATS str 1>", "<str 2>", "<str 3>", "<str 4>"],
  "weaknesses": ["<ATS wk 1>", "<wk 2>", "<wk 3>", "<wk 4>"],
  "improvements": ["<ATS imp 1>", "<imp 2>", "<imp 3>", "<imp 4>", "<imp 5>", "<imp 6>"],
  "bullet_rewrites": [
    {{"original": "<weak bullet from resume>", "rewritten": "<ATS-optimized version>"}},
    {{"original": "<another bullet>", "rewritten": "<optimized version>"}}
  ],
  "action_verb_analysis": {{
    "strong_verbs_found": ["<verb1>", "<verb2>"],
    "weak_verbs_found": ["<weak1>", "<weak2>"],
    "suggested_power_verbs": ["<sug1>", "<sug2>", "<sug3>", "<sug4>", "<sug5>"]
  }},
  "formatting_issues": ["<formatting issue 1>", "<issue 2>", "<issue 3>"],
  "missing_sections": ["<missing section>"],
  "missing_keywords": ["<kw1>", "<kw2>", "<kw3>", "<kw4>", "<kw5>", "<kw6>"],
  "found_keywords": ["<kw1>", "<kw2>", "<kw3>"],
  "ats_tips": ["<tip 1>", "<tip 2>", "<tip 3>", "<tip 4>", "<tip 5>"],
  "quick_wins": ["<quick ATS fix 1>", "<fix 2>", "<fix 3>"]
}}

Resume:
{text}"""

    else:
        return f"""You are a senior recruiter doing a focused quick review.

Review this resume {ctx}. Return ONLY valid JSON — no markdown, no code fences, no extra text.

{{
  "ats_score": <int 0-100>,
  "overall_score": <int 0-100>,
  "summary": "<2-3 sentence quick verdict>",
  "ats_verdict": "<one sentence ATS verdict>",
  "readability_score": <int 0-100>,
  "career_level": "<detected career level>",
  "estimated_experience_years": "<estimated years>",
  "competitive_ranking": "<Top 10%/Top 25%/Top 50%/Bottom 50%>",
  "scores": {{
    "First Impression": <int 0-100>,
    "Readability": <int 0-100>,
    "Relevance": <int 0-100>
  }},
  "section_review": [],
  "strengths": ["<str 1>", "<str 2>"],
  "weaknesses": ["<wk 1>", "<wk 2>"],
  "improvements": ["<imp 1>", "<imp 2>", "<imp 3>"],
  "bullet_rewrites": [],
  "action_verb_analysis": {{"strong_verbs_found": [], "weak_verbs_found": [], "suggested_power_verbs": []}},
  "formatting_issues": [],
  "missing_sections": [],
  "missing_keywords": [],
  "found_keywords": [],
  "ats_tips": ["<tip 1>", "<tip 2>"],
  "quick_wins": ["<quick win 1>", "<quick win 2>"]
}}

Resume:
{text}"""


def parse_json(text):
    text = text.strip()
    m = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if m:
        text = m.group(1)
    if not text.startswith('{'):
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m:
            text = m.group(0)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def render_score(ats, overall, verdict, g):
    c = color_class(ats)
    oc = color_class(overall)
    offset = 408 - (408 * ats / 100)
    st.markdown(f"""
    <div class="card" style="padding:1.8rem;">
        <div class="card-head" style="justify-content:center; margin-bottom:0.4rem;">
            <div class="card-dot dot-orange">🏆</div>
            <span class="card-title" style="font-size:1.05rem;">Resume Score</span>
        </div>
        <div class="score-section">
            <div class="score-circle">
                <svg width="150" height="150" viewBox="0 0 150 150">
                    <circle class="ring-bg" cx="75" cy="75" r="65"/>
                    <circle class="ring-fill ring-{c}" cx="75" cy="75" r="65"
                        style="stroke-dashoffset: {offset}"/>
                </svg>
                <div class="score-num">
                    <div class="score-big c-{c}">{ats}</div>
                    <div class="score-tag">ATS Score</div>
                </div>
            </div>
            <div class="score-details">
                <div class="score-detail-row">
                    <div class="score-detail-dot bg-{oc}"></div>
                    <span class="score-detail-label">Overall Score</span>
                    <span class="score-detail-val c-{oc}">{overall}/100</span>
                </div>
                <div class="score-detail-row">
                    <div class="score-detail-dot bg-{c}"></div>
                    <span class="score-detail-label">ATS Score</span>
                    <span class="score-detail-val c-{c}">{ats}/100</span>
                </div>
                <div class="score-detail-row">
                    <div class="score-detail-dot bg-{oc}"></div>
                    <span class="score-detail-label">Grade</span>
                    <span class="score-detail-val c-{oc}">{g}</span>
                </div>
            </div>
        </div>
        <p style="text-align:center; color:var(--text-secondary); font-size:0.88rem; margin:0.6rem 0 0;">
            {verdict}
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_bars(scores):
    html = ""
    for name, val in scores.items():
        c = color_class(val)
        html += f"""
        <div class="bar-wrap">
            <div class="bar-top">
                <span class="bar-name">{name}</span>
                <span class="bar-val c-{c}">{val}/100</span>
            </div>
            <div class="bar-track">
                <div class="bar-fill fill-{c}" style="width:{val}%"></div>
            </div>
        </div>"""
    st.markdown(html, unsafe_allow_html=True)


def render_items(items, cls, icon):
    html = "".join([f'<li><span class="li-icon">{icon}</span>{item}</li>' for item in items])
    st.markdown(f'<ul class="items {cls}">{html}</ul>', unsafe_allow_html=True)


def render_tags(found, missing):
    html = '<div class="tags">'
    for k in found:
        html += f'<span class="tag t-found">✓ {k}</span>'
    for k in missing:
        html += f'<span class="tag t-miss">✗ {k}</span>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# ─── Authentication Gate ───
if not is_logged_in():
    show_login_page()

_ui = get_user_info()
user_name = _ui.get("name", "User")
user_email = _ui.get("email", "")
user_picture = _ui.get("picture", "")


# ─── Sidebar ───
with st.sidebar:
    _avatar = f'<img src="{user_picture}" style="width:56px;height:56px;border-radius:50%;border:3px solid #f0ece6;" referrerpolicy="no-referrer"/>' if user_picture else '<div style="width:56px;height:56px;border-radius:50%;background:#fdeee8;display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:1.5rem;">👤</div>'
    st.markdown(f"""
    <div style="text-align:center; padding:1.2rem 0 0.5rem;">
        {_avatar}
        <div style="font-size:0.95rem; font-weight:700; color:#1f1f1f; margin-top:0.4rem;">{user_name}</div>
        <div style="font-size:0.7rem; color:#9ca3af; margin-top:0.1rem;">{user_email}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    analysis_mode = st.selectbox(
        "🔍 Analysis Mode",
        ["🎯 Full Analysis", "⚡ ATS Optimization", "📋 Quick Review"],
        help="Choose how deeply you want your resume analyzed."
    )

    st.markdown("---")

    st.markdown('<div style="font-weight:700; font-size:0.88rem; color:#1f1f1f; margin-bottom:0.5rem;">📋 Analysis History</div>', unsafe_allow_html=True)
    _history = load_history(user_email)
    if _history:
        for _h in _history[:8]:
            _fname = _h.get("file_name", "resume.pdf")
            _sc = _h.get("ats_score", 0)
            _role = _h.get("job_role", "General")
            _ts = _h.get("timestamp", "")
            _sc_color = "#16a34a" if _sc >= 70 else ("#ca8a04" if _sc >= 50 else "#dc2626")
            st.markdown(f"""
            <div style="padding:0.55rem 0.7rem; margin-bottom:0.4rem; background:#fff; border:1px solid #f0ece6; border-radius:10px; font-size:0.78rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:600; color:#1f1f1f;">📄 {_fname[:25]}</span>
                    <span style="font-weight:700; color:{_sc_color};">{_sc}/100</span>
                </div>
                <div style="color:#9ca3af; font-size:0.7rem; margin-top:0.2rem;">{_role} · {_ts}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No analyses yet. Upload a resume to get started!")

    st.markdown("---")

    st.markdown("""
    <div style="padding:1rem; background:#fff; border-radius:12px; border:1px solid #f0ece6; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
        <div style="font-weight:700; font-size:0.88rem; margin-bottom:0.6rem; color:#1f1f1f;">💡 Pro Tips</div>
        <div style="font-size:0.78rem; color:#6b7280; line-height:1.65;">
            • Upload PDF for best parsing<br>
            • Add target job role for tailored advice<br>
            • Use ATS mode before applying online<br>
            • Focus on top 3 improvements first
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.button("🚪 Sign Out", on_click=st.logout, use_container_width=True)


# ─── Hero ───
st.markdown("""
<div class="hero">
    <div class="hero-badge">✨ AI-Powered Analysis</div>
    <div class="hero-title">Resume <span>Critiquer</span></div>
    <div class="hero-sub">
        Upload your resume and get instant feedback with ATS scoring 
        and actionable insights to land your dream job.
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Upload ───
st.markdown("""
<div class="card">
    <div class="card-head">
        <div class="card-dot dot-orange">📄</div>
        <div>
            <div class="card-title">Upload Your Resume</div>
            <div class="card-desc">PDF or TXT · Max 200 MB</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload", type=["pdf", "txt"], label_visibility="collapsed")

# ─── Job Role Suggestions ───
JOB_ROLES = [
    "Python Developer", "Java Developer", "JavaScript Developer", "Full Stack Developer",
    "Frontend Developer", "Backend Developer", "React Developer", "Angular Developer",
    "Vue.js Developer", "Node.js Developer", "Django Developer", "Flask Developer",
    "Software Engineer", "Senior Software Engineer", "Staff Engineer", "Principal Engineer",
    "Data Scientist", "Data Analyst", "Data Engineer", "Machine Learning Engineer",
    "AI Engineer", "Deep Learning Engineer", "NLP Engineer", "Computer Vision Engineer",
    "DevOps Engineer", "SRE Engineer", "Cloud Engineer", "AWS Solutions Architect",
    "Platform Engineer", "Infrastructure Engineer", "Kubernetes Engineer",
    "Cybersecurity Analyst", "Security Engineer", "Penetration Tester",
    "Mobile Developer", "iOS Developer", "Android Developer", "Flutter Developer",
    "React Native Developer", "QA Engineer", "Test Automation Engineer", "SDET",
    "Product Manager", "Project Manager", "Scrum Master", "Agile Coach",
    "Business Analyst", "Systems Analyst", "Solutions Architect", "Technical Architect",
    "UI/UX Designer", "Product Designer", "Graphic Designer", "Web Designer",
    "Technical Writer", "Content Writer", "Copywriter",
    "Marketing Manager", "Digital Marketing Specialist", "SEO Specialist",
    "Sales Executive", "Account Manager", "Customer Success Manager",
    "HR Manager", "Recruiter", "Talent Acquisition Specialist",
    "Finance Analyst", "Accountant", "Investment Analyst",
    "Operations Manager", "Supply Chain Analyst", "Logistics Coordinator",
    "Research Scientist", "Biotech Engineer", "Mechanical Engineer",
    "Electrical Engineer", "Civil Engineer", "Chemical Engineer",
    "Fresher", "Intern", "Graduate Trainee", "Entry Level",
]

col1, col2 = st.columns([2, 1])
with col1:
    job_role = st.text_input(
        "🎯 Target Job Role (optional)",
        placeholder="Start typing... e.g. Python Dev..."
    )
with col2:
    st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)
    go = st.button("🚀 Analyze Resume", use_container_width=True)

# Inject datalist for autocomplete
_datalist_options = "\n".join([f'<option value="{role}">' for role in JOB_ROLES])
st.markdown(f"""
<datalist id="jobRoleList">
{_datalist_options}
</datalist>
<script>
// Attach datalist to the Streamlit text input for autocomplete
function attachDatalist() {{
    const inputs = document.querySelectorAll('input[type="text"]');
    inputs.forEach(input => {{
        if (input.getAttribute('placeholder') && 
            input.getAttribute('placeholder').includes('Start typing')) {{
            if (!input.getAttribute('list')) {{
                input.setAttribute('list', 'jobRoleList');
                input.setAttribute('autocomplete', 'on');
            }}
        }}
    }});
}}
// Run on load and observe for dynamic re-renders
attachDatalist();
const observer = new MutationObserver(() => {{ attachDatalist(); }});
observer.observe(document.body, {{ childList: true, subtree: true }});
</script>
""", unsafe_allow_html=True)


# ─── Analysis ───
if go and uploaded_file:
    GROQ_KEY = os.getenv("GROQ_API_KEY")
    OR_KEY = os.getenv("OPENAI_API_KEY")

    if GROQ_KEY:
        api_key, base_url, model, provider = GROQ_KEY, "https://api.groq.com/openai/v1", "llama-3.3-70b-versatile", "Groq"
    elif OR_KEY:
        api_key, base_url, model, provider = OR_KEY, "https://openrouter.ai/api/v1", "google/gemma-3n-e2b-it:free", "OpenRouter"
    else:
        st.error("⚠️ No API key found. Set `GROQ_API_KEY` or `OPENAI_API_KEY` in `.env`.")
        st.stop()

    try:
        with st.spinner("📖 Reading your resume..."):
            content = extract_text_from_upload(uploaded_file)

        if not content.strip():
            st.error("📭 The file appears empty. Please upload a valid resume.")
            st.stop()

        with st.spinner("🧠 Hang on buddy... Analyzing your resume!"):
            client = OpenAI(api_key=api_key, base_url=base_url)
            prompt = build_prompt(content, job_role, analysis_mode)

            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert resume reviewer and ATS specialist. Always respond with valid JSON only. No markdown, no extra text, no code fences. Be very specific and cite examples from the resume."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=4000
            )
            raw = resp.choices[0].message.content
            data = parse_json(raw)

        st.markdown("---")

        if data:
            ats = data.get("ats_score", 0)
            overall = data.get("overall_score", 0)
            verdict = data.get("ats_verdict", "")
            g = grade(overall)
            career_level = data.get("career_level", "")
            exp_years = data.get("estimated_experience_years", "")
            readability = data.get("readability_score", 0)
            ranking = data.get("competitive_ranking", "")

            # Mode Header Badge
            mode_labels = {
                "🎯 Full Analysis": ("🎯", "Full Analysis Report", "Complete deep-dive into every aspect"),
                "⚡ ATS Optimization": ("⚡", "ATS Optimization Report", "How ATS systems will parse your resume"),
                "📋 Quick Review": ("📋", "Quick Review", "Fast overview with key takeaways"),
            }
            m_icon, m_title, m_desc = mode_labels.get(analysis_mode, ("📋", "Report", ""))
            st.markdown(f"""
            <div class="card" style="text-align:center; border-left:4px solid var(--accent);">
                <div style="font-size:1.5rem; margin-bottom:0.3rem;">{m_icon}</div>
                <div style="font-size:1.15rem; font-weight:800; color:var(--text); margin-bottom:0.2rem;">{m_title}</div>
                <div style="font-size:0.85rem; color:var(--text-muted);">{m_desc}</div>
            </div>
            """, unsafe_allow_html=True)

            # ═══ QUICK REVIEW MODE ═══
            if analysis_mode == "📋 Quick Review":
                render_score(ats, overall, verdict, g)
                summary = data.get("summary", "")
                if summary:
                    st.markdown(f"""
                    <div class="card">
                        <div class="card-head"><div class="card-dot dot-blue">💬</div><span class="card-title">Quick Verdict</span></div>
                        <p style="color:var(--text-secondary); line-height:1.7; font-size:0.95rem; margin:0; font-style:italic;">"{summary}"</p>
                    </div>
                    """, unsafe_allow_html=True)
                scores = data.get("scores", {})
                if scores:
                    st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-purple">📊</div><span class="card-title">Quick Scores</span></div>""", unsafe_allow_html=True)
                    render_bars(scores)
                    st.markdown("</div>", unsafe_allow_html=True)
                strengths = data.get("strengths", [])
                weaknesses = data.get("weaknesses", [])
                if strengths or weaknesses:
                    cs, cw = st.columns(2)
                    with cs:
                        if strengths:
                            st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-green">👍</div><span class="card-title">What's Working</span></div>""", unsafe_allow_html=True)
                            render_items(strengths, "s-green", "✓")
                            st.markdown("</div>", unsafe_allow_html=True)
                    with cw:
                        if weaknesses:
                            st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-red">👎</div><span class="card-title">Fix These</span></div>""", unsafe_allow_html=True)
                            render_items(weaknesses, "s-red", "✗")
                            st.markdown("</div>", unsafe_allow_html=True)
                quick_wins = data.get("quick_wins", [])
                if quick_wins:
                    st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-green">⚡</div><span class="card-title">Do These Right Now</span></div>""", unsafe_allow_html=True)
                    render_items(quick_wins, "s-green", "🎯")
                    st.markdown("</div>", unsafe_allow_html=True)

            # ═══ ATS OPTIMIZATION MODE ═══
            elif analysis_mode == "⚡ ATS Optimization":
                render_score(ats, overall, verdict, g)
                summary = data.get("summary", "")
                if summary:
                    ats_color = color_class(ats)
                    st.markdown(f"""
                    <div class="card" style="border-left:4px solid var(--{ats_color});">
                        <div class="card-head"><div class="card-dot dot-yellow">🤖</div><span class="card-title">ATS Compatibility Assessment</span></div>
                        <p style="color:var(--text-secondary); line-height:1.7; font-size:0.92rem; margin:0;">{summary}</p>
                    </div>
                    """, unsafe_allow_html=True)
                scores = data.get("scores", {})
                if scores:
                    st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-orange">📊</div><span class="card-title">ATS Parsing Breakdown</span></div>""", unsafe_allow_html=True)
                    render_bars(scores)
                    st.markdown("</div>", unsafe_allow_html=True)
                section_review = data.get("section_review", [])
                if section_review:
                    st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-blue">🔍</div><span class="card-title">ATS Section Parsing Results</span></div>""", unsafe_allow_html=True)
                    for sec in section_review:
                        s_name, s_score, s_verdict = sec.get("section", ""), sec.get("score", 0), sec.get("verdict", "")
                        sc = color_class(s_score)
                        status = "✅ PASS" if s_score >= 70 else ("⚠️ WARNING" if s_score >= 50 else "❌ FAIL")
                        st.markdown(f'<div style="padding:0.7rem 0.9rem; margin-bottom:0.5rem; background:var(--bg); border:1px solid var(--border); border-radius:var(--radius-xs);"><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;"><span style="font-weight:600; font-size:0.88rem; color:var(--text);">{s_name}</span><span style="font-weight:700; font-size:0.8rem; color:var(--{sc});">{status} · {s_score}/100</span></div><div style="font-size:0.82rem; color:var(--text-secondary); line-height:1.55;">{s_verdict}</div></div>', unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                found_kw = data.get("found_keywords", [])
                missing_kw = data.get("missing_keywords", [])
                if found_kw or missing_kw:
                    total = len(found_kw) + len(missing_kw)
                    match_pct = round(len(found_kw) / total * 100) if total > 0 else 0
                    st.markdown(f'<div class="card"><div class="card-head"><div class="card-dot dot-yellow">🔑</div><div><div class="card-title">Keyword Match Analysis</div><div class="card-desc">Found {len(found_kw)} of {total} keywords · {match_pct}% match rate</div></div></div>', unsafe_allow_html=True)
                    render_tags(found_kw, missing_kw)
                    st.markdown("</div>", unsafe_allow_html=True)
                fmt_issues = data.get("formatting_issues", [])
                if fmt_issues:
                    st.markdown("""<div class="card" style="border-left:4px solid var(--red);"><div class="card-head"><div class="card-dot dot-red">🚨</div><span class="card-title">ATS Parsing Blockers</span></div>""", unsafe_allow_html=True)
                    render_items(fmt_issues, "s-red", "⛔")
                    st.markdown("</div>", unsafe_allow_html=True)
                missing_secs = data.get("missing_sections", [])
                if missing_secs:
                    st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-yellow">📌</div><span class="card-title">Missing ATS-Required Sections</span></div>""", unsafe_allow_html=True)
                    render_items(missing_secs, "s-yellow", "➕")
                    st.markdown("</div>", unsafe_allow_html=True)
                rewrites = data.get("bullet_rewrites", [])
                if rewrites:
                    st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-blue">✏️</div><span class="card-title">ATS-Optimized Rewrites</span></div>""", unsafe_allow_html=True)
                    for rw in rewrites:
                        orig, rewritten = rw.get("original", ""), rw.get("rewritten", "")
                        st.markdown(f'<div style="margin-bottom:0.7rem; padding:0.8rem; background:var(--bg); border:1px solid var(--border); border-radius:var(--radius-xs);"><div style="font-size:0.8rem; font-weight:600; color:var(--red); margin-bottom:0.3rem;">❌ ATS Unfriendly</div><div style="font-size:0.85rem; color:var(--text-secondary); line-height:1.55; margin-bottom:0.6rem; padding-left:0.5rem; border-left:2px solid var(--red-border);">{orig}</div><div style="font-size:0.8rem; font-weight:600; color:var(--green); margin-bottom:0.3rem;">✅ ATS Optimized</div><div style="font-size:0.85rem; color:var(--text); line-height:1.55; padding-left:0.5rem; border-left:2px solid var(--green-border);">{rewritten}</div></div>', unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                ats_tips = data.get("ats_tips", [])
                if ats_tips:
                    st.markdown("""<div class="card" style="border-left:4px solid var(--green);"><div class="card-head"><div class="card-dot dot-green">✅</div><span class="card-title">ATS Fix Checklist</span></div>""", unsafe_allow_html=True)
                    render_items(ats_tips, "s-green", "☐")
                    st.markdown("</div>", unsafe_allow_html=True)
                quick_wins = data.get("quick_wins", [])
                if quick_wins:
                    st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-blue">⚡</div><span class="card-title">Quick ATS Fixes</span></div>""", unsafe_allow_html=True)
                    render_items(quick_wins, "s-blue", "🎯")
                    st.markdown("</div>", unsafe_allow_html=True)

            # ═══ FULL ANALYSIS MODE ═══
            else:
                render_score(ats, overall, verdict, g)
                if career_level or exp_years or ranking:
                    r_color = color_class(readability)
                    st.markdown(f"""
                    <div class="card">
                        <div class="card-head"><div class="card-dot dot-purple">👤</div><span class="card-title">Candidate Profile</span></div>
                        <div style="display:flex; gap:0.8rem; flex-wrap:wrap;">
                            <div style="flex:1; min-width:140px; padding:0.7rem; background:var(--purple-light); border:1px solid var(--purple-border); border-radius:var(--radius-xs); text-align:center;">
                                <div style="font-size:0.72rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0.25rem;">Career Level</div>
                                <div style="font-size:0.95rem; font-weight:700; color:var(--purple);">{career_level}</div>
                            </div>
                            <div style="flex:1; min-width:140px; padding:0.7rem; background:var(--blue-light); border:1px solid var(--blue-border); border-radius:var(--radius-xs); text-align:center;">
                                <div style="font-size:0.72rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0.25rem;">Experience</div>
                                <div style="font-size:0.95rem; font-weight:700; color:var(--blue);">{exp_years}</div>
                            </div>
                            <div style="flex:1; min-width:140px; padding:0.7rem; background:var(--accent-light); border:1px solid #f5cfc0; border-radius:var(--radius-xs); text-align:center;">
                                <div style="font-size:0.72rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0.25rem;">Competitive Rank</div>
                                <div style="font-size:0.95rem; font-weight:700; color:var(--accent);">{ranking}</div>
                            </div>
                            <div style="flex:1; min-width:140px; padding:0.7rem; background:var(--{'green-light' if readability >= 70 else ('yellow-light' if readability >= 50 else 'red-light')}); border:1px solid var(--{r_color}-border); border-radius:var(--radius-xs); text-align:center;">
                                <div style="font-size:0.72rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0.25rem;">Readability</div>
                                <div style="font-size:0.95rem; font-weight:700; color:var(--{r_color});">{readability}/100</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Summary
                summary = data.get("summary", "")
                if summary:
                    st.markdown(f'<div class="card"><div class="card-head"><div class="card-dot dot-blue">📋</div><span class="card-title">Executive Summary</span></div><p style="color:var(--text-secondary); line-height:1.7; font-size:0.92rem; margin:0;">{summary}</p></div>', unsafe_allow_html=True)
                # Category Scores
                scores = data.get("scores", {})
                if scores:
                    st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-purple">📊</div><span class="card-title">Category Breakdown</span></div>""", unsafe_allow_html=True)
                    render_bars(scores)
                    st.markdown("</div>", unsafe_allow_html=True)
                # Section-by-Section
                section_review = data.get("section_review", [])
                if section_review:
                    st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-orange">📑</div><span class="card-title">Section-by-Section Review</span></div>""", unsafe_allow_html=True)
                    for sec in section_review:
                        s_name, s_score, s_verdict = sec.get("section", ""), sec.get("score", 0), sec.get("verdict", "")
                        sc = color_class(s_score)
                        st.markdown(f'<div style="padding:0.7rem 0.9rem; margin-bottom:0.5rem; background:var(--bg); border:1px solid var(--border); border-radius:var(--radius-xs);"><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;"><span style="font-weight:600; font-size:0.88rem; color:var(--text);">{s_name}</span><span style="font-weight:700; font-size:0.85rem; color:var(--{sc});">{s_score}/100</span></div><div style="font-size:0.82rem; color:var(--text-secondary); line-height:1.55;">{s_verdict}</div></div>', unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                # Strengths & Weaknesses
                strengths = data.get("strengths", [])
                weaknesses = data.get("weaknesses", [])
                if strengths or weaknesses:
                    cs, cw = st.columns(2)
                    with cs:
                        if strengths:
                            st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-green">✅</div><span class="card-title">Strengths</span></div>""", unsafe_allow_html=True)
                            render_items(strengths, "s-green", "💪")
                            st.markdown("</div>", unsafe_allow_html=True)
                    with cw:
                        if weaknesses:
                            st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-red">⚠️</div><span class="card-title">Needs Improvement</span></div>""", unsafe_allow_html=True)
                            render_items(weaknesses, "s-red", "🔴")
                            st.markdown("</div>", unsafe_allow_html=True)
                # Bullet Rewrites
                rewrites = data.get("bullet_rewrites", [])
                if rewrites:
                    st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-blue">✏️</div><span class="card-title">Bullet Point Rewrites</span></div>""", unsafe_allow_html=True)
                    for rw in rewrites:
                        orig, rewritten = rw.get("original", ""), rw.get("rewritten", "")
                        st.markdown(f'<div style="margin-bottom:0.7rem; padding:0.8rem; background:var(--bg); border:1px solid var(--border); border-radius:var(--radius-xs);"><div style="font-size:0.8rem; font-weight:600; color:var(--red); margin-bottom:0.3rem;">❌ Before</div><div style="font-size:0.85rem; color:var(--text-secondary); line-height:1.55; margin-bottom:0.6rem; padding-left:0.5rem; border-left:2px solid var(--red-border);">{orig}</div><div style="font-size:0.8rem; font-weight:600; color:var(--green); margin-bottom:0.3rem;">✅ After</div><div style="font-size:0.85rem; color:var(--text); line-height:1.55; padding-left:0.5rem; border-left:2px solid var(--green-border);">{rewritten}</div></div>', unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                # Action Verb Analysis
                verbs = data.get("action_verb_analysis", {})
                if verbs and (verbs.get("strong_verbs_found") or verbs.get("weak_verbs_found")):
                    st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-purple">💬</div><span class="card-title">Action Verb Analysis</span></div>""", unsafe_allow_html=True)
                    strong, weak, suggested = verbs.get("strong_verbs_found", []), verbs.get("weak_verbs_found", []), verbs.get("suggested_power_verbs", [])
                    html = '<div style="margin-bottom:0.6rem;"><span style="font-size:0.8rem; font-weight:600; color:var(--green);">Strong verbs:</span></div><div class="tags">'
                    for v in strong: html += f'<span class="tag t-found">{v}</span>'
                    html += '</div>'
                    if weak:
                        html += '<div style="margin:0.7rem 0 0.4rem;"><span style="font-size:0.8rem; font-weight:600; color:var(--red);">Weak verbs:</span></div><div class="tags">'
                        for v in weak: html += f'<span class="tag" style="background:var(--red-light); border:1px solid var(--red-border); color:var(--red);">{v}</span>'
                        html += '</div>'
                    if suggested:
                        html += '<div style="margin:0.7rem 0 0.4rem;"><span style="font-size:0.8rem; font-weight:600; color:var(--purple);">Power verbs:</span></div><div class="tags">'
                        for v in suggested: html += f'<span class="tag" style="background:var(--purple-light); border:1px solid var(--purple-border); color:var(--purple);">{v}</span>'
                        html += '</div>'
                    st.markdown(html, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                # Keywords
                found_kw, missing_kw = data.get("found_keywords", []), data.get("missing_keywords", [])
                if found_kw or missing_kw:
                    st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-yellow">🔑</div><span class="card-title">Keyword Analysis</span></div>""", unsafe_allow_html=True)
                    render_tags(found_kw, missing_kw)
                    st.markdown("</div>", unsafe_allow_html=True)
                # Formatting + Missing
                fmt_issues, missing_secs = data.get("formatting_issues", []), data.get("missing_sections", [])
                if fmt_issues or missing_secs:
                    fc, mc = st.columns(2)
                    with fc:
                        if fmt_issues:
                            st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-yellow">🎨</div><span class="card-title">Formatting Issues</span></div>""", unsafe_allow_html=True)
                            render_items(fmt_issues, "s-yellow", "⚡")
                            st.markdown("</div>", unsafe_allow_html=True)
                    with mc:
                        if missing_secs:
                            st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-red">📌</div><span class="card-title">Missing Sections</span></div>""", unsafe_allow_html=True)
                            render_items(missing_secs, "s-red", "➕")
                            st.markdown("</div>", unsafe_allow_html=True)
                # Quick Wins + Improvements + ATS Tips
                quick_wins = data.get("quick_wins", [])
                if quick_wins:
                    st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-green">⚡</div><span class="card-title">Quick Wins (5-min fixes)</span></div>""", unsafe_allow_html=True)
                    render_items(quick_wins, "s-green", "🎯")
                    st.markdown("</div>", unsafe_allow_html=True)
                improvements = data.get("improvements", [])
                if improvements:
                    st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-blue">🚀</div><span class="card-title">Actionable Improvements</span></div>""", unsafe_allow_html=True)
                    render_items(improvements, "s-blue", "→")
                    st.markdown("</div>", unsafe_allow_html=True)
                ats_tips = data.get("ats_tips", [])
                if ats_tips:
                    st.markdown("""<div class="card"><div class="card-head"><div class="card-dot dot-yellow">🤖</div><span class="card-title">ATS Optimization Tips</span></div>""", unsafe_allow_html=True)
                    render_items(ats_tips, "s-yellow", "💡")
                    st.markdown("</div>", unsafe_allow_html=True)

            # ── Download Report (all modes) ──
            st.markdown("---")
            lines = [
                f"AI RESUME ANALYSIS — {analysis_mode}", "=" * 55,
                f"ATS Score: {ats}/100", f"Overall: {overall}/100 (Grade: {g})",
                f"Readability: {readability}/100", f"Career Level: {career_level}",
                f"Experience: {exp_years}", f"Ranking: {ranking}",
                f"Mode: {analysis_mode}", f"Target Role: {job_role or 'General'}",
                "", "SUMMARY", "-" * 40, data.get("summary", ""),
                "", "ATS VERDICT", "-" * 40, data.get("ats_verdict", ""),
                "", "SCORES", "-" * 40
            ]
            for k, v in data.get("scores", {}).items(): lines.append(f"  {k}: {v}/100")
            for sec in data.get("section_review", []): lines.append(f"  [{sec.get('score',0)}] {sec.get('section','')}: {sec.get('verdict','')}")
            lines += ["", "STRENGTHS", "-" * 40]
            for s in data.get("strengths", []): lines.append(f"  ✓ {s}")
            lines += ["", "WEAKNESSES", "-" * 40]
            for w in data.get("weaknesses", []): lines.append(f"  ✗ {w}")
            for rw in data.get("bullet_rewrites", []):
                lines += [f"  Before: {rw.get('original','')}", f"  After:  {rw.get('rewritten','')}", ""]
            for k in data.get("found_keywords", []): lines.append(f"  ✓ {k}")
            for k in data.get("missing_keywords", []): lines.append(f"  ✗ {k}")
            for t in data.get("ats_tips", []): lines.append(f"  → {t}")
            for qw in data.get("quick_wins", []): lines.append(f"  ⚡ {qw}")
            for i, imp in enumerate(data.get("improvements", []), 1): lines.append(f"  {i}. {imp}")
            c1, _ = st.columns([1, 2])
            with c1:
                st.download_button("📥 Download Report", "\n".join(lines),
                                   "resume_analysis_report.txt", "text/plain", use_container_width=True)

            # Save to history
            save_to_history(user_email, {
                "timestamp": datetime.now().strftime("%b %d, %Y %I:%M %p"),
                "file_name": uploaded_file.name,
                "job_role": job_role or "General",
                "mode": analysis_mode,
                "ats_score": ats,
                "overall_score": overall,
                "grade": g,
            })

        else:
            st.markdown("""<div class="card"><div class="card-head">
                <div class="card-dot dot-orange">📋</div>
                <span class="card-title">Analysis Results</span>
            </div></div>""", unsafe_allow_html=True)
            st.markdown(raw)

    except Exception as e:
        msg = str(e)
        if "401" in msg or "Unauthorized" in msg or "User not found" in msg:
            st.error("🔑 **Auth Error**: Your API key may be invalid or expired. Check `.env`.")
        elif "429" in msg:
            st.warning("⏳ **Rate Limited**: Too many requests. Wait and retry.")
        elif "model" in msg.lower():
            st.error("🤖 **Model Error**: AI model unavailable. Try again shortly.")
        else:
            st.error(f"❌ **Error**: {msg}")
        with st.expander("🔧 Troubleshooting"):
            st.markdown("""
            1. **Check API Key**: Verify your key in `.env`
            2. **Groq**: Free key at [console.groq.com](https://console.groq.com)
            3. **OpenRouter**: Check credits at [openrouter.ai](https://openrouter.ai)
            4. **File**: Ensure your resume is a valid PDF or TXT
            """)

elif go and not uploaded_file:
    st.warning("📎 Please upload a resume file first!")


# ─── Footer ───
st.markdown("""
<div class="footer">
    Built with ❤️ using Streamlit & AI · 
    <a href="https://github.com" target="_blank">GitHub</a>
</div>
""", unsafe_allow_html=True)
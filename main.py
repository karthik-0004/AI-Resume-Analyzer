import streamlit as st
import PyPDF2
import io
import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
import PyPDF2

load_dotenv()

# ─── Page Config ───
st.set_page_config(
    page_title="AI Resume Critiquer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Warm Light Theme CSS ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&display=swap');

:root {
    --bg: #D1D5DB;
    --bg-card: #FFFFFF;
    --bg-warm: #E5E7EB;
    --bg-sidebar: #D1D5DB;
    
    --accent: #171717;
    --accent-light: rgba(0, 0, 0, 0.05);
    --accent-hover: #000000;
    --accent-gradient: linear-gradient(to right, #18181b, #71717a);
    
    --green: #2ecc71;
    --yellow: #f1c40f;
    --red: #e74c3c;
    --blue: #3498db;
    --purple: #9b59b6;
    
    --text: #171717;
    --text-secondary: #52525B;
    --text-muted: #71717A;
    
    --border: #E4E4E7;
    --border-dark: #D4D4D8;
}

html, body, .stApp {
    font-family: 'Geist', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text) !important;
    background: var(--bg) !important;
    letter-spacing: -0.01em;
}

#MainMenu, footer, header {visibility: hidden;}

::-webkit-scrollbar {width: 4px; height: 4px;}
::-webkit-scrollbar-track {background: transparent;}
::-webkit-scrollbar-thumb {background: #171717; border-radius: 4px;}

.hero { text-align: center; padding: 4rem 1rem 3rem; }
.hero-badge {
    display: inline-flex; align-items: center; padding: 4px 12px;
    background: #FFFFFF; border: 2px solid #000000;
    border-radius: 999px; font-size: 0.75rem; font-weight: 500; color: #171717;
    margin-bottom: 1.5rem; box-shadow: 2px 2px 0px #000000;
}
.hero-title {
    font-size: 3rem; font-weight: 600; color: var(--text);
    margin-bottom: 1rem; line-height: 1.1; letter-spacing: -0.03em;
}
.hero-title span {
    background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1.1rem; color: var(--text-secondary); max-width: 500px;
    margin: 0 auto; font-weight: 400;
}

.card {
    background: var(--bg-card); border: 2px solid #000000; border-radius: 8px;
    padding: 1.5rem; margin-bottom: 1rem; transition: all 0.2s ease;
    box-shadow: 4px 4px 0px #000000;
}
.card:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0px #000000; }
.card-head {
    display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;
    padding-bottom: 0.75rem; border-bottom: 2px solid #000000;
}
.card-title { font-size: 0.95rem; font-weight: 600; color: var(--text); text-transform: uppercase; letter-spacing: 1px; }
.card-desc { font-size: 0.8rem; color: var(--text-muted); }

.score-section { display: flex; align-items: center; justify-content: center; gap: 3rem; padding: 1rem 0; flex-wrap: wrap; }
.score-circle { position: relative; width: 140px; height: 140px; }
.score-circle svg { transform: rotate(-90deg); }
.ring-bg { fill: none; stroke: var(--border); stroke-width: 6; }
.ring-fill { fill: none; stroke-width: 6; stroke-linecap: round; stroke-dasharray: 408; transition: stroke-dashoffset 1.5s ease; filter: drop-shadow(0 0 4px currentColor); }
.ring-green {stroke: var(--green);} .ring-yellow {stroke: var(--yellow);} .ring-red {stroke: var(--red);}
.score-num { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; }
.score-big { font-size: 2.5rem; font-weight: 600; line-height: 1; color: var(--text); }
.score-tag { font-size: 0.65rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }
.score-details { display: flex; flex-direction: column; gap: 0.5rem; }
.score-detail-row { display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0.75rem; background: var(--bg-warm); border-radius: 4px; border: 2px solid #000000; min-width: 180px; box-shadow: 2px 2px 0px #000000; }
.score-detail-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; box-shadow: 0 0 5px currentColor; }
.bg-green {background: var(--green); color: var(--green);} .bg-yellow {background: var(--yellow); color: var(--yellow);} .bg-red {background: var(--red); color: var(--red);} .bg-blue {background: var(--accent); color: var(--accent);}
.score-detail-label { font-size: 0.85rem; color: var(--text-secondary); font-weight: 600; flex-grow: 1; text-transform: uppercase; }
.score-detail-val { font-size: 0.85rem; font-weight: 600; color: var(--text); }
.c-green {color: var(--green);} .c-yellow {color: var(--yellow);} .c-red {color: var(--red);} .c-blue {color: var(--blue);}

.bar-wrap {margin-bottom: 1rem;} .bar-top { display: flex; justify-content: space-between; margin-bottom: 0.4rem; } 
.bar-name {font-size: 0.85rem; font-weight: 600; color: var(--text-secondary); text-transform: uppercase;} .bar-val {font-size: 0.85rem; font-weight: 600;} 
.bar-track { width: 100%; height: 6px; background: rgba(0,0,0,0.1); border-radius: 0px; border: 1px solid #000000; overflow: hidden; } 
.bar-fill { height: 100%; border-radius: 0px; transition: width 1s ease; }
.fill-green {background: var(--green); color: var(--green);} .fill-yellow {background: var(--yellow); color: var(--yellow);} .fill-red {background: var(--red); color: var(--red);}

.items {list-style: none; padding: 0; margin: 0;}
.items li { padding: 0.75rem 1rem; margin-bottom: 0.5rem; border-radius: 4px; font-size: 0.85rem; font-weight: 500; line-height: 1.5; color: var(--text); display: flex; align-items: flex-start; gap: 0.75rem; background: var(--bg-card); border: 2px solid #000000; box-shadow: 2px 2px 0px #000000; }
.tags {display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem;}
.tag { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600; background: #FFFFFF; border: 2px solid #000000; box-shadow: 2px 2px 0px #000000; color: var(--text); }
.t-found {background: #e6f9ec;}
.t-miss {background: #fdf5ce;}

.stButton > button { background: var(--text) !important; color: var(--bg-card) !important; border: 2px solid #000000 !important; border-radius: 4px !important; font-weight: 600 !important; font-family: 'Geist', sans-serif !important; transition: all 0.1s !important; box-shadow: 4px 4px 0px #000000 !important; }
.stButton > button:hover { transform: translate(2px, 2px) !important; box-shadow: 2px 2px 0px #000000 !important; }
.stButton > button:active { transform: translate(4px, 4px) !important; box-shadow: 0px 0px 0px #000000 !important; }

.stTextInput input, .stSelectbox > div > div { background: var(--bg-card) !important; border: 2px solid #000000 !important; border-radius: 4px !important; color: var(--text) !important; font-family: 'Geist', sans-serif !important; font-weight: 500 !important; box-shadow: 3px 3px 0px #000000 !important; transition: all 0.1s; }
.stTextInput input:focus, .stSelectbox > div > div:focus { border-color: #000000 !important; box-shadow: 1px 1px 0px #000000 !important; transform: translate(2px, 2px); }
.stTextInput > div > div { background: transparent !important; border: none !important; }
.stFileUploader > div { background: var(--bg-card) !important; border: 2px dashed #000000 !important; border-radius: 8px !important; box-shadow: 4px 4px 0px #000000 !important; transition: all 0.1s; }
.stFileUploader > div:hover { background: #F3F4F6 !important; transform: translate(1px, 1px); box-shadow: 3px 3px 0px #000000 !important; }

section[data-testid="stSidebar"] { background: var(--bg-sidebar) !important; border-right: 2px solid #000000 !important; }
.stDownloadButton > button { background: var(--bg-card) !important; color: var(--text) !important; border: 2px solid #000000 !important; font-weight: 600 !important; border-radius: 4px !important; box-shadow: 3px 3px 0px #000000 !important; }
.stDownloadButton > button:hover { transform: translate(2px, 2px) !important; box-shadow: 1px 1px 0px #000000 !important; }
hr { border: none; height: 2px; background: #000000; margin: 2.5rem 0; }
.streamlit-expanderHeader { background: var(--bg-warm) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; font-weight: 500 !important; }
.footer { text-align: center; padding: 2rem 0 1rem; color: var(--text-muted); font-size: 0.8rem; }
.footer a {color: var(--text); text-decoration: none;}

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

    if mode == "Full Analysis":
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

    elif mode == "ATS Optimization":
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


# ─── Sidebar ───
with st.sidebar:
    analysis_mode = st.selectbox(
        "Analysis Mode",
        ["Full Analysis", "ATS Optimization", "Quick Review"],
        help="Choose how deeply you want your resume analyzed."
    )

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



# ─── Process Overview ───
st.markdown('''
<div style="padding: 2rem 1rem 1rem; max-width: 900px; margin: 0 auto;">
    <div style="font-size: 0.85rem; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2rem; text-align: center;">Process Overview</div>
    <div style="display: flex; gap: 2rem; justify-content: space-between; align-items: flex-start; text-align: center;">
        <div style="flex: 1; padding: 1.5rem; background: var(--bg-card); border: 2px solid #000000; border-radius: 8px; box-shadow: 4px 4px 0px #000000; transition: all 0.2s;">
            <div style="width: 32px; height: 32px; border-radius: 4px; border: 2px solid #000000; background: #000000; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: 700; margin: 0 auto 1rem; box-shadow: 2px 2px 0px #000000;">1</div>
            <div style="font-weight: 700; font-size: 1.05rem; color: var(--text); margin-bottom: 0.5rem; text-transform: uppercase;">Document Intake</div>
            <div style="color: var(--text-secondary); font-size: 0.9rem; line-height: 1.5; font-weight: 500;">Drop your PDF or TXT resume and supply a target role. Data is securely processed.</div>
        </div>
        <div style="flex: 1; padding: 1.5rem; background: var(--bg-card); border: 2px solid #000000; border-radius: 8px; box-shadow: 4px 4px 0px #000000; transition: all 0.2s;">
            <div style="width: 32px; height: 32px; border-radius: 4px; border: 2px solid #000000; background: #FFFFFF; color: #000000; display: flex; align-items: center; justify-content: center; font-weight: 700; margin: 0 auto 1rem; box-shadow: 2px 2px 0px #000000;">2</div>
            <div style="font-weight: 700; font-size: 1.05rem; color: var(--text); margin-bottom: 0.5rem; text-transform: uppercase;">Deep AI Audit</div>
            <div style="color: var(--text-secondary); font-size: 0.9rem; line-height: 1.5; font-weight: 500;">Cross-referenced against 30+ precise ATS parameters and industry benchmarks.</div>
        </div>
        <div style="flex: 1; padding: 1.5rem; background: var(--bg-card); border: 2px solid #000000; border-radius: 8px; box-shadow: 4px 4px 0px #000000; transition: all 0.2s;">
            <div style="width: 32px; height: 32px; border-radius: 4px; border: 2px solid #000000; background: #FFFFFF; color: #000000; display: flex; align-items: center; justify-content: center; font-weight: 700; margin: 0 auto 1rem; box-shadow: 2px 2px 0px #000000;">3</div>
            <div style="font-weight: 700; font-size: 1.05rem; color: var(--text); margin-bottom: 0.5rem; text-transform: uppercase;">Actionable Feedback</div>
            <div style="color: var(--text-secondary); font-size: 0.9rem; line-height: 1.5; font-weight: 500;">Get optimized formatting tips, line-by-line rewrites, and instant technical insight.</div>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# ─── Hero ───
st.markdown('''
<div class="hero" style="padding: 2rem 1rem 3rem;">
    <div class="hero-title">Elevate Your <span>Career</span></div>
    <div class="hero-sub" style="margin-top: 1rem;">
        Upload your resume and get actionable insights, ATS scoring, and targeted feedback to land your next role.
    </div>
</div>
''', unsafe_allow_html=True)

# ─── Upload Centered ───
_, center_col, _ = st.columns([1, 2, 1])

with center_col:
    st.markdown('''
    <div class="card" style="text-align: center; margin-bottom: 1.5rem; border: 1px dashed var(--border-dark);">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📄</div>
        <div style="font-weight: 600; font-size: 1.1rem; color: var(--text);">Upload Your Resume</div>
        <div style="font-size: 0.9rem; color: var(--text-muted);">PDF or TXT · Max 200 MB</div>
    </div>
    ''', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload", type=["pdf", "txt"], label_visibility="collapsed")

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
            "Target Job Role (optional)",
            placeholder="Start typing... e.g. Python Dev..."
        )
    with col2:
        st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)
        go = st.button("Analyze Resume", use_container_width=True)

# Inject datalist for autocomplete
_datalist_options = "\n".join([f'<option value="{role}">' for role in JOB_ROLES])
st.markdown(f'''
<datalist id="jobRoleList">
{_datalist_options}
</datalist>
<script>
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
attachDatalist();
const observer = new MutationObserver(() => {{ attachDatalist(); }});
observer.observe(document.body, {{ childList: true, subtree: true }});
</script>
''', unsafe_allow_html=True)


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
        with st.spinner("Reading document..."):
            content = extract_text_from_upload(uploaded_file)

        if not content.strip():
            st.error("📭 The file appears empty. Please upload a valid resume.")
            st.stop()

        with st.spinner("Analyzing document structure and metrics..."):
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
                "Full Analysis": ("📈", "Full Analysis Report", "Complete deep-dive into every aspect"),
                "ATS Optimization": ("⚙️", "ATS Optimization Report", "How ATS systems will parse your resume"),
                "Quick Review": ("⏱️", "Quick Review", "Fast overview with key takeaways"),
            }
            m_icon, m_title, m_desc = mode_labels.get(analysis_mode, ("", "Report", ""))
            st.markdown(f"""
            <div class="card" style="text-align:center; border-left:4px solid var(--accent);">
                <div style="font-size:1.5rem; margin-bottom:0.3rem;">{m_icon}</div>
                <div style="font-size:1.15rem; font-weight:800; color:var(--text); margin-bottom:0.2rem;">{m_title}</div>
                <div style="font-size:0.85rem; color:var(--text-muted);">{m_desc}</div>
            </div>
            """, unsafe_allow_html=True)

            # ═══ QUICK REVIEW MODE ═══
            if analysis_mode == "Quick Review":
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
            elif analysis_mode == "ATS Optimization":
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
    st.warning("Please upload a resume file first.")


# ─── Footer ───
st.markdown("""
<div class="footer">
    Built with ❤️ using Streamlit & AI · 
    <a href="https://github.com" target="_blank">GitHub</a>
</div>
""", unsafe_allow_html=True)

import sys

with open('c:/Users/3541/Desktop/resume_crtique/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace CSS
css_start = 'st.markdown("""\n<style>\n'
css_end = '</style>\n""", unsafe_allow_html=True)'
if css_start in text and css_end in text:
    head, rest = text.split(css_start, 1)
    old_css, tail = rest.split(css_end, 1)
    
    new_css = '''@import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&display=swap');

:root {
    --bg: #000000;
    --bg-card: #0A0A0A;
    --bg-warm: #111111;
    --bg-sidebar: #050505;
    
    --accent: #EDEDED;
    --accent-light: rgba(255, 255, 255, 0.1);
    --accent-hover: #FFFFFF;
    --accent-gradient: linear-gradient(to right, #ffffff, #a3a3a3);
    
    --green: #2ecc71;
    --yellow: #f1c40f;
    --red: #e74c3c;
    --blue: #3498db;
    --purple: #9b59b6;
    
    --text: #EDEDED;
    --text-secondary: #A1A1AA;
    --text-muted: #71717A;
    
    --border: #1F1F1F;
    --border-dark: #27272A;
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
::-webkit-scrollbar-thumb {background: #333; border-radius: 4px;}

.hero { text-align: center; padding: 4rem 1rem 3rem; }
.hero-badge {
    display: inline-flex; align-items: center; padding: 4px 12px;
    background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 999px; font-size: 0.75rem; font-weight: 500; color: #A1A1AA;
    margin-bottom: 1.5rem; backdrop-filter: blur(10px);
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
    background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px;
    padding: 1.5rem; margin-bottom: 1rem; transition: all 0.2s ease;
}
.card:hover { border-color: #333; }
.card-head {
    display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;
    padding-bottom: 0.75rem; border-bottom: 1px solid var(--border);
}
.card-title { font-size: 0.95rem; font-weight: 500; color: var(--text); }
.card-desc { font-size: 0.8rem; color: var(--text-muted); }

.score-section { display: flex; align-items: center; justify-content: center; gap: 3rem; padding: 1rem 0; flex-wrap: wrap; }
.score-circle { position: relative; width: 140px; height: 140px; }
.score-circle svg { transform: rotate(-90deg); }
.ring-bg { fill: none; stroke: var(--border); stroke-width: 6; }
.ring-fill { fill: none; stroke-width: 6; stroke-linecap: round; stroke-dasharray: 408; transition: stroke-dashoffset 1.5s ease; filter: drop-shadow(0 0 4px currentColor); }
.ring-green {stroke: var(--green);} .ring-yellow {stroke: var(--yellow);} .ring-red {stroke: var(--red);}
.score-num { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; }
.score-big { font-size: 2.5rem; font-weight: 300; line-height: 1; color: var(--text); }
.score-tag { font-size: 0.65rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }
.score-details { display: flex; flex-direction: column; gap: 0.5rem; }
.score-detail-row { display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0.75rem; background: var(--bg-warm); border-radius: 8px; border: 1px solid var(--border); min-width: 180px; }
.score-detail-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; box-shadow: 0 0 5px currentColor; }
.bg-green {background: var(--green); color: var(--green);} .bg-yellow {background: var(--yellow); color: var(--yellow);} .bg-red {background: var(--red); color: var(--red);} .bg-blue {background: var(--accent); color: var(--accent);}
.score-detail-label { font-size: 0.85rem; color: var(--text-secondary); flex-grow: 1; }
.score-detail-val { font-size: 0.85rem; font-weight: 500; color: var(--text); }
.c-green {color: var(--green);} .c-yellow {color: var(--yellow);} .c-red {color: var(--red);} .c-blue {color: var(--blue);}

.bar-wrap {margin-bottom: 1rem;} .bar-top { display: flex; justify-content: space-between; margin-bottom: 0.4rem; } 
.bar-name {font-size: 0.85rem; font-weight: 400; color: var(--text-secondary);} .bar-val {font-size: 0.85rem; font-weight: 500;} 
.bar-track { width: 100%; height: 4px; background: var(--border); border-radius: 2px; overflow: hidden; } 
.bar-fill { height: 100%; border-radius: 2px; transition: width 1s ease; box-shadow: 0 0 10px currentColor; }
.fill-green {background: var(--green); color: var(--green);} .fill-yellow {background: var(--yellow); color: var(--yellow);} .fill-red {background: var(--red); color: var(--red);}

.items {list-style: none; padding: 0; margin: 0;}
.items li { padding: 0.75rem 1rem; margin-bottom: 0.5rem; border-radius: 8px; font-size: 0.85rem; line-height: 1.5; color: var(--text); display: flex; align-items: flex-start; gap: 0.75rem; background: var(--bg-warm); border: 1px solid var(--border); }
.tags {display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem;}
.tag { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 16px; font-size: 0.75rem; font-weight: 500; background: var(--border); color: var(--text); }
.t-found {background: rgba(46, 204, 113, 0.1); border: 1px solid rgba(46, 204, 113, 0.3); color: var(--green);}
.t-miss {background: rgba(241, 196, 15, 0.1); border: 1px solid rgba(241, 196, 15, 0.3); color: var(--yellow);}

.stButton > button { background: var(--text) !important; color: var(--bg) !important; border: none !important; border-radius: 8px !important; font-weight: 500 !important; font-family: 'Geist', sans-serif !important; transition: opacity 0.2s !important; }
.stButton > button:hover { opacity: 0.9 !important; }
.stTextInput input, .stSelectbox > div > div { background: var(--bg-card) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; color: var(--text) !important; font-family: 'Geist', sans-serif !important; box-shadow: none !important; }
.stTextInput input:focus, .stSelectbox > div > div:focus { border-color: #555 !important; box-shadow: none !important; }
.stTextInput > div > div { background: transparent !important; border: none !important; }
.stFileUploader > div { background: var(--bg-card) !important; border: 1px dashed #333 !important; border-radius: 12px !important; }
.stFileUploader > div:hover { border-color: #666 !important; }
section[data-testid="stSidebar"] { background: var(--bg-sidebar) !important; border-right: 1px solid var(--border) !important; }
.stDownloadButton > button { background: var(--bg-warm) !important; color: var(--text) !important; border: 1px solid var(--border) !important; }
hr { border: none; height: 1px; background: var(--border); margin: 2rem 0; }
.streamlit-expanderHeader { background: var(--bg-warm) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; font-weight: 500 !important; }
.footer { text-align: center; padding: 2rem 0 1rem; color: var(--text-muted); font-size: 0.8rem; }
.footer a {color: var(--text); text-decoration: none;}
'''
    text = head + css_start + new_css + '\n' + css_end + tail

import re

# Replace Hero
hero_pattern = re.compile(r'# ─── Hero ───\nst\.markdown\("""\n<div class="hero">.*?</div>\n""", unsafe_allow_html=True\)', re.DOTALL)
new_hero = '''# ─── Hero ───
st.markdown("""
<div class="hero">
    <div class="hero-badge">AI-Powered Resume Analysis</div>
    <div class="hero-title">Elevate Your <span>Career</span></div>
    <div class="hero-sub">
        Upload your resume and get actionable insights, ATS scoring, and targeted feedback to land your next role.
    </div>
</div>
""", unsafe_allow_html=True)'''
text = hero_pattern.sub(new_hero, text)

# Replace right column
right_col_pattern = re.compile(r'st\.markdown\("""\n<div style="padding: 0 0\.5rem;">\n<h2 style="font-size: 1\.8rem; font-weight: 800;.*?</div>\n</div>\n""", unsafe_allow_html=True\)', re.DOTALL)
new_right = '''st.markdown("""
<div style="padding: 0.5rem 1rem;">
<div style="font-size: 0.85rem; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1.5rem;">Process Overview</div>

<div style="border-left: 1px solid var(--border); padding-left: 1.5rem; position: relative; margin-bottom: 2rem;">
    <div style="position: absolute; left: -5px; top: 0; width: 9px; height: 9px; border-radius: 50%; background: var(--text);"></div>
    <div style="font-weight: 500; font-size: 1rem; color: var(--text); margin-bottom: 0.25rem;">1. Document Intake</div>
    <div style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.5;">Drop your PDF or TXT resume and supply a target role. Data is securely processed.</div>
</div>

<div style="border-left: 1px solid var(--border); padding-left: 1.5rem; position: relative; margin-bottom: 2rem;">
    <div style="position: absolute; left: -5px; top: 0; width: 9px; height: 9px; border-radius: 50%; background: var(--bg); border: 1px solid var(--text);"></div>
    <div style="font-weight: 500; font-size: 1rem; color: var(--text); margin-bottom: 0.25rem;">2. Deep AI Audit</div>
    <div style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.5;">Cross-referenced against 30+ precise ATS parameters and industry benchmarks.</div>
</div>

<div style="border-left: 1px solid transparent; padding-left: 1.5rem; position: relative; margin-bottom: 2rem;">
    <div style="position: absolute; left: -5px; top: 0; width: 9px; height: 9px; border-radius: 50%; background: var(--bg); border: 1px solid var(--text);"></div>
    <div style="font-weight: 500; font-size: 1rem; color: var(--text); margin-bottom: 0.25rem;">3. Actionable Feedback</div>
    <div style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.5;">Get optimized formatting tips, line-by-line rewrites, and instant technical insight.</div>
</div>

<div style="display: flex; gap: 1rem; margin-top: 3rem;">
<div style="flex: 1; padding: 1rem; border: 1px solid var(--border); border-radius: 8px; background: var(--bg-card); text-align: center;">
<div style="font-size: 1.5rem; margin-bottom: 0.5rem; color: var(--text);">⚡</div>
<div style="font-size: 0.85rem; font-weight: 500; color: var(--text);">ATS Ready</div>
</div>
<div style="flex: 1; padding: 1rem; border: 1px solid var(--border); border-radius: 8px; background: var(--bg-card); text-align: center;">
<div style="font-size: 1.5rem; margin-bottom: 0.5rem; color: var(--text);">🎯</div>
<div style="font-size: 0.85rem; font-weight: 500; color: var(--text);">Targeted</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)'''

text = right_col_pattern.sub(new_right, text)

with open('c:/Users/3541/Desktop/resume_crtique/main.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Done')

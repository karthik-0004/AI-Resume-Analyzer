import sys
import re

with open('c:/Users/3541/Desktop/resume_crtique/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

# CSS Color Replacement
css_replacements = {
    '--bg: #000000;': '--bg: #FAFAFA;',
    '--bg-card: #0A0A0A;': '--bg-card: #FFFFFF;',
    '--bg-warm: #111111;': '--bg-warm: #F4F4F5;',
    '--bg-sidebar: #050505;': '--bg-sidebar: #FFFFFF;',
    
    '--accent: #EDEDED;': '--accent: #171717;',
    '--accent-light: rgba(255, 255, 255, 0.1);': '--accent-light: rgba(0, 0, 0, 0.05);',
    '--accent-hover: #FFFFFF;': '--accent-hover: #000000;',
    '--accent-gradient: linear-gradient(to right, #ffffff, #a3a3a3);': '--accent-gradient: linear-gradient(to right, #18181b, #71717a);',
    
    '--text: #EDEDED;': '--text: #171717;',
    '--text-secondary: #A1A1AA;': '--text-secondary: #52525B;',
    '--text-muted: #71717A;': '--text-muted: #71717A;',
    
    '--border: #1F1F1F;': '--border: #E4E4E7;',
    '--border-dark: #27272A;': '--border-dark: #D4D4D8;',
    
    '::-webkit-scrollbar-thumb {background: #333; border-radius: 4px;}': '::-webkit-scrollbar-thumb {background: #D4D4D8; border-radius: 4px;}',
    'background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);': 'background: rgba(0, 0, 0, 0.05); border: 1px solid rgba(0, 0, 0, 0.1);',
    '.card:hover { border-color: #333; }': '.card:hover { border-color: #D4D4D8; }',
    '.stTextInput input:focus, .stSelectbox > div > div:focus { border-color: #555 !important;': '.stTextInput input:focus, .stSelectbox > div > div:focus { border-color: #A1A1AA !important;',
    'border: 1px dashed #333 !important;': 'border: 1px dashed #D4D4D8 !important;',
    '.stFileUploader > div:hover { border-color: #666 !important; }': '.stFileUploader > div:hover { border-color: #A1A1AA !important; }'
}

for o, n in css_replacements.items():
    text = text.replace(o, n)

# Restructure layout
match = re.search(r'# ─── Hero ───(.*?)# ─── Analysis ───', text, re.DOTALL)
if match:
    old_layout = match.group(1)
    
    # Extract JOB_ROLES
    job_roles_match = re.search(r'JOB_ROLES = \[.*?\]', old_layout, re.DOTALL)
    job_roles_code = job_roles_match.group(0) if job_roles_match else 'JOB_ROLES = ["Software Engineer"]'
    
    new_layout = f"""
# ─── Process Overview ───
st.markdown('''
<div style="padding: 2rem 1rem 1rem; max-width: 900px; margin: 0 auto;">
    <div style="font-size: 0.85rem; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2rem; text-align: center;">Process Overview</div>
    <div style="display: flex; gap: 2rem; justify-content: space-between; align-items: flex-start; text-align: center;">
        <div style="flex: 1;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: var(--text); color: var(--bg); display: flex; align-items: center; justify-content: center; font-weight: 600; margin: 0 auto 1rem;">1</div>
            <div style="font-weight: 600; font-size: 1.05rem; color: var(--text); margin-bottom: 0.5rem;">Document Intake</div>
            <div style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.5;">Drop your PDF or TXT resume and supply a target role. Data is securely processed.</div>
        </div>
        <div style="flex: 1;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: transparent; border: 2px solid var(--text); color: var(--text); display: flex; align-items: center; justify-content: center; font-weight: 600; margin: 0 auto 1rem;">2</div>
            <div style="font-weight: 600; font-size: 1.05rem; color: var(--text); margin-bottom: 0.5rem;">Deep AI Audit</div>
            <div style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.5;">Cross-referenced against 30+ precise ATS parameters and industry benchmarks.</div>
        </div>
        <div style="flex: 1;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: transparent; border: 2px solid var(--text); color: var(--text); display: flex; align-items: center; justify-content: center; font-weight: 600; margin: 0 auto 1rem;">3</div>
            <div style="font-weight: 600; font-size: 1.05rem; color: var(--text); margin-bottom: 0.5rem;">Actionable Feedback</div>
            <div style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.5;">Get optimized formatting tips, line-by-line rewrites, and instant technical insight.</div>
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

    {job_roles_code}

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
_datalist_options = "\\n".join([f'<option value="{{role}}">' for role in JOB_ROLES])
st.markdown(f'''
<datalist id="jobRoleList">
{{_datalist_options}}
</datalist>
<script>
function attachDatalist() {{{{
    const inputs = document.querySelectorAll('input[type="text"]');
    inputs.forEach(input => {{{{
        if (input.getAttribute('placeholder') && 
            input.getAttribute('placeholder').includes('Start typing')) {{{{
            if (!input.getAttribute('list')) {{{{
                input.setAttribute('list', 'jobRoleList');
                input.setAttribute('autocomplete', 'on');
            }}}}
        }}}}
    }}}});
}}}}
attachDatalist();
const observer = new MutationObserver(() => {{{{ attachDatalist(); }}}});
observer.observe(document.body, {{{{ childList: true, subtree: true }}}});
</script>
''', unsafe_allow_html=True)

"""
    
    text = text[:match.start()] + new_layout + '\n# ─── Analysis ───\n' + text[match.end():]
    
with open('c:/Users/3541/Desktop/resume_crtique/main.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updates applied.")

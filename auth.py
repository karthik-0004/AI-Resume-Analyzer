"""Google OAuth Authentication & History Module for AI Resume Critiquer.
Uses Streamlit's native OIDC authentication (st.login / st.user / st.logout).
"""
import streamlit as st
import hashlib, json
from pathlib import Path
from datetime import datetime

HISTORY_DIR = Path("history")
HISTORY_DIR.mkdir(exist_ok=True)


# ─── Auth Helpers ───
def is_logged_in():
    return st.user.is_logged_in


def get_user_info():
    if is_logged_in():
        return {
            "name": getattr(st.user, "name", "User") or "User",
            "email": getattr(st.user, "email", "") or "",
            "picture": getattr(st.user, "picture", "") or "",
        }
    return {}


def get_user_email():
    return getattr(st.user, "email", "") if is_logged_in() else ""


# ─── History ───
def _history_path(email):
    safe = hashlib.md5(email.lower().strip().encode()).hexdigest()
    return HISTORY_DIR / f"{safe}.json"


def load_history(email):
    if not email:
        return []
    path = _history_path(email)
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_to_history(email, entry):
    if not email:
        return
    history = load_history(email)
    history.insert(0, entry)
    history = history[:20]
    path = _history_path(email)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


# ─── Login Page ───
def show_login_page():
    """Show a beautiful login page with Google sign-in button."""
    st.markdown("""
    <div style="text-align:center; padding:3.5rem 1rem 1rem;">
        <div style="font-size:3.5rem; margin-bottom:0.4rem;">📝</div>
        <div style="font-size:2.2rem; font-weight:800; color:#1f1f1f; letter-spacing:-0.5px; margin-bottom:0.3rem;">
            Resume <span style="background:linear-gradient(135deg,#e8734a,#d4623c); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Critiquer</span>
        </div>
        <p style="color:#6b7280; font-size:1rem; max-width:400px; margin:0.5rem auto 0; line-height:1.6;">
            Sign in to get AI-powered resume analysis<br>with ATS scoring &amp; actionable insights
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-bottom:-0.5rem;">
        <div style="font-weight:700; font-size:1.05rem; color:#1f1f1f; margin-bottom:0.15rem;">Welcome</div>
        <div style="font-size:0.82rem; color:#9ca3af; margin-bottom:0.8rem;">Sign in to continue</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        login_clicked = st.button("🔐 Continue with Google", use_container_width=True, type="primary")
        if login_clicked and not st.session_state.get("login_triggered", False):
            st.session_state["login_triggered"] = True
            st.login("google")
        elif not login_clicked:
            st.session_state["login_triggered"] = False

    st.markdown("""
    <div style="max-width:380px; margin:2rem auto; display:flex; flex-direction:column; gap:0.5rem;">
        <div style="display:flex; align-items:center; gap:0.6rem; font-size:0.85rem; color:#6b7280;">
            <span style="width:28px; height:28px; display:flex; align-items:center; justify-content:center; background:#fdeee8; border-radius:6px; flex-shrink:0;">🎯</span>
            Deep resume analysis with ATS scoring
        </div>
        <div style="display:flex; align-items:center; gap:0.6rem; font-size:0.85rem; color:#6b7280;">
            <span style="width:28px; height:28px; display:flex; align-items:center; justify-content:center; background:#f0fdf4; border-radius:6px; flex-shrink:0;">✏️</span>
            Bullet rewrites &amp; action verb analysis
        </div>
        <div style="display:flex; align-items:center; gap:0.6rem; font-size:0.85rem; color:#6b7280;">
            <span style="width:28px; height:28px; display:flex; align-items:center; justify-content:center; background:#eff6ff; border-radius:6px; flex-shrink:0;">📊</span>
            Section-by-section scoring &amp; review
        </div>
        <div style="display:flex; align-items:center; gap:0.6rem; font-size:0.85rem; color:#6b7280;">
            <span style="width:28px; height:28px; display:flex; align-items:center; justify-content:center; background:#f5f3ff; border-radius:6px; flex-shrink:0;">📋</span>
            Save &amp; review your analysis history
        </div>
    </div>
    <div style="text-align:center; font-size:0.72rem; color:#9ca3af;">🔒 Secured with Google OAuth 2.0</div>
    """, unsafe_allow_html=True)

    st.stop()

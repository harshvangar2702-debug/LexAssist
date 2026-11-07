"""
LexAssist — AI Legal Research Assistant
Presentation-Grade UI with Persistent Storage, Multi-Case Support, Quick Case Presets,
Authoritative Legal Typography, Structured Results, and Grounded Follow-Up Chat.
"""

import os
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

from analysis.case_analysis import run_lexassist_analysis, answer_case_followup
from utils.helpers import process_uploaded_file
from utils.chat_storage import (
    save_chat_session,
    load_chat_session,
    list_chat_sessions,
    create_new_chat_on_same_case,
    delete_chat_session,
    clear_all_chat_sessions,
    generate_session_title,
)
from retrieval.search import get_retrieval_collection
from utils.icons import get_lucide_svg, get_lucide_data_uri

# Load environment variables
load_dotenv()

# Streamlit Page Configuration with professional Scale emblem favicon
FAVICON_PATH = os.path.join(os.path.dirname(__file__), "data", "icons", "scale_favicon.png")
st.set_page_config(
    page_title="LexAssist — AI Legal Research Assistant",
    page_icon=FAVICON_PATH if os.path.exists(FAVICON_PATH) else "⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Session State
if "active_session_id" not in st.session_state:
    st.session_state["active_session_id"] = None
if "active_session_title" not in st.session_state:
    st.session_state["active_session_title"] = ""
if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None
if "case_facts" not in st.session_state:
    st.session_state["case_facts"] = ""
if "case_facts_input" not in st.session_state:
    st.session_state["case_facts_input"] = ""
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "all_provisions" not in st.session_state:
    st.session_state["all_provisions"] = []
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0

# Demo Preset Scenarios for Instant Testing
DEMO_PRESETS = {
    "contract": {
        "label": "Breach of Software Contract (ICA §73-74)",
        "icon": ":material/gavel:",
        "facts": (
            "A commercial client hired a software development agency to deliver an enterprise "
            "billing portal by April 30th with an advance payment of Rs. 3,00,000. The agency missed "
            "the agreed deadline by over four months, delivered non-functional source code, and "
            "refused to return the advance deposit or compensate for business disruption. "
            "What statutory provisions and compensation remedies apply under Indian contract law?"
        )
    },
    "consumer": {
        "label": "Defective Appliance & Injury (CPA §84)",
        "icon": ":material/shield:",
        "facts": (
            "A consumer purchased an electric induction cooktop from an e-commerce platform. "
            "During normal domestic usage two weeks later, the internal heating coil exploded due to "
            "manufacturing defects, causing serious burn injuries to the user and damaging the kitchen "
            "countertop. The seller and manufacturer refuse responsibility. "
            "What legal provisions govern product liability and compensation?"
        )
    },
    "cyber": {
        "label": "Unauthorized Server Access & Theft (IT Act §43)",
        "icon": ":material/lock:",
        "facts": (
            "An ex-employee of an accounting firm logged into the company internal client database "
            "using previously assigned admin credentials without authorization. The individual copied "
            "confidential tax records, audit spreadsheets, and client contact details onto an external "
            "drive and attempted to delete access logs. "
            "Which statutory provisions of the Information Technology Act apply?"
        )
    }
}

# Helper Navigation and Session Management Handlers
def start_new_chat_on_same_case():
    """Starts a fresh chat thread with the currently analyzed case & retrieved provisions."""
    if st.session_state.get("analysis_result") is not None:
        if not st.session_state.get("chat_history"):
            st.toast("Already in a fresh chat thread on this case.", icon=":material/info:")
            return

        new_session = create_new_chat_on_same_case(
            current_facts=st.session_state.get("case_facts", ""),
            current_analysis=st.session_state.get("analysis_result"),
            current_provisions=st.session_state.get("all_provisions", [])
        )
        st.session_state["active_session_id"] = new_session["id"]
        st.session_state["active_session_title"] = new_session.get("title", "")
        st.session_state["chat_history"] = []
        st.rerun()

def start_new_chat_on_different_case():
    """Clears the case and starts a completely fresh case input."""
    st.session_state["active_session_id"] = None
    st.session_state["active_session_title"] = ""
    st.session_state["analysis_result"] = None
    st.session_state["case_facts"] = ""
    st.session_state["case_facts_input"] = ""
    st.session_state["chat_history"] = []
    st.session_state["all_provisions"] = []
    st.session_state["uploader_key"] += 1
    st.rerun()

def load_selected_session(session_id: str):
    """Loads a past chat session from disk into active session state."""
    session_data = load_chat_session(session_id)
    if session_data:
        st.session_state["active_session_id"] = session_data.get("id", session_id)
        st.session_state["active_session_title"] = session_data.get("title", "Saved Case")
        facts = session_data.get("case_facts", "")
        st.session_state["case_facts"] = facts
        st.session_state["case_facts_input"] = facts
        st.session_state["analysis_result"] = session_data.get("analysis_result")
        st.session_state["all_provisions"] = session_data.get(
            "all_provisions",
            (session_data.get("analysis_result") or {}).get("retrieved_provisions", [])
        )
        st.session_state["chat_history"] = session_data.get("chat_history", [])
        st.rerun()

def sync_active_session():
    """Syncs the current active case & chat state into persistent storage."""
    curr_id = st.session_state.get("active_session_id")
    if not curr_id:
        title = generate_session_title(
            st.session_state.get("case_facts", ""),
            (st.session_state.get("analysis_result") or {}).get("case_summary", "")
        )
        session_data = {
            "title": title,
            "case_facts": st.session_state.get("case_facts", ""),
            "analysis_result": st.session_state.get("analysis_result"),
            "all_provisions": st.session_state.get("all_provisions", []),
            "chat_history": st.session_state.get("chat_history", [])
        }
        new_id = save_chat_session(session_data)
        st.session_state["active_session_id"] = new_id
        st.session_state["active_session_title"] = title
    else:
        existing = load_chat_session(curr_id) or {}
        existing["id"] = curr_id
        if "title" not in existing or not existing["title"]:
            existing["title"] = st.session_state.get("active_session_title") or generate_session_title(
                st.session_state.get("case_facts", ""),
                (st.session_state.get("analysis_result") or {}).get("case_summary", "")
            )
        existing["case_facts"] = st.session_state.get("case_facts", "")
        existing["analysis_result"] = st.session_state.get("analysis_result")
        existing["all_provisions"] = st.session_state.get("all_provisions", [])
        existing["chat_history"] = st.session_state.get("chat_history", [])
        save_chat_session(existing)

# ==============================================================================
# Modern Legal Scholar Visual Design System (Google Web Fonts, Tokens, Layout)
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --navy-deep: #0B192C;
        --navy-slate: #1E3E62;
        --gold-accent: #C5A059;
        --gold-subtle: #FDFBF7;
        --gold-border: #E5D5B5;
        --text-primary: #0F172A;
        --text-secondary: #475569;
        --bg-surface: #FFFFFF;
        --bg-warm: #F8F9FA;
        --border-subtle: #E2E8F0;
        --emerald-badge: #0F766E;
        --emerald-bg: #F0FDF4;
        --amber-badge: #B45309;
        --amber-bg: #FFFBEB;
    }

    /* Global Typography Harmonization */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
    }

    /* Hero Banner */
    .lex-hero-banner {
        background: linear-gradient(135deg, #0B192C 0%, #1E3E62 100%);
        border: 1px solid rgba(197, 160, 89, 0.35);
        border-radius: 14px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(11, 25, 44, 0.12);
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    .lex-hero-seal {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(197, 160, 89, 0.5);
        border-radius: 12px;
        width: 76px;
        height: 76px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .lex-brand-name {
        font-family: 'Cinzel', serif;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        color: #F8FAFC;
        line-height: 1.1;
        margin-bottom: 0.25rem;
    }
    .lex-brand-tagline {
        font-size: 0.98rem;
        color: #CBD5E1;
        font-weight: 500;
        margin-bottom: 0.75rem;
    }
    .lex-hero-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    .lex-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(197, 160, 89, 0.4);
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #F1F5F9;
        letter-spacing: 0.02em;
    }

    /* Section Headings */
    .lex-section-header {
        font-family: 'Cinzel', serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--navy-deep);
        border-bottom: 2px solid var(--border-subtle);
        padding-bottom: 0.4rem;
        margin-top: 1.2rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Preset Scenarios Strip */
    .preset-label {
        font-size: 0.84rem;
        font-weight: 700;
        color: var(--navy-slate);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* Statutory Provision Cards */
    .provision-card {
        background-color: #FFFFFF;
        border: 1px solid var(--border-subtle);
        border-top: 3px solid var(--gold-accent);
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .provision-card:hover {
        box-shadow: 0 4px 12px rgba(11, 25, 44, 0.08);
    }
    .provision-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 0.6rem;
    }
    .law-badge {
        display: inline-block;
        padding: 0.22rem 0.65rem;
        background-color: #EEF2F6;
        color: var(--navy-slate);
        border: 1px solid #D0D7DE;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    .distance-badge {
        display: inline-block;
        padding: 0.22rem 0.65rem;
        border-radius: 4px;
        font-size: 0.78rem;
        font-weight: 700;
    }
    .distance-badge-strong {
        background-color: var(--emerald-bg);
        color: var(--emerald-badge);
        border: 1px solid #BBF7D0;
    }
    .distance-badge-moderate {
        background-color: var(--amber-bg);
        color: var(--amber-badge);
        border: 1px solid #FDE68A;
    }
    .provision-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--navy-deep);
        margin-bottom: 0.5rem;
    }
    .provision-meta {
        font-size: 0.85rem;
        color: var(--text-secondary);
        display: flex;
        flex-wrap: wrap;
        gap: 1.5rem;
        align-items: center;
    }
    .gazette-link {
        color: #1D4ED8;
        font-weight: 600;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
    }
    .gazette-link:hover {
        text-decoration: underline;
    }

    /* Executive Summary & Issues Cards */
    .summary-card {
        background: #FDFBF7;
        border: 1px solid var(--gold-border);
        border-left: 4px solid var(--gold-accent);
        border-radius: 8px;
        padding: 1.1rem 1.3rem;
        font-size: 0.95rem;
        line-height: 1.6;
        color: #1E293B;
        margin-bottom: 1.2rem;
    }
    .issue-item {
        background: #FFFFFF;
        border: 1px solid var(--border-subtle);
        border-radius: 6px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: flex-start;
        gap: 0.7rem;
        font-size: 0.92rem;
        color: #1E293B;
    }
    .issue-num {
        background: var(--navy-slate);
        color: #FFFFFF;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 0.15rem 0.45rem;
        border-radius: 4px;
        flex-shrink: 0;
        margin-top: 0.15rem;
    }

    /* Statutory Disclaimer Box */
    .disclaimer-box {
        background-color: var(--amber-bg);
        border: 1px solid #FCD34D;
        border-left: 4px solid var(--amber-badge);
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin-top: 1.5rem;
        font-size: 0.88rem;
        color: #78350F;
        line-height: 1.55;
    }

    /* Chat Section Enhancements */
    .chat-header-bar {
        background: #FFFFFF;
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }
    .chat-title-text {
        font-family: 'Cinzel', serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--navy-deep);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .active-badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background-color: #F0FDF4;
        color: #166534;
        border: 1px solid #BBF7D0;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* Sidebar History Metadata */
    .history-meta {
        font-size: 0.76rem;
        color: #64748B;
        margin-top: -6px;
        margin-bottom: 12px;
        padding-left: 4px;
        line-height: 1.35;
    }

    /* Distinctive Drag & Drop Target Area */
    [data-testid="stFileUploader"] {
        background-color: #FAFAF7;
        border: 2px dashed #C5A059 !important;
        border-radius: 12px;
        padding: 0.8rem 1rem;
        transition: all 0.2s ease-in-out;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #0B192C !important;
        background-color: #F4F6F8;
    }
    [data-testid="stFileUploaderDropzone"] {
        padding: 0.6rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# Sidebar Configuration
# ==============================================================================
with st.sidebar:
    st.markdown(
        f"<div style='margin-bottom: 0.6rem;'>{get_lucide_svg('landmark', size=42, color='#1E3E62', stroke_width=1.75)}</div>",
        unsafe_allow_html=True
    )
    st.markdown("### **LexAssist System Hub**")
    st.caption("Zero-Hallucination Indian Statutory Intelligence Engine")

    # New Chat Options Section
    st.markdown("---")
    st.markdown(f"#### **{get_lucide_svg('message-square', size=18, color='#1E3E62')} Research Actions**", unsafe_allow_html=True)

    # Option: New Chat on Different Case
    if st.button("New Case Investigation", icon=":material/refresh:", use_container_width=True, help="Clear scenario and start research on a brand new case"):
        start_new_chat_on_different_case()

    # Option: New Chat on Same Case
    has_active_case = st.session_state.get("analysis_result") is not None
    if st.button(
        "New Chat on Same Case",
        icon=":material/add:",
        use_container_width=True,
        disabled=not has_active_case,
        help="Starts a fresh conversation thread with the currently analyzed case facts & retrieved provisions" if has_active_case else "Analyze a case first to start a chat thread on it"
    ):
        start_new_chat_on_same_case()

    # Past Case Chats History Section
    st.markdown("---")
    st.markdown(f"#### **{get_lucide_svg('history', size=18, color='#1E3E62')} Saved Case Inquiries**", unsafe_allow_html=True)

    past_sessions = list_chat_sessions()
    if not past_sessions:
        st.caption("No saved case inquiries yet. Analyzed cases and discussion threads will be saved automatically here.")
    else:
        active_sid = st.session_state.get("active_session_id")
        for sess in past_sessions:
            is_active = (sess["id"] == active_sid)
            sess_icon = ":material/bookmark:" if is_active else ":material/folder:"
            btn_label = sess['title']

            col_sess, col_del = st.columns([5, 1])
            with col_sess:
                if st.button(btn_label, icon=sess_icon, key=f"sidebar_sess_{sess['id']}", use_container_width=True, help=f"Load: {sess['title']}"):
                    load_selected_session(sess["id"])
            with col_del:
                if st.button("", icon=":material/delete:", key=f"del_item_{sess['id']}", help=f"Delete '{sess['title']}'"):
                    delete_chat_session(sess["id"])
                    if is_active:
                        start_new_chat_on_different_case()
                    else:
                        st.rerun()

            msg_count = sess.get("message_count", 0)
            msg_str = f"{msg_count} message{'s' if msg_count != 1 else ''}" if msg_count > 0 else "New inquiry"
            st.markdown(
                f"""
                <div class='history-meta'>
                    <span>{get_lucide_svg('clock', size=12, color='#64748B')} {sess['updated_at']}</span> • <span>{get_lucide_svg('message-square', size=12, color='#64748B')} {msg_str}</span><br>
                    <span style='color: #475569;'>"{sess['case_snippet']}"</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        with st.expander("Manage Session History", icon=":material/settings:"):
            if active_sid:
                if st.button("Delete Current Session", icon=":material/delete:", use_container_width=True, help="Delete the currently active inquiry"):
                    delete_chat_session(active_sid)
                    start_new_chat_on_different_case()

            confirm_del_all = st.checkbox("Confirm delete all stored inquiries", key="confirm_del_all_chats")
            if st.button("Clear All Saved History", icon=":material/delete_forever:", use_container_width=True, disabled=not confirm_del_all):
                clear_all_chat_sessions()
                start_new_chat_on_different_case()

    st.markdown("---")
    st.markdown(f"#### **{get_lucide_svg('landmark', size=18, color='#1E3E62')} Verified Statutory Corpus**", unsafe_allow_html=True)

    # Fetch vector database status
    try:
        coll = get_retrieval_collection()
        doc_count = coll.count()
        st.success(f"**Vector Store:** Connected ({doc_count} Sections)", icon=":material/check_circle:")
    except Exception:
        st.warning("Vector Store: Pending Ingestion", icon=":material/warning:")

    st.markdown(
        "**Indexed Central Acts (MVP):**\n"
        "1. **The Indian Contract Act, 1872**\n"
        "   - [India Code Source](https://www.indiacode.nic.in/handle/123456789/2187)\n"
        "2. **The Information Technology Act, 2000**\n"
        "   - [India Code Source](https://www.indiacode.nic.in/handle/123456789/1999)\n"
        "3. **The Consumer Protection Act, 2019**\n"
        "   - [India Code Source](https://www.indiacode.nic.in/handle/123456789/15256)\n"
    )

    st.markdown("---")
    st.markdown(f"#### **{get_lucide_svg('sliders-horizontal', size=18, color='#1E3E62')} System Diagnostics**", unsafe_allow_html=True)
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key.strip() != "your_gemini_api_key_here":
        st.success("Gemini API: Live Connected", icon=":material/check_circle:")
    else:
        st.info("Gemini API: Offline / Fallback Mode (Add key to `.env` for live LLM)", icon=":material/info:")

    with st.expander("Core Guardrails", icon=":material/shield:"):
        st.caption("Embeddings: `all-MiniLM-L6-v2` (Local)")
        st.caption("Collection: `lexassist_provisions`")
        st.caption("Relevance Cutoff: `0.52 Distance`")
        st.caption("Storage: Local Atomic JSON (`data/chats/`)")

    st.markdown("---")
    st.caption("LexAssist v1.4.0 • Zero-Hallucination Legal Research Engine")

# ==============================================================================
# Main Presentation Header Banner
# ==============================================================================
st.markdown(
    f"""
    <div class='lex-hero-banner'>
        <div class='lex-hero-seal'>{get_lucide_svg('scale', size=38, color='#C5A059', stroke_width=1.75)}</div>
        <div class='lex-hero-content'>
            <div class='lex-brand-name'>LEXASSIST</div>
            <div class='lex-brand-tagline'>AI-Assisted Legal Research Assistant • Zero-Hallucination Statutory Retrieval</div>
            <div class='lex-hero-chips'>
                <span class='lex-chip'>{get_lucide_svg('landmark', size=14, color='#E2E8F0')} Jurisdiction: India (Central)</span>
                <span class='lex-chip'>{get_lucide_svg('book-open', size=14, color='#E2E8F0')} 34 Official Sections Ingested</span>
                <span class='lex-chip'>{get_lucide_svg('shield-check', size=14, color='#E2E8F0')} Zero-Hallucination Guardrails</span>
                <span class='lex-chip'>{get_lucide_svg('database', size=14, color='#E2E8F0')} Local Session Memory</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# Step 1: Input Section & Case Presets
# ==============================================================================
st.markdown("<div class='lex-section-header'><span>1. Enter Legal Scenario or Select Sample Case</span></div>", unsafe_allow_html=True)

# Quick Preset Buttons for Instant Testing & Demonstrations
st.markdown(
    f"<div class='preset-label'>{get_lucide_svg('zap', size=15, color='var(--navy-slate)')} Instant Demo Presets (Click to Load Realistic Legal Case):</div>",
    unsafe_allow_html=True
)
col_p1, col_p2, col_p3 = st.columns(3)

with col_p1:
    if st.button(DEMO_PRESETS["contract"]["label"], icon=DEMO_PRESETS["contract"]["icon"], use_container_width=True, help="Load software contract breach scenario"):
        st.session_state["case_facts_input"] = DEMO_PRESETS["contract"]["facts"]
        st.rerun()

with col_p2:
    if st.button(DEMO_PRESETS["consumer"]["label"], icon=DEMO_PRESETS["consumer"]["icon"], use_container_width=True, help="Load defective induction appliance explosion scenario"):
        st.session_state["case_facts_input"] = DEMO_PRESETS["consumer"]["facts"]
        st.rerun()

with col_p3:
    if st.button(DEMO_PRESETS["cyber"]["label"], icon=DEMO_PRESETS["cyber"]["icon"], use_container_width=True, help="Load unauthorized internal database access scenario"):
        st.session_state["case_facts_input"] = DEMO_PRESETS["cyber"]["facts"]
        st.rerun()

st.write("")

# Dual Input Channels: Text Scenario & Document Upload
col_query, col_upload = st.columns([3, 2], gap="large")

with col_query:
    user_query = st.text_area(
        label="Enter factual dispute or research question:",
        placeholder=(
            "Example: 'A client contracted a web development agency to deliver an e-commerce website by June 1st. "
            "The agency failed to deliver and refuses to refund the deposit. Which provisions apply?'"
        ),
        height=145,
        key="case_facts_input",
    )

with col_upload:
    uploaded_file = st.file_uploader(
        label="Drag & drop case document (PDF / Image) or browse:",
        type=["pdf", "png", "jpg", "jpeg"],
        help="Drag and drop any case summary PDF or photo of a legal document directly into this box.",
        key=f"file_uploader_{st.session_state['uploader_key']}",
    )
    st.caption(
        f"{get_lucide_svg('folder', size=13, color='#475569')} *Test files ready in `data/sample_documents/`:* `sample_contract_breach_case.pdf` & `sample_consumer_complaint_image.png`",
        unsafe_allow_html=True
    )

col_btn, col_info = st.columns([1.2, 3.8])
with col_btn:
    analyze_btn = st.button("Analyze Case", icon=":material/search:", use_container_width=True, type="primary")

with col_info:
    st.caption(
        f"{get_lucide_svg('lock-keyhole', size=13, color='#475569')} LexAssist strictly queries indexed official Indian statutes. It never invents non-existent provisions.",
        unsafe_allow_html=True
    )

st.markdown("---")

# Handle Case Analysis Submission
if analyze_btn:
    combined_input = user_query.strip() if user_query else ""

    if uploaded_file is not None:
        with st.spinner(f"Extracting text from uploaded file '{uploaded_file.name}'..."):
            extracted_doc_text = process_uploaded_file(uploaded_file)
            if extracted_doc_text:
                if combined_input:
                    combined_input += "\n\n" + extracted_doc_text
                else:
                    combined_input = extracted_doc_text
                st.success(f"Extracted {len(extracted_doc_text)} characters from `{uploaded_file.name}`.", icon=":material/check_circle:")

    if not combined_input:
        st.warning("Please enter a research question or select one of the instant demo presets above to analyze.", icon=":material/warning:")
    else:
        with st.spinner("Analyzing legal scenario, extracting issues, and querying local ChromaDB index..."):
            analysis = run_lexassist_analysis(combined_input)
            st.session_state["analysis_result"] = analysis
            st.session_state["case_facts"] = combined_input
            st.session_state["chat_history"] = []
            st.session_state["all_provisions"] = analysis.get("retrieved_provisions", [])

            # Automatically create & save new chat session to persistent storage
            title = generate_session_title(combined_input, analysis.get("case_summary", ""))
            session_data = {
                "title": title,
                "case_facts": combined_input,
                "analysis_result": analysis,
                "all_provisions": st.session_state["all_provisions"],
                "chat_history": []
            }
            new_id = save_chat_session(session_data)
            st.session_state["active_session_id"] = new_id
            st.session_state["active_session_title"] = title

            st.rerun()

# ==============================================================================
# Step 2: Structured Legal Research Analysis (Tabbed Presentation)
# ==============================================================================
if st.session_state["analysis_result"] is not None:
    analysis = st.session_state["analysis_result"]
    provisions = st.session_state["all_provisions"]
    found_provisions = analysis.get("found_provisions", False) and len(provisions) > 0

    st.markdown("<div class='lex-section-header'><span>2. Structured Legal Research Findings</span></div>", unsafe_allow_html=True)

    tab_summary, tab_provisions, tab_rationale, tab_boundaries = st.tabs([
        ":material/description: Executive Summary & Issues",
        f":material/balance: Statutory Provisions ({len(provisions)})",
        ":material/auto_stories: Rationale & Application",
        ":material/shield: Corpus Scope & Disclaimer"
    ])

    # Tab 1: Executive Summary & Legal Issues
    with tab_summary:
        st.markdown("#### **Executive Case Summary**")
        st.markdown(
            f"""
            <div class='summary-card'>
                {analysis.get('case_summary', 'No summary generated.')}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("#### **Identified Legal Issues**")
        issues = analysis.get("legal_issues", [])
        if issues:
            for idx, issue in enumerate(issues, 1):
                st.markdown(
                    f"""
                    <div class='issue-item'>
                        <span class='issue-num'>ISSUE {idx}</span>
                        <span>{issue}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No specific legal issues identified.", icon=":material/info:")

    # Tab 2: Relevant Legal Provisions
    with tab_provisions:
        st.markdown("#### **Statutory Provisions Retrieved from Official Acts**")
        if not found_provisions:
            st.error("No sufficiently relevant provision was found in the indexed legal corpus.", icon=":material/warning:")
            st.caption("LexAssist refused to generate hallucinated provisions for unindexed laws.")
        else:
            for p in provisions:
                dist = p.get("distance", 0.5)
                # Visual quality rating based on distance
                if dist < 0.45:
                    dist_class = "distance-badge-strong"
                    dist_text = f"Strong Alignment • Distance: {dist:.4f}"
                else:
                    dist_class = "distance-badge-moderate"
                    dist_text = f"Moderate Alignment • Distance: {dist:.4f}"

                st.markdown(
                    f"""
                    <div class='provision-card'>
                        <div class='provision-header'>
                            <span class='law-badge'>{p['law_name']}</span>
                            <span class='distance-badge {dist_class}'>{dist_text}</span>
                        </div>
                        <div class='provision-title'>Section {p['section_number']}: {p['section_title']}</div>
                        <div class='provision-meta'>
                            <span><strong>Official Publication:</strong> {p['source_document']}</span>
                            <a class='gazette-link' href='{p['source_url']}' target='_blank'>Open India Code Gazette {get_lucide_svg('external-link', size=13, color='#1D4ED8')}</a>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                with st.expander(f"View Official Verbatim Text — Section {p['section_number']}", icon=":material/article:"):
                    st.code(p["text"], language="text")

    # Tab 3: Rationale & Application
    with tab_rationale:
        st.markdown("#### **Contextual Legal Application**")
        st.write(analysis.get("why_relevant", "No explanation available."))

    # Tab 4: Corpus Boundaries & Disclaimer
    with tab_boundaries:
        st.markdown("#### **Corpus Scope & Guardrail Boundaries**")
        st.warning(analysis.get("limitations", "No limitations specified."), icon=":material/warning:")

        st.markdown(
            f"""
            <div class='disclaimer-box'>
                <strong>{get_lucide_svg('scale', size=15, color='#78350F')} Mandatory Statutory Verification Disclaimer:</strong><br>
                {analysis.get('disclaimer')}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ==============================================================================
    # Step 3: Interactive Case Discussion Workspace (Chat)
    # ==============================================================================
    st.markdown("<div id='chat-section'></div>", unsafe_allow_html=True)

    # Active Thread Header
    active_title = st.session_state.get("active_session_title")
    if not active_title and st.session_state.get("active_session_id"):
        curr_session = load_chat_session(st.session_state["active_session_id"])
        if curr_session:
            active_title = curr_session.get("title", "Active Inquiry")
            st.session_state["active_session_title"] = active_title

    col_chat_title, col_btn_same, col_btn_diff = st.columns([3, 1.4, 1.4])
    with col_chat_title:
        st.markdown(
            f"<div class='chat-title-text'>{get_lucide_svg('messages-square', size=20, color='var(--navy-deep)')} 3. Interactive Case Discussion</div>",
            unsafe_allow_html=True
        )
        if active_title:
            st.markdown(
                f"<span class='active-badge-pill'>{get_lucide_svg('pin', size=12, color='#166534')} Active Thread: {active_title}</span>",
                unsafe_allow_html=True
            )
        else:
            st.caption("Ask questions, explore remedies, or test legal defenses grounded strictly in the case facts above.")

    with col_btn_same:
        st.write("")
        if st.button("New Chat (Same Case)", icon=":material/add:", key="chat_head_new_same", use_container_width=True, help="Starts a fresh chat thread with this case facts & retrieved provisions"):
            start_new_chat_on_same_case()

    with col_btn_diff:
        st.write("")
        if st.button("New Case Investigation", icon=":material/refresh:", key="chat_head_new_diff", use_container_width=True, help="Clears the current case and starts fresh"):
            start_new_chat_on_different_case()

    # Professional Avatars using Lucide SVG outlines
    USER_AVATAR = get_lucide_data_uri("user-round", size=40, color="#FFFFFF", bg_color="#1E3E62", stroke_width=2.0)
    ASSISTANT_AVATAR = get_lucide_data_uri("scale", size=40, color="#C5A059", bg_color="#0B192C", stroke_width=2.0)

    # Display Conversation Turns
    for msg in st.session_state["chat_history"]:
        avatar = USER_AVATAR if msg["role"] == "user" else ASSISTANT_AVATAR
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])
            if msg.get("new_provisions"):
                for np in msg["new_provisions"]:
                    st.info(
                        f"Additional Grounded Provision: **{np['law_name']} (Section {np['section_number']}: {np['section_title']})**",
                        icon=":material/bookmark:"
                    )

    # Chat Bottom Anchor for Auto-Scroll
    st.markdown("<div id='chat-bottom'></div>", unsafe_allow_html=True)

    # Automatic Smooth Scroll to Chat
    if st.session_state.get("chat_history"):
        components.html(
            """
            <script>
                setTimeout(function() {
                    const bottom = window.parent.document.getElementById('chat-bottom');
                    if (bottom) {
                        bottom.scrollIntoView({ behavior: 'smooth', block: 'end' });
                    } else {
                        const chatSec = window.parent.document.getElementById('chat-section');
                        if (chatSec) {
                            chatSec.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }
                    }
                }, 150);
            </script>
            """,
            height=0,
            width=0,
        )

    # Chat Input for Grounded Follow-Up
    follow_up_prompt = st.chat_input("Ask a follow-up question (e.g. 'Can the client claim interest or consequential loss under Section 73?')...")
    if follow_up_prompt:
        prior_history = list(st.session_state["chat_history"])
        # Append user message
        st.session_state["chat_history"].append({"role": "user", "content": follow_up_prompt})

        with st.spinner("Reviewing case facts and retrieved legal provisions..."):
            chat_reply = answer_case_followup(
                user_question=follow_up_prompt,
                case_facts=st.session_state["case_facts"],
                retrieved_provisions=st.session_state["all_provisions"],
                chat_history=prior_history
            )

            # If any new provisions were retrieved during conversation, append them
            new_provs = chat_reply.get("new_provisions", [])
            if new_provs:
                st.session_state["all_provisions"].extend(new_provs)

            st.session_state["chat_history"].append({
                "role": "assistant",
                "content": chat_reply.get("answer", ""),
                "new_provisions": new_provs
            })

            # Sync updated chat turn into persistent storage
            sync_active_session()

            st.rerun()

else:
    # Initial State Guide
    st.markdown("<div class='lex-section-header'><span>2. How LexAssist Legal Research Works</span></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"#### {get_lucide_svg('search', size=18, color='var(--navy-deep)')} 1. Analyze Case First", unsafe_allow_html=True)
        st.write("Input facts or select a demo preset. LexAssist extracts core issues and queries the local ChromaDB database of official Central Acts.")
    with col2:
        st.markdown(f"#### {get_lucide_svg('file-text', size=18, color='var(--navy-deep)')} 2. Review Structured Citations", unsafe_allow_html=True)
        st.write("Inspect exact verbatim statutory text, section numbers, official India Code links, and relevance scores.")
    with col3:
        st.markdown(f"#### {get_lucide_svg('messages-square', size=18, color='var(--navy-deep)')} 3. Talk with AI on the Case", unsafe_allow_html=True)
        st.write("Ask follow-up questions in an interactive chat grounded strictly in the case facts and retrieved legal provisions.")

    st.markdown(
        f"""
        <div class='disclaimer-box'>
            <strong>{get_lucide_svg('scale', size=15, color='#78350F')} Mandatory Legal Verification Disclaimer:</strong><br>
            LexAssist is an artificial intelligence-assisted legal research aid and does not constitute legal advice.
            The retrieved provisions, identified issues, and generated explanations must be independently verified against 
            official government gazettes and statutory texts by a qualified legal professional before being relied upon in any matter.
        </div>
        """,
        unsafe_allow_html=True,
    )

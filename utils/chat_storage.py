"""
Chat Session Persistence and Management Module for LexAssist.
Handles local file storage of past legal research cases and conversational chat threads
in `data/chats/`, enabling session reload, multi-turn history persistence, and multi-thread support.
"""

import os
import json
import uuid
import re
from datetime import datetime
from utils.logger import log_event

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHATS_DIR = os.path.join(BASE_DIR, "data", "chats")

def ensure_storage_dir() -> str:
    """Ensures that the persistent chat storage directory exists."""
    os.makedirs(CHATS_DIR, exist_ok=True)
    return CHATS_DIR

def generate_session_title(case_facts: str = "", summary: str = "", max_chars: int = 42) -> str:
    """
    Generates a concise, readable title from the case summary or facts.
    """
    raw_source = summary.strip() if summary and summary.strip() else (case_facts or "").strip()
    if not raw_source:
        return "New Legal Inquiry"

    # Take the first line
    first_line = raw_source.split("\n")[0].strip()
    # Strip leading markers like "1. ", "Case Summary: ", "Scenario: "
    cleaned = re.sub(r"^(case summary:?|\d+[\.\)]\s*|scenario:?)\s*", "", first_line, flags=re.IGNORECASE)
    cleaned = " ".join(cleaned.split())

    if not cleaned:
        return "Legal Inquiry"

    if len(cleaned) <= max_chars:
        return cleaned

    # Truncate at last word boundary before max_chars
    truncated = cleaned[:max_chars].rsplit(" ", 1)[0]
    if not truncated:
        truncated = cleaned[:max_chars]
    return f"{truncated}..."

def save_chat_session(session_data: dict) -> str:
    """
    Persists a chat session to disk as a JSON file in data/chats/{session_id}.json.
    Updates the session ID and timestamps, and returns the session ID.
    Uses atomic file replacement for Windows filesystem safety.
    """
    ensure_storage_dir()

    session_id = session_data.get("id")
    if not session_id:
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        short_uuid = uuid.uuid4().hex[:6]
        session_id = f"session_{timestamp_str}_{short_uuid}"
        session_data["id"] = session_id

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not session_data.get("created_at"):
        session_data["created_at"] = now_str
    session_data["updated_at"] = now_str

    if not session_data.get("title"):
        summary = ""
        analysis = session_data.get("analysis_result")
        if isinstance(analysis, dict):
            summary = analysis.get("case_summary", "")
        session_data["title"] = generate_session_title(session_data.get("case_facts", ""), summary)

    safe_filename = re.sub(r"[^A-Za-z0-9_\-]", "_", str(session_id)) + ".json"
    file_path = os.path.join(CHATS_DIR, safe_filename)

    temp_path = file_path + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2, default=str)

    try:
        os.replace(temp_path, file_path)
    except Exception:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
        os.rename(temp_path, file_path)

    try:
        log_event("CHAT_SESSION_SAVED", f"Session saved: {session_id} - Title: {session_data.get('title')}")
    except Exception:
        pass

    return session_id

def load_chat_session(session_id: str) -> dict | None:
    """
    Loads and returns a chat session from disk by its session ID.
    Returns None if the file is not found or cannot be parsed.
    """
    if not session_id:
        return None

    safe_filename = re.sub(r"[^A-Za-z0-9_\-]", "_", str(session_id)) + ".json"
    file_path = os.path.join(CHATS_DIR, safe_filename)

    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return None
    except Exception as e:
        try:
            log_event("CHAT_SESSION_LOAD_ERROR", f"Error loading {session_id}: {str(e)}")
        except Exception:
            pass
        return None

def list_chat_sessions() -> list[dict]:
    """
    Lists all saved chat sessions ordered by updated_at descending (most recent first).
    Returns lightweight metadata dicts for fast UI rendering.
    Safely ignores corrupted, temporary, or non-JSON files.
    """
    ensure_storage_dir()
    sessions = []

    try:
        file_list = os.listdir(CHATS_DIR)
    except Exception:
        return []

    for fname in file_list:
        if not fname.endswith(".json") or fname.endswith(".tmp"):
            continue

        file_path = os.path.join(CHATS_DIR, fname)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict):
                continue

            facts = data.get("case_facts", "")
            summary = ""
            if isinstance(data.get("analysis_result"), dict):
                summary = data["analysis_result"].get("case_summary", "")

            snippet_source = summary or facts or "No case facts provided."
            snippet = " ".join(str(snippet_source).split())
            if len(snippet) > 75:
                snippet = snippet[:72] + "..."

            sessions.append({
                "id": str(data.get("id") or fname[:-5]),
                "title": str(data.get("title") or "Untitled Session"),
                "created_at": str(data.get("created_at") or "Unknown"),
                "updated_at": str(data.get("updated_at") or "Unknown"),
                "case_snippet": snippet,
                "message_count": len(data.get("chat_history") or []),
                "has_analysis": bool(data.get("analysis_result"))
            })
        except Exception:
            continue

    sessions.sort(key=lambda x: (x.get("updated_at", ""), x.get("created_at", "")), reverse=True)
    return sessions

def create_new_chat_on_same_case(current_facts: str, current_analysis: dict, current_provisions: list) -> dict:
    """
    Creates and persists a fresh follow-up chat session grounded in the same case analysis.
    Preserves case facts, analysis, and retrieved provisions, while providing a clean chat history.
    Accurately calculates thread number using regex matching against existing session titles.
    """
    existing = list_chat_sessions()
    base_title = generate_session_title(current_facts, (current_analysis or {}).get("case_summary", ""))

    # Find highest existing thread index for this specific base title
    max_thread = 1
    found_any = False
    thread_pattern = re.compile(rf"^{re.escape(base_title)}(?:\s*\(Thread\s*(\d+)\))?$", re.IGNORECASE)

    for s in existing:
        title = s.get("title", "")
        match = thread_pattern.match(title)
        if match:
            found_any = True
            num_str = match.group(1)
            if num_str and num_str.isdigit():
                max_thread = max(max_thread, int(num_str))

    if found_any:
        new_title = f"{base_title} (Thread {max_thread + 1})"
    else:
        new_title = f"{base_title} (Thread 2)"

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    short_uuid = uuid.uuid4().hex[:6]
    session_id = f"session_{timestamp_str}_{short_uuid}"

    session_data = {
        "id": session_id,
        "title": new_title,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "case_facts": current_facts,
        "analysis_result": current_analysis,
        "all_provisions": list(current_provisions or []),
        "chat_history": []
    }
    save_chat_session(session_data)
    return session_data

def delete_chat_session(session_id: str) -> bool:
    """Deletes a chat session file from disk."""
    if not session_id:
        return False
    safe_filename = re.sub(r"[^A-Za-z0-9_\-]", "_", str(session_id)) + ".json"
    file_path = os.path.join(CHATS_DIR, safe_filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            try:
                log_event("CHAT_SESSION_DELETED", f"Session deleted: {session_id}")
            except Exception:
                pass
            return True
        except Exception:
            return False
    return False

def clear_all_chat_sessions() -> int:
    """Deletes all saved chat sessions."""
    ensure_storage_dir()
    deleted_count = 0
    try:
        for fname in os.listdir(CHATS_DIR):
            if fname.endswith(".json"):
                try:
                    os.remove(os.path.join(CHATS_DIR, fname))
                    deleted_count += 1
                except Exception:
                    pass
    except Exception:
        pass
    return deleted_count

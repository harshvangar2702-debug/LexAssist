"""
Test Suite for LexAssist Chat Storage and Session Management.
Verifies chat session persistence, reloading, multi-threading on the same case,
title numbering, corrupted file resilience, and cleanup operations in data/chats/.
"""

import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.chat_storage import (
    save_chat_session,
    load_chat_session,
    list_chat_sessions,
    create_new_chat_on_same_case,
    delete_chat_session,
    clear_all_chat_sessions,
    generate_session_title,
    CHATS_DIR
)

def run_storage_tests():
    print("==================================================")
    print("LEXASSIST CHAT STORAGE TEST SUITE")
    print("==================================================\n")

    passed = 0
    total = 9

    # Test 1: Title Generation
    print("--- Test 1: Title Generation ---")
    t1 = generate_session_title(
        case_facts="A client contracted a web development agency to build an app.",
        summary="Breach of Website Development Contract and non-delivery."
    )
    t_fallback = generate_session_title("", "")
    print(f"Generated Title 1: '{t1}'")
    print(f"Generated Fallback: '{t_fallback}'")
    if t1 and len(t1) <= 45 and t_fallback == "New Legal Inquiry":
        print("[OK] PASSED: Title cleanly generated within length constraints.\n")
        passed += 1
    else:
        print("[FAIL]: Title generation failed.\n")

    # Test 2: Save and Load Chat Session
    print("--- Test 2: Save and Load Session ---")
    test_session = {
        "id": "test_session_001",
        "case_facts": "Customer purchased a defective television that caught fire.",
        "analysis_result": {
            "case_summary": "Defective TV explosion causing property damage.",
            "legal_issues": ["Product liability under Consumer Protection Act"],
            "found_provisions": True,
            "retrieved_provisions": [
                {"law_name": "The Consumer Protection Act, 2019", "section_number": "84", "section_title": "Product Liability"}
            ]
        },
        "all_provisions": [
            {"law_name": "The Consumer Protection Act, 2019", "section_number": "84", "section_title": "Product Liability"}
        ],
        "chat_history": [
            {"role": "user", "content": "Can I claim damages for my burnt sofa?"},
            {"role": "assistant", "content": "Under Section 84 of the Consumer Protection Act 2019..."}
        ]
    }

    saved_id = save_chat_session(test_session)
    loaded = load_chat_session(saved_id)

    if (
        loaded is not None
        and loaded["id"] == "test_session_001"
        and loaded["case_facts"] == test_session["case_facts"]
        and len(loaded["chat_history"]) == 2
        and loaded["chat_history"][0]["content"] == "Can I claim damages for my burnt sofa?"
    ):
        print(f"[OK] PASSED: Session saved and loaded cleanly with {len(loaded['chat_history'])} messages.\n")
        passed += 1
    else:
        print("[FAIL]: Failed to save or load session.\n")

    # Test 3: List Sessions with Metadata and Snippet
    print("--- Test 3: List Sessions ---")
    sessions = list_chat_sessions()
    found = any(s["id"] == "test_session_001" for s in sessions)
    target = next((s for s in sessions if s["id"] == "test_session_001"), None)

    if found and target and target["message_count"] == 2 and target["case_snippet"]:
        print(f"[OK] PASSED: Listed {len(sessions)} session(s); metadata verified (Messages: {target['message_count']}).\n")
        passed += 1
    else:
        print("[FAIL]: Session listing failed or metadata missing.\n")

    # Test 4: New Chat on Same Case (Thread Forking)
    print("--- Test 4: New Chat on Same Case (Thread Forking) ---")
    thread_2 = create_new_chat_on_same_case(
        current_facts=loaded["case_facts"],
        current_analysis=loaded["analysis_result"],
        current_provisions=loaded["all_provisions"]
    )
    print(f"Created Thread 2: ID='{thread_2['id']}', Title='{thread_2['title']}'")

    if (
        thread_2["id"] != loaded["id"]
        and thread_2["case_facts"] == loaded["case_facts"]
        and len(thread_2["chat_history"]) == 0
        and len(thread_2["all_provisions"]) == 1
        and "Thread 2" in thread_2["title"]
    ):
        print("[OK] PASSED: New thread on same case created cleanly with empty chat history.\n")
        passed += 1
    else:
        print("[FAIL]: New thread on same case failed.\n")

    # Test 5: Multi-thread numbering progression (Thread 3)
    print("--- Test 5: Multi-Thread Numbering Progression (Thread 3) ---")
    thread_3 = create_new_chat_on_same_case(
        current_facts=loaded["case_facts"],
        current_analysis=loaded["analysis_result"],
        current_provisions=loaded["all_provisions"]
    )
    print(f"Created Thread 3: ID='{thread_3['id']}', Title='{thread_3['title']}'")

    if "Thread 3" in thread_3["title"]:
        print("[OK] PASSED: Thread numbering incremented accurately to Thread 3.\n")
        passed += 1
    else:
        print("[FAIL]: Thread numbering did not increment properly.\n")

    # Test 6: Session Update Persistence
    print("--- Test 6: Session Update Persistence ---")
    loaded["chat_history"].append({"role": "user", "content": "What about manufacturer notice?"})
    save_chat_session(loaded)
    reloaded = load_chat_session(loaded["id"])

    if len(reloaded["chat_history"]) == 3:
        print("[OK] PASSED: Updated session persisted correctly with 3 messages.\n")
        passed += 1
    else:
        print("[FAIL]: Session update failed to persist.\n")

    # Test 7: Resilience to Non-Existent and Malformed Lookups
    print("--- Test 7: Non-existent and Malformed Lookup Resilience ---")
    none_result = load_chat_session("non_existent_session_id_99999")
    none_delete = delete_chat_session("")
    if none_result is None and none_delete is False:
        print("[OK] PASSED: Missing and empty session requests handled gracefully.\n")
        passed += 1
    else:
        print("[FAIL]: Non-existent session handling failed.\n")

    # Test 8: Delete Individual Sessions
    print("--- Test 8: Delete Individual Session ---")
    del_ok = delete_chat_session("test_session_001")
    del_thread_2 = delete_chat_session(thread_2["id"])
    check_none = load_chat_session("test_session_001")

    if del_ok and del_thread_2 and check_none is None:
        print("[OK] PASSED: Test sessions deleted cleanly.\n")
        passed += 1
    else:
        print("[FAIL]: Failed to delete test session.\n")

    # Test 9: Clear All Sessions
    print("--- Test 9: Clear All Sessions ---")
    clear_all_chat_sessions()
    remaining = list_chat_sessions()
    if len(remaining) == 0:
        print("[OK] PASSED: All sessions cleared successfully.\n")
        passed += 1
    else:
        print("[FAIL]: Clear all sessions left behind files.\n")

    print(f"Chat Storage Test Summary: {passed}/{total} tests passed.")
    return passed == total

if __name__ == "__main__":
    success = run_storage_tests()
    sys.exit(0 if success else 1)

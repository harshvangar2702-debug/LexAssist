"""
Standalone Retrieval Test Script for LexAssist.
Test 6: Verifies that known legal queries return relevant statutory provisions from ChromaDB.
"""

import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from retrieval.search import search_provisions

def run_retrieval_tests():
    print("==================================================")
    print("LEXASSIST RETRIEVAL TEST SUITE (TEST-06)")
    print("==================================================\n")

    test_cases = [
        {
            "name": "Contract Breach & Damages",
            "query": "What happens when a contract is broken and one party suffers financial loss?",
            "expected_law": "The Indian Contract Act, 1872",
            "expected_sec": ["73", "74", "75", "39"]
        },
        {
            "name": "Unauthorized Computer Access / Hacking",
            "query": "A person accesses a computer network without permission and downloads sensitive data.",
            "expected_law": "The Information Technology Act, 2000",
            "expected_sec": ["43", "66", "66B"]
        },
        {
            "name": "Defective Product & Product Liability",
            "query": "A consumer bought a product that was defective in design and caused injury.",
            "expected_law": "The Consumer Protection Act, 2019",
            "expected_sec": ["84", "83", "2", "82", "85", "86"]
        }
    ]

    passed = 0
    for i, test in enumerate(test_cases, 1):
        print(f"--- Scenario {i}: {test['name']} ---")
        print(f"Query: \"{test['query']}\"")
        results = search_provisions(test["query"], top_k=3, distance_threshold=0.90)

        if not results:
            print("[FAIL]: No provisions retrieved.\n")
            continue

        print(f"Retrieved {len(results)} provision(s):")
        matched_expected = False
        for res in results:
            sec = res["section_number"]
            law = res["law_name"]
            dist = res["distance"]
            title = res["section_title"]
            print(f"  * {law} | Section {sec}: {title} (Distance: {dist})")
            if res["law_name"] == test["expected_law"] and sec in test["expected_sec"]:
                matched_expected = True

        if matched_expected:
            print("[OK] PASSED: Correct expected statutory section retrieved.\n")
            passed += 1
        else:
            print("[WARNING]: Results retrieved, but expected specific section was not in top results.\n")

    print(f"Retrieval Test Summary: {passed}/{len(test_cases)} scenarios passed.")
    return passed == len(test_cases)

if __name__ == "__main__":
    run_retrieval_tests()


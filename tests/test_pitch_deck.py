"""
Verification Test Suite for LexAssist Business Pitch Deck
Validates slide count, dimensions, titles, speaker notes, and content integrity.
"""

import os
from pptx import Presentation
from pptx.util import Inches

def test_pitch_deck():
    pptx_path = r"d:\vs code\Entrepenuarship\LexAssist_Business_Pitch.pptx"
    assert os.path.exists(pptx_path), f"File {pptx_path} does not exist!"
    assert os.path.getsize(pptx_path) > 10000, f"File size too small: {os.path.getsize(pptx_path)} bytes"

    prs = Presentation(pptx_path)
    
    # 1. Slide Count
    assert len(prs.slides) == 12, f"Expected 12 slides, found {len(prs.slides)}"

    # 2. Aspect Ratio (16:9 Widescreen)
    width_in = prs.slide_width / Inches(1)
    height_in = prs.slide_height / Inches(1)
    assert abs(width_in - 13.333) < 0.1, f"Expected width ~13.333, got {width_in}"
    assert abs(height_in - 7.5) < 0.1, f"Expected height 7.5, got {height_in}"

    # 3. Slide Content and Notes Inspection
    expected_topics = [
        "LexAssist",
        "PROBLEM",
        "PROPOSED SOLUTION",
        "TECHNOLOGY",
        "TARGET CUSTOMERS",
        "MARKET",
        "BUSINESS MODEL",
        "COST",
        "MARKETING",
        "FUTURE SCOPE",
        "ASK",
        "CLOSING PITCH"
    ]

    for idx, slide in enumerate(prs.slides):
        all_text = " ".join([shape.text_frame.text for shape in slide.shapes if shape.has_text_frame])
        assert len(all_text) > 50, f"Slide {idx+1} has insufficient text content!"
        
        # Verify speaker notes are populated
        notes = slide.notes_slide.notes_text_frame.text
        assert len(notes.strip()) > 20, f"Slide {idx+1} is missing speaker notes!"

        # Verify topic presence
        matched = any(topic.lower() in all_text.lower() for topic in expected_topics)
        assert matched, f"Slide {idx+1} content did not match expected topics: {all_text[:100]}"
        print(f"Slide {idx+1:02d}: Verified ({len(slide.shapes)} shapes, {len(all_text)} chars text, {len(notes)} chars notes)")

    print("\nALL 12 SLIDES VERIFIED SUCCESSFULLY!")

if __name__ == "__main__":
    test_pitch_deck()

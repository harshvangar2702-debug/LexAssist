"""
LexAssist Business Pitch Presentation Generator
Generates a 12-slide presentation deck adhering strictly to:
- White/light-shade backgrounds (zero dark backgrounds)
- Professional typography, cards, and data metrics
- 16:9 widescreen layout (13.333" x 7.5")
- Complete financial unit economics, competitive matrix, and GTM strategy
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Design System Color Tokens (Strict Light Theme)
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_BG_LIGHT = RGBColor(248, 250, 252)       # Light Slate #F8FAFC
COLOR_SURFACE_CARD = RGBColor(255, 255, 255)   # Pure White Card #FFFFFF
COLOR_BORDER = RGBColor(226, 232, 240)         # Hairline Border #E2E8F0
COLOR_PRIMARY_NAVY = RGBColor(11, 25, 44)      # Oxford Deep Navy #0B192C
COLOR_TEXT_CHARCOAL = RGBColor(30, 41, 59)     # Slate-800 #1E293B
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)     # Slate-500 #64748B
COLOR_ACCENT_GOLD = RGBColor(197, 160, 89)     # Antique Gold #C5A059
COLOR_METRIC_EMERALD = RGBColor(15, 118, 110)  # Trust Emerald #0F766E
COLOR_ACCENT_AMBER = RGBColor(180, 83, 9)      # Warning Amber #B45309
COLOR_PILL_BG = RGBColor(241, 245, 249)        # Pill Tag Background #F1F5F9

LOGO_SOURCE_PATH = r"C:\Users\Harsh\.gemini\antigravity-ide\brain\56186390-faed-4da1-9186-38b3e763a91e\lexassist_logo_1793117807292.jpg"
OUTPUT_PPTX_PATH = r"d:\vs code\Entrepenuarship\LexAssist_Business_Pitch.pptx"

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # Blank slide

    def apply_slide_background(slide):
        """Applies a crisp pure white background with subtle top accent line."""
        bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = COLOR_WHITE
        bg_shape.line.fill.background()

        # Subtle gold top brand bar (0.08 inch)
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.08))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = COLOR_ACCENT_GOLD
        top_bar.line.fill.background()

        # Subtle footer text
        footer = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.7), Inches(0.3))
        tf = footer.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = "LexAssist — Zero-Hallucination AI Legal Research | Confidential Business Pitch"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_TEXT_MUTED

    def add_header(slide, title, category=None):
        """Creates an authoritative legaltech header zone."""
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_top = 0
        tf.margin_bottom = 0
        tf.margin_left = 0
        tf.margin_right = 0

        if category:
            p_cat = tf.paragraphs[0]
            p_cat.text = category.upper()
            p_cat.font.name = "Segoe UI"
            p_cat.font.size = Pt(10)
            p_cat.font.bold = True
            p_cat.font.color.rgb = COLOR_ACCENT_GOLD
            p_title = tf.add_paragraph()
        else:
            p_title = tf.paragraphs[0]

        p_title.text = title
        p_title.font.name = "Segoe UI"
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_PRIMARY_NAVY

    def add_card(slide, left, top, width, height, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER):
        """Draws a rounded card container."""
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # ==========================================================
    # SLIDE 1: TITLE & COVER
    # ==========================================================
    slide1 = prs.slides.add_slide(blank_layout)
    apply_slide_background(slide1)

    # Embed High-Resolution Logo
    if os.path.exists(LOGO_SOURCE_PATH):
        slide1.shapes.add_picture(LOGO_SOURCE_PATH, Inches(1.0), Inches(1.8), Inches(3.8), Inches(3.8))

    # Title & Tagline Box
    title_box = slide1.shapes.add_textbox(Inches(5.2), Inches(1.8), Inches(7.3), Inches(4.5))
    tf1 = title_box.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "BUSINESS PITCH PRESENTATION"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_GOLD

    p = tf1.add_paragraph()
    p.text = "LexAssist"
    p.font.name = "Segoe UI"
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_NAVY
    p.space_after = Pt(10)

    p = tf1.add_paragraph()
    p.text = "Zero-Hallucination AI Legal Research Assistant for Indian Law"
    p.font.name = "Segoe UI"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_METRIC_EMERALD
    p.space_after = Pt(14)

    p = tf1.add_paragraph()
    p.text = (
        "Empowering 1.5 million advocates and 200,000+ law students with local-first, "
        "statutorily-grounded AI intelligence. Decoupling legal reasoning from model memory "
        "to deliver 100% verifiable citations from official India Code enactments."
    )
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT_CHARCOAL
    p.space_after = Pt(20)

    # Metadata pills
    p = tf1.add_paragraph()
    p.text = "Venture Track: LegalTech & Enterprise AI  |  Jurisdiction: India 🇮🇳  |  Stage: Working MVP"
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MUTED

    slide1.notes_slide.notes_text_frame.text = (
        "Good morning esteemed judges and evaluators. Today, we are proud to introduce LexAssist—an AI legal "
        "research assistant engineered specifically to solve the single greatest hazard preventing artificial "
        "intelligence from entering the Indian courtroom: AI hallucination. We have developed a fully working "
        "local-first platform that indexes official government statutes, delivers deterministic citations, and "
        "refuses to invent law."
    )

    # ==========================================================
    # SLIDE 2: THE PROBLEM
    # ==========================================================
    slide2 = prs.slides.add_slide(blank_layout)
    apply_slide_background(slide2)
    add_header(slide2, "The Real-World Problem: Research Paralysis & Hallucination Risk", "01. PROBLEM STATEMENT")

    card_w = Inches(3.64)
    card_h = Inches(5.1)
    top_pos = Inches(1.6)

    # Card 1: Drowning in Volume
    add_card(slide2, Inches(0.8), top_pos, card_w, card_h)
    tb = slide2.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.2), card_w - Inches(0.4), card_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "1. Massive Time Drain"
    p.font.name = "Segoe UI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_NAVY
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "Who faces it:"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_ACCENT_AMBER
    p = tf.add_paragraph()
    p.text = "1.5M practicing Indian advocates and 200,000+ law students.\n"
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT_CHARCOAL

    p = tf.add_paragraph()
    p.text = "The Reality:"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_PRIMARY_NAVY
    p = tf.add_paragraph()
    p.text = (
        "• Junior advocates spend 15 to 20 hours per week manually navigating hundreds of pages of statutory enactments, gazettes, and schedules.\n"
        "• 4.4 Crore cases are currently pending in Indian courts; research bottlenecks directly compound judicial delays.\n"
        "• Solo practitioners in Tier-2/3 courts cannot afford massive research chambers."
    )
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT_CHARCOAL

    # Card 2: Keyword Inefficiency
    add_card(slide2, Inches(4.84), top_pos, card_w, card_h)
    tb = slide2.shapes.add_textbox(Inches(5.04), top_pos + Inches(0.2), card_w - Inches(0.4), card_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "2. Keyword Search Failure"
    p.font.name = "Segoe UI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_NAVY
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "The Friction:"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_ACCENT_AMBER
    p = tf.add_paragraph()
    p.text = (
        "• Incumbent legal databases (SCC Online, Manupatra) rely heavily on exact-string matching.\n"
        "• When an advocate enters natural case facts (e.g., 'agency missed deadline after advance payment'), keyword search fails to map to statutory terms like 'breach of contract' or Section 73.\n"
        "• Requires knowing the exact legal conclusion before finding the statute."
    )
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT_CHARCOAL

    # Card 3: Hallucination Hazard
    add_card(slide2, Inches(8.88), top_pos, card_w, card_h)
    tb = slide2.shapes.add_textbox(Inches(9.08), top_pos + Inches(0.2), card_w - Inches(0.4), card_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "3. LLM Hallucinations"
    p.font.name = "Segoe UI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_AMBER
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "The Dangerous Trap:"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_ACCENT_AMBER
    p = tf.add_paragraph()
    p.text = (
        "• When lawyers turn to ChatGPT or Claude, generic LLMs hallucinate non-existent sections, cite fake rulings, or cite repealed colonial laws.\n"
        "• Citing a hallucinated law in court leads to contempt petitions, disbarment, or loss of client cases.\n"
        "• Generic AI cannot be trusted with legal counsel."
    )
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT_CHARCOAL

    slide2.notes_slide.notes_text_frame.text = (
        "The problem we are addressing is three-fold. First, Indian lawyers spend 15 to 20 hours every week "
        "wading through statutory acts across 44 million pending cases. Second, incumbent databases like SCC Online "
        "rely on rigid keyword searches that fail when fed real-world factual scenarios. Third, and most dangerous, "
        "commercial AI tools like ChatGPT hallucinate section numbers and cite repealed statutes. In law, hallucination "
        "is not just an error—it is professional malpractice."
    )

    # ==========================================================
    # SLIDE 3: PROPOSED SOLUTION
    # ==========================================================
    slide3 = prs.slides.add_slide(blank_layout)
    apply_slide_background(slide3)
    add_header(slide3, "LexAssist: Grounded, Verifiable Legal Intelligence", "02. PROPOSED SOLUTION")

    # Left Column: Solution Architecture Narrative
    add_card(slide3, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.1))
    tb = slide3.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(6.2), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "How LexAssist Solves the Legal Research Crisis"
    p.font.name = "Segoe UI"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_NAVY
    p.space_after = Pt(12)

    bullet_points = [
        ("Grounded Retrieval-Augmented Generation (RAG):", 
         "Instead of relying on LLM memory weights, LexAssist indexes official legislative texts directly from government gazettes (indiacode.nic.in)."),
        ("Boundary-Aware Statutory Ingestion:",
         "Laws are parsed cleanly at exact Section and Article boundaries, preserving explanations, illustrations, and legislative schedules intact."),
        ("Deterministic Provenance & Citations:",
         "Every response provides the exact statutory title, verbatim legal clause, and direct clickable link to the official gazette repository."),
        ("Mandatory Refusal (Zero-Hallucination):",
         "If an entered dispute falls outside indexed law, the AI explicitly reports that no provision was found. It is strictly prohibited from inventing sections.")
    ]

    for title, desc in bullet_points:
        p = tf.add_paragraph()
        p.text = f"• {title} "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_PRIMARY_NAVY
        p2 = tf.add_paragraph()
        p2.text = f"   {desc}"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_TEXT_CHARCOAL
        p2.space_after = Pt(6)

    # Right Column: Visual Feature Highlights
    add_card(slide3, Inches(7.8), Inches(1.6), Inches(4.7), Inches(5.1))
    tb_r = slide3.shapes.add_textbox(Inches(8.0), Inches(1.8), Inches(4.3), Inches(4.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Core Product Capabilities"
    p.font.name = "Segoe UI"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_METRIC_EMERALD
    p.space_after = Pt(14)

    caps = [
        ("📁 Multimodal Case Analysis", "Accepts plain text, case PDF filings, and scanned evidence photos via Gemini Multimodal OCR."),
        ("⚖️ Grounded Follow-up Chat", "Allows lawyers to ask follow-up questions constrained strictly to retrieved provisions."),
        ("💾 Persistent Case Workspaces", "Auto-saves research sessions, enables multiple exploration threads per dispute without data loss."),
        ("🔒 Local-First Data Privacy", "Vector embeddings and search run 100% locally on user machine; sensitive case files stay private.")
    ]

    for cap_title, cap_desc in caps:
        p = tf_r.add_paragraph()
        p.text = cap_title
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_PRIMARY_NAVY
        p2 = tf_r.add_paragraph()
        p2.text = cap_desc
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_TEXT_CHARCOAL
        p2.space_after = Pt(10)

    slide3.notes_slide.notes_text_frame.text = (
        "Our solution is LexAssist. Unlike raw chatbots, LexAssist uses a grounded RAG architecture. We index official "
        "government legislation from indiacode.nic.in, chunk statutes precisely at Section boundaries, and retrieve "
        "matching provisions locally using ChromaDB. Gemini then synthesizes an objective legal brief using ONLY the "
        "retrieved text. If a law is not in our database, the system explicitly refuses to answer rather than inventing "
        "a hallucination."
    )

    # ==========================================================
    # SLIDE 4: INNOVATION / TECHNOLOGY
    # ==========================================================
    slide4 = prs.slides.add_slide(blank_layout)
    apply_slide_background(slide4)
    add_header(slide4, "Engineering Innovation: Zero-Hallucination Pipeline", "03. TECHNOLOGY & ARCHITECTURE")

    # 4 Architecture Pillars Grid (2x2)
    grid_w = Inches(5.6)
    grid_h = Inches(2.4)

    tech_pillars = [
        ("1. Boundary-Aware Statutory Chunking",
         "Traditional naive RAG splits text every 500 characters, severing sections in half and losing legal exceptions. LexAssist parses statutory enactments precisely at Section/Article headers, packaging statutory text, official explanations, and legislative illustrations in a single atomic vector unit.",
         Inches(0.8), Inches(1.6)),
        ("2. Dual-Stage Distance Guardrail (<0.59)",
         "We implement an algorithmic cosine distance threshold of 0.59. If user queries do not reach this threshold, the LLM synthesis is never triggered. The system immediately outputs an explicit non-retrieval notification, acting as a deterministic firewall against off-topic generation.",
         Inches(6.8), Inches(1.6)),
        ("3. Local-First Vector Storage (ChromaDB)",
         "Statutes are indexed and queried on-device via ChromaDB disk persistence. Confidential client facts do not reside in cloud vector stores, eliminating third-party data leakage and ensuring offline-capable resilience for district court practice.",
         Inches(0.8), Inches(4.3)),
        ("4. Constrained LLM Synthesis (Gemini 2.5 Flash)",
         "Gemini is governed by a strict zero-hallucination prompt envelope: temperature set to 0.1, instructed strictly to act as a grounded compiler rather than a creative writer. Every statutory proposition links to its verified India Code handle.",
         Inches(6.8), Inches(4.3)),
    ]

    for title, desc, left, top in tech_pillars:
        add_card(slide4, left, top, grid_w, grid_h)
        tb = slide4.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), grid_w - Inches(0.4), grid_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_NAVY
        p.space_after = Pt(6)
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_TEXT_CHARCOAL

    slide4.notes_slide.notes_text_frame.text = (
        "Here is the engineering core that makes LexAssist unique. First, we engineered boundary-aware statutory "
        "chunking—we never split legal clauses arbitrarily. Second, we built a dual-stage distance firewall: if semantic "
        "similarity is below our 0.59 threshold, the LLM is never invoked. Third, our local-first vector architecture keeps "
        "confidential case files on the client machine. Fourth, Gemini operates as a grounded reasoning compiler with "
        "zero creative liberty."
    )

    # ==========================================================
    # SLIDE 5: TARGET CUSTOMERS
    # ==========================================================
    slide5 = prs.slides.add_slide(blank_layout)
    apply_slide_background(slide5)
    add_header(slide5, "Target Customers: Who Will Buy & Use LexAssist?", "04. CUSTOMER PERSONAS & SEGMENTS")

    cust_w = Inches(3.64)
    cust_h = Inches(5.1)

    segments = [
        ("Segment 1: Solo Advocates & Chambers",
         "1,500,000+ Registered Advocates in India",
         COLOR_PRIMARY_NAVY,
         [
             ("Who They Are:", "Solo practitioners and small 2-5 person chambers in High Courts & District Courts."),
             ("Current Pain:", "Cannot afford expensive enterprise databases (₹40,000+/year). Lose 3-4 hours daily manually searching enactments."),
             ("Value Proposition:", "Affordable, desktop-ready legal assistant that delivers verified section matches in 5 seconds."),
             ("Willingness to Pay:", "₹999 / month per advocate.")
         ],
         Inches(0.8)),
        ("Segment 2: Law Students & Scholars",
         "200,000+ Students across 1,700 Law Schools",
         COLOR_METRIC_EMERALD,
         [
             ("Who They Are:", "Undergraduate (BA LLB) and postgraduate scholars preparing for moot courts, exams, and litigation internships."),
             ("Current Pain:", "University IP logins restricted to campus libraries; struggle with statutory analysis on real cases."),
             ("Value Proposition:", "Free / low-cost learning copilot that teaches grounded statutory reasoning and legal drafting."),
             ("Willingness to Pay:", "Freemium entry; ₹299/mo for advanced features.")
         ],
         Inches(4.84)),
        ("Segment 3: Corporate Legal & In-House",
         "60,000+ Enterprises & Legal Tech Ops",
         COLOR_ACCENT_GOLD,
         [
             ("Who They Are:", "In-house general counsels, contract managers, and compliance officers in fintech, e-commerce, and SaaS."),
             ("Current Pain:", "Need rapid cross-referencing of IT Act, Consumer Protection, and Contract provisions during audit."),
             ("Value Proposition:", "Audit-ready statutory summaries with direct government gazette links for compliance reporting."),
             ("Willingness to Pay:", "₹25,000 - ₹50,000 / month per organization.")
         ],
         Inches(8.88))
    ]

    for title, subtitle, color, points, left in segments:
        add_card(slide5, left, Inches(1.6), cust_w, cust_h)
        tb = slide5.shapes.add_textbox(left + Inches(0.2), Inches(1.8), cust_w - Inches(0.4), cust_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(2)

        p = tf.add_paragraph()
        p.text = subtitle
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.space_after = Pt(12)

        for heading, text in points:
            p = tf.add_paragraph()
            p.text = heading
            p.font.bold = True
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_PRIMARY_NAVY
            p2 = tf.add_paragraph()
            p2.text = text
            p2.font.size = Pt(10)
            p2.font.color.rgb = COLOR_TEXT_CHARCOAL
            p2.space_after = Pt(6)

    slide5.notes_slide.notes_text_frame.text = (
        "Our customer strategy targets three distinct tiers. Our primary revenue driver is India's 1.5 million practicing "
        "advocates, 85% of whom are solo or small chamber litigators priced out of legacy tools. Our adoption beachhead "
        "is 200,000 law students across 1,700 universities, who act as our product-led growth ambassadors. Finally, corporate "
        "compliance teams represent high-value enterprise accounts."
    )

    # ==========================================================
    # SLIDE 6: MARKET & COMPETITION
    # ==========================================================
    slide6 = prs.slides.add_slide(blank_layout)
    apply_slide_background(slide6)
    add_header(slide6, "Market Opportunity & Competitive Landscape", "05. MARKET & COMPETITION")

    # Top: TAM / SAM / SOM Metrics Row
    metric_w = Inches(3.64)
    metric_h = Inches(1.4)
    metrics_data = [
        ("₹15,000 Cr ($1.8B)", "TAM: Total Addressable Market", "Total Indian Legal, Compliance & RegTech Market by 2028", Inches(0.8)),
        ("₹3,200 Cr ($385M)", "SAM: Serviceable Addressable", "Litigation research and statutory workflow tools for Indian practitioners", Inches(4.84)),
        ("₹180 Cr ($22M)", "SOM: Serviceable Obtainable", "Target 15% penetration of tech-forward advocates & firms within 5 years", Inches(8.88)),
    ]

    for val, lbl, sub, left in metrics_data:
        add_card(slide6, left, Inches(1.6), metric_w, metric_h)
        tb = slide6.shapes.add_textbox(left + Inches(0.15), Inches(1.7), metric_w - Inches(0.3), metric_h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = val
        p.font.name = "Segoe UI"
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_NAVY
        p = tf.add_paragraph()
        p.text = lbl
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_METRIC_EMERALD
        p = tf.add_paragraph()
        p.text = sub
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_TEXT_MUTED

    # Bottom: Competitive Matrix Card
    add_card(slide6, Inches(0.8), Inches(3.2), Inches(11.72), Inches(3.6))
    tb_m = slide6.shapes.add_textbox(Inches(1.0), Inches(3.35), Inches(11.3), Inches(3.3))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True

    p = tf_m.paragraphs[0]
    p.text = "Competitive Positioning Matrix"
    p.font.name = "Segoe UI"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_NAVY
    p.space_after = Pt(8)

    # Comparison Table Text Frame
    comp_rows = [
        ("Feature / Dimension", "SCC Online / Manupatra", "ChatGPT / Generic AI", "Harvey AI", "LexAssist (Our Solution)"),
        ("Search Paradigm", "Exact Keyword Matching", "Ungrounded Generative", "Enterprise US/UK RAG", "Grounded Statutory Semantic RAG"),
        ("Hallucination Risk", "Low (Pure Database)", "CRITICAL (Fabricates Sections)", "Moderate (Model drift)", "ZERO (Enforced Refusal & Firewall)"),
        ("Statute Provenance", "Static Text Page", "None (Opaque / Hallucinated)", "Generic Links", "Exact India Code Link + Verbatim Text"),
        ("Data Privacy", "Cloud Search Logs", "Public Cloud Training Risk", "Enterprise Cloud Only", "Local-First On-Device Vector Store"),
        ("Annual Pricing", "₹35,000 – ₹60,000 / seat", "$240 / year (Unsafe)", "$12,000+ / seat (Foreign)", "₹9,990 / year (Affordable India SaaS)")
    ]

    for idx, row in enumerate(comp_rows):
        p = tf_m.add_paragraph()
        p.space_after = Pt(4)
        if idx == 0:
            p.text = f"{row[0]:<22} | {row[1]:<24} | {row[2]:<24} | {row[3]:<22} | {row[4]}"
            p.font.bold = True
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_ACCENT_GOLD
        else:
            p.text = f"{row[0]:<22} | {row[1]:<24} | {row[2]:<24} | {row[3]:<22} | {row[4]}"
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_PRIMARY_NAVY if "LexAssist" in row[4] else COLOR_TEXT_CHARCOAL

    slide6.notes_slide.notes_text_frame.text = (
        "The Indian LegalTech market represents a 15,000 Crore rupee opportunity. Looking at our competitive matrix: "
        "SCC Online and Manupatra are expensive legacy keyword tools with no semantic reasoning. ChatGPT has a fatal "
        "hallucination risk that makes it unusable for actual filings. Harvey AI is built for elite multi-million dollar "
        "US/UK firms at $1,000 a month. LexAssist occupies the sweet spot: zero hallucination, semantic intelligence, "
        "local-first privacy, and disruptive Indian pricing at ₹999 a month."
    )

    # ==========================================================
    # SLIDE 7: BUSINESS MODEL
    # ==========================================================
    slide7 = prs.slides.add_slide(blank_layout)
    apply_slide_background(slide7)
    add_header(slide7, "Business Model: Monetization & Pricing Tiers", "06. REVENUE & BUSINESS MODEL")

    tier_w = Inches(2.75)
    tier_h = Inches(5.1)
    tier_tops = Inches(1.6)

    tiers = [
        ("Community Free", "₹0", "Perpetual Free", COLOR_TEXT_MUTED, [
            "3 Core Central Acts indexed",
            "15 Case queries / day",
            "Plain text fact input",
            "Official India Code citations",
            "Standard community support",
            "Target: Law Students & Interns"
        ], Inches(0.8)),
        ("Advocate Pro", "₹999", "Per month (billed ₹9,990/yr)", COLOR_METRIC_EMERALD, [
            "ALL Central & State Acts",
            "UNLIMITED Case analyses",
            "Multimodal PDF & Scan upload",
            "Persistent Case History & Threads",
            "Grounded Interactive Follow-up Chat",
            "Priority Gemini 2.5 Flash Engine"
        ], Inches(3.79)),
        ("Chambers Team", "₹4,999", "Per month (includes 5 seats)", COLOR_PRIMARY_NAVY, [
            "Includes 5 Pro Advocate accounts",
            "Shared Chamber Case Dossiers",
            "Multi-associate collaboration",
            "Client Brief PDF Export",
            "Firm-wide search history audit",
            "Additional seat @ ₹799/mo"
        ], Inches(6.78)),
        ("Enterprise & API", "Custom", "From ₹25,000 / month", COLOR_ACCENT_GOLD, [
            "On-Premise Private Server deployment",
            "Custom Corporate Contract Indexing",
            "API Access for Legal ERPs / CRM",
            "Dedicated Account Manager & SLA",
            "Custom Security & Audit Reviews",
            "Target: Law Firms & Enterprises"
        ], Inches(9.77))
    ]

    for name, price, freq, color, feats, left in tiers:
        add_card(slide7, left, tier_tops, tier_w, tier_h)
        tb = slide7.shapes.add_textbox(left + Inches(0.15), tier_tops + Inches(0.2), tier_w - Inches(0.3), tier_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = name
        p.font.name = "Segoe UI"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = color

        p = tf.add_paragraph()
        p.text = price
        p.font.name = "Segoe UI"
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_NAVY

        p = tf.add_paragraph()
        p.text = freq
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.space_after = Pt(14)

        for feat in feats:
            p = tf.add_paragraph()
            p.text = f"✓ {feat}"
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_TEXT_CHARCOAL
            p.space_after = Pt(6)

    slide7.notes_slide.notes_text_frame.text = (
        "Our business model uses a freemium SaaS architecture. Our free community tier drives rapid viral adoption "
        "among law students and junior associates. Our core cash cow is the Advocate Pro plan at ₹999 per month, which "
        "unlocks the complete statutory database, multimodal document uploads, and persistent case threads. For law "
        "firms, we offer the Chambers Team plan at ₹4,999 for 5 seats, and enterprise licenses for corporate legal departments."
    )

    # ==========================================================
    # SLIDE 8: COST & PRICING (UNIT ECONOMICS)
    # ==========================================================
    slide8 = prs.slides.add_slide(blank_layout)
    apply_slide_background(slide8)
    add_header(slide8, "Cost Structure & Exceptional Unit Economics", "07. COST & PRICING")

    # Left: Unit Economics Breakdown
    add_card(slide8, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.1))
    tb = slide8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.6), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Monthly COGS per Active Pro User"
    p.font.name = "Segoe UI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_NAVY
    p.space_after = Pt(12)

    cost_items = [
        ("Gemini 2.5 Flash API Calls", "₹6.00", "Avg 150 queries/mo @ ₹0.04 per query"),
        ("Local ChromaDB Vector Compute", "₹2.00", "Zero cloud DB cost (client disk offload)"),
        ("Cloud Auth, Storage & Sync", "₹5.00", "Encrypted session sync & telemetry"),
        ("Payment Gateway & Billing (2%)", "₹19.98", "Razorpay / Stripe gateway fees"),
        ("TOTAL COGS PER USER / MONTH", "₹32.98", "Direct cost of delivering service"),
        ("PRO SELLING PRICE / MONTH", "₹999.00", "Retail subscription price"),
        ("GROSS PROFIT PER USER", "₹966.02", "96.7% Gross Margin")
    ]

    for title, val, note in cost_items:
        p = tf.add_paragraph()
        p.text = f"{title}: {val}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_METRIC_EMERALD if "PROFIT" in title or "MARGIN" in val else COLOR_PRIMARY_NAVY
        p2 = tf.add_paragraph()
        p2.text = f"   ({note})"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_TEXT_MUTED
        p2.space_after = Pt(4)

    # Right: Financial Health & SaaS Multiples
    add_card(slide8, Inches(7.1), Inches(1.6), Inches(5.42), Inches(5.1))
    tb_r = slide8.shapes.add_textbox(Inches(7.3), Inches(1.8), Inches(5.0), Inches(4.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Key SaaS Metrics & Ratios"
    p.font.name = "Segoe UI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_NAVY
    p.space_after = Pt(14)

    saas_metrics = [
        ("Customer Acquisition Cost (CAC)", "₹1,200", "Kept low via organic campus PLG and Bar Council demo workshops."),
        ("Customer Lifetime Value (LTV)", "₹11,988", "Assumes conservative 12-month average subscription lifespan @ ₹999/mo."),
        ("LTV / CAC Ratio", "10.0x", "World-class SaaS unit efficiency (industry benchmark > 3.0x)."),
        ("Payback Period", "1.2 Months", "Acquisition investment recouped in under 40 days of paid usage."),
        ("Target Year 1 ARR", "₹1.44 Crore", "Based on 1,200 active paid Pro subscribers by Month 12.")
    ]

    for metric, val, desc in saas_metrics:
        p = tf_r.add_paragraph()
        p.text = f"{metric} — {val}"
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_PRIMARY_NAVY
        p2 = tf_r.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_TEXT_CHARCOAL
        p2.space_after = Pt(8)

    slide8.notes_slide.notes_text_frame.text = (
        "Now let's examine our unit economics. Because LexAssist leverages local-first ChromaDB vector compute, we don't "
        "pay massive cloud database hosting fees. Our total cost to service one active subscriber making 150 queries a "
        "month is only ₹33. At our ₹999 price point, our gross margin is an astonishing 96.7%. With an estimated CAC of "
        "₹1,200 and an LTV of nearly ₹12,000, our LTV-to-CAC ratio is 10x, with payback achieved in just 1.2 months."
    )

    # ==========================================================
    # SLIDE 9: MARKETING STRATEGY
    # ==========================================================
    slide9 = prs.slides.add_slide(blank_layout)
    apply_slide_background(slide9)
    add_header(slide9, "Marketing Strategy: Product-Led Growth & Bar Channels", "08. GO-TO-MARKET STRATEGY")

    card_w = Inches(3.64)
    card_h = Inches(5.1)

    gtm_pillars = [
        ("Pillar 1: Campus-to-Chamber Flywheel",
         "Bottom-Up Organic Adoption",
         COLOR_PRIMARY_NAVY,
         [
             ("Moot Court Sponsorships:", "Partner with top National Law Universities (NLSIU, NALSAR, NUJS) as the official statutory research partner."),
             ("Student Ambassador Network:", "Empower law students with free accounts during their degree."),
             ("Graduation Conversion:", "When students transition to junior advocates in litigation chambers, they bring LexAssist as their indispensable research copilot.")
         ],
         Inches(0.8)),
        ("Pillar 2: Bar Council Demonstrations",
         "Direct Professional Roadshows",
         COLOR_METRIC_EMERALD,
         [
             ("Live Hallucination Challenge:", "Host live interactive workshops at High Court and District Bar Associations."),
             ("Real Case Teardowns:", "Pit LexAssist head-to-head against ChatGPT on stage, proving how ChatGPT hallucinates while LexAssist cites exact India Code provisions."),
             ("Chamber Bulk Onboarding:", "Onboard entire senior advocate chambers in 15-minute group workshops.")
         ],
         Inches(4.84)),
        ("Pillar 3: Content-Led Digital Trust",
         "Thought Leadership & Community",
         COLOR_ACCENT_GOLD,
         [
             ("Weekly Case Bulletins:", "Publish LinkedIn teardowns of trending Supreme Court and High Court disputes with statutory mindmaps."),
             ("Verified Report Watermark:", "Every PDF brief exported by LexAssist carries a digital verification badge with share link, driving viral referral loops."),
             ("BNS Transition Guides:", "Provide free migration cheat sheets helping advocates map old IPC sections to new BNS provisions.")
         ],
         Inches(8.88))
    ]

    for title, subtitle, color, points, left in gtm_pillars:
        add_card(slide9, left, Inches(1.6), card_w, card_h)
        tb = slide9.shapes.add_textbox(left + Inches(0.2), Inches(1.8), card_w - Inches(0.4), card_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(2)

        p = tf.add_paragraph()
        p.text = subtitle
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.space_after = Pt(12)

        for heading, text in points:
            p = tf.add_paragraph()
            p.text = heading
            p.font.bold = True
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_PRIMARY_NAVY
            p2 = tf.add_paragraph()
            p2.text = text
            p2.font.size = Pt(10)
            p2.font.color.rgb = COLOR_TEXT_CHARCOAL
            p2.space_after = Pt(8)

    slide9.notes_slide.notes_text_frame.text = (
        "Our go-to-market strategy avoids expensive mass-media advertising in favor of a targeted 3-pillar flywheel. "
        "First, our campus-to-chamber engine seeds LexAssist across 200,000 law students who graduate into law firms as "
        "power users. Second, we run live 'Hallucination Challenge' demos at High Court Bar Associations, proving our "
        "superiority over ChatGPT right before senior advocates. Third, every legal report exported carries our verified "
        "badge, creating a natural viral loop."
    )

    # ==========================================================
    # SLIDE 10: FUTURE SCOPE & ROADMAP
    # ==========================================================
    slide10 = prs.slides.add_slide(blank_layout)
    apply_slide_background(slide10)
    add_header(slide10, "Future Scope: Strategic Roadmap & Scaling", "09. DEVELOPMENT & SCALING ROADMAP")

    phase_w = Inches(3.64)
    phase_h = Inches(5.1)

    phases = [
        ("Phase 1: Foundation (Months 1–6)",
         "Full Central Acts & BNS Migration",
         COLOR_PRIMARY_NAVY,
         [
             ("Scale to 1,000+ Acts:", "Expand local vector index to cover all Indian central statutes, commercial schedules, and consumer rules."),
             ("BNS-IPC Migration Mapper:", "Automated bridge allowing advocates to input historic IPC, CrPC, and IEA sections and instantly retrieve corresponding provisions in BNS, BNSS, and BSA."),
             ("Desktop App Packaging:", "Electron / PyInstaller desktop installer with background auto-updates.")
         ],
         Inches(0.8)),
        ("Phase 2: Judicial Precedents (Months 7–12)",
         "High Court & Supreme Court Case Law",
         COLOR_METRIC_EMERALD,
         [
             ("Case Precedent Ingestion:", "Integrate official judgment datasets from Supreme Court e-Courts and High Courts."),
             ("Statutory Cross-Linking:", "When a section is retrieved, automatically link the top 3 landmark rulings interpreting that specific clause."),
             ("Drafting Assistant:", "Export structured legal research memos and factual chronologies directly into formatted Word (.docx) briefs.")
         ],
         Inches(4.84)),
        ("Phase 3: Vernacular & Enterprise (Months 13–24)",
         "Pan-India Regional AI & Compliance",
         COLOR_ACCENT_GOLD,
         [
             ("Multi-Lingual Indian Languages:", "Support case query retrieval in Hindi, Marathi, Tamil, Bengali, and Gujarati for Tier-2/3 district courts."),
             ("Enterprise Contract Audit:", "Allow corporate legal teams to upload 500-page vendor contracts and check statutory compliance automatically."),
             ("Law School LMS Integration:", "Direct plugin for university legal clinics.")
         ],
         Inches(8.88))
    ]

    for title, subtitle, color, points, left in phases:
        add_card(slide10, left, Inches(1.6), phase_w, phase_h)
        tb = slide10.shapes.add_textbox(left + Inches(0.2), Inches(1.8), phase_w - Inches(0.4), phase_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(2)

        p = tf.add_paragraph()
        p.text = subtitle
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.space_after = Pt(12)

        for heading, text in points:
            p = tf.add_paragraph()
            p.text = heading
            p.font.bold = True
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_PRIMARY_NAVY
            p2 = tf.add_paragraph()
            p2.text = text
            p2.font.size = Pt(10)
            p2.font.color.rgb = COLOR_TEXT_CHARCOAL
            p2.space_after = Pt(8)

    slide10.notes_slide.notes_text_frame.text = (
        "Our roadmap is divided into three execution horizons. In Phase 1, we expand to all 1,000+ Indian central acts "
        "and launch our proprietary BNS-IPC migration tool, which is critical given the recent criminal law overhaul. "
        "In Phase 2, we integrate landmark Supreme Court judgments to connect statutes with judicial interpretation. "
        "In Phase 3, we democratize justice across India by introducing vernacular language support in Hindi, Tamil, and "
        "Marathi for district courts."
    )

    # ==========================================================
    # SLIDE 11: THE ASK & USE OF FUNDS
    # ==========================================================
    slide11 = prs.slides.add_slide(blank_layout)
    apply_slide_background(slide11)
    add_header(slide11, "The Ask: Funding Requirements & Milestones", "10. CAPITAL REQUIREMENT & ALLOCATION")

    # Left: Funding & Allocation Card
    add_card(slide11, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.1))
    tb = slide11.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(5.4), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Pre-Seed Incubator Ask: ₹25,00,000"
    p.font.name = "Segoe UI"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_NAVY
    p.space_after = Pt(4)

    p = tf.add_paragraph()
    p.text = "12-Month Operating Runway to Achieve Scale"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_METRIC_EMERALD
    p.space_after = Pt(16)

    allocations = [
        ("45% (₹11.25 Lakhs) — Legal Corpus & Engineering",
         "Ingesting 1,000+ statutes, building automated gazette scrapers, hiring legal research interns for ground-truth verification of section vectors."),
        ("30% (₹7.50 Lakhs) — Go-To-Market & Bar Council Outreach",
         "Sponsoring 10 national moot court competitions, hosting 25 Bar Association demonstration workshops, and student ambassador grants."),
        ("25% (₹6.25 Lakhs) — Infrastructure, SOC-2 & Security",
         "Cloud authentication infrastructure, SSL/TLS audit, security penetration testing, and LLM reasoning API buffer.")
    ]

    for title, desc in allocations:
        p = tf.add_paragraph()
        p.text = title
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_PRIMARY_NAVY
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_TEXT_CHARCOAL
        p2.space_after = Pt(10)

    # Right: 12-Month Target Milestones
    add_card(slide11, Inches(7.1), Inches(1.6), Inches(5.42), Inches(5.1))
    tb_r = slide11.shapes.add_textbox(Inches(7.3), Inches(1.8), Inches(5.0), Inches(4.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "12-Month Target Milestones"
    p.font.name = "Segoe UI"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_GOLD
    p.space_after = Pt(14)

    goals = [
        ("🎯 15,000 Registered Users", "Reaching 10,000 law students and 5,000 practicing advocates within 12 months."),
        ("💼 1,200 Paid Pro Subscribers", "Generating ₹12 Lakhs monthly recurring revenue (₹1.44 Crore ARR)."),
        ("⚖️ 100% Central Acts Coverage", "Complete, verified index of all Indian central enactments and rules."),
        ("🚀 Institutional Partnerships", "MoUs signed with at least 5 National Law Universities and 3 State Bar Councils."),
        ("📈 Cash Flow Breakeven", "Achieving sustainable operating profitability by Month 9 of the deployment.")
    ]

    for title, desc in goals:
        p = tf_r.add_paragraph()
        p.text = title
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_PRIMARY_NAVY
        p2 = tf_r.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_TEXT_CHARCOAL
        p2.space_after = Pt(8)

    slide11.notes_slide.notes_text_frame.text = (
        "To execute this vision, we are seeking an investment or incubator grant of ₹25 Lakhs for a 12-month runway. "
        "45% of these funds will go directly into statutory corpus engineering and legal ground-truth verification. "
        "30% will fund our Bar Council and law school GTM campaigns, and 25% will secure our infrastructure and data security. "
        "With this capital, we will achieve 15,000 active users, 1,200 paid subscribers, and cross ₹1.4 Crore in ARR."
    )

    # ==========================================================
    # SLIDE 12: CLOSING PITCH
    # ==========================================================
    slide12 = prs.slides.add_slide(blank_layout)
    apply_slide_background(slide12)
    add_header(slide12, "Why Back LexAssist? The Irresistible Opportunity", "11. CLOSING PITCH & VISION")

    # Center Hero Vision Card
    add_card(slide12, Inches(0.8), Inches(1.6), Inches(11.72), Inches(5.1))
    tb_c = slide12.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(4.7))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    p = tf_c.paragraphs[0]
    p.text = "The Right Solution at India's Defining Legal Moment"
    p.font.name = "Segoe UI"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_NAVY
    p.space_after = Pt(12)

    pillars = [
        ("1. Perfect Regulatory Timing:", 
         "India is undergoing the largest legal overhaul in 160 years with the transition to Bharatiya Nyaya Sanhita (BNS). Every lawyer in India is forced to re-learn statutory mappings. LexAssist is their indispensable guide."),
        ("2. Real Technical Defensibility:", 
         "Zero-hallucination is not marketing fluff; it is enforced via boundary-aware chunking, vector distance firewalls, and local ChromaDB persistence. We solve the exact problem keeping AI out of courts."),
        ("3. High-Margin Scalability:", 
         "With 96.7% gross margins, an LTV/CAC ratio of 10x, and local-first compute efficiency, LexAssist is built for capital-efficient, high-velocity growth."),
        ("4. Mission of Justice:", 
         "By democratizing legal research at ₹999/month, we empower solo district court advocates to match the research horsepower of elite multi-partner corporate law firms.")
    ]

    for title, desc in pillars:
        p = tf_c.add_paragraph()
        p.text = title
        p.font.bold = True
        p.font.size = Pt(12.5)
        p.font.color.rgb = COLOR_METRIC_EMERALD
        p2 = tf_c.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_TEXT_CHARCOAL
        p2.space_after = Pt(8)

    p = tf_c.add_paragraph()
    p.text = "Let's build the future of Indian jurisprudence together. Thank you."
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT_GOLD
    p.space_after = Pt(4)

    p = tf_c.add_paragraph()
    p.text = "Contact: Founding Team  |  Email: contact@lexassist.ai  |  Demo: http://localhost:8501"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MUTED

    slide12.notes_slide.notes_text_frame.text = (
        "In closing, why should you back LexAssist? First, the timing is historic—as India transitions to the BNS, "
        "lawyers need reliable statutory navigation now more than ever. Second, we solve the hallucination crisis that "
        "disqualifies general-purpose AI. Third, our unit economics are extraordinary with 96% gross margins. And fourth, "
        "we are leveling the playing field for 1.5 million lawyers across India. Thank you, and we welcome your questions."
    )

    # Save presentation
    os.makedirs(os.path.dirname(OUTPUT_PPTX_PATH), exist_ok=True)
    prs.save(OUTPUT_PPTX_PATH)
    print(f"Presentation generated successfully with {len(prs.slides)} slides at: {OUTPUT_PPTX_PATH}")

if __name__ == "__main__":
    create_deck()

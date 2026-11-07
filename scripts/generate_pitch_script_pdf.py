"""
LexAssist Pitch Presentation Script PDF Generator
Builds an executive-grade PDF document containing:
- Comprehensive Hinglish verbal presentation script for all 12 slides
- Slide visual cues, English content summaries, and stage transitions
- Presenter tips, pacing timeline, and evaluator Q&A defense answers
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image,
    KeepTogether,
    HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_OUTPUT_PATH = r"d:\vs code\Entrepenuarship\LexAssist_Pitch_Script.pdf"
LOGO_PATH = r"C:\Users\Harsh\.gemini\antigravity-ide\brain\56186390-faed-4da1-9186-38b3e763a91e\lexassist_logo_1793117807292.jpg"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress header/footer on title cover

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0B192C"))
        self.drawString(40, 802, "LEXASSIST")
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(95, 802, "— Zero-Hallucination AI Legal Research | Business Pitch Script")
        
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(40, 796, 555, 796)

        # Footer
        self.line(40, 42, 555, 42)
        self.drawString(40, 30, "Confidential | Prepared for Entrepreneurship Business Pitch Evaluation")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(555, 30, page_str)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=52,
        bottomMargin=52
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    c_navy = colors.HexColor("#0B192C")
    c_gold = colors.HexColor("#C5A059")
    c_emerald = colors.HexColor("#0F766E")
    c_charcoal = colors.HexColor("#1E293B")
    c_muted = colors.HexColor("#64748B")
    c_card_bg = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#E2E8F0")

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=c_navy,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        textColor=c_emerald,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_navy,
        spaceBefore=14,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_gold,
        spaceBefore=6,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_charcoal,
        spaceAfter=6
    )

    script_box_style = ParagraphStyle(
        'ScriptBoxText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=14.5,
        textColor=colors.HexColor("#0F172A")
    )

    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=c_muted
    )

    story = []

    # ==========================================================
    # COVER PAGE
    # ==========================================================
    story.append(Spacer(1, 25))
    if os.path.exists(LOGO_PATH):
        story.append(Image(LOGO_PATH, width=2.4*inch, height=2.4*inch))
        story.append(Spacer(1, 15))

    story.append(Paragraph("LexAssist", title_style))
    story.append(Paragraph("Zero-Hallucination AI Legal Research Assistant for Indian Law", subtitle_style))
    story.append(Paragraph("<b>Complete Presentation Pitch Script & Evaluator Defense Handbook (Hinglish & English)</b>", ParagraphStyle(
        'CoverDesc', parent=styles['Normal'], fontName='Helvetica', fontSize=10.5, leading=15, textColor=c_charcoal, spaceAfter=20
    )))

    # Cover Metadata Table
    meta_data = [
        [Paragraph("<b>Venture Track:</b>", label_style), Paragraph("LegalTech & Enterprise Artificial Intelligence", body_style)],
        [Paragraph("<b>Target Pitch Duration:</b>", label_style), Paragraph("5 to 7 Minutes (with 3-Minute Elevator Variant)", body_style)],
        [Paragraph("<b>Deck Structure:</b>", label_style), Paragraph("12 Widescreen Slides (White/Light Theme Compliance)", body_style)],
        [Paragraph("<b>Evaluation Target:</b>", label_style), Paragraph("Entrepreneurship Business Pitch / Angel Incubator Defense", body_style)],
        [Paragraph("<b>Current Status:</b>", label_style), Paragraph("Working MVP (Streamlit UI, ChromaDB, Gemini 2.5 Flash)", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[130, 385])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 20))

    # Presenter Guidelines Box
    guide_html = """
    <b>PRESENTER QUICK RULES:</b><br/>
    • <b>Pacing:</b> Fast mat boliye. Crucial numbers (4.4 Crore pending cases, 96.7% gross margin, 10x LTV/CAC) bolte waqt pause lijiye.<br/>
    • <b>Tone:</b> Professional, calm aur confident. Screen par continuously mat dekhiye; maintain strong eye-contact with evaluators.<br/>
    • <b>Keywords:</b> Legal & business terms (RAG, Hallucination, TAM, Unit Economics, BNS) ko accurately pronounce kijiye.
    """
    guide_table = Table([[Paragraph(guide_html, body_style)]], colWidths=[515])
    guide_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#F59E0B")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(guide_table)

    story.append(PageBreak())

    # ==========================================================
    # SLIDE BY SLIDE HINGLISH SCRIPTS
    # ==========================================================
    slides = [
        {
            "num": 1,
            "title": "Title & Startup Brand",
            "time": "0:00 - 0:30 (30 sec)",
            "visual": "Slide 1: Crisp white canvas, high-res LexAssist scale & tech logo, gold brand bar, and value tags.",
            "hinglish": (
                "Good morning respected judges and evaluators! "
                "Aaj main aapke saamne introduce karne ja raha hoon hamara startup — <b>LexAssist</b>.<br/>"
                "Hamara tagline aur core mission hai: <b>Zero-Hallucination AI Legal Research Assistant for Indian Law</b>.<br/><br/>"
                "Aaj artificial intelligence har industry ko transform kar raha hai — finance, healthcare, software. "
                "Lekin jab baat aati hai legal courtroom ki, toh lawyers AI use karne se darte hain. Kyun? "
                "Kyunki generic AI <b>hallucinate</b> karta hai — fake section numbers aur fabricated rulings invent kar deta hai.<br/><br/>"
                "LexAssist is problem ko root level pe solve karta hai ek fully grounded, local-first legal intelligence engine ke saath, "
                "jo official Indian statutes se 100% verifiable citations deliver karta hai."
            ),
            "english_summary": "Introduces LexAssist, defines the core zero-hallucination mission, and explains why generic AI is locked out of courts."
        },
        {
            "num": 2,
            "title": "The Problem: Research Paralysis & Hallucinations",
            "time": "0:30 - 1:15 (45 sec)",
            "visual": "Slide 2: 3 Cards — Time Drain (15-20 hrs/wk), Keyword Search Failure, and LLM Hallucination Trap.",
            "hinglish": (
                "Ab aate hain ground reality pe — problem kya hai aur ise kaun face kar raha hai?<br/>"
                "India mein <b>15 Lakh se zyada practicing advocates</b> hain aur <b>2 Lakh law students</b>. "
                "Aur hamare courts mein <b>4.4 Crore cases pending</b> hain!<br/><br/>"
                "Is massive pressure mein lawyers teen critical problems face karte hain:<br/>"
                "1. <b>Pehla — Massive Time Drain:</b> Ek junior advocate har hafte 15 se 20 ghante sirf bare acts, gazettes aur amendments ke panno ko manually palatne mein gawa deta hai.<br/>"
                "2. <b>Doosra — Keyword Search Failure:</b> Purane legacy tools (SCC Online, Manupatra) exact keyword matching pe chalte hain. Agar advocate natural case facts daalta hai, toh purana software link nahi kar pata ki yeh Section 73 breach of contract hai.<br/>"
                "3. <b>Aur teesra, sabse dangerous — ChatGPT ki Hallucinations:</b> Generic AI fake sections aur repealed laws quote karta hai. Court mein galat section bolna seedha contempt of court aur license cancel hone ka risk ban jata hai!"
            ),
            "english_summary": "Quantifies the problem: 4.4Cr pending cases, 15-20 hrs/wk lost in manual search, keyword mismatch, and legal malpractice risk from ChatGPT."
        },
        {
            "num": 3,
            "title": "Proposed Solution: Grounded Legal Intelligence",
            "time": "1:15 - 1:55 (40 sec)",
            "visual": "Slide 3: Split layout — Grounded RAG Ingestion Pipeline + 4 Core Product Capabilities.",
            "hinglish": (
                "Iska solid solution hai hamara product: <b>LexAssist</b>.<br/>"
                "LexAssist ungrounded memory se nahi, balki strict <b>Retrieval-Augmented Generation (RAG)</b> pipeline pe kaam karta hai.<br/><br/>"
                "Yeh kaise kaam karta hai?<br/>"
                "• <b>Pehla:</b> Hamara system sirf official government gazettes (<i>indiacode.nic.in</i>) ke verified statutes ko index karta hai. Koi random blog ya unverified summary nahi.<br/>"
                "• <b>Doosra:</b> Hum legal text ko fixed characters mein nahi kaat-te, balki exact Section aur Article boundaries pe cleanly parse karte hain.<br/>"
                "• <b>Teesra:</b> Har retrieved provision ke saath uska exact title, verbatim statutory text, aur government portal ka direct clickable URL link milta hai.<br/>"
                "• <b>Aur sabse bada feature — Zero-Hallucination:</b> Agar user koi aisa question puchta hai jo hamare database mein nahi hai, toh LexAssist fake law banane ke bajaye bol deta hai: <i>'No sufficiently relevant provision was found.'</i> Yaani, no guesswork, zero hallucination!"
            ),
            "english_summary": "Details the 4-step grounded RAG solution: official government repositories, boundary-level chunking, verbatim citations, and explicit refusal."
        },
        {
            "num": 4,
            "title": "Innovation & Technology: Engineering Defensibility",
            "time": "1:55 - 2:40 (45 sec)",
            "visual": "Slide 4: 2x2 Engineering Grid — Boundary Chunking, Distance Threshold (<0.59), Local ChromaDB, Constrained Gemini.",
            "hinglish": (
                "Next, aate hain hamari core engineering innovation pe:<br/>"
                "Humne 4 major technical innovations implement kiye hain jo generic AI mein nahi milte:<br/>"
                "1. <b>Boundary-Aware Statutory Chunking:</b> Standard AI tools har 500 characters pe text kaat dete hain, jisse legal provisions beech mein se toot jaate hain. Humne custom parser banaya hai jo pure Section, explanation aur illustrations ko ek atomic vector unit mein lock rakhta hai.<br/>"
                "2. <b>Dual-Stage Distance Firewall (<0.59):</b> Humne ek strict mathematical threshold lagaya hai. Agar user query ka semantic match 0.59 distance se kam hai, toh LLM trigger hi nahi hota. Yeh hallucinations ke khilaaf automated firewall hai.<br/>"
                "3. <b>Local-First Vector Architecture:</b> Hamara ChromaDB vector database user ke system pe locally chalta hai. Confidential case files kisi cloud server pe leak nahi hote — 100% data privacy!<br/>"
                "4. <b>Constrained Synthesis:</b> Google Gemini 2.5 Flash model ko 0.1 temperature pe strict compiler mode mein chalaya jata hai jo sirf retrieved text ko synthesize karta hai."
            ),
            "english_summary": "Explains the technological moat: boundary-aware chunking, cosine distance firewall (<0.59), local-first ChromaDB privacy, and constrained LLM synthesis."
        },
        {
            "num": 5,
            "title": "Target Customers: Who Will Buy & Use LexAssist?",
            "time": "2:40 - 3:20 (40 sec)",
            "visual": "Slide 5: 3 Customer Segments — Solo Advocates & Chambers, Law Students & Scholars, Corporate Legal & In-House.",
            "hinglish": (
                "Ab sawal aata hai — hamare customers kaun hain aur hum kiske liye build kar rahe hain?<br/><br/>"
                "1. <b>Primary Market — Solo Advocates & Small Chambers:</b><br/>"
                "India mein 15 Lakh registered advocates hain, jisme se 85% Tier-2 aur Tier-3 District Courts mein practice karte hain. Ye log 40,000 se 60,000 rupaye saal ka legacy subscription afford nahi kar sakte. Unke liye hamara ₹999/month ka tool ek game-changer hai.<br/><br/>"
                "2. <b>Beachhead Market — 2 Lakh Law Students across 1,700 Colleges:</b><br/>"
                "Law students moot courts aur internships ke liye fast aur authentic tool dhoondhte hain. Ye hamara viral Product-Led Growth engine banenge.<br/><br/>"
                "3. <b>Enterprise Market — Corporate Legal & In-House Compliance Teams:</b><br/>"
                "Fintech, SaaS aur E-commerce companies ke in-house lawyers jinhe contracts, IT Act aur Consumer Protection regulations ke automated statutory audits chahiye hote hain."
            ),
            "english_summary": "Segments the market into 3 tiers: Solo advocates (₹999/mo), Law students (PLG beachhead), and Corporate compliance teams (Enterprise retainers)."
        },
        {
            "num": 6,
            "title": "Market Opportunity & Competitive Landscape",
            "time": "3:20 - 4:05 (45 sec)",
            "visual": "Slide 6: TAM ₹15,000 Cr, SAM ₹3,200 Cr, SOM ₹180 Cr metrics + 5-column competitor matrix table.",
            "hinglish": (
                "Market opportunity ki baat karein:<br/>"
                "• Hamara <b>Total Addressable Market (TAM)</b> hai <b>₹15,000 Crore ($1.8 Billion)</b>.<br/>"
                "• Hamara <b>Serviceable Addressable Market (SAM)</b> hai <b>₹3,200 Crore</b>, jo Indian advocates aur law firms ka litigation research budget hai.<br/>"
                "• Hamara 5-year <b>Serviceable Obtainable Market (SOM)</b> target hai <b>₹180 Crore</b>, jo 15% tech-forward legal professionals ko capture karta hai.<br/><br/>"
                "<b>Competitive Matrix dekhiye:</b><br/>"
                "• <b>SCC Online / Manupatra:</b> Bahut mehenge hain (₹35k-₹60k), sirf purana keyword search dete hain, aur koi AI reasoning nahi hai.<br/>"
                "• <b>ChatGPT:</b> Free ya sasta hai, lekin hallucination hazard ki wajah se Indian courts ke liye totally unsafe hai.<br/>"
                "• <b>Harvey AI:</b> US/UK corporate firms ke liye bana hai ($1,000/seat/month), jisme Indian law ka koi depth nahi hai.<br/>"
                "• <b>LexAssist:</b> Uniquely positioned hai — high semantic intelligence, ZERO hallucination risk, complete local privacy, aur affordable Indian pricing!"
            ),
            "english_summary": "Presents market sizing (TAM ₹15k Cr, SAM ₹3.2k Cr, SOM ₹180 Cr) and positions LexAssist as the only zero-hallucination, affordable legal AI in India."
        },
        {
            "num": 7,
            "title": "Business Model & Monetization Tiers",
            "time": "4:05 - 4:40 (35 sec)",
            "visual": "Slide 7: 4 Pricing Cards — Community Free (₹0), Advocate Pro (₹999/mo), Chambers Team (₹4,999/mo), Enterprise API.",
            "hinglish": (
                "Hamara revenue model ek high-margin B2B SaaS architecture pe based hai:<br/><br/>"
                "1. <b>Community Free Plan (₹0):</b> Students aur interns ke liye 3 core acts aur 15 queries daily — isse hamara viral user base build hota hai.<br/>"
                "2. <b>Advocate Pro Plan (₹999 / month ya ₹9,990 / year):</b> Hamara main revenue driver! Isme saare Central & State acts, unlimited queries, PDF/image upload, persistent case workspaces, aur grounded follow-up chat milta hai.<br/>"
                "3. <b>Chambers Team Plan (₹4,999 / month):</b> 5 seats include karta hai litigation partnerships ke liye, jisme shared case dossiers aur team search history ka feature hai.<br/>"
                "4. <b>Enterprise & API (₹25,000+ / month):</b> Law firms aur corporate legal teams ke liye on-premise deployment aur internal contracts indexing."
            ),
            "english_summary": "Details the freemium B2B SaaS tiers: Free (students), Pro (₹999/mo), Chambers (₹4,999/mo), and Enterprise custom deployments."
        },
        {
            "num": 8,
            "title": "Cost Structure & Unit Economics",
            "time": "4:40 - 5:20 (40 sec)",
            "visual": "Slide 8: Cost Breakdown Table (COGS ₹32.98 vs ₹999 Price) + SaaS Health Ratios (10x LTV/CAC, 1.2 mo payback).",
            "hinglish": (
                "Aap sochenge ki AI tools mein computing cost bahut high hoti hai, toh hamari unit economics kaisi hai?<br/>"
                "Yahan hamara local-first architecture hume ek unfair advantage deta hai!<br/><br/>"
                "Kyunki ChromaDB local machine pe chalta hai, hamara cloud database cost zero hai.<br/>"
                "Ek active Pro user jo mahine mein 150 queries karta hai:<br/>"
                "• Gemini Flash API cost: sirf ₹6.00<br/>"
                "• Local Compute & storage: ₹2.00<br/>"
                "• Cloud Auth & Sync: ₹5.00<br/>"
                "• Payment Gateway fees: ₹19.98<br/>"
                "<b>Total COGS per user/month: sirf ₹32.98!</b><br/><br/>"
                "Aur hamara selling price hai <b>₹999 per month</b>. Iska matlab hamara <b>Gross Margin hai 96.7%</b>!<br/>"
                "Hamara Customer Acquisition Cost (CAC) estimated hai ₹1,200 aur Customer Lifetime Value (LTV) hai lagbhag ₹12,000. "
                "Yaani hamara <b>LTV-to-CAC ratio hai 10x</b>, aur payback period sirf 1.2 months hai!"
            ),
            "english_summary": "Demonstrates world-class SaaS unit economics: ₹32.98 monthly COGS, 96.7% gross margin, 10x LTV/CAC ratio, and 1.2-month payback."
        },
        {
            "num": 9,
            "title": "Marketing & Go-to-Market Strategy",
            "time": "5:20 - 5:55 (35 sec)",
            "visual": "Slide 9: 3 GTM Pillars — Campus-to-Chamber Flywheel, Bar Council Roadshows, Verified Watermark Virality.",
            "hinglish": (
                "Hum customers tak kaise pahunchenge? Hum costly ads pe paise burn nahi karenge. Hamari strategy hai ek organic 3-pillar flywheel:<br/><br/>"
                "1. <b>Pehla — Campus-to-Chamber Flywheel:</b> Hum top National Law Universities ke national moot court competitions ko sponsor karenge aur students ko free access denge. Jab yeh students graduate hoke senior advocates ke chambers join karenge, toh wo LexAssist ko demand karenge.<br/>"
                "2. <b>Doosra — Bar Council Live Demonstrations:</b> Hum High Court aur District Bar Associations mein live workshops karenge — aur stage pe ChatGPT aur LexAssist ka live comparison dikhayenge ki kaise ChatGPT fake section deta hai jabki LexAssist exact official India Code link nikaalta hai.<br/>"
                "3. <b>Teesra — Viral Verified Watermarks:</b> LexAssist se export hone wali har legal research memo pe ek digital verified badge hoga — <i>'Verified by LexAssist'</i>. Jab ek advocate doosre advocate ya client ko brief bhejega, toh product khud apna marketing karega."
            ),
            "english_summary": "Outlines organic GTM: Campus moot courts (PLG), Bar Association live hallucination showdowns, and viral verified report watermarks."
        },
        {
            "num": 10,
            "title": "Future Scope & Scaling Roadmap",
            "time": "5:55 - 6:30 (35 sec)",
            "visual": "Slide 10: 3 Horizons — Foundation (M1-6), Judicial Precedents (M7-12), Vernacular Multi-Lingual AI (M13-24).",
            "hinglish": (
                "Hamara roadmap teen clear horizons mein divided hai:<br/><br/>"
                "• <b>Phase 1 (Next 6 Months):</b> Saare 1,000+ Indian Central Acts index karna, aur hamara <b>BNS-IPC Migration Mapper</b> launch karna — taaki purane Indian Penal Code ke sections naye Bharatiya Nyaya Sanhita (BNS) mein 1 click mein map ho sakein.<br/>"
                "• <b>Phase 2 (Months 7 to 12):</b> Supreme Court aur High Courts ke landmark judgments ko integrate karna, taaki har statutory provision ke saath leading judicial precedents automatically cross-link ho sakein.<br/>"
                "• <b>Phase 3 (Year 2):</b> India ke regional district courts ke liye vernacular AI launch karna — Hindi, Marathi, Tamil, Bengali mein voice aur text search support, taaki justice Bharat ke har kone tak democratize ho sake."
            ),
            "english_summary": "Outlines 3-phase roadmap: 1,000+ Acts & BNS Migration Mapper (Phase 1), Supreme Court judgments (Phase 2), and Vernacular multi-lingual AI (Phase 3)."
        },
        {
            "num": 11,
            "title": "The Ask & Allocation of Funds",
            "time": "6:30 - 7:00 (30 sec)",
            "visual": "Slide 11: Ask ₹25 Lakhs Pre-Seed, Allocation Breakdown (45% Corpus, 30% GTM, 25% Security) + 12-Month Targets.",
            "hinglish": (
                "Is vision ko execute karne ke liye, hamara ask hai:<br/>"
                "<b>₹25 Lakhs ($30,000 USD) ka Pre-Seed Incubator Grant ya Angel Capital</b> ek 12-month runway ke liye.<br/><br/>"
                "Is funding ka allocation bilkul strategic hai:<br/>"
                "• <b>45% (₹11.25 Lakhs):</b> Legal corpus engineering aur law interns dwara statutory ground-truth verification ke liye.<br/>"
                "• <b>30% (₹7.50 Lakhs):</b> Bar Council workshops aur university partnerships ke liye.<br/>"
                "• <b>25% (₹6.25 Lakhs):</b> Cloud infrastructure, SSL/TLS data security aur SOC-2 compliance audits ke liye.<br/><br/>"
                "Is capital ke saath 12 months mein hum deliver karenge: <b>15,000 registered users</b>, <b>1,200 paid Pro subscribers</b>, aur <b>₹1.44 Crore ka Annual Recurring Revenue (ARR)</b>, achieving operational break-even by Month 9!"
            ),
            "english_summary": "Requests ₹25 Lakhs pre-seed capital for 12 months, targeting 15k users, 1,200 paid subscribers, and ₹1.44 Cr ARR."
        },
        {
            "num": 12,
            "title": "Closing Pitch & Vision",
            "time": "7:00 - 7:30 (30 sec)",
            "visual": "Slide 12: High-impact vision card, 4 pillar justifications, founder contact details.",
            "hinglish": (
                "To conclude, evaluators — LexAssist mein invest ya support kyun karein?<br/><br/>"
                "1. <b>Timing perfect hai:</b> India mein 160 saal baad naye criminal laws (BNS, BNSS, BSA) aaye hain. Har lawyer ko naye laws seekhne hain, aur LexAssist unka sabse bharosemand saathi hai.<br/>"
                "2. <b>Product defensible hai:</b> Zero-hallucination koi marketing slogan nahi, hamara tested algorithmic firewall hai.<br/>"
                "3. <b>Economics solid hain:</b> 96.7% gross margins aur 10x LTV/CAC ratio ke saath yeh ek cash-efficient, scalable SaaS venture hai.<br/>"
                "4. <b>Mission of Justice:</b> Sirf ₹999 mein hum ek small-town district lawyer ko wahi research horsepower de rahe hain jo Delhi ya Mumbai ki top corporate law firms ke paas hoti hai.<br/><br/>"
                "<b>AI with integrity. Legal research without hallucinations.</b><br/>"
                "Yeh hai <b>LexAssist</b>. Thank you so much! We are now open for your questions!"
            ),
            "english_summary": "Delivers closing punchline: perfect regulatory timing with BNS, zero-hallucination defensibility, 96.7% margins, and democratizing justice across India."
        }
    ]

    for s in slides:
        card_content = []
        # Header Row
        header_text = f"<b>SLIDE {s['num']:02d}: {s['title'].upper()}</b> &nbsp;&nbsp;|&nbsp;&nbsp; <i>Timing: {s['time']}</i>"
        card_content.append(Paragraph(header_text, h1_style))
        card_content.append(Paragraph(f"<b>Slide Visual Cues:</b> {s['visual']}", label_style))
        card_content.append(Spacer(1, 4))
        card_content.append(HRFlowable(width="100%", thickness=0.8, color=c_gold, spaceAfter=8))

        # Hinglish Dialogue Box
        box_data = [[
            Paragraph("<b>SPEAKER PITCH SCRIPT (HINGLISH):</b>", h2_style),
        ], [
            Paragraph(s['hinglish'], script_box_style)
        ]]
        box_table = Table(box_data, colWidths=[505])
        box_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
            ('BOX', (0,0), (-1,-1), 1, c_border),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        card_content.append(box_table)

        # English Core Takeaway
        card_content.append(Spacer(1, 4))
        card_content.append(Paragraph(f"<b>Evaluator Takeaway:</b> {s['english_summary']}", label_style))
        card_content.append(Spacer(1, 14))

        story.append(KeepTogether(card_content))

    # ==========================================================
    # JUDGES' TOUGH Q&A DEFENSE
    # ==========================================================
    story.append(PageBreak())
    story.append(Paragraph("Evaluator Q&A Defense (Tough Questions & Answers)", h1_style))
    story.append(Paragraph("Anticipated questions from business evaluators and angel investors with strategic Hinglish responses:", body_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_navy, spaceAfter=12))

    qa_list = [
        ("Q1: Google ya OpenAI apne general AI model mein yeh feature kal hi kyun nahi daal dega?",
         "Sir, OpenAI aur Google horizontal foundation models banate hain. Unka target hota hai general chatter aur text generation. Law mein language model ko strictly restrict karna padta hai official enactments tak. General LLMs creative hote hain, jabki law mein creativity fatal hai. Doosri baat, koi bhi practicing lawyer apna confidential client case public ChatGPT pe upload nahi karega. Hamara local-first ChromaDB aur Indian-law-specific ground-truth pipeline hamara moated advantage hai jo horizontal players build nahi karte."),
        ("Q2: Agar aapka AI galat section bata de aur lawyer case haar jaye, toh liability kiski hogi?",
         "Bilkul valid concern hai sir. LexAssist legally ek research productivity tool hai, legal advisor nahi. Hamare har analysis ke neeche clear statutory disclaimer hota hai. Lekin generic AI ke mukable, LexAssist user ko direct government portal ka link aur exact verbatim text saamne dikhata hai. Advocate ko verify karne mein sirf 5 second lagte hain. Hum legal judgment replace nahi kar rahe, lawyer ke 15 ghante ka manual search time bacha rahe hain."),
        ("Q3: Lawyers technology adopt karne mein bahut slow hote hain. Wo pay kyun karenge?",
         "Sir, lawyers tab reject karte hain jab unhe complex training leni pade. Lekin unhone WhatsApp aur e-Courts turant adopt kiya kyunki usme zero effort tha. LexAssist mein advocate ko sirf natural case facts type karne hain ya FIR ki photo upload karni hai, aur 5 second mein verified sections screen pe hote hain. Aur pricing humne rakhi hai ₹999/month, jo unke office ke chai-nashte ke kharche se bhi kam hai!"),
        ("Q4: 96.7% gross margin bohot high lag raha hai. Kya yeh realistic hai?",
         "Yes sir, 100% realistic hai aur iska reason hamara local-first architecture hai. Traditional cloud AI apps har user ke vector database ko AWS ya Google Cloud pe host karte hain jiska server bill bohot high hota hai. LexAssist mein ChromaDB user ke local disk pe chalta hai, toh cloud storage cost zero ho jati hai. Hum sirf Gemini Flash API calls ka payment karte hain jo ₹0.04 per query padta hai. Isliye 150 queries ka total cost sirf ₹6 aata hai. Even if compute doubles, hamara margin 90%+ maintain rahega.")
    ]

    for q, a in qa_list:
        qa_data = [
            [Paragraph(f"<b>{q}</b>", h2_style)],
            [Paragraph(f"<b>Response:</b> {a}", script_box_style)]
        ]
        qa_table = Table(qa_data, colWidths=[515])
        qa_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
            ('BOX', (0,0), (-1,-1), 1, c_border),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(KeepTogether([qa_table, Spacer(1, 10)]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF pitch script generated successfully at: {PDF_OUTPUT_PATH}")

if __name__ == "__main__":
    build_pdf()

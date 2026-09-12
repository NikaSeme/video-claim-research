#!/usr/bin/env python3
"""Build the original, vector-only public example. No source-media input exists.

Requires ReportLab and pdftoppm. Building invalidates the recorded visual review.
The historical evidence assessment is retained; this is not a new product test.
"""
from pathlib import Path
from hashlib import sha256
from html import escape
import json
import subprocess

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.graphics import renderPDF, renderSVG
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples/elu-mcp-claim-check"
INK, BLUE, PALE, LINE, MUTED = "#102c3d", "#226586", "#eaf7fc", "#bfd7e4", "#435f70"
SOURCES = [
    ("Source reel", "https://www.instagram.com/reel/DXwo4xAxmsG/", "Original claim; not evidence of performance."),
    ("ELU product description", "https://elu.dev/", "Vendor description of analysis and proposed fixes."),
    ("ELU privacy policy", "https://elu.dev/privacy-policy", "Vendor account of data processing and human review."),
    ("ELU terms", "https://elu.dev/terms-service", "Vendor account of product scope and output risks."),
    ("MCP introduction", "https://modelcontextprotocol.io/docs/getting-started/intro", "Protocol scope, not a product benchmark."),
    ("Anthropic MCP announcement", "https://www.anthropic.com/news/model-context-protocol", "Original context for the connection standard."),
    ("NSA MCP security guidance", "https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI_MCP_SECURITY.pdf", "Security constraints and review considerations."),
    ("Mixpanel: user friction", "https://mixpanel.com/blog/what-is-user-friction/", "General analytics context, not ELU-specific validation."),
]


def label(drawing, text, x, y, size=16, bold=False, color=INK):
    drawing.add(String(x, y, text, fontName="Helvetica-Bold" if bold else "Helvetica",
                       fontSize=size, fillColor=HexColor(color)))


def workflow():
    d = Drawing(720, 550)
    d.add(Rect(0, 0, 720, 550, fillColor=HexColor(PALE), strokeColor=None, rx=20, ry=20))
    label(d, "A connection is one part of the workflow.", 32, 510, 23, True)
    label(d, "Original explanatory diagram / not captured from the reel", 32, 483, 12, color=MUTED)
    rows = [
        ("01", "Usage data", "Relevant events and observations"),
        ("02", "AI analysis via MCP", "Possible friction points and interpretations"),
        ("03", "Proposed change", "A recommendation or coding task"),
        ("04", "Human review + tests", "Check correctness before approving a release"),
    ]
    for i, (number, title, desc) in enumerate(rows):
        y = 372 - i * 90
        d.add(Rect(32, y, 656, 72, fillColor=white, strokeColor=HexColor(LINE), rx=12, ry=12))
        label(d, number, 52, y+29, 18, True, BLUE)
        label(d, title, 110, y+43, 18, True)
        label(d, desc, 110, y+20, 14, color=MUTED)
        if i < 3:
            d.add(Line(68, y-2, 68, y-15, strokeColor=HexColor(BLUE), strokeWidth=1.5))
            d.add(Polygon([64, y-12, 68, y-17, 72, y-12], fillColor=HexColor(BLUE), strokeColor=None))
    label(d, "A suggested review path, not a tested ELU deployment.", 32, 57, 13, color=MUTED)
    label(d, "Reliable unattended self-improvement is not established.", 32, 32, 15, True)
    return d


def boundary():
    d = Drawing(720, 550)
    d.add(Rect(0, 0, 720, 550, fillColor=HexColor(PALE), strokeColor=None, rx=20, ry=20))
    label(d, "What the evidence can establish", 32, 508, 24, True)
    label(d, "Original evidence map / no measured results are shown", 32, 480, 12, color=MUTED)
    rows = [
        ("Documented", "Connections + stated capabilities", "MCP documentation and ELU's own descriptions."),
        ("Plausible", "Assisted analysis + code handoff", "An interpretation supported by the integration premise."),
        ("Not demonstrated", "Dependable autonomous improvement", "No independent deployment test or before/after results."),
    ]
    for i, (tag, title, desc) in enumerate(rows):
        y = 318-i*112
        d.add(Rect(32, y, 656, 96, fillColor=white, strokeColor=HexColor(LINE), rx=12, ry=12))
        label(d, tag.upper(), 54, y+69, 12, True, BLUE)
        label(d, title, 54, y+42, 19, True)
        label(d, desc, 54, y+18, 13, color=MUTED)
    label(d, "Confidence: medium for this wording assessment.", 32, 46, 15, True)
    label(d, "This is not a certification of product performance or safety.", 32, 23, 13, color=MUTED)
    return d


def build_pdf(path):
    c = canvas.Canvas(str(path), pagesize=(595.28, 841.89), pageCompression=1)
    c.setTitle("ELU and MCP: claim and evidence")
    c.setAuthor("Nikolozi Semenenko")
    c.setSubject("Historical claim review with original explanatory diagrams; no runtime validation")
    body = ParagraphStyle("body", fontName="Helvetica", fontSize=11, leading=16, textColor=HexColor(INK))
    small = ParagraphStyle("small", parent=body, fontSize=9, leading=13, textColor=HexColor(MUTED))
    heading = ParagraphStyle("heading", parent=body, fontName="Helvetica-Bold", fontSize=16, leading=21)

    def p(text, y, style=body, x=42, width=511):
        par = Paragraph(text, style)
        _, height = par.wrap(width, 740)
        if y-height < 57:
            raise ValueError(f"Page overflow: {text[:70]}")
        par.drawOn(c, x, y-height)
        return y-height-12

    def page(number, title, subtitle):
        c.setFillColor(HexColor(BLUE)); c.setFont("Helvetica-Bold", 9)
        c.drawString(42, 799, "NS / CLAIM RESEARCH")
        c.setFillColor(HexColor(INK)); c.setFont("Helvetica-Bold", 24)
        c.drawString(42, 761, title)
        p(subtitle, 743, small)
        c.setStrokeColor(HexColor(LINE)); c.line(42, 52, 553, 52)
        c.setFont("Helvetica", 8); c.setFillColor(HexColor(MUTED))
        c.drawString(42, 35, "Evidence reviewed 09 Jul 2026 / publication revision 10 Sep 2026")
        c.drawRightString(553, 35, f"{number} / 4")

    page(1, "ELU and MCP: claim and evidence", "Experimental research sample / source attribution [1] / no product test")
    y = p("Plausible workflow. Autonomy not demonstrated.", 694, heading)
    y = p("Product-usage data can plausibly inform an AI assistant's recommendations and coding tasks. That does not establish dependable, unattended software improvement. Tests, scoped permissions, data quality, and human approval remain separate requirements. [2-7]", y)
    y = p("What is being assessed", y-10, heading)
    for text in [
        "The reel presents a vibe-coded application as able to improve itself in a human-like way.",
        "Its narrower premise combines ELU analytics, MCP access, and prompts that turn friction findings into proposed implementation work.",
        "The question is whether that integration proves the stronger autonomy claim. This report assesses that claim, not the source's personal reputation.",
    ]:
        y = p(text, y)
    y = p("Scope and limits", y-10, heading)
    y = p("No ELU account, API integration, deployment, or before/after product metric was tested. The original review did not establish whether the reel used real, demo, or synthetic analytics data.", y)
    y = p("Claim assessment", y-10, heading)
    y = p("<b>Likelihood:</b> assisted analysis is plausible; reliable autonomous improvement is unproven.<br/><b>Confidence:</b> medium for the wording assessment, not for real-world performance.<br/><b>Evidence quality:</b> primary documentation supports protocol scope and vendor statements; independent validation is missing.", y)
    p("This revision replaces video imagery with original diagrams and removes personal ratings. The July evidence assessment has not been refreshed into a September product review.", y-6, small)
    c.showPage()

    page(2, "How the proposed workflow fits", "Original explanatory illustration / no source-video imagery")
    d = workflow(); d.scale(511/720, 511/720)
    renderPDF.draw(d, c, 42, 293)
    y = p("Where the claim goes further", 263, heading)
    y = p("The connection and recommendation steps do not establish that generated changes are correct, safe to deploy, or useful to people. That would require separate evidence at the review and release boundary.", y)
    p("This diagram is an original interpretation of the proposed workflow. It is not a reproduction of a prompt, screenshot, or observed system execution.", y, small)
    c.showPage()

    page(3, "Evidence in both directions", "Assessing statements, documentation, and missing tests")
    y = p("What supports the narrower claim", 694, heading)
    for text in [
        "<b>Vendor descriptions [2-4].</b> ELU describes session analysis, AI findings, proposed fixes, and MCP access. Its privacy and terms pages describe data processing and automated-output risks. These establish the vendor's stated scope, not independent effectiveness.",
        "<b>Protocol documentation [5-6].</b> MCP supports connecting AI applications to outside data and tools. That supports the integration premise, without guaranteeing accurate interpretation or correct code.",
        "<b>Analytics context [8].</b> Usage patterns can help identify friction. General analytics guidance is not an ELU benchmark.",
    ]:
        y = p(text, y)
    y = p("What remains unproven", y-4, heading)
    for text in [
        "<b>Human-like autonomy.</b> No independent deployment test, controlled comparison, or measured improvement was available in this review.",
        "<b>Safety and review [3, 4, 7].</b> Product disclosures and MCP security guidance leave data access, permissions, generated changes, and human review as distinct concerns.",
        "<b>Data provenance.</b> A demonstration alone does not establish whether its data is representative, genuine, or sufficient to guide product decisions.",
    ]:
        y = p(text, y)
    y = p("What would change the assessment?", y-4, heading)
    p("A reproducible test with disclosed data, a baseline, independently checked changes, regression results, and a measured user outcome would strengthen the claim. An interface connection or successful prompt is not that test.", y)
    c.showPage()

    page(4, "Sources and review questions", "Historical source register / accessed 09 July 2026")
    y = p("Before trying a similar workflow", 694, heading)
    y = p("Which outcome will you measure? Is the data appropriate to use? What can the agent read or change? Who checks the diff and tests, and how would you roll back a harmful change?", y)
    y = p("Sources", y-4, heading)
    for i, (title, url, purpose) in enumerate(SOURCES, 1):
        y = p(f'<b>[{i}] <link href="{escape(url, quote=True)}" color="{BLUE}">{escape(title)}</link></b> - {escape(purpose)}', y, small)
    y = p("Publication note", y-4, heading)
    p("Source links support attribution and verification. All visuals in this edition are original explanatory work. No video frames, screenshots, portraits, audio, or source-video excerpts are included. Corrections: contact@semenenko-nikoloz.dev.", y, small)
    c.save()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    build_pdf(OUT / "report.pdf")
    for name, drawing in [("workflow-diagram.svg", workflow()), ("evidence-map.svg", boundary())]:
        renderSVG.drawToFile(drawing, str(OUT / name))
    subprocess.run(["pdftoppm", "-scale-to", "1400", "-png", str(OUT / "report.pdf"), str(OUT / "page")], check=True)
    assets = []
    for name in ["report.pdf", "workflow-diagram.svg", "evidence-map.svg", *[f"page-{n}.png" for n in range(1,5)]]:
        assets.append({"path": name, "sha256": sha256((OUT/name).read_bytes()).hexdigest(),
                       "kind": "original_report" if name.endswith(".pdf") else "report_render" if name.endswith(".png") else "original_diagram",
                       "source": "scripts/build_public_example.py"})
    (OUT / "publication-manifest.json").write_text(json.dumps({
        "policy_version": 1, "review_status": "pending", "reviewer": "", "reviewed_at": "",
        "original_visuals_only": True, "claim_focused": True,
        "assets": assets,
    }, indent=2)+"\n")
    print("Built four-page public example. Inspect all pages and diagrams before approving the manifest.")


if __name__ == "__main__":
    main()

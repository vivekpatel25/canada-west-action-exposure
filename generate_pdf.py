from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
HTML_FILE = ROOT / "index.html"
OUTPUT_DIR = ROOT / "reports"
OUTPUT_DIR.mkdir(exist_ok=True)

PDF_FILE = OUTPUT_DIR / "Dinos_Position_Action_Exposure.pdf"

# Read the actual website HTML
if not HTML_FILE.exists():
    raise FileNotFoundError(
        "index.html was not found. Make sure generate_pdf.py is in the same folder as index.html."
    )

html = HTML_FILE.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

# Remove ONLY the Conference-Wide Results section and its navigation link.
# Keep the conference averages shown in the University of Calgary section.
conference_section = soup.find("section", id="conference")

if conference_section:
    conference_section.decompose()
else:
    print("Warning: No section with id='conference' was found.")

for link in soup.select('nav a[href="#conference"]'):
    link.decompose()

# Add print styling while retaining the website's existing design.
style = soup.find("style")

if style is None:
    style = soup.new_tag("style")
    soup.head.append(style)

style.append("""
@page {
    size: Letter;
    margin: 0.45in 0.45in 0.5in;
}

@media print {
    html,
    body {
        background: #f4f7fb !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }

    nav {
        display: none !important;
    }

    .pdf-actions {
        display: none !important;
    }

    .hero {
        break-after: avoid;
    }

    .card,
    .position-card {
        break-inside: avoid;
    }

    a {
        text-decoration: none !important;
    }

    img {
        max-width: 100% !important;
    }
}
""")

# Save temporary HTML beside index.html so relative image paths continue to work.
TEMP_HTML = ROOT / "_dinos_pdf_print.html"
TEMP_HTML.write_text(str(soup), encoding="utf-8")

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            viewport={"width": 1440, "height": 1000},
            device_scale_factor=1
        )

        page.goto(
            TEMP_HTML.as_uri(),
            wait_until="networkidle"
        )

        page.emulate_media(media="print")

        page.pdf(
            path=str(PDF_FILE),
            format="Letter",
            print_background=True,
            prefer_css_page_size=True,
            display_header_footer=False
        )

        browser.close()

finally:
    TEMP_HTML.unlink(missing_ok=True)

print(f"PDF successfully created: {PDF_FILE}")

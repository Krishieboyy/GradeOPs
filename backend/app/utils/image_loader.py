import fitz  # pymupdf
from PIL import Image


def load_image(path: str) -> Image.Image:
    if path.lower().endswith(".pdf"):
        return _pdf_to_image(path)
    return Image.open(path).convert("RGB")


def _pdf_to_image(path: str) -> Image.Image:
    """Render all PDF pages and stack them vertically into one RGB image."""
    doc = fitz.open(path)
    pages = []
    for page in doc:
        pix = page.get_pixmap(dpi=200)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pages.append(img)
    doc.close()

    if len(pages) == 1:
        return pages[0]

    total_h = sum(p.height for p in pages)
    max_w = max(p.width for p in pages)
    combined = Image.new("RGB", (max_w, total_h), (255, 255, 255))
    y = 0
    for p in pages:
        combined.paste(p, (0, y))
        y += p.height
    return combined

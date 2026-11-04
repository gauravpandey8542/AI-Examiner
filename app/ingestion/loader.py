from pypdf import PdfReader
def load_pdf(path: str) -> list[dict]:
    reader = PdfReader(path)
    pages=[]
    for number, page in enumerate(reader.pages,start=1):
        text=page.extract_text() or ""  #extract_text() or "" handles pages that return None (scanned images have no text layer).
        if text.strip():
            pages.append({"page":number,"text":text})
    return pages
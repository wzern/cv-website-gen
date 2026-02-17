import pdfplumber
from pathlib import Path

def extract_links_from_cv(cv_dir: str = "cv") -> dict[str, dict]:
    """Extract hyperlinks from PDFs alongside text."""
    cv_path = Path(cv_dir)
    results = {}

    for pdf_file in cv_path.glob("*.pdf"):
        with pdfplumber.open(pdf_file) as pdf:
            text = "\n".join(
                page.extract_text() for page in pdf.pages if page.extract_text()
            )
            # Extract actual hyperlink URIs from annotations
            links = []
            for page in pdf.pages:
                for annot in page.annots or []:
                    uri = annot.get("uri")
                    if uri:
                        links.append(uri)

            results[pdf_file.name] = {
                "text": text,
                "links": links
            }

    return results
import fitz
import requests


def extract_text_from_pdf_bytes(file_bytes):

    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""

    for page in doc:

        text += page.get_text()

        blocks = page.get_text("blocks")
        for block in blocks:
            block_text = block[4].strip()
            if block_text and block_text not in text:
                text += f"\n{block_text}"

        for field in page.widgets():
            label = field.field_label or ""
            value = field.field_value or ""
            if value.strip():
                text += f"\n{label}: {value}"

        page_dict = page.get_text("dict")
        for block in page_dict.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    span_text = span.get("text", "").strip()
                    if span_text and span_text not in text:
                        text += f"\n{span_text}"

    doc.close()
    return text.strip()


def extract_text_from_url(pdf_url):
    response = requests.get(pdf_url)
    return extract_text_from_pdf_bytes(response.content)
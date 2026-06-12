import fitz
import requests
import tempfile


def extract_text_from_url(pdf_url):

    response = requests.get(pdf_url)

    with tempfile.NamedTemporaryFile(
        delete=True,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(response.content)
        temp_file.flush()

        document = fitz.open(temp_file.name)

        text = ""

        for page in document:

            # standard text
            text += page.get_text()

            # tables via blocks
            blocks = page.get_text("blocks")
            for block in blocks:
                block_text = block[4].strip()
                if block_text and block_text not in text:
                    text += f"\n{block_text}"

            # form fields
            for field in page.widgets():
                label = field.field_label or ""
                value = field.field_value or ""
                if value.strip():
                    text += f"\n{label}: {value}"

            # dict-based extraction (catches missed spans)
            page_dict = page.get_text("dict")
            for block in page_dict.get("blocks", []):
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        span_text = span.get("text", "").strip()
                        if span_text and span_text not in text:
                            text += f"\n{span_text}"

        document.close()

    return text
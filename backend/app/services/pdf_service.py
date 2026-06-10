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


        document = fitz.open(
            temp_file.name
        )

        text = ""

        for page in document:
            text += page.get_text()


        document.close()


    return text
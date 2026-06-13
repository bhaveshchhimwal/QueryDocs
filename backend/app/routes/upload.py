from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import fitz
import io

from app.storage.cloudinary_storage import upload_pdf_to_cloudinary
from app.services.pdf_service import extract_text_from_pdf_bytes
from app.services.chunk_service import create_chunks
from app.services.rag_service import store_embeddings

router = APIRouter(prefix="/pdf", tags=["PDF"])


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_bytes = await file.read()

    doc = fitz.open(stream=file_bytes, filetype="pdf")
    page_count = len(doc)
    doc.close()

    if page_count > 100:
        return JSONResponse(
            status_code=400,
            content={"error": f"PDF has {page_count} pages. Please upload a PDF with 100 pages or less."}
        )

    pdf_url = upload_pdf_to_cloudinary(io.BytesIO(file_bytes))

    extracted_text = extract_text_from_pdf_bytes(file_bytes)

    if not extracted_text.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "This appears to be a scanned PDF. Only text-based PDFs are supported."}
        )

    chunks = create_chunks(extracted_text)
    vectors = store_embeddings(chunks, extracted_text)

    return {
        "message": "PDF stored successfully",
        "url": pdf_url,
        "characters_extracted": len(extracted_text),
        "chunks_created": len(chunks),
        "vectors_stored": vectors
    }
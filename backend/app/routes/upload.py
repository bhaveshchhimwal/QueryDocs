from fastapi import (
    APIRouter,
    UploadFile,
    File
)

from app.storage.cloudinary_storage import (
    upload_pdf_to_cloudinary
)

from app.services.pdf_service import (
    extract_text_from_url
)

from app.services.chunk_service import (
    create_chunks
)

from app.services.rag_service import (
    store_embeddings
)

router = APIRouter(
    prefix="/pdf",
    tags=["PDF"]
)


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    pdf_url = upload_pdf_to_cloudinary(
        file.file
    )

    extracted_text = extract_text_from_url(
        pdf_url
    )

    chunks = create_chunks(
        extracted_text
    )

    vectors = store_embeddings(
        chunks,
        extracted_text
    )

    return {
        "message": "PDF stored successfully",
        "url": pdf_url,
        "characters_extracted": len(extracted_text),
        "chunks_created": len(chunks),
        "vectors_stored": vectors
    }
import uuid
import requests

from qdrant_client.models import (
    PointStruct,
    VectorParams,
    Distance
)

from langchain_groq import ChatGroq

from app.database.qdrant import qdrant_client
from app.core.config import settings

HF_URL = (
    "https://router.huggingface.co/hf-inference/"
    "models/BAAI/bge-small-en-v1.5/"
    "pipeline/feature-extraction"
)

headers = {
    "Authorization":
    f"Bearer {settings.HUGGINGFACE_API_KEY}"
}

FULL_TEXT_THRESHOLD = 15_000
MEDIUM_THRESHOLD = 150_000
RAG_MEDIUM_LIMIT = 10   
RAG_LARGE_LIMIT = 8     

# in-memory store for current PDF text
current_pdf_text = None


def get_embedding(text):
    response = requests.post(
        HF_URL,
        headers=headers,
        json={"inputs": text},
        timeout=60
    )

    response.raise_for_status()

    embedding = response.json()

    if (
        isinstance(embedding, list)
        and len(embedding) > 0
        and isinstance(embedding[0], list)
    ):
        embedding = embedding[0]

    return embedding


def store_embeddings(chunks, full_text):
    global current_pdf_text
    current_pdf_text = full_text

    if not chunks:
        raise ValueError("No chunks to embed.")

    collection = settings.QDRANT_COLLECTION_NAME

    existing = [
        c.name
        for c in
        qdrant_client.get_collections().collections
    ]

    if collection in existing:
        qdrant_client.delete_collection(
            collection_name=collection
        )

    qdrant_client.create_collection(
        collection_name=collection,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

    points = []

    for chunk in chunks:
        vector = get_embedding(chunk)
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"text": chunk}
            )
        )

    BATCH_SIZE = 50
    for i in range(0, len(points), BATCH_SIZE):
        qdrant_client.upsert(
            collection_name=collection,
            points=points[i:i + BATCH_SIZE]
        )

    return len(points)


def ask_question(question):
    global current_pdf_text

    char_count = len(current_pdf_text) if current_pdf_text else 0

    if current_pdf_text and char_count <= FULL_TEXT_THRESHOLD:
        context = current_pdf_text

    else:
        limit = (
            RAG_MEDIUM_LIMIT
            if char_count <= MEDIUM_THRESHOLD
            else RAG_LARGE_LIMIT
        )

        question_vector = get_embedding(question)

        result = qdrant_client.query_points(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query=question_vector,
            limit=limit
        )

        context = ""
        for point in result.points:
            context += point.payload["text"] + "\n"

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=settings.GROQ_API_KEY
    )

    prompt = f"""
You are QueryDocs AI assistant.

Use ONLY the uploaded document context below to answer the question.

Rules:
- Answer strictly from the document.
- If the answer is present in any form (table, list, paragraph), extract and present it clearly.
- If the user asks for a summary, provide a clear and concise summary of the entire document.
- Only say "I could not find this information in the document." if the information is truly absent.
- Do not make up information.

DOCUMENT:
{context}

QUESTION:
{question}
"""

    response = llm.invoke(prompt)
    return response.content
import uuid

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)

from qdrant_client.models import (
    PointStruct,
    VectorParams,
    Distance
)

from app.database.qdrant import qdrant_client
from app.core.config import settings


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=settings.GEMINI_API_KEY
)


def store_embeddings(chunks):

    collection_name = settings.QDRANT_COLLECTION_NAME

    existing_collections = [
        collection.name

        for collection in
        qdrant_client.get_collections().collections
    ]


    if collection_name not in existing_collections:

        qdrant_client.create_collection(

            collection_name=collection_name,

            vectors_config=VectorParams(
                size=3072,
                distance=Distance.COSINE
            )
        )


    points = []


    for chunk in chunks:

        vector = embeddings.embed_query(
            chunk
        )


        points.append(

            PointStruct(

                id=str(uuid.uuid4()),

                vector=vector,

                payload={
                    "text": chunk
                }
            )
        )


    qdrant_client.upsert(

        collection_name=collection_name,

        points=points
    )


    return len(points)


def ask_question(question):

    question_vector = embeddings.embed_query(
        question
    )


    search_result = qdrant_client.query_points(

        collection_name=settings.QDRANT_COLLECTION_NAME,

        query=question_vector,

        limit=3
    )


    context = ""


    for point in search_result.points:

        context += (
            point.payload["text"]
            +
            "\n"
        )


    llm = ChatGoogleGenerativeAI(

        model="gemini-2.5-flash",

        google_api_key=settings.GEMINI_API_KEY
    )


    prompt = f"""
You are QueryDocs AI assistant.

Answer the user's question using only the document context.

If the answer is not present in the document,
say "I could not find this information in the document."

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}
"""


    response = llm.invoke(
        prompt
    )


    return response.content
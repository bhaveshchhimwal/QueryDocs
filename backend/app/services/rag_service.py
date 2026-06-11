import uuid


from langchain_huggingface import (
    HuggingFaceEmbeddings
)


from langchain_groq import (
    ChatGroq
)


from qdrant_client.models import (
    PointStruct,
    VectorParams,
    Distance
)


from app.database.qdrant import (
    qdrant_client
)


from app.core.config import (
    settings
)



embeddings = HuggingFaceEmbeddings(

    model_name=
    "sentence-transformers/paraphrase-MiniLM-L3-v2"
)



def store_embeddings(chunks):


    collection_name = settings.QDRANT_COLLECTION_NAME


    existing_collections = [

        collection.name

        for collection in

        qdrant_client
        .get_collections()
        .collections
    ]


    if collection_name in existing_collections:


        qdrant_client.delete_collection(

            collection_name=
            collection_name
        )


    qdrant_client.create_collection(

        collection_name=
        collection_name,


        vectors_config=VectorParams(

            size=384,

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

        collection_name=
        collection_name,


        points=
        points
    )


    return len(points)





def ask_question(question):


    question_vector = embeddings.embed_query(
        question
    )


    search_result = qdrant_client.query_points(

        collection_name=
        settings.QDRANT_COLLECTION_NAME,


        query=
        question_vector,


        limit=10
    )


    context = ""


    for point in search_result.points:


        context += (

            point.payload["text"]

            +

            "\n"
        )


    llm = ChatGroq(

        model=
        "llama-3.1-8b-instant",


        api_key=
        settings.GROQ_API_KEY
    )


    prompt = f"""

You are QueryDocs, an AI assistant that answers questions about uploaded documents.

Use the provided document content to answer the user.

Instructions:

- Understand the user's question.
- If asked to summarize, summarize the document.
- Extract relevant details from the document.
- Answer naturally.
- Do not mention chunks, embeddings, or database.
- If the information is not present, say:
"I could not find this information in the document."


DOCUMENT:

{context}


QUESTION:

{question}


ANSWER:

"""


    response = llm.invoke(
        prompt
    )


    return response.content
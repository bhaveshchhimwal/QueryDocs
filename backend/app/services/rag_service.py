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



# HuggingFace Inference API
HF_URL = (

    "https://router.huggingface.co/hf-inference/"
    "models/sentence-transformers/all-MiniLM-L6-v2/"
    "pipeline/feature-extraction"

)



headers = {

    "Authorization":
    f"Bearer {settings.HUGGINGFACE_API_KEY}"

}





def get_embedding(text):


    response = requests.post(

        HF_URL,


        headers=headers,


        json={

            "inputs": text

        },


        timeout=60

    )



    response.raise_for_status()



    embedding = response.json()



    # HF sometimes returns [[vector]]
    # convert to [vector]
    if (

        isinstance(embedding, list)

        and

        len(embedding) > 0

        and

        isinstance(embedding[0], list)

    ):


        embedding = embedding[0]



    return embedding








def store_embeddings(chunks):


    collection = (

        settings.QDRANT_COLLECTION_NAME

    )



    existing = [

        c.name

        for c in

        qdrant_client
        .get_collections()
        .collections

    ]




    # remove previous pdf vectors
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



        vector = get_embedding(

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


        collection_name=collection,


        points=points

    )




    return len(points)









def ask_question(question):



    question_vector = get_embedding(

        question

    )




    result = qdrant_client.query_points(


        collection_name=
        settings.QDRANT_COLLECTION_NAME,



        query=
        question_vector,



        limit=5

    )





    context = ""




    for point in result.points:


        context += (

            point.payload["text"]

            +

            "\n"

        )






    llm = ChatGroq(


        model="llama-3.1-8b-instant",


        api_key=settings.GROQ_API_KEY

    )





    prompt = f"""

You are QueryDocs AI assistant.

Use ONLY the uploaded document context.

Rules:
- Answer questions from the document.
- If user asks for summary, summarize the document.
- If information is missing, say:
"I could not find this information in the document."


DOCUMENT:

{context}


QUESTION:

{question}

"""





    response = llm.invoke(

        prompt

    )




    return response.content
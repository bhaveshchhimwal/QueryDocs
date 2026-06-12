import os

from dotenv import load_dotenv


load_dotenv()



class Settings:


    APP_NAME = os.getenv(
        "APP_NAME",
        "QueryDocs"
    )


    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY"
    )


    HUGGINGFACE_API_KEY = os.getenv(
        "HUGGINGFACE_API_KEY"
    )


    QDRANT_URL = os.getenv(
        "QDRANT_URL"
    )


    QDRANT_API_KEY = os.getenv(
        "QDRANT_API_KEY"
    )


    QDRANT_COLLECTION_NAME = os.getenv(
        "QDRANT_COLLECTION_NAME",
        "querydocs"
    )


    CLOUDINARY_CLOUD_NAME = os.getenv(
        "CLOUDINARY_CLOUD_NAME"
    )


    CLOUDINARY_API_KEY = os.getenv(
        "CLOUDINARY_API_KEY"
    )


    CLOUDINARY_API_SECRET = os.getenv(
        "CLOUDINARY_API_SECRET"
    )



settings = Settings()
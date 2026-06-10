import os
from dotenv import load_dotenv


load_dotenv()


class Settings:

    # App
    APP_NAME = os.getenv(
        "APP_NAME",
        "QueryDocs"
    )


    # Gemini
    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )


    # Qdrant
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


    # Cloudinary
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
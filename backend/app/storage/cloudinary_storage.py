import cloudinary
import cloudinary.uploader

from app.core.config import settings


cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)


def upload_pdf_to_cloudinary(file):

    result = cloudinary.uploader.upload(
        file,
        resource_type="raw",
        folder="QueryDocs"
    )

    return result["secure_url"]
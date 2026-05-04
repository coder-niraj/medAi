from datetime import timedelta
import os
from google.cloud import storage

from services.kms import KMSService


class StorageManager:
    def __init__(self):
        # If STORAGE_EMULATOR_HOST is set, this connects to your Docker container
        self.client = storage.Client(project=KMSService.get_secret("GCP_PROJECT_ID"))
        self.bucket_name = KMSService.get_secret("REPORTS_BUCKET_NAME")

        # Create bucket if it doesn't exist (helpful for local testing)
        try:
            self.bucket = self.client.get_bucket(self.bucket_name)
        except Exception:
            self.bucket = self.client.create_bucket(self.bucket_name)

    def delete_file(self, report):
        # Use the class variables instead of hardcoding new ones
        file_name = report.file_url.rsplit("/", 1)[-1]
        blob = self.bucket.blob(file_name)

        try:
            blob.delete()
            print(f"✅ Deleted {file_name} from {self.bucket_name}")
        except Exception as e:
            # Check if it was already deleted or bucket is missing
            print(f"❌ Storage Deletion failed: {e}")
            raise e

    def upload_file(
        self,
        file_content: bytes,
        destination_name: str,
        content_type: str = "application/pdf",
    ):

        blob = self.bucket.blob(destination_name)
        # Using upload_from_string is perfect for bytes/PDFs
        blob.upload_from_string(file_content, content_type=content_type)

        # In a real GCS scenario, you'd return the public URL or the blob name
        return f"gs://{self.bucket_name}/{destination_name}"

    def download_file(self, gs_path: str) -> bytes:
        
       
        path_without_prefix = gs_path.replace("gs://", "")
        bucket_name, blob_name = path_without_prefix.split("/", 1)

        target_bucket = self.client.bucket(bucket_name)
        blob = target_bucket.blob(blob_name)

        return blob.download_as_bytes()

    def list_files(self):
        blobs = self.client.list_blobs(self.bucket_name)
        return [blob.name for blob in blobs]

    def get_short_lived_url(self, blob_name: str, expires_in_hours: int = 24):
        blob = self.bucket.blob(blob_name)
        try:
           
            blob.reload()
            content_type = blob.content_type
        except Exception:
            content_type = None

       
        if not content_type:
            
            import mimetypes

            content_type, _ = mimetypes.guess_type(blob_name)
            content_type = content_type or "application/octet-stream"

        if os.getenv("STORAGE_EMULATOR_HOST"):
            url = f"{os.getenv('STORAGE_EMULATOR_HOST')}/download/storage/v1/b/{self.bucket_name}/o/{blob_name}?alt=media"
        else:
            url = blob.generate_signed_url(
                version="v4",
                expiration=timedelta(hours=expires_in_hours),
                method="GET",
            )

        return {
            "url": url,
            "content_type": content_type,
        }


storage_manager = StorageManager()

import os
from google.cloud import storage


class StorageManager:
    def __init__(self):
        # If STORAGE_EMULATOR_HOST is set, this connects to your Docker container
        self.client = storage.Client(project=os.getenv("GCP_PROJECT_ID", "medai-dev"))
        self.bucket_name = os.getenv("REPORTS_BUCKET_NAME", "medai-reports")

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
        """
        Extracts bytes from a gs:// path.
        Example: gs://medical-reports/anc -> returns binary data
        """
        # Logic: Remove prefix, split once at the first '/' to separate bucket from filename
        path_without_prefix = gs_path.replace("gs://", "")
        bucket_name, blob_name = path_without_prefix.split("/", 1)

        target_bucket = self.client.bucket(bucket_name)
        blob = target_bucket.blob(blob_name)

        return blob.download_as_bytes()

    def list_files(self):
        blobs = self.client.list_blobs(self.bucket_name)
        return [blob.name for blob in blobs]


storage_manager = StorageManager()

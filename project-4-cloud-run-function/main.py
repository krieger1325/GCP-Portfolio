import functions_framework
from google.cloud import storage, pubsub_v1
from PIL import Image
import io, os, json, logging

logging.getLogger().setLevel(logging.INFO)
storage_client = storage.Client()

# Create clients at import (OK), but read env vars at invoke
publisher = pubsub_v1.PublisherClient()

def _get_env(name: str, required: bool = True, default: str | None = None) -> str | None:
    val = os.getenv(name, default)
    if required and not val:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return val

@functions_framework.cloud_event
def process_image(cloud_event):
    data = cloud_event.data
    bucket_name = data.get("bucket")
    file_name   = data.get("name")

    if not bucket_name or not file_name:
        logging.error("Event missing bucket/name: %s", data)
        return

    # Env vars at invoke time
    output_bucket_name     = _get_env("OUTPUT_BUCKET", required=True)
    quarantine_bucket_name = _get_env("QUARANTINE_BUCKET", required=False)
    pubsub_topic           = _get_env("PUBSUB_TOPIC", required=False)

    # Only handle images
    if not file_name.lower().endswith((".jpg", ".jpeg", ".png")):
        logging.info("Skipping non-image: %s", file_name)
        if quarantine_bucket_name:
            _move_to_quarantine(bucket_name, file_name, quarantine_bucket_name)
        else:
            logging.warning("QUARANTINE_BUCKET not set; skipping quarantine move.")
        return

    # Download
    in_blob = storage_client.bucket(bucket_name).blob(file_name)
    img_bytes = in_blob.download_as_bytes()

    # Convert to grayscale
    img = Image.open(io.BytesIO(img_bytes)).convert("L")

    # Upload
    out_name = file_name.rsplit(".", 1)[0] + ".png"
    out_blob = storage_client.bucket(output_bucket_name).blob(out_name)
    buff = io.BytesIO()
    img.save(buff, format="PNG")
    out_blob.upload_from_string(buff.getvalue(), content_type="image/png")

    logging.info("Processed → gs://%s/%s", output_bucket_name, out_name)

    # Publish downstream notification (full topic path required)
    if pubsub_topic:
        payload = {
            "source_bucket": bucket_name,
            "source_object": file_name,
            "output_bucket": output_bucket_name,
            "output_object": out_name,
            "status": "processed"
        }
        publisher.publish(pubsub_topic, json.dumps(payload).encode("utf-8"))
        logging.info("Published Pub/Sub notification to %s", pubsub_topic)

def _move_to_quarantine(src_bucket_name: str, obj: str, quarantine_bucket_name: str):
    src_blob = storage_client.bucket(src_bucket_name).blob(obj)
    dst_blob = storage_client.bucket(quarantine_bucket_name).blob(obj)
    # rewrite works across locations; copy + delete is also fine
    token, bytes_rewritten, total_bytes = dst_blob.rewrite(src_blob)
    src_blob.delete()
    logging.info("Moved %s to quarantine bucket %s", obj, quarantine_bucket_name)


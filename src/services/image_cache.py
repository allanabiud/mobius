from pathlib import Path
import requests

PUBLISHER_IMAGE_DIR = Path("src/assets/publishers")
PUBLISHER_IMAGE_DIR.mkdir(parents=True, exist_ok=True)


def get_publisher_image(pub_id: int, image_url: str | None) -> str | None:
    """
    Returns a local file path for the publisher image.
    Downloads the image once if not already cached.
    """
    if not image_url:
        return None

    image_path = PUBLISHER_IMAGE_DIR / f"{pub_id}.png"

    # Already cached on disk
    if image_path.exists():
        return str(image_path)

    # First run: download
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        image_path.write_bytes(response.content)
        return str(image_path)
    except Exception as e:
        print(f"Failed to cache image for publisher {pub_id}: {e}")
        return None

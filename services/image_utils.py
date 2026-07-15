from PIL import Image, ImageOps
from io import BytesIO
from pathlib import Path
import uuid

def image_processing(content: bytes) -> tuple:
  with Image.open(BytesIO(content)) as Original:
    img = ImageOps.exif_transpose(Original)

  
  img = ImageOps.fit(img, (300, 300), method=Image.Resampling.LANCZOS)

  if img.mode in ("RGBA", "LA", "P"):
   img = img.convert("RGB")

  filename = f"{uuid.uuid4().hex}.jpg"

  output = BytesIO()
  img.save(output, "JPEG", quality=85, optimize=True)
  output.seek(0)


  return output, filename








  

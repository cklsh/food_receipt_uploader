import pytesseract
from PIL import Image

def text_extract_from_image(image_path: str) -> str:
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

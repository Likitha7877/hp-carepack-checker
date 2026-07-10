import sys
import re
import pytesseract
from PIL import Image, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_serial_from_image(image_path):
    try:
        img = Image.open(image_path)
        img = img.convert('L')
        img = ImageEnhance.Contrast(img).enhance(2.0)
        img = img.resize((img.width * 2, img.height * 2))
        
        text = pytesseract.image_to_string(img, config='--psm 6')
        
        # Remove spaces within potential serial numbers near SN keyword
        # Look for SN followed by fragmented alphanumeric
        sn_match = re.search(r'S[Nn#:\s]+([A-Z0-9][\s A-Z0-9]{7,15})', text)
        if sn_match:
            candidate = re.sub(r'\s+', '', sn_match.group(1))
            candidate = candidate[:10]
            if len(candidate) >= 8:
                print(candidate.upper())
                sys.exit(0)

        # Try direct pattern
        matches = re.findall(r'\b([A-Z0-9]{8,12})\b', text)
        for m in matches:
            if not m.startswith('INPUT') and not m.startswith('HTTP'):
                print(m.upper())
                sys.exit(0)

        print("NOT_FOUND")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    extract_serial_from_image(sys.argv[1])
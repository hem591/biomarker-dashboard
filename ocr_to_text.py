import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

# --- SETTINGS ---
pdf_path = "report1.pdf"
output_txt_path = "ocr_report1.txt"
poppler_path = r"C:\poppler-24.08.0\Library\bin"
tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Point Python to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# --- Step 1: Convert PDF pages to images ---
print(f"📄 Converting all pages of {pdf_path} to images...")
images = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)

# --- Step 2: OCR each page and collect text ---
print("🔍 Running OCR on each page...")
full_text = ""

for i, img in enumerate(images):
    text = pytesseract.image_to_string(img)
    full_text += f"\n\n--- PAGE {i + 1} ---\n{text}"

# --- Step 3: Save OCR text to .txt file ---
with open(output_txt_path, "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"\n✅ OCR complete. Text saved to: {output_txt_path}")

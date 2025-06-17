import re
import json
import os
import sys
from fuzzywuzzy import fuzz
from pdf2image import convert_from_path
import pytesseract
import tempfile

# ─── Setup Tesseract Path if Needed ────────────────────────────────
# Uncomment and edit if tesseract is not in PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# ─── Check CLI Args ────────────────────────────────────────────────
if len(sys.argv) < 2:
    print(json.dumps({"error": "No PDF path provided"}))
    sys.exit(1)

pdf_path = sys.argv[1]
if not os.path.exists(pdf_path):
    print(json.dumps({"error": f"File not found: {pdf_path}"}))
    sys.exit(1)

# ─── Convert PDF Pages to Images ───────────────────────────────────
try:
    images = convert_from_path(pdf_path, dpi=300)
except Exception as e:
    print(json.dumps({"error": f"Failed to convert PDF: {str(e)}"}))
    sys.exit(1)

# ─── Run OCR on All Pages ──────────────────────────────────────────
text = ""
for i, image in enumerate(images):
    try:
        text += pytesseract.image_to_string(image, lang='eng') + "\n"
    except Exception as e:
        print(json.dumps({"error": f"OCR failed on page {i+1}: {str(e)}"}))
        sys.exit(1)

if not text.strip():
    print(json.dumps({"error": "OCR produced empty text"}))
    sys.exit(1)

# ─── Utilities for Extraction ──────────────────────────────────────
def extract_value_near_unit(keywords, text, unit):
    for line in text.splitlines():
        for keyword in keywords:
            if fuzz.partial_ratio(keyword.lower(), line.lower()) >= 80:
                if unit in line:
                    unit_index = line.find(unit)
                    numbers = list(re.finditer(r"[-+]?\d*\.\d+|\d+", line))
                    closest = None
                    min_distance = float("inf")
                    for match in numbers:
                        distance = abs(unit_index - match.start())
                        if distance < min_distance:
                            closest = match
                            min_distance = distance
                    if closest:
                        return float(closest.group())
    return None

def extract_value(label_keywords, text, unit=None):
    for keyword in label_keywords:
        pattern = fr"{keyword}.*?(\d+\.?\d*)\s*{unit if unit else ''}"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return float(match.group(1))
    return None

def extract_date(text):
    date_patterns = [
        r"\b\d{2}[/-][A-Za-z]{3}[/-]\d{4}\b",
        r"\b\d{2}[./-]\d{2}[./-]\d{4}\b",
        r"\b\d{4}-\d{2}-\d{2}\b",
        r"\b\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}\b"
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()
    return "unknown"

# ─── Extract Biomarker Data ────────────────────────────────────────
data = {
    "date": extract_date(text),
    "total_cholesterol": extract_value(["total cholesterol"], text, "mg/dL"),
    "ldl": extract_value(["ldl", "ldl cholesterol"], text, "mg/dL"),
    "hdl": extract_value_near_unit(["hdl", "hdl cholesterol"], text, "mg/dL"),
    "triglycerides": extract_value(["triglycerides"], text, "mg/dL"),
    "creatinine": extract_value_near_unit(["creatinine"], text, "mg/dL"),
    "vitamin_d": extract_value_near_unit(["vitamin d"], text, "ng/mL"),
    "vitamin_b12": extract_value_near_unit(["vitamin b12", "vit b-12"], text, "pg/mL"),
    "hba1c": extract_value(["hba1c", "glycosylated hemoglobin"], text, "%")
}

# ─── Output Clean JSON to STDOUT ───────────────────────────────────
print(json.dumps(data))
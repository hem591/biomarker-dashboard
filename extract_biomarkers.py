import re
import json
import os

# Step 1: Load the OCR text
with open("ocr_report1.txt", "r", encoding="utf-8") as f:
    text = f.read()
from fuzzywuzzy import fuzz
import re

def extract_value_near_unit(keywords, text, unit, debug=False):
    for line in text.splitlines():
        for keyword in keywords:
            if fuzz.partial_ratio(keyword.lower(), line.lower()) >= 80:
                if debug:
                    print(f"\n[MATCH] '{keyword}' matched → {line.strip()}")
                if unit in line:
                    unit_index = line.find(unit)
                    # Find all numbers in the line with positions
                    numbers = list(re.finditer(r"[-+]?\d*\.\d+|\d+", line))
                    if debug:
                        for match in numbers:
                            print(f"  number: {match.group()} at index {match.start()}")

                    # Find number closest to the unit
                    closest = None
                    min_distance = float("inf")
                    for match in numbers:
                        distance = abs(unit_index - match.start())
                        if distance < min_distance:
                            closest = match
                            min_distance = distance

                    if closest:
                        value = float(closest.group())
                        if debug:
                            print(f"[RESULT] Closest to unit '{unit}': {value}")
                        return value
    return None

# Step 2: Define an extraction helper
def extract_value(label_keywords, text, unit=None):
    for keyword in label_keywords:
        # Allow anything (even dots or spaces) between keyword and value
        pattern = fr"{keyword}.*?(\d+\.?\d*)\s*{unit if unit else ''}"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            print(f"[DEBUG] Matched {keyword}: {match.group(1)}")
            return float(match.group(1))
    print(f"[DEBUG] No match for {label_keywords}")
    return None


# Step 3: Extract values
def extract_date(text):
    # Match formats like: 13-Sep-2024, 13/09/2024, 2024-09-13, 13.09.2024
    date_patterns = [
        r"\b\d{2}[/-][A-Za-z]{3}[/-]\d{4}\b",  # 13-Sep-2024
        r"\b\d{2}[./-]\d{2}[./-]\d{4}\b",      # 13/09/2024 or 13.09.2024
        r"\b\d{4}-\d{2}-\d{2}\b",              # 2024-09-13
        r"\b\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}\b"      # 13 Sep 2024
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()
    return "unknown"


data = {
    "date": extract_date(text),  # extracted dynamically

    # Lipids
    "total_cholesterol": extract_value(["total cholesterol"], text, "mg/dL"),
    "ldl": extract_value(["ldl", "ldl cholesterol"], text, "mg/dL"),
    "hdl": extract_value_near_unit(["hdl", "hdl cholesterol"], text, "mg/dL"),
    "triglycerides": extract_value(["triglycerides"], text, "mg/dL"),

    # Renal function
    "creatinine": extract_value_near_unit(["creatinine"], text, "mg/dL"),

    # Vitamins
    "vitamin_d": extract_value_near_unit(["vitamin d"], text, "ng/mL"),
    "vitamin_b12": extract_value_near_unit(["vitamin b12", "vit b-12"], text, "pg/mL"),

    # Diabetes marker
    "hba1c": extract_value(["hba1c", "glycosylated hemoglobin"], text, "%")
}


# Step 4: Save to sample.json
os.makedirs("data", exist_ok=True)
with open("data/sample.json", "w") as f:
    json.dump([data], f, indent=2)

print("✅ Biomarker values extracted and saved to data/sample.json")

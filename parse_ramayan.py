import pdfplumber
import json
import re

pdf_path = "Shrimad Valmiki Ramayana (Hindi Edition) - Valmiki.pdf"
output_json = "ramayana_data.json"

database = {}

current_kanda = 1
current_sarga = 1

print("PDF ko parse kiya ja raha hai, kripya intezaar karein...")

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text:
            continue
        
        # Kandas ki pehchan ke liye keywords check karna
        if "बालकाण्ड" in text:
            current_kanda = 1
        elif "अयोध्याकाण्ड" in text:
            current_kanda = 2
        elif "अरण्यकाण्ड" in text:
            current_kanda = 3
        elif "किष्किन्धाकाण्ड" in text:
            current_kanda = 4
        elif "सुन्दरकाण्ड" in text:
            current_kanda = 5
        elif "युद्धकाण्ड" in text or "लंकाकाण्ड" in text:
            current_kanda = 6
        elif "उत्तरकाण्ड" in text:
            current_kanda = 7

        # Sarga number detect karne ke liye logic
        sarga_match = re.search(r'सर्ग\s*[:\-]?\s*(\d+)', text)
        if sarga_match:
            current_sarga = int(sarga_match.group(1))

        # Shlokon ko extract karne ke liye lines ko process karna
        lines = text.split('\n')
        buffer_lines = []
        
        for line in lines:
            shloka_match = re.search(r'॥\s*(\d+)\s*॥', line)
            if shloka_match:
                shloka_num = int(shloka_match.group(1))
                buffer_lines.append(line)
                full_text = " ".join(buffer_lines)
                
                key = f"{current_kanda}-{current_sarga}-{shloka_num}"
                database[key] = {
                    "num": shloka_num,
                    "sanskrit": full_text,
                    "words": [],
                    "hindi": "Yahan Hindi bhavarth aayega.",
                    "aiExplanation": "Mahatvapurna jeevan seekh aur katha sandarbh."
                }
                buffer_lines = []
            else:
                buffer_lines.append(line)

# JSON file mein save karna
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(database, f, ensure_ascii=False, indent=4)

print(f"Data successfully parse ho gaya hai aur '{output_json}' file ban gayi hai!")
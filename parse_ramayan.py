import pdfplumber
import json
import re

pdf_path = "Ramayan.pdf"
output_json = "ramayana_data.json"

database = {}
current_kanda = 1
current_sarga = 1

print("PDF se shlok aur Hindi bhavarth parse kiye ja rahe hain...")

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text:
            continue
        
        # Kandas ki pehchan
        if "बालकाण्ड" in text: current_kanda = 1
        elif "अयोध्याकाण्ड" in text: current_kanda = 2
        elif "अरण्यकाण्ड" in text: current_kanda = 3
        elif "किष्किन्धाकाण्ड" in text: current_kanda = 4
        elif "सुन्दरकाण्ड" in text: current_kanda = 5
        elif "युद्धकाण्ड" in text or "लंकाकाण्ड" in text: current_kanda = 6
        elif "उत्तरकाण्ड" in text: current_kanda = 7

        # Sarga detection
        sarga_match = re.search(r'सर्ग\s*[:\-]?\s*(\d+)', text)
        if sarga_match:
            current_sarga = int(sarga_match.group(1))

        # Text blocks ko line-by-line analyse karna
        lines = text.split('\n')
        current_shlok_num = None
        sanskrit_buffer = []
        hindi_buffer = []
        capturing_hindi = False

        for line in lines:
            shloka_match = re.search(r'॥\s*(\d+)\s*॥', line)
            if shloka_match:
                # Agar pehle se koi shlok tha, toh use save karo
                if current_shlok_num is not None:
                    key = f"{current_kanda}-{current_sarga}-{current_shlok_num}"
                    database[key] = {
                        "num": current_shlok_num,
                        "sanskrit": "\n".join(sanskrit_buffer).strip(),
                        "words": [],
                        "hindi": " ".join(hindi_buffer).strip() or "इस श्लोक का हिंदी भावार्थ यहाँ उपलब्ध है।",
                        "aiExplanation": "मर्यादा पुरुषोत्तम भगवान श्रीराम का यह पावन चरित्र जीवन में धर्म और कर्म का मार्ग दिखाता है।"
                    }
                
                current_shlok_num = int(shloka_match.group(1))
                sanskrit_buffer = [line]
                hindi_buffer = []
                capturing_hindi = True
            elif capturing_hindi:
                # Shlok ke baad ka text hindi bhavarth maana jayega tab tak jab agla shlok na aaye
                if "ISBN" in line or "श्रीवाल्मीकीय" in line:
                    continue
                hindi_buffer.append(line)
            else:
                sanskrit_buffer.append(line)

# JSON file mein save karna
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(database, f, ensure_ascii=False, indent=4)

print(f"Badiya! Poora data parse hokar '{output_json}' mein save ho gaya hai.")
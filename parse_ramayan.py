import pdfplumber
import json
import re

pdf_path = "Shrimad Valmiki Ramayana (Hindi Edition) - Valmiki.pdf"
output_json = "ramayana_data.json"

# Define the data structure
database = {}

# Regex patterns (adjust these based on the exact PDF text formatting)
# Matches "सर्ग १", "सर्ग २", etc.
sarga_pattern = re.compile(r'सर्ग\s+(\d+)') 
# Matches Shloka numbers like "॥१॥", "॥२॥"
shloka_pattern = re.compile(r'॥(\d+)॥')

current_kanda = 1 # Update manually or via regex if Kanda headers are clear
current_sarga = 1

with pdfplumber.open(pdf_path) as pdf:
    full_text = ""
    # Skip index pages; start from the actual text (e.g., page 50)
    for page in pdf.pages[50:100]: 
        text = page.extract_text()
        if text:
            full_text += text + "\n"

# Logic to split text into blocks based on Shloka markers
shloka_blocks = shloka_pattern.split(full_text)

# Example parsing logic to build the JSON dictionary
# In a real scenario, you will need to tweak the string splitting to accurately separate Sanskrit, Padachhed, and Bhavarth.
for i in range(1, len(shloka_blocks), 2):
    shloka_num = int(shloka_blocks[i])
    content = shloka_blocks[i+1].strip()
    
    # Generate the unique key (Kanda-Sarga-Shloka)
    key = f"{current_kanda}-{current_sarga}-{shloka_num}"
    
    database[key] = {
        "num": shloka_num,
        "sanskrit": "Extracted Sanskrit Text", # Requires fine-tuned regex
        "words": [], # Padachhed extraction
        "hindi": "Extracted Hindi Bhavarth",
        "aiExplanation": ""
    }

# Save to JSON
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(database, f, ensure_ascii=False, indent=4)

print("JSON Database generated successfully.")
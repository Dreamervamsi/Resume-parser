import fitz
from fastapi import FastAPI,UploadFile,File
from pathlib import Path
import pytesseract as pt
from PIL import Image
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

def model(raw_text):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"user",
                "content":f""" 
                You are a hiring bias removal assistant.
    
                Given the raw resume text below, do the following:
                    1. Remove or mask all personally identifiable information:
                       - Name → replace with [NAME]
                       - Email → replace with [EMAIL]
                       - Phone → replace with [PHONE]
                       - Location / City / Country → remove
                       - Date of Birth → remove
                       - Graduation years → remove, keep degree name only
                       - Work date ranges (e.g. 2015-2022) → convert to duration (e.g. 7 years)
                       - Photo references → remove
                       - Ethnicity, Marital Status, Religion → remove
                    2. Neutralize gendered language:
                       - "mother/father" → "parent"
                       - "maternity/paternity leave" → "parental leave"
                       - "female/male engineer" → "engineer"
                    3. Return a clean JSON with this structure:
                    {{
                        "summary": "...",
                        "skills": ["skill1", "skill2"],
                     "experience": [
                            {{"role": "...", "company": "...", "duration": "X years"}}
                        ],
                        "total_experience": "X years",
                        "education": "...",
                        "projects": "..."
                    }}
    
            Return ONLY the JSON. No explanation, no extra text.
    
            Resume Text:
            {raw_text}
            """
            
            }
        ]
    )
    return res.choices[0].message.content

@app.post('/upload')
async def file_upload(file:UploadFile = File(...)):
    data = await file.read()

    path = Path(file.filename)
    
    text = ""
    if path.suffix.lower() == '.pdf' or path.suffix.lower() == '.docx' or path.suffix.lower() == '.txt':
        doc = fitz.open(stream=data)
        for i in doc:
            text+=i.get_text()
        
        if text == '':
            for pn,page in enumerate(doc):
                pix = page.get_pixmap()

                img = Image.frombytes("RGB",[pix.width,pix.height],pix.samples)
                
                text += pt.image_to_string(img)

        res = model(text)

        return res
    else:
        doc = fitz.open(stream=data)
       
        for pn,page in enumerate(doc):
                pix = page.get_pixmap()

                img = Image.frombytes("RGB",[pix.width,pix.height],pix.samples)
                
                text += pt.image_to_string(img)

        res = model(text)

        return res



pt.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
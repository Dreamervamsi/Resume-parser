import fitz
from fastapi import FastAPI,UploadFile,File
# import ollama

app = FastAPI()

# client = ollama.Client(host="https://ollama.com", headers={"Authorization": "Bearer "})

@app.post('/upload')
async def file_upload(file:UploadFile = File(...)):
    data = await file.read()

    doc=""
    if file.content_type == "application/pdf":
        doc = fitz.open(stream=data)
    
    text=""
    for i in doc:
        text+=i.get_text() 
        
    if text == '':
        return "file contains scanned docs"

    return text

# @app.get('/ask')
# def get_details():
#     response = ollama.chat(model='llama3.2', messages=[
#     {
#         'role': 'user',
#         'content': 'Explain how to use an API in one sentence.',
#     },
#     ])
#     return response['message']['content']
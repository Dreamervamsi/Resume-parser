I realized recently that the hardest part of building a side project is actually just picking what to build.

**For a few days, I found myself wanting to start a new project, but nothing was really striking my mind. Then I decided to look at recent hackathon problem statements for inspiration. I browsed through a few options and finally selected one that stood out: an AI-powered resume parser designed to mask hiring bias.**

I just wrapped up the first phase of the build. Here are 3 specific technical challenges I solved to get the data foundation working.

**1. Processing PDFs completely in memory**

I initially thought I had to save uploaded resumes directly to the server's disk to read them. 

Instead, I learned how to pass the Raw byte stream directly into my Python parser (PyMuPDF). 

This completely bypasses the need for temporary file storage and makes the upload process much faster.

**2. Separating the UI from the logic**

It is always tempting to build a single app script to save time. 

I decided to split the architecture from day one instead. 

I built a standalone backend using FastAPI to handle the text extraction and API requests. 

Then, I built a lightweight Streamlit frontend just to act as the user interface.

**3. Handling scanned resumes gracefully**

Not all PDFs contain actual text. Some are just scanned images. 

When testing my parser, it was returning blank strings for these files and breaking my logic. 

I added a check to catch when the extracted text is empty. Now, the API immediately returns a helpful alert that the file contains scanned documents, rather than failing silently down the line.

Next up, I am setting up a local LLM to do the actual parsing and masking of the extracted data. 

**The Tech Stack so far:**
* Frontend: Streamlit
* Backend: FastAPI (Python)
* PDF Parser: PyMuPDF (fitz)
* Coming soon: Local LLMs via Ollama

What is your favorite tool or library for extracting text from messy PDFs?

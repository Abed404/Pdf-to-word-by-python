# file: main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
import uuid
import fitz  # PyMuPDF
from docx import Document

app = FastAPI()

@app.post("/convert/")
async def convert_pdf_to_word(file: UploadFile = File(...)):
    file_location = f"temp/{uuid.uuid4()}.pdf"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Convert PDF to Word
    doc = fitz.open(file_location)
    word_doc = Document()

    for page in doc:
        text = page.get_text()
        word_doc.add_paragraph(text)

    output_path = file_location.replace(".pdf", ".docx")
    word_doc.save(output_path)

    # Cleanup PDF
    os.remove(file_location)

    return FileResponse(output_path, filename="converted.docx", media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
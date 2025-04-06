import os
import PyPDF2
import fitz  # PyMuPDF
from PIL import Image
import pytesseract

# Optional: specify Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"



def extract_text_with_pypdf2(filepath):
    """Extract text from PDF using PyPDF2."""
    print("🔎 Trying PyPDF2 text extraction...")
    text = ""
    try:
        with open(filepath, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text() or ""
                text += f"\n\n--- PyPDF2 Page {page_num} ---\n\n{page_text}"
        return text.strip()
    except Exception as e:
        print(f"❌ PyPDF2 error: {e}")
        return ""

def extract_text_with_fitz(filepath):
    """Extract text from PDF using PyMuPDF (fitz)."""
    print("🔎 Trying PyMuPDF text extraction...")
    text = ""
    try:
        with fitz.open(filepath) as doc:
            for page_num, page in enumerate(doc, start=1):
                page_text = page.get_text()
                text += f"\n\n--- PyMuPDF Page {page_num} ---\n\n{page_text}"
        return text.strip()
    except Exception as e:
        print(f"❌ PyMuPDF error: {e}")
        return ""

def extract_text_with_ocr(filepath):
    """Fallback OCR for scanned PDFs."""
    print("🔎 Trying OCR extraction with pytesseract...")
    text = ""
    try:
        with fitz.open(filepath) as doc:
            for page_num, page in enumerate(doc, start=1):
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                page_text = pytesseract.image_to_string(img)
                text += f"\n\n--- OCR Page {page_num} ---\n\n{page_text}"
        return text.strip()
    except Exception as e:
        print(f"❌ OCR error: {e}")
        return ""

def extract_text_from_pdf(filepath):
    """
    Try PyPDF2 ➡️ PyMuPDF ➡️ OCR
    """
    print(f"📂 Extracting text from: {filepath}")

    # 1. Try PyPDF2
    text = extract_text_with_pypdf2(filepath)
    if text:
        return text

    # 2. Try PyMuPDF
    text = extract_text_with_fitz(filepath)
    if text:
        return text

    # 3. Fallback to OCR
    text = extract_text_with_ocr(filepath)
    if text:
        return text

    # Nothing worked
    print("⚠️ No text could be extracted!")
    return None

# 👉 Call the function here
if __name__ == "__main__":
    pdf_path = "c:/Users/MEVIN/Downloads/sample.pdf"  # Change to your file path

    extracted_text = extract_text_from_pdf(pdf_path)

    if extracted_text:
        print("\n✅ Extracted Text:\n")
        print(extracted_text)
    else:
        print("\n⚠️ No text extracted from the PDF.")

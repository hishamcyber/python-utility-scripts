print("SCRIPT STARTED")

import os
import sys
import easyocr
import PyPDF2

# 1. Validate terminal arguments
if len(sys.argv) < 2:
    print("Usage: python script.py <filename>")
    sys.exit(1)

file_path = sys.argv[1]

# 2. Check file existence
if os.path.exists(file_path):
    print("File found! Processing...")
else:
    print("Error: File not found.")
    sys.exit(1)

# 3. Handle file extensions cleanly
filename, file_ext = os.path.splitext(file_path)
file_ext = file_ext.lower()
print(f"Detected file extension: {file_ext}")

# Use file_type instead of the built-in 'type' keyword
if file_ext in [".png", ".jpg", ".jpeg", ".webp"]:
    print("Detected image file.")
    file_type = "image"
elif file_ext == ".pdf":
    print("Detected PDF file.")
    file_type = "pdf"
else:
    print("Error: Unsupported file format.")
    sys.exit(1)

# filename already contains the original directory structure!
# Adding .txt directly saves it in the exact same folder as the original file.
result_path = f"{filename}.txt"


# 4. Define extraction helper functions
def extract_text_from_image(image_path):
    print("📸 Initializing EasyOCR engine (this may take a few seconds)...")
    # Initialize the reader for English (gpu=False runs on CPU)
    reader = easyocr.Reader(["en"], gpu=False)
    
    print("🔍 Scanning image for text...")
    results = reader.readtext(image_path)
    
    # Extract just the text strings from the results tuple (bounding_box, text, confidence)
    extracted_lines = [line[1] for line in results]
    
    # Join all lines into a single string separated by newlines
    extracted_text = "\n".join(extracted_lines)
    return extracted_text


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(reader.pages)
        extracted_text = ""

        for page_num in range(num_pages):
            page = reader.pages[page_num]
            page_text = page.extract_text()

            if page_text:
                extracted_text += (
                    page_text + f"\n--- Page {page_num + 1} Break ---\n\n"
                )

        return extracted_text


# 5. Route processing based on file type
if file_type == "image":
    extracted_text = extract_text_from_image(file_path)
elif file_type == "pdf":
    extracted_text = extract_text_from_pdf(file_path)

# 6. Save results to disk
with open(result_path, "w", encoding="utf-8") as output_file:
    output_file.write(extracted_text)

print(f"✅ Success! Extracted {len(extracted_text)} characters.")

# 7. Optimized warning handling
if not extracted_text.strip():
    print(
        "⚠️ Warning: The extracted text is completely empty. No readable text was found."
    )

import os
from docx import Document
import PyPDF2

def extract_text(file_path):
    """Extract text from .docx, .pdf, or .txt files."""
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if ext == '.docx':
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs if para.text])
        elif ext == '.pdf':
            with open(file_path, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                return "\n".join([page.extract_text() or "" for page in pdf.pages])
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    except Exception as e:
        raise RuntimeError(f"Error extracting {file_path}: {str(e)}")

def extract_all_resumes(input_dir, output_dir):
    """Extract text from all resumes in input_dir and save to output_dir as .txt."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    extracted_files = []
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        if os.path.isfile(input_path):
            try:
                text = extract_text(input_path)
                output_filename = os.path.splitext(filename)[0] + '.txt'
                output_path = os.path.join(output_dir, output_filename)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                extracted_files.append(output_filename)
            except Exception as e:
                print(f"Failed to extract {filename}: {str(e)}")
    
    return extracted_files

if __name__ == "__main__":
    input_dir = "data/resumes_raw"
    output_dir = "data/resumes_parsed"
    extracted = extract_all_resumes(input_dir, output_dir)
    print("Extracted files:", extracted)
import re
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    """
    Membaca file PDF asli dan mengekstrak seluruh teks di dalamnya,
    termasuk teks yang berstatus sebagai annotations/catatan.
    """
    try:
        reader = PdfReader(pdf_path)
        extracted_text = ""
        
        for page in reader.pages:
            # 1. Ambil teks standar di halaman PDF
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
                
            # 2. Ambil teks dari Annotations (Solusi buat file dummy kita)
            if '/Annots' in page:
                for annot in page['/Annots']:
                    obj = annot.get_object()
                    if obj and '/Contents' in obj:
                        extracted_text += str(obj['/Contents']) + "\n"
                        
        return extracted_text
    except Exception as e:
        print(f"[ERROR] Gagal membaca file {pdf_path}: {str(e)}")
        return ""
def clean_resume_text(text):
    """
    Pipeline NLP untuk membersihkan teks CV:
    Ubah ke lowercase, bersihkan spasi berlebih, dan hilangkan karakter aneh
    tanpa merusak kata kunci teknologi (seperti C++, Node.js, dll).
    """
    # 1. Ubah jadi huruf kecil semua
    text = text.lower()
    
    # 2. Bersihkan URL/Link dan Email agar tidak mengacaukan skor kompetensi
    text = re.sub(r'http\S+\s*', ' ', text)
    text = re.sub(r'\S*@\S*\s*', ' ', text)
    
    # 3. Ganti karakter baris baru dan spasi berlebih menjadi satu spasi biasa
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

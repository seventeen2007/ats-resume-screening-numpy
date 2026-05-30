import re

# Daftar stop words bahasa Indonesia & Inggris standar lowongan kerja
STOP_WORDS = {
    'saya', 'dengan', 'di', 'dan', 'yang', 'untuk', 'pada', 'ke', 'dari', 'ini',
    'itu', 'adalah', 'bisa', 'memiliki', 'mampu', 'dapat', 'i', 'with', 'and', 
    'the', 'to', 'in', 'of', 'for', 'a', 'an', 'is', 'have', 'has', 'am'
}

def clean_text(text):
    # 1. Case Folding (Ubah jadi huruf kecil semua)
    text = text.lower()
    
    # 2. Hapus tanda baca, angka, dan karakter aneh
    text = re.sub(r'[^a-z\s]', ' ', text)
    
    # 3. Tokenisasi (Pecah teks jadi per kata)
    words = text.split()
    
    # 4. Stopwords Removal (Buang kata yang tidak bermakna teknis)
    cleaned_words = [w for w in words if w not in STOP_WORDS]
    
    return cleaned_words

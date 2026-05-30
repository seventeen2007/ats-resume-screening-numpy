import re

# Stopwords esensial agar AI fokus pada pola kata kunci penipuan
STOP_WORDS = {'dan', 'yang', 'di', 'untuk', 'dari', 'ini', 'itu', 'ke', 'adalah', 'bisa'}

def preprocess_sms(text):
    # 1. Case Folding
    text = text.lower()
    
    # 2. Standarisasi URL/Link (Ubah semua link spesifik menjadi token khusus 'url_token')
    text = re.sub(r'https?://\S+|www\.\S+|bit\.ly/\S+', 'url_token', text)
    
    # 3. Standarisasi Nomor Rekening / Angka Jutaan (Ubah jadi 'angka_token')
    text = re.sub(r'\d+', 'angka_token', text)
    
    # 4. Hapus tanda baca sisa
    text = re.sub(r'[^a-z\s_]', '', text)
    
    # 5. Tokenisasi & Buang Stopwords
    words = text.split()
    cleaned_words = [w for w in words if w not in STOP_WORDS and len(w) > 1]
    
    return cleaned_words

import numpy as np

def hitung_tfidf(semua_dokumen):
    # semua_dokumen berisi list dari list kata [[kata1, kata2], [kata1, kata3]]
    
    # 1. Bikin Kosakata Unik (Vocabulary Global)
    vocab = sorted(list(set([kata for dok in semua_dokumen for kata in dok])))
    word_to_idx = {word: i for i, word in enumerate(vocab)}
    
    N = len(semua_dokumen)
    M = len(vocab)
    
    # 2. Hitung Term Frequency (TF)
    tf = np.zeros((N, M))
    for i, dok in enumerate(semua_dokumen):
        for kata in dok:
            if kata in word_to_idx:
                tf[i, word_to_idx[kata]] += 1
        # Normalisasi TF (Term Frequency relatif terhadap panjang dokumen)
        total_kata = len(dok) if len(dok) > 0 else 1
        tf[i, :] = tf[i, :] / total_kata
        
    # 3. Hitung Inverse Document Frequency (IDF)
    # Menghitung berapa banyak dokumen yang mengandung kata X
    doc_counts = np.sum(tf > 0, axis=0)
    # Rumus IDF standard dengan smoothing (+1) agar tidak pembagian dengan nol
    idf = np.log((1 + N) / (1 + doc_counts)) + 1
    
    # 4. Gabungkan jadi Matriks TF-IDF
    tfidf_matrix = tf * idf
    
    return tfidf_matrix, vocab

def hitung_cosine_similarity(vektor_a, vektor_b):
    # Rumus Cosine Similarity: (A dot B) / (||A|| * ||B||)
    dot_product = np.dot(vektor_a, vektor_b)
    norm_a = np.linalg.norm(vektor_a)
    norm_b = np.linalg.norm(vektor_b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

import os
from pdf_parser import extract_text_from_pdf, clean_resume_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from colorama import Fore, init

# Inisialisasi visual warna terminal
init(autoreset=True)

# 1. DEFINE JOB DESCRIPTION (KRITERIA YANG DICARI PERUSAHAAN)
# Kita set kembali ke core kompetensi kamu: Backend Developer
JOB_DESCRIPTION = """
Dibutuhkan Senior Backend Developer yang mahir menggunakan framework Laravel dan Python. 
Menguasai manajemen database SQL / MySQL, pembuatan REST API yang efisien, 
serta terbiasa menggunakan Git untuk version control di dalam tim developer.
"""

def main():
    print(f"{Fore.CYAN}=======================================================")
    print(f"{Fore.GREEN}     MITRA KREASI DIGITAL - AI CV ANALYZER v2.0        ")
    print(f"{Fore.CYAN}=======================================================")
    
    # 2. DEFINISIKAN DATABASE FILE PDF PELAMAR
    # Memetakan file PDF riil yang ada di folder project
    resume_files = {
        "Pelamar_AL (Senior Backend)": "cv_al.pdf",
        "Pelamar_Budi (Digital Marketing)": "cv_budi.pdf"
    }
    
    # 3. PIPELINE PARSING & CLEANING TEXT
    print(f"{Fore.YELLOW}[INFO] Memulai ekstraksi dokumen PDF asli...")
    cleaned_resumes = []
    candidate_names = []
    
    for name, file_path in resume_files.items():
        if os.path.exists(file_path):
            # Ekstrak teks dari PDF beneran
            raw_text = extract_text_from_pdf(file_path)
            # Bersihkan teks menggunakan NLP preprocessor kita
            cleaned_text = clean_resume_text(raw_text)
            
            cleaned_resumes.append(cleaned_text)
            candidate_names.append(name)
            print(f"{Fore.BLUE}[PARSED] Successfully extracted: {file_path}")
        else:
            print(f"{Fore.RED}[WARN] File {file_path} tidak ditemukan!")

    if not cleaned_resumes:
        print(f"{Fore.RED}[ERROR] Tidak ada data CV yang berhasil diproses. Pembatalan.")
        return

    # Bersihkan juga teks Kriteria Lowongan
    cleaned_job_desc = clean_resume_text(JOB_DESCRIPTION)
    
    # 4. UPGRADE KE SKLEARN MACHINE LEARNING ENGINE
    # Gabungkan kriteria lowongan dengan teks CV untuk proses enkoding vektor
    all_documents = [cleaned_job_desc] + cleaned_resumes
    
    # Inisialisasi TF-IDF Vectorizer standar industri
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_documents)
    
    # Hitung Cosine Similarity antara Kriteria Lowongan (index 0) dengan semua CV pelamar
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    # 5. GENERATE HRD DASHBOARD REPORT
    print(f"\n{Fore.MAGENTA}>>> RANKING KANDIDAT BERDASARKAN SKOR ATS <<<")
    print(f"{'-'*60}")
    
    # Gabungkan nama kandidat dan skornya, lalu urutkan dari yang tertinggi
    results = list(zip(candidate_names, similarity_scores))
    results.sort(key=lambda x: x[1], reverse=True)
    
    for rank, (name, score) in enumerate(results, 1):
        percentage = score * 100
        
        # Formatting warna berdasarkan skor kelulusan (Threshold: 40%)
        if percentage >= 30:
            status = f"{Fore.GREEN}LOLOS (Rekomendasi Interview)"
            warna_skor = Fore.GREEN
        else:
            status = f"{Fore.RED}GAGAL (Kualifikasi Tidak Cocok)"
            warna_skor = Fore.RED
            
        print(f"Peringkat {rank} : {name}")
        print(f"Skor Aliansi : {warna_skor}{percentage:.2f}%")
        print(f"Status       : {status}")
        print(f"{'-'*60}")

if __name__ == "__main__":
    main()

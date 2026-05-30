from preprocessor import clean_text
from vectorizer import hitung_tfidf, hitung_cosine_similarity
import numpy as np
from colorama import Fore, init

init(autoreset=True)

# 1. INPUT STANDARD KUALIFIKASI LOWONGAN (JOB DESCRIPTION)
JOB_DESCRIPTION = """
Dibutuhkan Digital Marketer dan Content Writer profesional. Menguasai teknik SEO, copy writing iklan, 
dan mampu mengelola campaign di media sosial. Mahir membuat konten visual menggunakan Canva 
serta terbiasa menulis artikel di blog berbasis WordPress untuk meningkatkan traffic.
"""

# 2. DATA PELAMAR (RESUME DATABASE SIMULATION)
# Kita bikin profil pelamar dengan variasi skill yang kontras
RESUME_DATABASE = {
    "Pelamar_Al": """
    Software Engineer lulusan SMK jurusan Rekayasa Perangkat Lunak (RPL). Memiliki keahlian kuat 
    dalam web development menggunakan framework Laravel PHP, database MySQL SQL, serta otomatisasi script 
    menggunakan Python. Berpengalaman membangun sistem manajemen digital, RESTful API backend, 
    dan melatih model machine learning sederhana menggunakan library NumPy. Aktif menggunakan Git untuk kolaborasi kode.
    """,
    "Pelamar_Budi": """
    Saya seorang Fullstack Web Developer. Fokus pada frontend teknologi seperti HTML, CSS, JavaScript, 
    dan framework ReactJS. Bisa sedikit PHP native untuk backend, tapi lebih suka mendesain UI/UX yang responsif 
    menggunakan TailwindCSS dan Figma. Kurang menyukai Python ataupun data science.
    """,
    "Pelamar_Chandra": """
    Seorang Content Writer dan Digital Marketer berpengalaman selama 3 tahun. Mahir menulis artikel SEO, 
    mengelola campaign di media sosial, copy writing iklan, serta berkomunikasi dengan klien. 
    Menguasai tools Microsoft Office, Canva, dan WordPress dasar untuk blogging.
    """
}

def running_screening_system():
    print(f"{Fore.CYAN}=======================================================")
    print(f"{Fore.GREEN}     AL ENTERPRISE NLP RESUME SCREENING ENGINE V1      ")
    print(f"{Fore.CYAN}=======================================================")
    
    # Preprocessing teks Job Desc
    job_desc_tokens = clean_text(JOB_DESCRIPTION)
    
    nama_pelamar = list(RESUME_DATABASE.keys())
    semua_dokumen = [job_desc_tokens] # Index 0 selalu milik Job Desc
    
    # Preprocessing teks semua CV pelamar
    for nama in nama_pelamar:
        cv_tokens = clean_text(RESUME_DATABASE[nama])
        semua_dokumen.append(cv_tokens)
        
    print(f"{Fore.YELLOW}[INFO] Berhasil memproses {len(nama_pelamar)} resume dari database.")
    print(f"{Fore.YELLOW}[INFO] Membangun Vektor Matriks TF-IDF secara dinamis...")
    
    # Proses ekstraksi fitur dan pembobotan kata menggunakan NumPy
    matrix, vocab = hitung_tfidf(semua_dokumen)
    
    vektor_job_desc = matrix[0] # Vektor target
    hasil_scoring = []
    
    # Hitung kemiripan tiap CV dengan Job Desc
    for idx, nama in enumerate(nama_pelamar):
        vektor_cv = matrix[idx + 1] # Index bergeser 1 karena index 0 dipakai Job Desc
        skor_kemiripan = hitung_cosine_similarity(vektor_job_desc, vektor_cv)
        
        # Konversi ke bentuk persentase
        match_percentage = skor_kemiripan * 100
        hasil_scoring.append((nama, match_percentage))
        
    # Sortir hasil berdasarkan persentase kecocokan tertinggi (Descending)
    hasil_scoring.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n{Fore.GREEN}>>> HASIL EVALUASI RANKING PELAMAR AUTOMATIS <<<")
    print(f"{'-'*55}")
    print(f"{'Peringkat':<10} | {'Nama Kandidat':<18} | {'Persentase Match':<15}")
    print(f"{'-'*55}")
    
    for rank, (nama, skor) in enumerate(hasil_scoring, 1):
        # Tentukan warna teks berdasarkan kelayakan skor
        if skor >= 50.0:
            warna = Fore.GREEN  # Layak interview
        elif skor >= 25.0:
            warna = Fore.YELLOW # Pertimbangan
        else:
            warna = Fore.RED    # Auto-reject
            
        print(f"{rank:<10} | {nama:<18} | {warna}{skor:.2f}%")
        
    print(f"{'-'*55}")
    print(f"{Fore.CYAN}=======================================================")

if __name__ == "__main__":
    running_screening_system()

# Cara Menjalankan WargaBot

## 1. Persiapan

Pasang Python 3.10 atau yang lebih baru. Ekstrak ZIP, buka terminal pada folder `aplikasi-final`, lalu jalankan:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
```

## 2. Isi data kampung

Buka `themes/kampung.json`. File saat ini memakai nilai contoh fiktif untuk tugas kuliah. Ganti `terakhir_diperbarui` dan seluruh 21 nilai di blok `data` dengan informasi yang dikonfirmasi pengurus sebelum digunakan warga. Baca `PANDUAN-PENGURUS.md` untuk aturan privasi dan format isian. Jangan menerbitkan data pribadi warga.

## 3. Jalankan chatbot

```bash
python app.py
```

Buka http://127.0.0.1:5000 atau langsung http://127.0.0.1:5000/chat/kampung. Chat API menerima `POST /api/chat` dengan JSON `{"message":"jadwal sampah kapan","theme":"kampung"}`.

## 4. Pantau pertanyaan

Buka `/admin/kampung` untuk melihat jumlah pertanyaan, intent yang dikenali, serta pertanyaan yang belum dikenali. Untuk membatasi akses, atur environment variable `ADMIN_KEY` sebelum menjalankan aplikasi, lalu tambahkan `?key=...` pada URL admin. Gunakan pertanyaan yang tidak dikenali sebagai bahan tinjauan; masukkan ke pola hanya setelah maksudnya jelas dan jawabannya tervalidasi.

## 5. Evaluasi

Dari folder `aplikasi-final`, jalankan:

```bash
pytest -v
python evaluate.py --tema kampung
python evaluate.py --tema kampung --data kampung_sulit
```

CSV evaluasi memuat pertanyaan contoh dan beberapa pertanyaan di luar cakupan yang seharusnya mendapat fallback. Hasilnya adalah pemeriksaan regresi; ukur performa lapangan dengan kalimat asli warga yang tidak digunakan untuk menyusun pola.

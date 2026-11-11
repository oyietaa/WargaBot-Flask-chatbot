# WargaBot

WargaBot adalah chatbot berbasis aturan untuk membantu warga memperoleh informasi rutin kampung/RT/RW. Cakupannya meliputi jadwal dan aturan sampah, kerja bakti, ronda, tamu menginap, iuran, surat pengantar, warga pindahan, agenda, posyandu dan PKK, informasi duka, kontak pengurus, laporan masalah lingkungan, fasilitas, serta langkah awal keadaan darurat.

Informasi yang berbeda di setiap kampung disimpan pada blok `data` dalam `aplikasi-final/themes/kampung.json`. File tema berisi data contoh fiktif untuk demonstrasi tugas kuliah, bukan jadwal atau aturan kampung sungguhan. Ganti seluruh nilai di blok `data` dan `terakhir_diperbarui` dengan informasi yang dikonfirmasi pengurus sebelum digunakan warga. Nilai `[ISI: ...]` yang tersisa tidak akan ditampilkan; bot akan meminta warga menghubungi pengurus.

## Menjalankan aplikasi

```bash
cd aplikasi-final
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Buka http://127.0.0.1:5000. Halaman chat WargaBot tersedia di `/chat/kampung`; halaman pemantauan admin ada di `/admin/kampung`. Atur `ADMIN_KEY` untuk melindungi halaman admin.

## Knowledge dan evaluasi

- Knowledge map, pola, respons, normalisasi, dan isian pengurus: `aplikasi-final/themes/kampung.json`.
- Panduan pengisian: `aplikasi-final/PANDUAN-PENGURUS.md`.
- Data uji rancangan (40 kalimat): `aplikasi-final/evaluasi/kampung.csv`.
- Data uji sulit (31 kalimat): `aplikasi-final/evaluasi/kampung_sulit.csv`.

Dari folder `aplikasi-final`, jalankan:

```bash
pytest -v
python evaluate.py --tema kampung
python evaluate.py --tema kampung --data kampung_sulit
```

Akurasi data uji yang disusun bersama pola perlu dibaca sebagai pemeriksaan regresi, bukan ukuran performa lapangan. Evaluasi yang lebih representatif memerlukan kalimat asli dari warga yang tidak dipakai saat menyusun pola.

## Batas penggunaan

WargaBot tidak memberi saran diagnosis atau obat, informasi hukum, harga terkini, cuaca, berita, maupun topik umum. Bot tidak menyimpan data pribadi warga di file tema. Untuk informasi yang belum diisi atau kasus yang perlu keputusan pengurus, warga diarahkan menghubungi pengurus RT/RW. Pada keadaan darurat, bot mengarahkan pengguna menghubungi 112 dan kontak darurat lokal yang telah diverifikasi.

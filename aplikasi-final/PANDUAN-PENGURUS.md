# Panduan Pengurus: Mengisi Data WargaBot

Panduan ini untuk pengurus RT/RW. Tidak perlu bisa pemrograman: cukup mengubah teks di satu berkas.

> **Catatan tugas kuliah:** nilai yang tersedia di `themes/kampung.json` saat ini hanyalah data contoh fiktif. Ganti semua nilainya dengan informasi yang benar dan terverifikasi sebelum bot digunakan oleh warga.

## Yang diubah

Buka `themes/kampung.json` dengan editor teks (misalnya Notepad atau VS Code). Cari bagian `"data"`
dan `"terakhir_diperbarui"` di bagian atas berkas.

```json
"terakhir_diperbarui": "[ISI: tanggal terakhir pengurus memperbarui data]",
"data": {
  "jadwal_sampah": "[ISI: hari dan jam pengangkutan sampah]",
  ...
}
```

Ganti teks `[ISI: ...]` dengan informasi yang benar untuk kampung Anda, **tetap di dalam tanda kutip**.

```json
"terakhir_diperbarui": "5 November 2026",
"jadwal_sampah": "Selasa dan Sabtu pagi",
```

## Aturan penting

1. **Isi hanya yang pasti.** Bot tidak mengarang. Jawaban yang masih berisi `[ISI: ...]` tidak akan
   dikirim; warga akan diminta menghubungi pengurus. Lebih baik dibiarkan kosong daripada salah.
2. **Perbarui `terakhir_diperbarui`** setiap kali mengubah data. Tanggal ini ditampilkan ke warga.
3. **Jangan memasukkan data pribadi warga** (nama, alamat, nomor HP pribadi). Untuk kontak, cukup
   jabatan dan kontak resmi pengurus yang memang sudah diumumkan.
4. **Jangan mengubah teks di dalam kurung kurawal** pada bagian lain berkas (misalnya `{jadwal_sampah}`).
   Itu penanda tempat data akan muncul.
5. Tanda kutip ganda di dalam isian harus ditulis `\"`, dan baris baru ditulis `\n`.

## Isian yang tersedia (21)

| Kunci | Isi |
|---|---|
| `jadwal_sampah`, `aturan_sampah` | Jadwal pengangkutan dan aturan sampah |
| `jadwal_kerja_bakti` | Hari, jam, titik kumpul |
| `jadwal_ronda`, `aturan_ronda` | Pola giliran, cara ikut, tukar giliran |
| `aturan_tamu` | Aturan lapor tamu menginap |
| `info_iuran`, `info_jimpitan` | Jenis iuran, nominal, cara bayar, jimpitan |
| `syarat_surat`, `alur_surat` | Dokumen dan langkah surat pengantar |
| `syarat_pindah` | Syarat warga baru atau pindahan |
| `agenda`, `jadwal_arisan_pengajian` | Agenda dan kegiatan rutin |
| `jadwal_posyandu`, `info_pkk` | Posyandu dan PKK |
| `prosedur_duka`, `info_santunan` | Pengumuman duka dan santunan |
| `kontak_pengurus` | Kontak resmi pengurus |
| `cara_lapor` | Cara melapor masalah lingkungan |
| `info_fasilitas` | Fasilitas yang bisa dipinjam |
| `kontak_darurat_lokal` | Kontak darurat lokal |

## Memeriksa hasil

1. Simpan berkas, lalu minta pembuat bot menjalankan ulang aplikasi.
2. Cek berkas tidak rusak: `python -m json.tool themes/kampung.json` (tidak boleh muncul pesan galat).
3. Coba tanyakan beberapa pertanyaan di `/chat/kampung`. Jika muncul "informasi ini belum diisi oleh
   pengurus", berarti isian terkait masih berisi `[ISI: ...]`.
4. Buka `/admin/kampung` untuk melihat pertanyaan warga yang belum dipahami bot.

## Menambah pertanyaan yang belum dipahami

Dari halaman admin, salin kalimat asli warga ke daftar `"patterns"` pada intent yang sesuai di
`themes/kampung.json`. Satu intent sebaiknya memiliki 4 sampai 8 pola.

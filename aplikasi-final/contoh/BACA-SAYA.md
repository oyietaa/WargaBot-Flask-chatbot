# Contoh data WargaBot

`kampung-contoh-terisi.json` berisi data **FIKTIF** agar kamu bisa melihat WargaBot menjawab dengan isi
yang lengkap. Jangan dipakai untuk kampung sungguhan.

Mencoba:

1. Simpan dulu `themes/kampung.json` (misalnya salin ke `kampung.asli.json` di luar folder `themes/`).
2. Salin `contoh/kampung-contoh-terisi.json` ke `themes/kampung.json`.
3. Jalankan `python app.py`, buka http://127.0.0.1:5000/chat/kampung.

Untuk kampung sungguhan, isi blok `data` di `themes/kampung.json` dengan informasi dari pengurus
dan ganti `terakhir_diperbarui` dengan tanggal pembaruan. Selama masih ada `[ISI: ...]`,
bot menjawab "informasi ini belum diisi oleh pengurus".

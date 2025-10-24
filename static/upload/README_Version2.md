# Ujian Online Flask - Siap Deploy ke Vercel

## Struktur Folder

```
ujian_online_vercel/
│
├── api/
│   └── index.py                   # ENTRY POINT Flask untuk Vercel
│
├── models/
│   ├── __init__.py
│   ├── user_model.py
│   ├── soal_model.py
│   └── hasil_model.py
│
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py
│   ├── admin_routes.py
│   ├── mahasiswa_routes.py
│   └── ujian_routes.py
│
├── templates/
│   └── ... (semua html)
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── uploads/
│       ├── soal_gambar/
│       ├── soal_video/
│       └── README.md
│
├── config.py
├── requirements.txt
├── vercel.json
├── database.db                    # Dibuat otomatis saat running
├── ujian_status.txt               # Dibuat otomatis saat running
└── README.md
```

## Cara Deploy ke Vercel

1. **Clone repo** ke komputer lokal/generate repo dari struktur ini.
2. **Push ke GitHub**.
3. **Hubungkan ke Vercel**:
   - Buat project baru di vercel.com, pilih repo ini.
   - Vercel akan otomatis mendeteksi file `api/index.py` sebagai entry point Python.
   - Deploy!
4. Static files (`/static/`) sudah bisa diakses dan diatur oleh Vercel sesuai `vercel.json`.

## Catatan Penggunaan

- File **uploads** (gambar/video soal) dan **database.db** di Vercel bersifat sementara (ephemeral).
- Untuk production, gunakan storage eksternal (misal S3, Cloudinary) jika ingin data lebih awet.
- Untuk pengembangan lokal, jalankan:
  ```
  cd api
  flask run
  ```
  atau buat file `run.py` jika ingin dev server di root.

- **Admin login**:  
  Username: `admin`  
  Password: `admin123`  

- Mahasiswa bisa register sendiri.

## Fitur

- Admin: kelola soal, mulai/akhiri ujian, lihat leaderboard.
- Mahasiswa: register, login, ikuti ujian, lihat hasil & pembahasan.
- Skor & hasil ujian tersimpan di database SQLite.

---

Jika ada error, cek dependensi (`requirements.txt`) sudah terinstall dan struktur folder sudah sesuai.
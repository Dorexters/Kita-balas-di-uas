from api.index import db

class Soal(db.Model):
    __tablename__ = 'soal'
    id = db.Column(db.Integer, primary_key=True)
    pertanyaan = db.Column(db.Text, nullable=False)
    tipe = db.Column(db.String(16), nullable=False)  # 'teks', 'gambar', 'video'
    file_path = db.Column(db.String(256))  # jika gambar/video, path filenya
    opsi_a = db.Column(db.String(255), nullable=False)
    opsi_b = db.Column(db.String(255), nullable=False)
    opsi_c = db.Column(db.String(255), nullable=False)
    opsi_d = db.Column(db.String(255), nullable=False)
    jawaban_benar = db.Column(db.String(1), nullable=False)  # A/B/C/D
    penjelasan = db.Column(db.Text)

    def __repr__(self):
        return f'<Soal {self.id}>'
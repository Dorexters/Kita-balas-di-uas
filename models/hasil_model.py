from api.index import db

class HasilUjian(db.Model):
    __tablename__ = 'hasil_ujian'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skor = db.Column(db.Integer, nullable=False)
    jawaban = db.Column(db.Text, nullable=False)  # JSON string: {soal_id: jawaban_mahasiswa}
    benar_salah = db.Column(db.Text, nullable=False)  # JSON string: {soal_id: true/false}
    waktu_ujian = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref=db.backref('hasil_ujian', lazy=True))

    def __repr__(self):
        return f'<HasilUjian User={self.user_id} Skor={self.skor}>'
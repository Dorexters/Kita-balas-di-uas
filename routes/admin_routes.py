from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from api.index import db
from models.soal_model import Soal
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def allowed_file(filename, allowed_set):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_set

@admin_bp.before_request
def admin_only():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash("Akses hanya untuk admin!", "danger")
        return redirect(url_for('auth.login'))

@admin_bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/kelola_soal', methods=['GET', 'POST'])
def kelola_soal():
    if request.method == 'POST':
        pertanyaan = request.form['pertanyaan']
        tipe = request.form['tipe']
        file_path = None
        # Upload handling
        if tipe in ['gambar', 'video']:
            file = request.files['file']
            if file and allowed_file(file.filename,
                    current_app.config['ALLOWED_EXTENSIONS_GAMBAR'] if tipe == 'gambar' else current_app.config['ALLOWED_EXTENSIONS_VIDEO']):
                filename = secure_filename(file.filename)
                folder = (current_app.config['UPLOAD_FOLDER_GAMBAR'] if tipe == 'gambar' else current_app.config['UPLOAD_FOLDER_VIDEO'])
                if not os.path.exists(folder):
                    os.makedirs(folder)
                file.save(os.path.join(folder, filename))
                file_path = os.path.join(folder, filename)
            else:
                flash('Format file tidak didukung.', 'danger')
                return redirect(url_for('admin.kelola_soal'))
        opsi_a = request.form['opsi_a']
        opsi_b = request.form['opsi_b']
        opsi_c = request.form['opsi_c']
        opsi_d = request.form['opsi_d']
        jawaban_benar = request.form['jawaban_benar']
        penjelasan = request.form['penjelasan']

        soal = Soal(
            pertanyaan=pertanyaan,
            tipe=tipe,
            file_path=file_path,
            opsi_a=opsi_a,
            opsi_b=opsi_b,
            opsi_c=opsi_c,
            opsi_d=opsi_d,
            jawaban_benar=jawaban_benar,
            penjelasan=penjelasan
        )
        db.session.add(soal)
        db.session.commit()
        flash('Soal berhasil ditambahkan!', 'success')
        return redirect(url_for('admin.kelola_soal'))

    daftar_soal = Soal.query.all()
    return render_template('admin/kelola_soal.html', daftar_soal=daftar_soal)

@admin_bp.route('/edit_soal/<int:soal_id>', methods=['GET', 'POST'])
def edit_soal(soal_id):
    soal = Soal.query.get_or_404(soal_id)
    if request.method == 'POST':
        soal.pertanyaan = request.form['pertanyaan']
        soal.tipe = request.form['tipe']
        if soal.tipe in ['gambar', 'video']:
            file = request.files['file']
            if file and allowed_file(file.filename,
                    current_app.config['ALLOWED_EXTENSIONS_GAMBAR'] if soal.tipe == 'gambar' else current_app.config['ALLOWED_EXTENSIONS_VIDEO']):
                filename = secure_filename(file.filename)
                folder = (current_app.config['UPLOAD_FOLDER_GAMBAR'] if soal.tipe == 'gambar' else current_app.config['UPLOAD_FOLDER_VIDEO'])
                if not os.path.exists(folder):
                    os.makedirs(folder)
                file.save(os.path.join(folder, filename))
                soal.file_path = os.path.join(folder, filename)
        soal.opsi_a = request.form['opsi_a']
        soal.opsi_b = request.form['opsi_b']
        soal.opsi_c = request.form['opsi_c']
        soal.opsi_d = request.form['opsi_d']
        soal.jawaban_benar = request.form['jawaban_benar']
        soal.penjelasan = request.form['penjelasan']
        db.session.commit()
        flash('Soal berhasil diubah!', 'success')
        return redirect(url_for('admin.kelola_soal'))
    return render_template('admin/edit_soal.html', soal=soal)

@admin_bp.route('/hapus_soal/<int:soal_id>', methods=['POST'])
def hapus_soal(soal_id):
    soal = Soal.query.get_or_404(soal_id)
    # Hapus file jika ada
    if soal.file_path and os.path.exists(soal.file_path):
        os.remove(soal.file_path)
    db.session.delete(soal)
    db.session.commit()
    flash('Soal berhasil dihapus!', 'success')
    return redirect(url_for('admin.kelola_soal'))

# Sesi ujian flag (disimpan di file ujian_status.txt di root)
UJIAN_STATUS_FILE = 'ujian_status.txt'

def set_ujian_status(status):
    with open(UJIAN_STATUS_FILE, 'w') as f:
        f.write(str(status))

def get_ujian_status():
    if not os.path.exists(UJIAN_STATUS_FILE):
        set_ujian_status('0')
    with open(UJIAN_STATUS_FILE, 'r') as f:
        return f.read().strip()

@admin_bp.route('/sesi_ujian', methods=['GET', 'POST'])
def sesi_ujian():
    status = get_ujian_status()
    if request.method == 'POST':
        if 'mulai' in request.form:
            set_ujian_status('1')
            flash('Ujian dimulai.', 'success')
        elif 'akhiri' in request.form:
            set_ujian_status('0')
            flash('Ujian diakhiri.', 'danger')
        elif 'hapus' in request.form:
            from models.hasil_model import HasilUjian
            HasilUjian.query.delete()
            Soal.query.delete()
            db.session.commit()
            set_ujian_status('0')
            flash('Semua data ujian dihapus.', 'danger')
    return render_template('admin/sesi_ujian.html', status=status)

@admin_bp.route('/leaderboard')
def leaderboard():
    from models.hasil_model import HasilUjian
    hasil_terbaik = HasilUjian.query.order_by(HasilUjian.skor.desc()).limit(10).all()
    top_mahasiswa = [
        {
            'nama': hasil.user.nama,
            'username': hasil.user.username,
            'skor': hasil.skor
        }
        for hasil in hasil_terbaik
    ]
    return render_template('admin/leaderboard.html', top_mahasiswa=top_mahasiswa)
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.hasil_model import HasilUjian
from models.soal_model import Soal
from api.index import db
import os

mahasiswa_bp = Blueprint('mahasiswa', __name__, url_prefix='/mahasiswa')

@mahasiswa_bp.before_request
def mahasiswa_only():
    if not current_user.is_authenticated or current_user.is_admin:
        flash("Akses hanya untuk mahasiswa!", "danger")
        return redirect(url_for('auth.login'))

@mahasiswa_bp.route('/dashboard')
@login_required
def dashboard():
    status_file = 'ujian_status.txt'
    if not os.path.exists(status_file):
        status = '0'
        with open(status_file, 'w') as f:
            f.write(status)
    else:
        with open(status_file, 'r') as f:
            status = f.read().strip()
    if status == '0':
        return render_template('mahasiswa/ujian_belum_mulai.html')
    else:
        hasil = HasilUjian.query.filter_by(user_id=current_user.id).first()
        if hasil:
            return redirect(url_for('mahasiswa.hasil'))
        return redirect(url_for('ujian.ujian'))

@mahasiswa_bp.route('/hasil')
@login_required
def hasil():
    hasil = HasilUjian.query.filter_by(user_id=current_user.id).first()
    if not hasil:
        flash('Belum ada hasil ujian.', 'danger')
        return redirect(url_for('mahasiswa.dashboard'))
    import json
    jawaban = json.loads(hasil.jawaban)
    benar_salah = json.loads(hasil.benar_salah)
    soal_list = Soal.query.order_by(Soal.id).all()
    return render_template('mahasiswa/hasil.html', hasil=hasil, jawaban=jawaban, benar_salah=benar_salah, soal_list=soal_list)
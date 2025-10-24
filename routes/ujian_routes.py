from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from models.soal_model import Soal
from models.hasil_model import HasilUjian
from api.index import db
import json
from datetime import datetime

ujian_bp = Blueprint('ujian', __name__, url_prefix='/ujian')

def get_soal_list():
    return Soal.query.order_by(Soal.id).all()

@ujian_bp.before_request
def mahasiswa_only():
    if not current_user.is_authenticated or current_user.is_admin:
        flash("Akses hanya untuk mahasiswa!", "danger")
        return redirect(url_for('auth.login'))

@ujian_bp.route('/', methods=['GET', 'POST'])
@login_required
def ujian():
    soal_list = get_soal_list()
    total_soal = len(soal_list)
    if total_soal == 0:
        flash('Belum ada soal tersedia.', 'warning')
        return redirect(url_for('mahasiswa.dashboard'))

    if 'current_soal' not in session:
        session['current_soal'] = 0
        session['jawaban'] = ['' for _ in range(total_soal)]

    page = int(request.args.get('page', session['current_soal']))
    if request.method == 'POST':
        selected = request.form.get('jawaban')
        session['jawaban'][page] = selected

        if 'next' in request.form:
            if page < total_soal - 1:
                page += 1
        elif 'prev' in request.form:
            if page > 0:
                page -= 1
        elif 'submit' in request.form:
            if '' in session['jawaban']:
                flash('Semua soal wajib dijawab.', 'danger')
                return redirect(url_for('ujian.ujian', page=page))
            skor = 0
            benar_salah = {}
            jawaban_dict = {}
            for idx, soal in enumerate(soal_list):
                user_jwb = session['jawaban'][idx]
                jawaban_dict[str(soal.id)] = user_jwb
                benar = (user_jwb == soal.jawaban_benar)
                benar_salah[str(soal.id)] = benar
                if benar:
                    skor += 1
            hasil = HasilUjian(
                user_id=current_user.id,
                skor=skor,
                jawaban=json.dumps(jawaban_dict),
                benar_salah=json.dumps(benar_salah),
                waktu_ujian=datetime.now()
            )
            db.session.add(hasil)
            db.session.commit()
            session.pop('current_soal', None)
            session.pop('jawaban', None)
            return redirect(url_for('mahasiswa.hasil'))
        session['current_soal'] = page

    soal = soal_list[page]
    jawaban_terpilih = session['jawaban'][page]
    return render_template('mahasiswa/ujian.html',
                           soal=soal,
                           page=page,
                           total_soal=total_soal,
                           jawaban_terpilih=jawaban_terpilih)
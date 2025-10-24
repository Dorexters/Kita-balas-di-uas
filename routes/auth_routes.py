from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from api.index import db, login_manager
from models.user_model import User

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Admin login (hardcode)
        if username == 'admin' and password == 'admin123':
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(username='admin', nama='Administrator', is_admin=True)
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
            login_user(admin)
            return redirect(url_for('admin.dashboard'))

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('mahasiswa.dashboard'))
        else:
            flash('Username atau password salah.', 'danger')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        nama = request.form['nama']
        password = request.form['password']
        password2 = request.form['password2']
        if password != password2:
            flash('Password tidak cocok.', 'danger')
            return render_template('register.html')
        if User.query.filter_by(username=username).first():
            flash('Username sudah terdaftar.', 'danger')
            return render_template('register.html')
        user = User(username=username, nama=nama, is_admin=False)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registrasi berhasil, silakan login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
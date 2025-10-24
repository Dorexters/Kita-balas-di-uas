import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'database.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER_GAMBAR = os.path.join('static', 'uploads', 'soal_gambar')
    UPLOAD_FOLDER_VIDEO = os.path.join('static', 'uploads', 'soal_video')
    ALLOWED_EXTENSIONS_GAMBAR = {'png', 'jpg', 'jpeg', 'gif'}
    ALLOWED_EXTENSIONS_VIDEO = {'mp4', 'webm', 'ogg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
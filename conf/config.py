import os


class Config:
    DEBUG = False
    DATABASE_URL = os.getenv('DATABASE_URL')


class Development(Config):
    DEBUG = True


class Testing(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'postgresql://postgres:kukuer1210@localhost/test_db'
    DATABASE = 'test_db'


app_config = {'DEVELOPMENT': Development, 'TESTING': Testing}

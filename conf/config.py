import os


class Config:
    DEBUG = False
    DATABASE_URL = os.getenv('DATABASE_URL')


class Development(Config):
    DEBUG = True


class Testing(Config):
    DEBUG = True
    TESTING = True


app_config = {'DEVELOPMENT': Development, 'TESTING': Testing}

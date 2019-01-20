import os


class Config:
    DEBUG = False
    DATABASE_URL = 'postgresql: //postgres:kukuer1210@localhost/zero'


class Development(Config):
    DEBUG = True


class Testing(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'postgresql: //postgres:kukuer1210@localhost/twice'


app_config = {'DEVELOPMENT': Development, 'TESTING': Testing}

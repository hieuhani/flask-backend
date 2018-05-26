class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    @staticmethod
    def init_app(app):
        pass

class Development(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres@localhost:5432/backend_dev'

config = {
    'development': Development,
}

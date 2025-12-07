import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dicromat.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_EXPIRY_HOURS = int(os.getenv('SESSION_EXPIRY_HOURS', 24))
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    IMAGE_SIZE = int(os.getenv('IMAGE_SIZE', 400))
    IMAGE_FORMAT = os.getenv('IMAGE_FORMAT', 'PNG')
    RANDOM_SEED_SALT = os.getenv('RANDOM_SEED_SALT', 'dicromat-salt')


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

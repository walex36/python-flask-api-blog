import os

class Config:
    TESTING = False
    SECRET_KEY= os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI= os.getenv('DATABASE_URL')
    JWT_SECRET_KEY= os.getenv('JWT_SECRET_KEY')

class ProductionConfig(Config):
    TESTING = False
    SECRET_KEY= os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI= os.getenv('DATABASE_URL')
    JWT_SECRET_KEY= os.getenv('JWT_SECRET_KEY')

class DevelopmentConfig(Config):
    SECRET_KEY= 'dev'
    SQLALCHEMY_DATABASE_URI= 'sqlite:///blog.sqlite'
    JWT_SECRET_KEY= 'dev'

class TestingConfig(Config):
    TESTING = True
    SECRET_KEY= 'dev'
    DATABASE_URI = 'sqlite://'
    JWT_SECRET_KEY= 'dev'
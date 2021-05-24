import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY =' j/6Ds!3#dmOJVS3P_i!^>eGaC@sw(Z'
    JWT_AUTH_USERNAME_KEY =  "email"
    JWT_AUTH_URL_RULE =  "/auth/login"
    JWT_SECRET_KEY =  "j/6Ds!3#dmOJVS3P_i!^>eGaC@sw(Z"
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ENV = "development"
    
class TestConfig(Config):
    DEVELOPMENT = True
    TESTING = True
    DEBUG = True
    ENV = "testing"
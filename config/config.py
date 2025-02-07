class Config:
    DEBUG=False
    TESTING=False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:123456@localhost:5432/db_movie'
    SECRET_KEY='f64b6790ba78cd243e0c5849dc5e7fd97c47e8f37234fe6403b1432a4a7705caadcc729936593a00939b3bd0e3554533961121715e4ffeac1b84cc10835a4d95'

class DevelopmentConfig(Config):
    DEBUG=True
    
class ProductionConfig(Config):
    DEBUG=True
    
class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:123456@localhost:5432/db_movie'

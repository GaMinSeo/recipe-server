
class Config :
    
    HOST = 'yh-db.c9auuqkqamau.ap-northeast-2.rds.amazonaws.com'
    DATABASE = 'recipe_db'
    DB_USER = 'recipe_db_user'
    DB_PASSWORD = '0000'

    # password seed
    SALT = 'your_salt_value'

    # JWT 관련 변수 셋팅
    JWT_SECRET_KEY = 'djaiwnb,12850sksj'
    JWT_ACCESS_TOKEN_EXPIRES = False
    PROPAGATE_EXCEPTIONS = True
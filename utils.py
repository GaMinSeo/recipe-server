from passlib.hash import pbkdf2_sha256

# Config 클래스를 정의합니다.
class Config:
    SALT = "your_salt_value"

# 원문 비밀번호를 단방향으로 암호화하는 함수
def hash_password(original_password):
    original_password = original_password + Config.SALT
    password = pbkdf2_sha256.hash(original_password)
    return password

# 유저가 로그인할 때 입력한 비밀번호가 맞는지 체크하는 함수
def check_password(original_password, hashed_password):
    original_password = original_password + Config.SALT
    return pbkdf2_sha256.verify(original_password, hashed_password)

# 비밀번호 해싱 예제
hashed_password = hash_password('0000')
print(hashed_password)

check = check_password('0000','$pbkdf2-sha256$29000$ck4phZCy9n7PGSMk5LxXCg$35EY2fL4MXPj3ej5OvaXYu/LpefJLPtbp9JwN4h6Lbc' )
print (check)
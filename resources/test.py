from flask_restful import Resource

# API를 처리하는 코드는
# Resource 클래스를 상속받아서 작성한다.
# 이 클래스에는 get, post, put, delete 함수를 상속받는다.
# 따라서 이 함수들을, 우리의 서비스에 맞게 수정해서 사용하면 된다.
class TestResource(Resource) :

    def get(self) :
        return {'data' : '안녕하세요'}
    
    def post(self) :
        return {'data' : '반갑습니다.'}
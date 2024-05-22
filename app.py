from flask import Flask
from flask_restful import Api
from resources.recipe import RecipeListResource, RecipePublishResource, RecipeResource
from resources.user import UserRegisterResource

from flask_jwt_extended import JWTManager
from config import Config

app = Flask(__name__)

# 환경변수 셋팅
app.config.from_object(Config)

# JWT 매니저 초기화
jwt = JWTManager(app)

api = Api(app)

# 경로(path)와 리소스(Api 코드)를 연결한다.

api.add_resource( RecipeListResource , '/recipes' )
api.add_resource( RecipeResource , '/recipes/<int:recipe_id>' )
api.add_resource( RecipePublishResource , '/recipes/<int:recipe_id>/publish')
api.add_resource( UserRegisterResource , '/users/register' )

if __name__ == '__main__' :
    app.run()
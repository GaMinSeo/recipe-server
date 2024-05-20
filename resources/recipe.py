from flask_restful import Resource

class RecipeListResource(Resource) :

    def post(self) :
        return {'data' : 'hello'}
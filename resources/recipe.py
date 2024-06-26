from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from mysql_connection import get_connection
from mysql.connector import Error

class RecipePublishResource(Resource) : 
    @jwt_required()
    def put(self, recipe_id):
        user_id = get_jwt_identity()
        try :
            connection = get_connection()
            query = '''update recipe
                    set is_publish = 1
                    where id = %s and user_id = %s;'''
            record = (recipe_id, user_id)
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()

        except Error as e:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close
            return {'result' : 'fail', 'error' : str(e)}, 500

        return {'result' : 'success'}

    @jwt_required()
    def delete(self, recipe_id):
        user_id = get_jwt_identity()
        try :
            connection = get_connection()
            query = '''update recipe
                    set is_publish = 0
                    where id =  %s and user_id = %s;'''
            record = (recipe_id,user_id)
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()

        except Error as e:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close
            return {'result' : 'fail', 'error' : str(e)}, 500

        return {'result' : 'success'}

class RecipeResource(Resource) :
    
    @jwt_required()
    def get(self, recipe_id) :

        # 1. 클라이언트로부터 데이터를 받는다.
        
        print(recipe_id)

        user_id = get_jwt_identity()
        # 2. DB로 부터 데이터를 가져온다.
        try:
            
            connection = get_connection()

            print('커넥션 실행')

            # '''++''' 로 작성했기에 recode = ()는 안써도 된다
            query = '''
                    select *
                    from recipe
                    where id = %s;'''
            record = (recipe_id,)

            print(record)

            cursor = connection.cursor(dictionary=True)

            print('커서 가져오기 성공')

            cursor.execute(query, record)

            print('쿼리문 실행')

            result_list = cursor.fetchall()

            print(result_list)

            cursor.close()
            connection.close()

        except Error as e:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
            return {'result': 'fail',
                    'error': str(e)}, 500
        
        
        # 3. 응답할 데이터를 json 으로 만든다
        i = 0
        for row in result_list :
            result_list[i]['created_at'] = row['created_at'].isoformat()
            result_list[i]['updated_at'] = row['updated_at'].isoformat()
            i = i + 1

        if len(result_list) == 1:
            # 2-2. 내 레시피인지 확인한다.
            if result_list[0]['user_id'] == user_id :
                return {'item' : result_list[0],
                        'result' : 'success'}
            else :
                return {'result': 'fail'}, 401
        else :
            return {'result': 'fail',
                    'error': '해당 아이디는 존재하지 않습니다.'}
    
    @jwt_required()
    def put(self,recipe_id):

        # 1. 클라이언트로 부터 데이터를 받아온다.
        print(recipe_id)

        data = request.get_json()
        user_id = get_jwt_identity()
        # 2. DB 에 수정한다.
        try:
            connection = get_connection()
            print(data)
            query = '''update recipe
                set name = %s,
                    description = %s,
                    num_of_servings = %s,
                    cook_time = %s,
                    directions = %s
                where id = %s and user_id = %s;'''
            record = (data['name'],
                        data['description'],
                        data['num_of_servings'],
                        data['cook_time'],
                        data['directions'],
                        recipe_id,
                        user_id)

            cursor = connection.cursor()
            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()

        except Error as e:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()

            return {'result' :'fail',
                    'error' : str(e)}, 500
        
        return {'result' : 'success'}
    
    @jwt_required()
    def delete(self, recipe_id) :

        user_id = get_jwt_identity()

        try:
            connection = get_connection()
            query = '''delete from recipe where id = %s and user_id = %s;'''
            record = (recipe_id, user_id)
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()
        except Error as e:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()

            return {'result' :'fail',
                    'error' : str(e)}, 500

        return { "result" : "success"}

class RecipeListResource(Resource):
    
    # JWT 토큰이 헤더에 있어야지만 이 API를 실행할수 있다는 뜻
    # JWT 토큰이 필수!!! == 로그인 한 유저만 이 API 실행 가능.
    @jwt_required()
    def post(self) :

        # 1. 클라이언트가 보내준 데이터가 있으면 그 데이터를 받아준다.
        
        data = request.get_json()

        # 1-1. 헤더의 JWT 토큰이 있으면, 토큰 정보도 받는다.
        user_id = get_jwt_identity()

        # 2. 이 정보를 DB에 저장한다.
        try:
            ### 1. DB에 연결
            connection = get_connection()

            ### 2. 쿼리문 만들기
            query = '''insert into recipe
                        (user_id, name, description, num_of_servings, cook_time, directions)
                        values
                        (%s, %s, %s, %s, %s, %s);'''
            
            ### 3. 쿼리에 매칭되는 변수 처리 => 튜.플.로.
            record = (user_id, data['name'], data['description'], data['num_of_servings'], data['cook_time'], data['directions'])

            ### 4. 커서를 가져온다.
            cursor = connection.cursor()

            ### 5. 쿼리문을 커서로 실행한다.
            cursor.execute(query, record)

            ### 6. DB에 완전히 반영하기 위해서는 commit 한다.
            connection.commit()

            ### 7. 자원 해제
            cursor.close()
            connection.close()

        except Error as e:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
            return {'result' : 'fail', 'error' : str(e)}, 500
        
        return {'result' : 'success'}
    @jwt_required()
    def get(self) :
        
        # 1. 클라이언트가 보낸 데이터가 있으면
        #    받아준다.
        offset = request.args['offset']
        limit = request.args['limit']

        # 1-2 JWT 토큰에서 유저아이디를 가져온다
        user_id = get_jwt_identity()
        
        # 2. DB로 부터 데이터를 가져온다.
        try :
            
            connection = get_connection()

            # '''++''' 로 작성했기에 recode = ()는 안써도 된다
            query = '''
                    select *
                    from recipe
                    where user_id = %s
                    limit '''+offset+''','''+limit+''' ;
                    '''
            record = (user_id,)

            # 딕셔너리 트루 파라미터를 설정하여 데이터를 딕셔너리로 받는다
            cursor = connection.cursor(dictionary=True)
        
            cursor.execute(query, record)

            result_list = cursor.fetchall()

            print(result_list)

            cursor.close()
            connection.close()

        except Error as e:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close
            return {'result' : 'fail', 'error' : str(e)}, 500
        # 3. 클라이언트에 json 만들어서 응답한다.
        i = 0
        for row in result_list :
            result_list[i]['created_at'] = row['created_at'].isoformat()
            result_list[i]['updated_at'] = row['updated_at'].isoformat()
            i = i + 1

            print(result_list)

        return {'result' : 'success', 'item' : result_list, 'count' : len(result_list)}


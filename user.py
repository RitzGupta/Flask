import sqlite3
from flask_restful import Resource, reqparse



class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


    @classmethod  #It is used in place of self  'cls'
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        # users is table name
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query,(username,))#(username,)  'comma' needed is it show it is arg which is need to be search
        row = result.fetchone()
        if row: 
            user = cls(*row) #we can place row[0],raw[1],raw[2] in place of '*row'   // user is class
        else:
            user = None
        
        connection.close()
        return user

    @classmethod  #It is used in place of self  'cls'
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query,(_id,))#(username,)  'comma' needed is it show it is arg which is need to be search
        row = result.fetchone()
        if row: 
            user = cls(*row) #we can place row[0],raw[1],raw[2] in place of '*row'
        else:
            user = None
        
        connection.close()
        return user


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required = True,
        help = "This field can't be blank."
    )
    parser.add_argument('password',
        type=str,
        required = True,
        help = "This field can't be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        #preventing multiple users have same username....

        if User.find_by_username(data['username']):
            return {"message":"A user with that username already exists"},400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL,?,?)"
        cursor.execute(query,(data['username'],data['password']))

        connection.commit()
        connection.close()
        
        return{"message": "user created successfully."},201
































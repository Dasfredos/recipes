from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import recipe
from flask import flash
import re
EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



class Users:
    db = "recipes_schema"
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.all_recipes = []


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users
    

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])


    @classmethod
    def save(cls, data ):
        query = """
            INSERT into users 
            (first_name, last_name, email, password) 
            VALUES 
            ( %(first_name)s , %(last_name)s , %(email)s ,  %(password)s)
        
        """
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def get_one(cls, data):
        query = """SELECT * FROM users WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @staticmethod
    def validate_user(form_data):
        is_valid = True
        data= { "email": form_data["email"]}
        valid_user = Users.get_by_email(data)

        if len(form_data["first_name"]) < 3:
            flash("First name must be at least 3 characters.", "register")
            is_valid = False
        if len(form_data["last_name"]) < 3:
            flash("Last name must be at least 3 characters.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(form_data["email"]):
            flash ("Invalid email address.", "register")
            is_valid = False
        if valid_user:
            flash ("Email is already in use!.", "register")
            is_valid=False
        if len(form_data["password"]) < 8:
            flash ("Password must be at least 8 characters", "register")
            is_valid = False
        if form_data['conf_password'] != form_data['password']:
            flash("Password and confirm password must match!", "register")
            is_valid=False
        
        return is_valid

    @staticmethod
    def validate_login(form_data):
        is_valid= True
        
        data= { "email": form_data["login_email"]}
        valid_user = Users.get_by_email(data)
        if not valid_user:
            flash('Invalid Crendentials', "login")
            is_valid=False
        if valid_user:
            if not bcrypt.check_password_hash(valid_user.password, form_data['login_password']):
                flash('Invalid Credentials',"login")
                is_valid=False
        
        if len(form_data['login_email']) <1 and len(form_data['login_password']) <1:
            flash('Invalid Crendentials', "login")
            is_valid = False
        return is_valid



from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash


class Recipes:
    db = "recipes_schema"
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def save_recipe(cls, data):

        query= '''
                INSERT INTO recipes (user_id, name, description, instructions, under_30)
                VALUES (%(user_id)s, %(name)s, %(description)s, %(instructions)s, %(under_30)s);
        '''
        result = connectToMySQL(cls.db).query_db(query,data)
        return result



    @classmethod
    def get_all_recipes(cls):
        query= """
            SELECT * FROM recipes
            JOIN Users
            Where recipes.user_id = users.id
            ORDER BY recipes.id DESC;
            
        """
        results = connectToMySQL(cls.db).query_db(query)
        
        all_posts = []

        for row in results:

            one_post = cls(row)
            
            user_data = {
                'id': row ['user_id'],
                'first_name': row ['first_name'],
                'last_name': row ['last_name'],
                'email': row ['email'],
                'password': row ['password'],
                'created_at': row ['created_at'],
                'updated_at': row ['updated_at']
            }
            one_post.creator = user.Users(user_data)
            all_posts.append(one_post)
        return all_posts

    @classmethod
    def get_one_recipe(cls, data):
        query = """SELECT * FROM recipes WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_one_recipe_with_user(cls,data):
        query='''
            SELECT * FROM recipes
            JOIN users
            ON recipes.user_id = users.id
            WHERE recipes.id= %(id)s;

        '''
        results= connectToMySQL(cls.db).query_db(query,data)
        for row in results:
            one_recipe = cls(row)
            user_data={
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': ' ',
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
            one_recipe.creator= user.Users(user_data)
        return one_recipe

    @classmethod
    def update_recipe(cls,data):

        query = """
                UPDATE recipes
                SET 
                name = %(name)s,
                description = %(description)s, 
                instructions = %(instructions)s, 
                under_30 = %(under_30)s 
                WHERE id = %(id)s;
        """
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def delete_recipe(cls, data):
            query= '''
                DELETE FROM recipes
                WHERE recipes.id=%(id)s;
            '''
            return connectToMySQL(cls.db).query_db(query, data)


    @staticmethod
    def validate_recipe(form_data):
            is_valid = True
            
            if len(form_data["name"]) < 1:
                flash("Post content must not be blank.")
                is_valid = False
            if len(form_data["description"]) < 1:
                flash("Post content must not be blank.")
                is_valid = False
            if len(form_data["instructions"]) < 1:
                flash("Post content must not be blank.")
                is_valid = False
            if 'under_30' not in form_data:
                flash("under 30 must not be blank.")
                is_valid = False
                
            if form_data['created_at']  == '':
                flash("date must not be blank.")
                is_valid = False
            

            
            return is_valid

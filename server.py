from flask_app import app
from flask_app.controllers import user_routes, recipe_routes


if __name__=="__main__":
    app.run(debug=True)
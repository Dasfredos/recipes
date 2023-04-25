from flask_app import app
from flask import Flask, render_template, request, redirect, session
from flask_app.models import recipe, user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash

@app.route("/")
def index():
    return render_template("homepage.html")


@app.route("/create/account", methods=["POST"])
def create_account():
    if not user.Users.validate_user(request.form):
        return redirect ("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    id = user.Users.save(data)
    session['user_id'] = id

    return redirect (f'/user/account/{id}')


@app.route('/user/account/<int:id>')
def user_account(id):
    if 'user_id' not in session:
        return redirect ('/')
    id_data={
        'id': id
    }
    one_user= user.Users.get_one(id_data)
    all_posts= recipe.Recipes.get_all_recipes()
    return render_template ('all_recipes.html', listed_user = one_user, all_posts = all_posts)

@app.route('/login', methods=['POST'])
def login_user():
    if not user.Users.validate_login(request.form):
        return redirect('/')
    email_data={
        'email':request.form['login_email']
    }

    returning_user= user.Users.get_by_email(email_data)
    session['user_id']= returning_user.id
    return redirect(f'/user/account/{returning_user.id}')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/signed_out')

@app.route('/signed_out')
def sign_out():
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
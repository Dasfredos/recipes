from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import recipe, user


@app.route('/new_recipe')
def new_recipe():
    if 'user_id' not in session: 
        return redirect('/')
    id_data={
        'id': session['user_id']
    }
    one_user= user.Users.get_one(id_data)

    return render_template("new_recipe.html", user=one_user )

@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session: 
        return redirect('/')
    if not recipe.Recipes.validate_recipe(request.form):
        return redirect('/new_recipe')

    recipe.Recipes.save_recipe(request.form)
    
    id_data={
        'id': session['user_id']
    }
    one_user= user.Users.get_one(id_data)
    return redirect(f'/user/account/{one_user.id}')

@app.route('/edit/recipe/<int:id>')
def edit_form(id):
    if 'user_id' not in session: 
        return redirect('/')
    id_data={
        'id': id
    }
    one_recipe= recipe.Recipes.get_one_recipe_with_user(id_data)

    data={
        'id': session['user_id']
    }
    one_user= user.Users.get_one(data)
    return render_template('edit_recipe.html', one_recipe=one_recipe, user=one_user)

@app.route('/update/recipe/<int:id>', methods=['POST'])
def update_recipe(id):


    if 'user_id' not in session: 
        return redirect('/logout')
    if not recipe.Recipes.validate_recipe(request.form):
        recipe_id = request.form['id'] 
        return redirect(f'/edit/recipe/{recipe_id}')

    recipe.Recipes.update_recipe(request.form)
    user= session['user_id']

    return redirect(f'/user/account/{user}')

@app.route('/recipe/delete/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    id_data={
        'id': id
    }
    recipe.Recipes.delete_recipe(id_data)
    user= session['user_id']
    return redirect(f'/user/account/{user}')

@app.route('/show_recipe/<int:id>')
def show_recipe(id):
    if 'user_id' not in session: 
        return redirect('/')
    data={
        'id': id
    }
    one_recipe= recipe.Recipes.get_one_recipe_with_user(data)
    user_data={
        'id': session['user_id']
    }
    one_user= user.Users.get_one(user_data)
    return render_template('view_recipe.html', recipe=one_recipe, listed_user=one_user)







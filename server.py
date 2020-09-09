"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """Display the homepage."""

    return render_template('homepage.html')

@app.route('/movies')
def all_movies():
    """Display the list of all movies."""

    movie_list = crud.get_all_movies()

    return render_template('all_movies.html', movies=movie_list)

@app.route('/movies/<movie_id>')
def moviedetails(movie_id):
    "Show details."

    movie_details = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie_details)

@app.route('/users')
def get_users():
    """Users"""

    users = crud.get_all_users()
    return render_template("users.html", users = users)
    
@app.route('/users/<user_id>')
def userdetails(user_id):
    """show details"""
    user = crud.get_user_by_id(user_id)
    return render_template("user_details.html", user=user)

@app.route('/users', methods=['POST'])
def register_user():
    """Registers user."""
    
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('Cannot create an account with that email. Try again.')
    else:
        crud.create_user(email, password)
        flash('Account created! Please log in.')
    
    return redirect('/')

@app.route('/userlogin', methods=['POST'])
def login_user():

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:
        if password == user.password:
            session['user_id'] = user.user_id
            flash('Logged in!')
            
        else:
            flash("Incorrect Password")
            
    else:
        flash('User does not exist')
        
    return redirect('/')

    


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

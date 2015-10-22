"""Movie Ratings."""


from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session 
from flask_debugtoolbar import DebugToolbarExtension


from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """ Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/login', methods=["GET", "POST"])
def login_page():
    """Users login here"""
    if request.method == 'GET':
        # displaying the log in form from the GET request 
        flash("messages")
        return render_template("login_form.html")

    else: 
        email = request.form.get('email')
        password = request.form.get('password')
        email = User.query.filter_by(email=email, password=password).first()
        if request.form['email'] != 'email' or \
            request.form['password'] != 'password':
            flash("Invalid email and password")
            return render_template("login_form.html")

        else:
            flash("You were successfully logged in")
            return redirect('/homepage')




    # this is for sign up form how to create a new user into the DB 
    #new_user = User(username=username, password=password)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
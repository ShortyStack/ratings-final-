"""Utility file to seed ratings database from MovieLens data in seed_data/"""
#seed.py populates the tables. 

from model import User
from model import Rating
from model import Movie

from model import connect_to_db, db
from server import app

from datetime import datetime 




def load_users():
    """Load users from u.user into database."""
    # open and read a file 
    # read by line and split by pipe |

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        # striping on the right side, removing extra white space
        row = row.rstrip()
        # spliting by the | pipe
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""
    print "Movies"

    Movie.query.delete()

    for row in open("seed_data/u.movies"):
        #stripping on the right side to remove whitespace
        print row
        #row = row.strip()
        #splitting by the ('|')
        movie_id, title, released_at, imdb_url = row.split("|")[:4]

        title = title[:-7]

        if released_at == "":
            released_at = None
        else:
            released_at = datetime.strptime(released_at, "%d-%b-%Y")



        # now we will create the table
        # created an instance of of the movie class and importing it from Movie in model.py    
        # Movie is (Cat) movie is (Auden) = movie_id, title..is(hunger=10)
        movie = Movie(movie_id=movie_id,
                       title=title,
                       released_at=released_at,
                       imdb_url=imdb_url)
        # we need to add to the session or it won't be stored
        db.session.add(movie)

    #once we are done, we should commit our work
    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""
    print "Ratings"
    # this means that when it loads the second time deltes after the query 
    Rating.query.delete()

    for row in open("seed_data/u.ratings"):
        row = row.rstrip()
        # user_id move_id and score underscore means we dont want to show timestamp 
        user_id, movie_id, score, _ = row.split()

        rating = Rating(movie_id=movie_id, user_id=user_id, score=score)

        # we need to add to the session or it won't be stored
        db.session.add(rating)

    #once we are done, we should commit our work
    db.session.commit()







if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_users()
    load_movies()
    # load_ratings()

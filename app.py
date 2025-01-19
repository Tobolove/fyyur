#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import os
from os import name
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from streamlit import form
from forms import *
from datetime import datetime

from flask_migrate import Migrate   # migration initiators

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abc@localhost:5432/fyyur'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/fyyur')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'abc'  
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF  for testing purposes
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(50000)) #for long image links, that did not work
    genres = db.Column(db.String, nullable=True)
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(1000))
    website_link = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
        return f"<Venue {self.id} {self.name}>"

    
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String, nullable=False)  #added for completiuons
    image_link = db.Column(db.String(5000))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(1000))
    website_link = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    shows = db.relationship('Show', backref='artist', lazy=True)

  
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Show {self.id} artist_id={self.artist_id} venue_id={self.venue_id}>"
    
# DONE: Implement Show and Artist models, and complete all model relationships.

#----------------------------------------------------------------------------#
# Test Center /Graveyard Codes 
#----------------------------------------------------------------------------#
 
#from app import app, db, Venue

#with app.app_context():
#    venues = Venue.query.all()
#    for venue in venues:
#        print(venue)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    venues = Venue.query.order_by(Venue.created_at.desc()).limit(10).all()
    artists = Artist.query.order_by(Artist.created_at.desc()).limit(10).all()
    return render_template('pages/home.html', venues=venues, artists=artists)


# ----------------------------------------------------------------
#  Venues /works also added nr. of upcoming shows 
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
    # Group venues by city and states
    data = []
    locations = db.session.query(Venue.city, Venue.state).distinct().all()

    for city, state in locations:
        # Fetch venues
        venues_in_location = Venue.query.filter_by(city=city, state=state).all()
        
        # Venue data
        location_data = {
            "city": city,
            "state": state,
            "venues": [{
                "id": venue.id,
                "name": venue.name,
                "image_link": venue.image_link,  
                "num_upcoming_shows": len([
                    show for show in venue.shows if show.start_time > datetime.now()
                ])
            } for venue in venues_in_location]
        }
        data.append(location_data)

    return render_template('pages/venues.html', areas=data)

#   ---------------------------------------------------------------- 
#   Show Venues by ID with Shows  / works with error handling / final: del redundant code
#   ---------------------------------------------------------------- 

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if not venue:
        return render_template('Venue doesnt exist')

    past_shows = []
    upcoming_shows = []

    for show in venue.shows:
        daten = {
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        if show.start_time < datetime.now():
            past_shows.append(daten)
        else:
            upcoming_shows.append(daten)

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres.split(','),
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

    return render_template('pages/show_venue.html', venue=data)

#  ----------------------------------------------------------------
# Create Venue // Works     
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    if form.validate_on_submit():
        try:
            new_venue = Venue(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                address=form.address.data,
                phone=form.phone.data,
                genres=",".join(form.genres.data),
                image_link=form.image_link.data,
                facebook_link=form.facebook_link.data,
                seeking_talent=form.seeking_talent.data,
                seeking_description=form.seeking_description.data,
                website_link=form.website_link.data,
            )
            db.session.add(new_venue)
            db.session.commit()
            flash(f'Venue {form.name.data} was successfully created!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Venue {form.name.data} could not be created. Error Grund: {str(e)}', 'danger')
        finally:
            db.session.close()
    else:
        flash('Sorry we could not create your venue. Please check your details.', 'danger')

    return redirect(url_for('index'))

#  ----------------------------------------------------------------
#  Update Venue // Works
#  ----------------------------------------------------------------

@app.route('/venues/<int:venue_id>/edit', methods=['GET', 'POST'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)

    if not venue:
        flash(f"Venue with ID {venue_id} does not exist.")
        return redirect(url_for('venues'))

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                venue.name = form.name.data
                venue.city = form.city.data
                venue.state = form.state.data
                venue.address = form.address.data
                venue.phone = form.phone.data
                venue.genres = ",".join(form.genres.data)  # GENRE STRING - IN EINE LSITE UMWANDELN
                venue.facebook_link = form.facebook_link.data
                venue.image_link = form.image_link.data
                venue.seeking_talent = form.seeking_talent.data
                venue.seeking_description = form.seeking_description.data
                venue.website_link = form.website_link.data

                db.session.commit()
                flash(f"Venue {venue.name} was successfully updated! Woop Woop!", 'success')
                return redirect(url_for('show_venue', venue_id=venue_id))

            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred while updating yousr venue: {e}", 'danger') 
                print(e)

            finally:
                db.session.close()
        else:
            flash('Sorry we could not update your venue. Please check your details.', 'danger')

    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.address.data = venue.address
    form.phone.data = venue.phone
    form.genres.data = venue.genres.split(",") if venue.genres else []
    form.facebook_link.data = venue.facebook_link
    form.image_link.data = venue.image_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
    form.website_link.data = venue.website_link

    return render_template('forms/edit_venue.html', form=form, venue=venue)

#  ----------------------------------------------------------------
#  Delete Venue  Works
#  ----------------------------------------------------------------

@app.route('/venues/<venue_id>', methods=['DELETE'])  
def delete_venue(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        if not venue:
            flash(f'Venue with the ID {venue_id} does not exist!!',  'danger') 
            return redirect(url_for('index'))
        
        db.session.delete(venue)
        db.session.commit()
        flash('Venue was successfully deleted!', 'success') 
    except Exception as e:
        db.session.rollback()
        flash(f'Sorry, something did go wrong... Venue could not be deleted: {e}', 'danger')  
    finally:
        db.session.close()
    return redirect(url_for('index'))

#  ----------------------------------------------------------------
#  Search for a venue works
#  ----------------------------------------------------------------

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  search_results = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  
  response = {
    "count": len(search_results),
    "data": []
  }
  
  for venue in search_results:
    response['data'].append({
      "id": venue.id,
      "name": venue.name,
    })
  
  return render_template('pages/search_venues.html', results=response, search_term=search_term)



#  ----------------------------------------------------------------
#  Artists List all Artists Works 
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = []
    artists = Artist.query.all()
    for artist in artists:
        num_upcoming_shows = len([
            show for show in artist.shows
            if show.start_time > datetime.now()
        ])
        data.append({
            "id": artist.id,
            "name": artist.name,
            "image_link": artist.image_link,
            "num_upcoming_shows": num_upcoming_shows
        })
    return render_template('pages/artists.html', artists=data)

#  ----------------------------------------------------------------
#  Artists SEARCH  Works 
#  ----------------------------------------------------------------

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  search_results = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  
  response = {
    "count": len(search_results),
    "data": []
  }
  
  for artist in search_results:
    response['data'].append({
      "id": artist.id,
      "name": artist.name,
    })
  
  return render_template('pages/search_artists.html', results=response, search_term=search_term)


#  ----------------------------------------------------------------
#  Artists Page 
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    
    if not artist:
        flash(f"Artist with ID {artist_id} not in database.")
        return redirect(url_for('artists'))  # Return artists list if artist doesn't exist
    
  
    artist.genres = artist.genres.split(",") if artist.genres else []
    
    past_shows = []
    for show in artist.shows:
        if show.start_time < datetime.now():
            past_shows.append({
                "venue_id": show.venue.id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            })
    
    upcoming_shows = []
    for show in artist.shows:
        if show.start_time > datetime.now():
            upcoming_shows.append({
                "venue_id": show.venue.id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            })
    
    # Additional infoes
    artist.past_shows = past_shows
    artist.past_shows_count = len(past_shows)
    artist.upcoming_shows = upcoming_shows
    artist.upcoming_shows_count = len(upcoming_shows)
    
    return render_template('pages/show_artist.html', artist=artist)


#  ----------------------------------------------------------------
#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(request.form)

    if form.validate_on_submit():  #form data validation
        try:
            new_artist = Artist(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                genres=",".join(form.genres.data),  # Convert list to  string
                image_link=form.image_link.data,
                facebook_link=form.facebook_link.data,
                website_link=form.website_link.data,
                seeking_venue=form.seeking_venue.data,
                seeking_description=form.seeking_description.data,
            )
            db.session.add(new_artist)
            db.session.commit()
            flash(f"Artist '{form.name.data}' was successfully Created!", "success")
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            flash(f"An error occurred. Artist '{form.name.data}' could not be created.", "danger")
        finally:
            db.session.close()
    else:
        flash("An error occurred. Please check the details and try again.", "danger")
        print("Form Errors:", form.errors)

    return redirect(url_for("index"))

#  ----------------------------------------------------------------
# Edit Artist
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)

    if not artist:
        flash(f"Artist with ID {artist_id} not found.", "danger")
        return redirect(url_for('artists'))  # Goto artists list if the artist doesn't exist

    form = ArtistForm()

    # Handle POST request
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                # Update artist fields
                artist.name = form.name.data
                artist.city = form.city.data
                artist.state = form.state.data
                artist.phone = form.phone.data
                artist.genres = ",".join(form.genres.data)  # Convert list to string
                artist.facebook_link = form.facebook_link.data
                artist.image_link = form.image_link.data
                artist.seeking_venue = form.seeking_venue.data
                artist.seeking_description = form.seeking_description.data
                artist.website_link = form.website_link.data

                db.session.commit()
                flash(f"Artist '{artist.name}' was successfully updated!", "success")
                return redirect(url_for('show_artist', artist_id=artist_id))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")
                print(f"Error updating artist: {e}")
            finally:
                db.session.close()
        else:
            flash("Errors occurred. Please check your details.", "danger")
            print("Form Errors:", form.errors)

    # Fills the form with the artist current data for GET request
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres.split(",") if artist.genres else []
    form.facebook_link.data = artist.facebook_link
    form.image_link.data = artist.image_link
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description
    form.website_link.data = artist.website_link

    return render_template('forms/edit_artist.html', form=form, artist=artist)

#  ---------------------------------------------------------------- 
#  Delte Artist works?  
#  ---------------------------------------------------------------- 
@app.route("/artists/<int:artist_id>/delete", methods=["POST"])
def delete_artist(artist_id):
    try:
        artist = Artist.query.get(artist_id)
        if not artist:
            flash(f"Artist with ID {artist_id} not found.", "danger")
            return redirect(url_for("artists"))

        db.session.delete(artist)
        db.session.commit()
        flash(f"Artist '{artist.name}' was successfully deleted!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}", "danger")
    finally:
        db.session.close()

    return redirect(url_for("index"))


# ----------------------------------------------------------------
# Shows
# ----------------------------------------------------------------

@app.route('/shows')
def shows():
    upcoming_shows = Show.query.filter(Show.start_time > datetime.now()).all()
    data = []
    for show in upcoming_shows:
        data.append({
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "artist_id": show.artist.id,
            "venue_name": show.venue.name,
            "venue_id": show.venue.id,
            "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    return render_template('pages/shows.html', shows=data)




@app.route('/shows/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm(request.form)
    
    if form.validate_on_submit():
        try:
            # Create a new show
            new_show = Show(
                artist_id=form.artist_id.data,
                venue_id=form.venue_id.data,
                start_time=form.start_time.data
            )
            db.session.add(new_show)
            db.session.commit()
            flash('Show was successfully created!', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            flash('An error occurred. Show could not be created.', 'danger')
        finally:
            db.session.close()
    else:
        flash('An error occurred. Please check your details and try again.', 'danger')
        print("Form Errors:", form.errors)

    return redirect(url_for("index"))

@app.route('/shows/search', methods=['POST'])
def search_show():
    search_term = request.form.get('search_term', '')
    
    # Filter shows where artist name or venue name matches the search
    search_results = Show.query.filter(
        Show.artist.has(Artist.name.ilike(f'%{search_term}%')) |
        Show.venue.has(Venue.name.ilike(f'%{search_term}%'))
    ).all()

    response = {
        "count": len(search_results),
        "data": []
    }

    for show in search_results:
        response['data'].append({
            "id": show.id,
            "artist_name": show.artist.name,
            "venue_id": show.venue.id,  
            "venue_name": show.venue.name,
            "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    print(f"Passing to template: {response['data']}")
    return render_template('pages/search_show.html', results=response['data'], search_term=search_term)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

#----------------------------------------------------------------------------#
# Seed.
#----------------------------------------------------------------------------#

 # data = [{
    #     "venue_id": 1,
    #     "venue_name": "The Musical Hop",
    #     "artist_id": 4,
    #     "artist_name": "Guns N Petals",
    #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #     "start_time": "2019-05-21T21:30:00.000Z"
    # }, {
    #     "venue_id": 3,
    #     "venue_name": "Park Square Live Music & Coffee",
    #     "artist_id": 5,
    #     "artist_name": "Matt Quevedo",
    #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #     "start_time": "2019-06-15T23:00:00.000Z"
    # }, {
    #     "venue_id": 3,
    #     "venue_name": "Park Square Live Music & Coffee",
    #     "artist_id": 6,
    #     "artist_name": "The Wild Sax Band",
    #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #     "start_time": "2035-04-01T20:00:00.000Z"
    # }, {
    #     "venue_id": 3,
    #     "venue_name": "Park Square Live Music & Coffee",
    #     "artist_id": 6,
    #     "artist_name": "The Wild Sax Band",
    #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #     "start_time": "2035-04-08T20:00:00.000Z"
    # }, {
    #     "venue_id": 3,
    #     "venue_name": "Park Square Live Music & Coffee",
    #     "artist_id": 6,
    #     "artist_name": "The Wild Sax Band",
    #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #     "start_time": "2035-04-15T20:00:00.000Z"
    # }]

    # venue = {
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #     "address": "1015 Folsom Street",
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "123-123-1234",
    #     "website": "https://www.themusicalhop.com",
    #     "facebook_link": "https://www.facebook.com/TheMusicalHop",
    #     "seeking_talent": True,
    #     "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #     "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    # }

    # artist = {
    #     "id": 4,
    #     "name": "Guns N Petals",
    #     "genres": ["Rock n Roll"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "326-123-5000",
    #     "website": "https://www.gunsnpetalsband.com",
    #     "facebook_link": "https://www.facebook.com/GunsNPetals",
    #     "seeking_venue": True,
    #     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #     "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    # }

    # data1 = {
    #     "id": 4,
    #     "name": "Guns N Petals",
    #     "genres": ["Rock n Roll"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "326-123-5000",
    #     "website": "https://www.gunsnpetalsband.com",
    #     "facebook_link": "https://www.facebook.com/GunsNPetals",
    #     "seeking_venue": True,
    #     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #     "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #     "past_shows": [{
    #         "venue_id": 1,
    #         "venue_name": "The Musical Hop",
    #         "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #         "start_time": "2019-05-21T21:30:00.000Z"
    #     }],
    #     "upcoming_shows": [],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 0,
    # }
    # data2 = {
    #     "id": 5,
    #     "name": "Matt Quevedo",
    #     "genres": ["Jazz"],
    #     "city": "New York",
    #     "state": "NY",
    #     "phone": "300-400-5000",
    #     "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    #     "seeking_venue": False,
    #     "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #     "past_shows": [{
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #         "start_time": "2019-06-15T23:00:00.000Z"
    #     }],
    #     "upcoming_shows": [],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 0,
    # }
    # data3 = {
    #     "id": 6,
    #     "name": "The Wild Sax Band",
    #     "genres": ["Jazz", "Classical"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "432-325-5432",
    #     "seeking_venue": False,
    #     "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #     "past_shows": [],
    #     "upcoming_shows": [{
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #         "start_time": "2035-04-01T20:00:00.000Z"
    #     }, {
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #         "start_time": "2035-04-08T20:00:00.000Z"
    #     }, {
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #         "start_time": "2035-04-15T20:00:00.000Z"
    #     }],
    #     "past_shows_count": 0,
    #     "upcoming_shows_count": 3,
    # }
    # data = list(filter(lambda d: d['id'] ==
    #                    artist_id, [data1, data2, data3]))[0]

     # data1 = {
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #     "address": "1015 Folsom Street",
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "123-123-1234",
    #     "website": "https://www.themusicalhop.com",
    #     "facebook_link": "https://www.facebook.com/TheMusicalHop",
    #     "seeking_talent": True,
    #     "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #     "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #     "past_shows": [{
    #         "artist_id": 4,
    #         "artist_name": "Guns N Petals",
    #         "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #         "start_time": "2019-05-21T21:30:00.000Z"
    #     }],
    #     "upcoming_shows": [],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 0,
    # }
    # data2 = {
    #     "id": 2,
    #     "name": "The Dueling Pianos Bar",
    #     "genres": ["Classical", "R&B", "Hip-Hop"],
    #     "address": "335 Delancey Street",
    #     "city": "New York",
    #     "state": "NY",
    #     "phone": "914-003-1132",
    #     "website": "https://www.theduelingpianos.com",
    #     "facebook_link": "https://www.facebook.com/theduelingpianos",
    #     "seeking_talent": False,
    #     "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    #     "past_shows": [],
    #     "upcoming_shows": [],
    #     "past_shows_count": 0,
    #     "upcoming_shows_count": 0,
    # }
    # data3 = {
    #     "id": 3,
    #     "name": "Park Square Live Music & Coffee",
    #     "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    #     "address": "34 Whiskey Moore Ave",
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "415-000-1234",
    #     "website": "https://www.parksquarelivemusicandcoffee.com",
    #     "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    #     "seeking_talent": False,
    #     "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #     "past_shows": [{
    #         "artist_id": 5,
    #         "artist_name": "Matt Quevedo",
    #         "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #         "start_time": "2019-06-15T23:00:00.000Z"
    #     }],
    #     "upcoming_shows": [{
    #         "artist_id": 6,
    #         "artist_name": "The Wild Sax Band",
    #         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #         "start_time": "2035-04-01T20:00:00.000Z"
    #     }, {
    #         "artist_id": 6,
    #         "artist_name": "The Wild Sax Band",
    #         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #         "start_time": "2035-04-08T20:00:00.000Z"
    #     }, {
    #         "artist_id": 6,
    #         "artist_name": "The Wild Sax Band",
    #         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #         "start_time": "2035-04-15T20:00:00.000Z"
    #     }],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 1,
    # }
    # data = list(filter(lambda d: d['id'] ==
    #                    venue_id, [data1, data2, data3]))[0]
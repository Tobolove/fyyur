from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ARRAY

db = SQLAlchemy()
#----------------------------------------------------------------------------#
# Models. Updated Models
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(50000)) 
    # genres = db.Column(db.String, nullable=True) => old code
    # genres = db.ARRAY(db.String) => keep getting errors as the array is not iterable, please assist
    genres = db.Column(ARRAY(db.String), nullable=True)
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
    genres = db.Column(db.String, nullable=False) 
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
    
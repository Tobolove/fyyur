

from app import app, db, Venue, Artist, Show
from datetime import datetime

# INFO: Use this script to populate the database and have fun :)!!

with app.app_context():  
    # Drop all existing data and recreate tables
    db.drop_all()
    db.create_all()

    # Seed data for venues
    venues = [
        Venue(
            id=1,
            name="The Musical Hop",
            city="San Francisco",
            state="CA",
            address="1015 Folsom Street",
            phone="123-123-1234",
            genres="Jazz,Reggae,Swing,Classical,Folk",
            website_link="https://www.themusicalhop.com",
            facebook_link="https://www.facebook.com/TheMusicalHop",
            seeking_talent=True,
            seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
            image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        ),
        Venue(
            id=2,
            name="The Dueling Pianos Bar",
            city="New York",
            state="NY",
            address="335 Delancey Street",
            phone="914-003-1132",
            genres="Classical,R&B,Hip-Hop",
            website_link="https://www.theduelingpianos.com",
            facebook_link="https://www.facebook.com/theduelingpianos",
            seeking_talent=False,
            image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
        ),
        Venue(
            id=3,
            name="Park Square Live Music & Coffee",
            city="San Francisco",
            state="CA",
            address="34 Whiskey Moore Ave",
            phone="415-000-1234",
            genres="Rock n Roll,Jazz,Classical,Folk",
            website_link="https://www.parksquarelivemusicandcoffee.com",
            facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
            seeking_talent=False,
            image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        ),
    ]

    # Seed data for artists
    artists = [
        Artist(
            id=4,
            name="Guns N Petals",
            city="San Francisco",
            state="CA",
            phone="326-123-5000",
            genres="Rock n Roll",
            website_link="https://www.gunsnpetalsband.com",
            facebook_link="https://www.facebook.com/GunsNPetals",
            seeking_venue=True,
            seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
            image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        ),
        Artist(
            id=5,
            name="Matt Quevedo",
            city="New York",
            state="NY",
            phone="300-400-5000",
            genres="Jazz",
            facebook_link="https://www.facebook.com/mattquevedo923251523",
            seeking_venue=False,
            image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        ),
        Artist(
            id=6,
            name="The Wild Sax Band",
            city="San Francisco",
            state="CA",
            phone="432-325-5432",
            genres="Jazz,Classical",
            seeking_venue=False,
            image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        ),
    ]

    # Seed data for shows
    shows = [
        Show(
            venue_id=1,
            artist_id=4,
            start_time=datetime.strptime("2019-05-21T21:30:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        ),
        Show(
            venue_id=3,
            artist_id=5,
            start_time=datetime.strptime("2019-06-15T23:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        ),
        Show(
            venue_id=3,
            artist_id=6,
            start_time=datetime.strptime("2035-04-01T20:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        ),
        Show(
            venue_id=3,
            artist_id=6,
            start_time=datetime.strptime("2035-04-08T20:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        ),
        Show(
            venue_id=3,
            artist_id=6,
            start_time=datetime.strptime("2035-04-15T20:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        ),
    ]

    # Add data to the database
    db.session.bulk_save_objects(venues)
    db.session.bulk_save_objects(artists)
    db.session.bulk_save_objects(shows)
    db.session.commit()

    print("Database seeded successfully!")
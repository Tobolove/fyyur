from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, URL, Optional
from wtforms.fields import DateTimeLocalField


class ShowForm(FlaskForm):
    artist_id = StringField('artist_id', validators=[DataRequired()])
    venue_id = StringField('venue_id', validators=[DataRequired()])
    start_time = DateTimeLocalField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today(),
        format='%Y-%m-%dT%H:%M'
    )


class VenueForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField(
        'state',
        validators=[DataRequired()],
        choices=[
            ('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'), ('CA', 'CA'),
            ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'), ('DC', 'DC'), ('FL', 'FL'),
            ('GA', 'GA'), ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'),
            ('IA', 'IA'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'),
            ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'), ('NJ', 'NJ'),
            ('NM', 'NM'), ('NY', 'NY'), ('NC', 'NC'), ('ND', 'ND'), ('OH', 'OH'),
            ('OK', 'OK'), ('OR', 'OR'), ('MD', 'MD'), ('MA', 'MA'), ('MI', 'MI'),
            ('MN', 'MN'), ('MS', 'MS'), ('MO', 'MO'), ('PA', 'PA'), ('RI', 'RI'),
            ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'),
            ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'), ('WV', 'WV'), ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField('address', validators=[DataRequired()])
    phone = StringField('phone')
    website_link = StringField(
    'website_link', validators=[Optional(), URL(message="Invalid URL")])
    image_link = StringField(
    'image_link', validators=[Optional(), URL(message="Invalid URL")])
    genres = SelectMultipleField(
        'genres',
        validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'), ('Blues', 'Blues'),
            ('Classical', 'Classical'), ('Country', 'Country'),
            ('Electronic', 'Electronic'), ('Folk', 'Folk'),
            ('Funk', 'Funk'), ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'), ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'), ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'), ('Punk', 'Punk'), ('R&B', 'R&B'),
            ('Reggae', 'Reggae'), ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'), ('Other', 'Other'),
        ]
    )
    facebook_link = StringField('facebook_link', validators=[Optional(), URL()])
    seeking_talent = BooleanField('seeking_talent')
    seeking_description = TextAreaField('seeking_description')


class ArtistForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField(
        'state',
        validators=[DataRequired()],
        choices=[
            ('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'), ('CA', 'CA'),
            ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'), ('DC', 'DC'), ('FL', 'FL'),
            ('GA', 'GA'), ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'),
            ('IA', 'IA'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'),
            ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'), ('NJ', 'NJ'),
            ('NM', 'NM'), ('NY', 'NY'), ('NC', 'NC'), ('ND', 'ND'), ('OH', 'OH'),
            ('OK', 'OK'), ('OR', 'OR'), ('MD', 'MD'), ('MA', 'MA'), ('MI', 'MI'),
            ('MN', 'MN'), ('MS', 'MS'), ('MO', 'MO'), ('PA', 'PA'), ('RI', 'RI'),
            ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'),
            ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'), ('WV', 'WV'), ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField('phone')
    website_link = StringField(
    'website_link', validators=[Optional(), URL(message="Invalid URL")])
    image_link = StringField(
    'image_link', validators=[Optional(), URL(message="Invalid URL")])
    genres = SelectMultipleField(
        'genres',
        validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'), ('Blues', 'Blues'),
            ('Classical', 'Classical'), ('Country', 'Country'),
            ('Electronic', 'Electronic'), ('Folk', 'Folk'),
            ('Funk', 'Funk'), ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'), ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'), ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'), ('Punk', 'Punk'), ('R&B', 'R&B'),
            ('Reggae', 'Reggae'), ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'), ('Other', 'Other'),
        ]
    )
    facebook_link = StringField('facebook_link', validators=[Optional(), URL(message="Invalid URL")])
    seeking_venue = BooleanField('seeking_venue')
    seeking_description = TextAreaField('seeking_description')
 
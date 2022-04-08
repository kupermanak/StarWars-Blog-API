from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.Integer())
    population = db.Column(db.Integer())
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    surface_water = db.Column(db.Integer())
    characters = db.relationship("Character", back_populates="planet")
    def __repr__(self):
        return '<Planet %r>' % self.name
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "characters": list(map(lambda x: x.serialize(), self.characters))
            }

class Starship(db.Model):
    __tablename__ = 'starship'
    id = db.Column(Integer, primary_key=True)
    model = db.Column(String(50))
    starship_class = db.Column(String(50))
    manufacturer = db.Column(String(50))
    cost_in_credits = db.Column(String(50))
    length = db.Column(String(50))
    crew = db.Column(String(50))
    passengers = db.Column(String(50))
    characters = db.relationship("Character", back_populates="starship")
    def __repr__(self):
        return '<Starship %r>' % self.model
    def serialize(self):
        return {
            "id": self.id,
            "model": self.model,
            "starship_class": self.starship_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "characters": list(map(lambda x: x.serialize(), self.characters))
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer())
    mass = db.Column(db.Integer())
    hair_color = db.Column(db.String(250))
    homeworld = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    planet = relationship("Planet", primaryjoin=planet_id == Planet.id)
    starship_id = db.Column(db.Integer, db.ForeignKey("starship.id"))
    starship = relationship("Starship", primaryjoin=starship_id == Starship.id)
    def __repr__(self):
        return '<Character %r>' % self.name
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "homeworld": self.homeworld,
            "eye_color": self.eye_color,
            "gender": self.gender,
        }

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class favorite_characters(db.Model):
    __tablename__= "favorite_characters"
    favorite_characters_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    user = relationship("User", primaryjoin=user_id == User.id)
    character = relationship("Character", primaryjoin=character_id == Character.id)

    def __repr__(self):
        return '<favorite_characters %r>' % self.favorite_characters_id

    def serialize(self):
        return {
            
            "id": self.favorite_characters_id,
            "user_id": self.user_id,
            "character_id": self.character_id,
        
            # do not serialize the password, its a security breach
        }

class favorite_planets(db.Model):
    __tablename__= "favorite_planets"
    favorite_planets_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    user = relationship("User", primaryjoin=user_id == User.id)
    planet = relationship("Planet", primaryjoin=planet_id == Planet.id)

    def __repr__(self):
        return '<favorite_planets %r>' % self.favorite_planets_id

    def serialize(self):
        return {
            
            "id": self.favorite_planets_id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        
            # do not serialize the password, its a security breach
        }


class favorite_starships(db.Model):
    __tablename__= "favorite_starships"
    favorite_starships_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    starship_id = db.Column(db.Integer, db.ForeignKey('starship.id'))
    user = relationship("User", primaryjoin=user_id == User.id)
    starship = relationship("Starship", primaryjoin=starship_id == Starship.id)

    def __repr__(self):
        return '<favorite_starships %r>' % self.favorite_starships_id

    def serialize(self):
        return {
            
            "id": self.favorite_starships_id,
            "user_id": self.user_id,
            "starship_id": self.starship_id,
        
            # do not serialize the password, its a security breach
        }
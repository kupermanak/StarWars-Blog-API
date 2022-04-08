"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Starship, favorite_characters, favorite_planets, favorite_starships
from sqlalchemy import join, select
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def get_user():
    users = User.query.all()
    users = list(map(lambda user : user.serialize(), users))
    return jsonify(users), 200

@app.route('/create/user', methods=['POST'])
def handle_user():
    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'email' not in body:
        raise APIException('You need to specify the email', status_code=400)
    if 'password' not in body:
        raise APIException('You need to specify the password', status_code=400)
    if "is_active" not in body:
        raise APIException("you need to specify if is active", status_code=400)

# at this point, all data has been validated, we can proceed to inster into the bd
    user1 = User(email=body['email'], password=body['password'], is_active=body["is_active"])
    db.session.add(user1)
    db.session.commit()
    return "ok", 200

@app.route('/people', methods=['GET'])
def get_character():
    characters = Character.query.all()
    characters = list(map(lambda character : character.serialize(), characters))
    return jsonify(characters), 200

@app.route("/people/<int:character_id>")
def get_character_id(character_id):
    characters = Character.query.get(character_id)
    character = characters.serialize()
    return jsonify(character), 200

@app.route('/create/characters', methods=['POST'])
def handle_characters():
    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'name' not in body:
        raise APIException('You need to specify the name', status_code=400)
    if 'height' not in body:
        raise APIException('You need to specify the height', status_code=400)
    if "mass" not in body:
        raise APIException("you need to specify the mass", status_code=400)
    if "hair_color" not in body:
        raise APIException("you need to specify the hair color", status_code=400)
    if "homeworld" not in body:
        raise APIException("you need to specify the homeworld", status_code=400)
    if "eye_color" not in body:
        raise APIException("you need to specify the eye color", status_code=400)
    if "gender" not in body:
        raise APIException("you need to specify gender", status_code=400)
    if "planet" not in body:
        raise APIException("you need to specify planet", status_code=400)
    if "starship" not in body:
        raise APIException("you need to specify starship", status_code=400)

    is_planet = Planet.query.get(body["planet"])
    print(is_planet)
    if is_planet == None:
        raise APIException("you need to specify planet ID", status_code=400)
    
    is_starship = Starship.query.get(body["starship"])
    print(is_starship)
    if is_starship == None:
        raise APIException("you need to specify starship ID", status_code=400)

# at this point, all data has been validated, we can proceed to inster into the bd
    characters1 = Character(name=body['name'], height=body['height'], mass=body["mass"], hair_color=body["hair_color"], homeworld=body["homeworld"], eye_color=body["eye_color"], gender=body["gender"], planet_id=body["planet"], starship_id=body["starship"])
    db.session.add(characters1)
    db.session.commit()
    return "ok", 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planets = list(map(lambda planet : planet.serialize(), planets))
    return jsonify(planets), 200

@app.route("/planets/<int:planet_id>")
def get_planet_id(planet_id):
    planets = Planet.query.get(planet_id)
    planets = planets.serialize()
    return jsonify(planets), 200


@app.route('/create/planet', methods=['POST'])
def handle_planet():
    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'name' not in body:
        raise APIException('You need to specify the name', status_code=400)
    if 'diameter' not in body:
        raise APIException('You need to specify the diameter', status_code=400)
    if "population" not in body:
        raise APIException("you need to specify the population", status_code=400)
    if "climate" not in body:
        raise APIException("you need to specify the climate", status_code=400)
    if "terrain" not in body:
        raise APIException("you need to specify the terrain", status_code=400)
    if "surface_water" not in body:
        raise APIException("you need to specify the surface_water", status_code=400)

# at this point, all data has been validated, we can proceed to inster into the bd
    planets1 = Planet(name=body['name'], diameter=body['diameter'], population=body["population"], climate=body["climate"], terrain=body["terrain"], surface_water=body["surface_water"])
    db.session.add(planets1)
    db.session.commit()
    return "ok", 200

@app.route('/starship', methods=['GET'])
def get_starship():
    starships = Starship.query.all()
    starships = list(map(lambda starship : starship.serialize(), starships))
    return jsonify(starships), 200

@app.route("/starships/<int:starship_id>")
def get_starship_id(starship_id):
    starships = Starship.query.get(starship_id)
    starships = starships.serialize()
    return jsonify(starships), 200

@app.route('/create/starship', methods=['POST'])
def handle_starship():
    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'model' not in body:
        raise APIException('You need to specify the model', status_code=400)
    if 'starship_class' not in body:
        raise APIException('You need to specify the starship_class', status_code=400)
    if 'manufacturer' not in body:
        raise APIException('You need to specify the manufacturer', status_code=400)
    if "cost_in_credits" not in body:
        raise APIException("you need to specify the cost_in_credits", status_code=400)
    if "length" not in body:
        raise APIException("you need to specify the length", status_code=400)
    if "crew" not in body:
        raise APIException("you need to specify the crew", status_code=400)
    if "passengers" not in body:
        raise APIException("you need to specify the passengers", status_code=400)

# at this point, all data has been validated, we can proceed to inster into the bd
    starships1 = Starship(model=body['model'], starship_class=body['starship_class'], manufacturer=body['manufacturer'], cost_in_credits=body["cost_in_credits"], length=body["length"], crew=body["crew"], passengers=body["passengers"])
    db.session.add(starships1)
    db.session.commit()
    return "ok", 200

@app.route("/User/favorites_characters/<int:user_id>", methods=["GET"])
def get_favorites_characters(user_id):
    favorites_user = Character.query.join(favorite_characters, favorite_characters.character_id == Character.id).filter(favorite_characters.user_id == user_id).all()
    serialize_fav_user = list(map(lambda favorite_user : favorite_user.serialize(), favorites_user))
    print(favorites_user)
    return jsonify(serialize_fav_user), 200

@app.route("/User/favorites_characters/<int:user_id>", methods=["DELETE"])
def delete_favorito1(user_id):
    del_fav_char = favorites_characters.query.get(user_id)
    if del_fav_char is None:
        raise APIException('Favorito no encontrado', status_code=404)
    db.session.delete(del_fav_char)
    db.session.commit()

    return jsonify("ok"), 200

@app.route('/create/User/favorites_characters/<int:user_id>', methods=['POST'])
def handle_favorites_characters(user_id):
    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'user_id' not in body:
        raise APIException('You need to specify the user_id', status_code=400)
    if 'character_id' not in body:
        raise APIException('You need to specify the character_id', status_code=400)

    fav_char = favorite_characters(user_id=body['user_id'], character_id=body['character_id'])
    db.session.add(fav_char)
    db.session.commit()
    return "ok", 200

@app.route("/User/favorites_planets/<int:user_id>", methods=["GET"])
def get_favorites_planets(user_id):
    favorites_user = Planet.query.join(favorite_planets, favorite_planets.planet_id == Planet.id).filter(favorite_planets.user_id == user_id).all()
    serialize_fav_user = list(map(lambda favorite_user : favorite_user.serialize(), favorites_user))
    print(favorites_user)
    return jsonify(serialize_fav_user), 200

@app.route("/User/favorites_planets/<int:user_id>", methods=["DELETE"])
def delete_favorito2(user_id):
    del_fav_plan = favorite_planets.query.get(user_id)
    if del_fav_plan is None:
        raise APIException('Favorito no encontrado', status_code=404)
    db.session.delete(del_fav_plan)
    db.session.commit()
    return jsonify("ok"), 200

@app.route('/create/User/favorites_planets/<int:user_id>', methods=['POST'])
def handle_favorites_planets(user_id):
    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'user_id' not in body:
        raise APIException('You need to specify the user_id', status_code=400)
    if 'planet_id' not in body:
        raise APIException('You need to specify the planet_id', status_code=400)

    fav_plan = favorite_planets(user_id=body['user_id'], planet_id=body['planet_id'])
    db.session.add(fav_plan)
    db.session.commit()
    return "ok", 200

@app.route("/User/favorites_starships/<int:user_id>", methods=["GET"])
def get_favorites_starships(user_id):
    favorites_user = Starship.query.join(favorite_starships, favorite_starships.starship_id == Starship.id).filter(favorite_starships.user_id == user_id).all()
    serialize_fav_user = list(map(lambda favorite_user : favorite_user.serialize(), favorites_user))
    print(favorites_user)
    return jsonify(serialize_fav_user), 200

@app.route("/User/favorites_starships/<int:user_id>", methods=["DELETE"])
def delete_favorito3(user_id):
    del_fav_star = favorite_starships.query.get(user_id)
    if del_fav_star is None:
        raise APIException('Favorito no encontrado', status_code=404)
    db.session.delete(del_fav_star)
    db.session.commit()
    return jsonify("ok"), 200

@app.route('/create/User/favorites_starships/<int:user_id>', methods=['POST'])
def handle_favorites_starships(user_id):
    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'user_id' not in body:
        raise APIException('You need to specify the user_id', status_code=400)
    if 'starship_id' not in body:
        raise APIException('You need to specify the starship_id', status_code=400)

    fav_star = favorite_starships(user_id=body['user_id'], starship_id=body['starship_id'])
    db.session.add(fav_star)
    db.session.commit()
    return "ok", 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

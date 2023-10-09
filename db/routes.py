from flask import Blueprint, jsonify, request
from app.models import Hero, Power, HeroPower

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes])


@bp.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

@bp.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404
    return jsonify(power.to_dict())

@bp.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404
    data = request.get_json()
    power.description = data.get('description', power.description)
    if not power.validate():
        return jsonify({'error': 'Invalid input'}), 400
    power.save()
    return jsonify(power.to_dict())

@bp.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
    if hero is None or power is None:
        return jsonify({'error': 'Hero or Power not found'}), 404
    hero_power = HeroPower(hero=hero, power=power)
    hero_power.save()
    return jsonify(hero.to_dict(include_powers=True))

app.register_blueprint(bp) 
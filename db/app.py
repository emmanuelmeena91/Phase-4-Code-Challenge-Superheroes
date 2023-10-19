from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from random import randint, choice

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Power(db.Model): 
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)


class Hero(db.Model): 
    __tablename__ = 'hero' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False)


class HeroPower(db.Model):
    __tablename__ = 'hero_power'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)
    strength = db.Column(db.String(100), nullable=False)

    hero = db.relationship('Hero', backref=db.backref('hero_powers', cascade='all, delete-orphan'))
    power = db.relationship('Power', backref=db.backref('hero_powers', cascade='all, delete-orphan'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        powers = [
            {"name": "super strength", "description": "gives the wielder super-human strengths"},
            {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
            {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
            {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
        ]

        print("🦸‍♀️ Seeding powers...")
        for power_data in powers:
            power = Power(**power_data)
            db.session.add(power)
        db.session.commit()

        heroes = [
            {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
            {"name": "Doreen Green", "super_name": "Squirrel Girl"},
            {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
            {"name": "Janet Van Dyne", "super_name": "The Wasp"},
            {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
            {"name": "Carol Danvers", "super_name": "Captain Marvel"},
            {"name": "Jean Grey", "super_name": "Dark Phoenix"},
            {"name": "Ororo Munroe", "super_name": "Storm"},
            {"name": "Kitty Pryde", "super_name": "Shadowcat"},
            {"name": "Elektra Natchios", "super_name": "Elektra"}
        ]

        print("🦸‍♀️ Seeding heroes...")
        for hero_data in heroes:
            hero = Hero(**hero_data)
            db.session.add(hero)
        db.session.commit()

        strengths = ["Strong", "Weak", "Average"]

        print("🦸‍♀️ Adding powers to heroes...")
        all_heroes = Hero.query.all()
        for hero in all_heroes:
            num_powers = randint(1, 3)
            powers = Power.query.order_by(db.func.random()).limit(num_powers).all()

            for power in powers:
                hero_power = HeroPower(hero_id=hero.id, power_id=power.id, strength=choice(strengths))
                db.session.add(hero_power)
        db.session.commit()

        print("🦸‍♀️ Done seeding!")
from models import db, Power, Hero, HeroPower
from random import randint, choice

def clear_data():
    db.session.query(HeroPower).delete()
    db.session.query(Hero).delete()
    db.session.query(Power).delete()
    db.session.commit()

# Create powers
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

# Create heroes
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

# Create hero powers
strengths = ["Strong", "Weak", "Average"]

print("🦸‍♀️ Adding powers to heroes...")
all_heroes = Hero.query.all()
for hero in all_heroes:
    num_powers = randint(1, 3)
    powers = Power.query.all()
    shuffle(powers)
    selected_powers = powers[:num_powers]

    for power in selected_powers:
        hero_power = HeroPower(hero_id=hero.id, power_id=power.id, strength=choice(strengths))
        db.session.add(hero_power)
db.session.commit()

print("🦸‍♀️ Done seeding!")